from chat.standard_messages import StandardMessages
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
            raise ValueError("rag_system must be a RAGSystem object")

        self.max_input_tokens = max_input_tokens

        self.rag_system = rag_system

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )

        self.prompts = ChainPrompt()

        self.messages = StandardMessages()

    def _catch_user_input(self):
        """ Aspetta input utente """
        while True:
            question = input("Tu: ").strip()

            if question.lower() in ['exit']:
                self.messages.goodbye()
                break

            if question.lower() in ["upload"]:
                self._catch_user_file_upload()
                break

            if not question:
                self.messages.wrong_bitch()
                continue

            answer = self.ask_agent(question)

            if answer:
                self.messages.bot_answer(answer)
            else:
                self.messages.generic_error()

    def start_chatbot(self):
        """Avvia chat con l'utente"""

        if self.rag_system:
            self.messages.welcome_rag_enabled()
        else:
            self.messages.welcome_rag_disabled()

        self._catch_user_input()

    def _catch_user_file_upload(self):
        """Avvia interazione caricamento file"""

        while True:
            if is_colab():
                from google.colab import files
                uploaded = files.upload()
                filename = list(uploaded.keys())[0]
            else:
                filename = input("Inserisci il percorso del file PDF: ")

            self.generate_report(filename)


    def ask_agent(self, query):
        """
        Metodo che gestisce retrieval e chiamata verso llm
        """
        if not isinstance(query, str):
            raise ValueError("query must be a string")
        if not query:
            raise ValueError("query must not be empty")

        try:
            context = ""

            if rag_system:
                context_results = self.rag_system.retrieve(query)

                if len(context_results) == 0:
                    self.messages.no_results()

                context = "\n---\n".join([res.text for res in context_results])

            chain = self.prompts.simple_query() | self.llm | StrOutputParser()
            answer = chain.invoke({"context": context, "question": query})

            return answer

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

        try:
            if not file.lower().endswith('.pdf'):
                self.messages.file_format_not_permitted(["PDF"])
                return

            content = self.extract_text_from_pdf(file)

            if not content:
                self.messages.no_content_extracted()
                return

            if count_tokens(content) > self.max_input_tokens:
                self.messages.max_input_tokens()
                return

            chain = self.prompts.report() | self.llm | StrOutputParser()
            answer = chain.invoke({"content": content})

            if answer:
                self.messages.bot_answer(answer)
            else:
                self._reset_after_error()


        except Exception as e:
            raise Exception(f"Error during report generation: {e}")

    def _reset_after_error(self):
        self.messages.generic_error()
        self._catch_user_input()
