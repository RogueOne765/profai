from app_logger import LoggerHandler
from chat.message_printer import MessagePrinter
from chat.prompt import ChainPrompt
from rag import rag_system
from rag.rag_system import RAGSystem
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from llama_index.readers.file import PDFReader
from utils import is_colab, count_tokens


class ChatAgent():
    """
    Classe per interfaccia sistema RAG->LLM
    """
    def __init__(self, rag_system: RAGSystem = None, max_input_tokens: int = 10000):
        """
        Inizializza client LLM e chain con LangChain
        """
        if rag_system and not isinstance(rag_system, RAGSystem):
            raise ValueError("rag_system must be a RAGSystem instance")

        self.app_logger = LoggerHandler().get_app_logger(__name__)
        self.llm_logger = LoggerHandler().get_llm_logger(__name__)

        self.app_logger.info("Start chat agent instance...")

        self.max_input_tokens = max_input_tokens

        self.rag_system = rag_system

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )

        self.app_logger.debug(f"Set llm object as {self.llm}")

        self.prompts = ChainPrompt()

        self.printer = MessagePrinter()

    def _catch_user_input(self):
        """ Aspetta input utente """
        self.app_logger.debug("Ready to catch user input...")

        try:
            while True:
                question = input("Tu: ").strip()

                if question.lower() in ['exit']:
                    self.printer.goodbye()
                    break

                if question.lower() in ["upload"]:
                    self._catch_user_file_upload()
                    break

                if not question:
                    self.printer.wrong_bitch()
                    continue

                self.ask_agent(question)

        except Exception as e:
            self.llm_logger.error(f"Error while evaluating user request: {e}")
            self._reset_after_error()


    def start_chatbot(self):
        """Avvia chat con l'utente"""

        if self.rag_system:
            self.printer.welcome_rag_enabled()
        else:
            self.printer.welcome_rag_disabled()

        self._catch_user_input()

    def _catch_user_file_upload(self):
        """Avvia interazione caricamento file"""
        self.app_logger.debug("Ready to catch file upload...")

        try:
            while True:
                if is_colab():
                    from google.colab import files
                    uploaded = files.upload()
                    filename = list(uploaded.keys())[0]
                else:
                    filename = input("Inserisci il percorso del file PDF: ")

                self.generate_report(filename)

        except Exception as e:
            self.llm_logger.error(f"Error while evaluating user request: {e}")
            self._reset_after_error()


    def ask_agent(self, query):
        """
        Metodo che gestisce retrieval e chiamata verso llm
        """
        if not isinstance(query, str):
            raise ValueError("query must be a string")
        if len(query) == 0:
            raise ValueError("query must not be empty")

        self.llm_logger.info(f"New query request from user. Query: {query}")

        try:
            tot_tokens = count_tokens(query)
            if tot_tokens > self.max_input_tokens:
                self.llm_logger.warning(f"Limit exceed for query length. Total tokens: {tot_tokens}")
                self.printer.max_input_tokens()
                return

            context = ""

            if isinstance(self.rag_system, RAGSystem):
                context_results = self.rag_system.retrieve(query)

                if len(context_results) == 0:
                    self.llm_logger.warning(f"No context retrieved for current query: {query}")
                    self.printer.no_results()

                context = "\n---\n".join([res.text for res in context_results])

                self.llm_logger.debug(f"Context retrieved properties: number of docs {len(context_results)}, context tokens length {count_tokens(context)}")

            prompt = self.prompts.simple_query()
            chain = prompt | self.llm | StrOutputParser()
            answer = chain.invoke({"context": context, "question": query})

            self.llm_logger.info(f"New response from LLM. Answer: {answer} \n\n Query: {query} \n\n Context: {context} \n\n Prompt: {prompt}")

            if answer:
                self.printer.bot_answer(answer)
            else:
                self._reset_after_error(f"No answer returned for query: {query}")

        except Exception as e:
            raise Exception(f"Error asking agent: {e}")

    def extract_text_from_pdf(self, file):
        try:
            reader = PDFReader()
            documents = reader.load_data(file=file)
            return "\n".join([doc.text for doc in documents])
        except Exception as e:
            raise Exception(f"Error extracting text: {e}")

    def generate_report(self, file):
        """ Metodo per generazione report strutturato a partire da file """
        if not file:
            raise ValueError("file must be provided")

        self.llm_logger.info(f"New request to generate report. File: {file}")

        try:
            if not file.lower().endswith('.pdf'):
                self.printer.file_format_not_permitted(["PDF"])
                self.llm_logger.warning(f"File extension not permitted. File: {file}")
                return

            content = self.extract_text_from_pdf(file)

            self.llm_logger.debug(f"Content extracted from {file}: {content}")

            if not content:
                self.printer.no_content_extracted()
                self.llm_logger.warning(f"No content extracted from {file}")
                return

            if count_tokens(content) > self.max_input_tokens:
                self.llm_logger.warning(f"Max input tokens reached for submitted file: {file}")
                self.printer.max_input_tokens()
                return

            prompt = self.prompts.report()
            chain = prompt | self.llm | StrOutputParser()
            answer = chain.invoke({"content": content})

            self.llm_logger.info(f"New response from LLM. Answer: {answer} \n\n Content: {content} \n\n Prompt: {prompt}")

            if answer:
                self.printer.bot_answer(answer)
            else:
                self._reset_after_error(f"No report generated for file: {file}")

        except Exception as e:
            raise Exception(f"Error during report generation: {e}")

    def _reset_after_error(self, error = ""):
        generic_error_msg = "Invalid response from LLM client"
        self.llm_logger.error(error if error else generic_error_msg)
        self.printer.generic_error()
        self._catch_user_input()
