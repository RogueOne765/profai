import os
from dotenv import load_dotenv

import time
from app_logger import LoggerHandler
from chat.messages_templates import ChatMessagesTemplates
from chat.prompt import ChainPrompt
from enums import AgentActionType, AppEnv, GroqModelId
from monitoring.models import AgentPerformanceMetrics, RAGPerformanceMetrics
from monitoring.collector import MetricsCollector
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
        self.mon_logger = LoggerHandler().get_monitoring_logger(__name__)

        self.app_logger.info("Start chat agent instance...")

        self.max_input_tokens = max_input_tokens

        self.rag_system = rag_system

        load_dotenv()
        self.app_env = os.getenv("APP_ENV")

        self.llm = ChatGroq(
            #model=GroqModelId.LLAMA70.value,
            model=GroqModelId.OSS120.value,
            temperature=0.1,
            verbose=self.app_env == AppEnv.STAGING.value,
            max_tokens=max_input_tokens + int(max_input_tokens/10),
            streaming=True
        )

        self.app_logger.debug(f"Set llm object as {self.llm}")

        self.prompts = ChainPrompt()

        self.msg_templates = ChatMessagesTemplates()

    def _catch_user_input(self):
        """ Aspetta input utente """
        self.app_logger.debug("Ready to catch user input...")

        try:
            while True:
                question = input("Tu: ").strip()

                if question.lower() in ['exit']:
                    print(self.msg_templates.goodbye())
                    break

                if question.lower() in ["upload"]:
                    print(self._catch_user_file_upload())
                    break

                if not question:
                    print(self.msg_templates.wrong_bitch())
                    continue

                answer = self.ask_agent(question)
                print(self.msg_templates.bot_answer(answer))

        except Exception as e:
            self.llm_logger.error(f"Error while evaluating user request: {e}")
            print(self.msg_templates.generic_error())
            self._catch_user_input()


    def start_chatbot(self):
        """Avvia chat con l'utente"""

        if self.rag_system:
            print(self.msg_templates.welcome_rag_enabled())
        else:
            print(self.msg_templates.welcome_rag_disabled())

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

                answer = self.generate_report(filename)
                print(self.msg_templates.bot_answer(answer))

        except Exception as e:
                self.llm_logger.error(f"Error while evaluating user request: {e}")
                print(self.msg_templates.generic_error())
                self._catch_user_input()


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
            start_time = time.perf_counter()

            tot_tokens = count_tokens(query)
            if tot_tokens > self.max_input_tokens:
                self.llm_logger.warning(f"Limit exceed for query length. Total tokens: {tot_tokens}")
                return self.msg_templates.max_input_tokens()

            context = ""

            if isinstance(self.rag_system, RAGSystem):
                start_rag_time = time.perf_counter()
                retrieve_results = self.rag_system.retrieve(query)
                end_rag_time = time.perf_counter()

                if len(retrieve_results) == 0:
                    self.llm_logger.warning(f"No context retrieved for current query: {query}")
                    return self.msg_templates.no_results()

                context = "\n---\n".join([res.text for res in retrieve_results])

                self.llm_logger.debug(f"Context retrieved properties: number of docs {len(retrieve_results)}, context tokens length {count_tokens(context)}")

            prompt = self.prompts.simple_query()
            chain = prompt | self.llm | StrOutputParser()
            start_llm_time = time.perf_counter()
            answer = ""

            for chunk in chain.stream({"context": context, "question": query}):
                if chunk:
                    answer += chunk

            end_llm_time = time.perf_counter()

            self.llm_logger.info(f"New response from LLM. Answer: {answer} \n\n Query: {query} \n\n Context: {context}")
            end_time = time.perf_counter()
            self.save_metrics(
                query=query,
                action_type=AgentActionType.DIRECT_QUERY,
                retrieve_results=retrieve_results or [],
                start_time=start_time,
                start_rag_time=start_rag_time or 0.0,
                start_llm_time=start_llm_time,
                end_time=end_time,
                end_llm_time=end_llm_time,
                end_rag_time=end_rag_time or 0.0
            )

            if answer:
                return answer
            else:
                self.llm_logger.error(f"No answer returned for query: {query}")
                return self.msg_templates.generic_error()

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
            start_time = time.perf_counter()

            if not file.lower().endswith('.pdf'):
                self.llm_logger.warning(f"File extension not permitted. File: {file}")
                return self.msg_templates.file_format_not_permitted(["PDF"])

            start_upload_time = time.perf_counter()
            content = self.extract_text_from_pdf(file)
            end_upload_time = time.perf_counter()
            self.llm_logger.debug(f"Content extracted from {file}: {content}")

            if not content:
                self.llm_logger.warning(f"No content extracted from {file}")
                return self.msg_templates.no_content_extracted()

            if count_tokens(content) > self.max_input_tokens:
                self.llm_logger.warning(f"Max input tokens reached for submitted file: {file}")
                return self.msg_templates.max_input_tokens()

            prompt = self.prompts.report()
            chain = prompt | self.llm | StrOutputParser()
            start_llm_time = time.perf_counter()
            answer = chain.invoke({"content": content})
            end_llm_time = time.perf_counter()
            self.llm_logger.info(f"New response from LLM. Answer: {answer} \n\n Content: {content}")

            end_time = time.perf_counter()
            self.save_metrics(
                query="report for file: " + file,
                action_type=AgentActionType.REPORT,
                start_time=start_time,
                start_upload_time=start_upload_time,
                start_llm_time=start_llm_time,
                end_time=end_time,
                end_llm_time=end_llm_time,
                end_upload_time=end_upload_time
            )

            if answer:
                return answer
            else:
                self.llm_logger.error(f"No report generated for file: {file}")
                return self.msg_templates.generic_error()

        except Exception as e:
            raise Exception(f"Error during report generation: {e}")

    def save_metrics(
            self,
            action_type=None,
            query="",
            start_time=0.0,
            start_llm_time=0.0,
            start_rag_time=0.0,
            start_upload_time=None,
            end_time=0.0,
            end_llm_time=0.0,
            end_rag_time=0.0,
            end_upload_time=None,
            retrieve_results=[]
    ):
        try:
            if not isinstance(action_type, AgentActionType):
                raise ValueError("Action type must be AgentActionType instance")

            req_metrics = AgentPerformanceMetrics(
                action_type=action_type.value,
                query=query,
                total_time=round(end_time - start_time,2),
                llm_time=round(end_llm_time - start_llm_time,2),
            )

            if start_upload_time and end_upload_time:
                req_metrics.upload_time = round(end_upload_time - start_upload_time,2)

            rag_metrics = None

            if len(retrieve_results) > 0:

                scores = [float(res.score) for res in retrieve_results if res.score]
                if scores:
                    best_score = max(scores)
                    worst_score = min(scores)
                    mean_score = sum(scores) / len(scores)

                chunks_ids = ",".join([res.id_ for res in retrieve_results])

                rag_metrics = RAGPerformanceMetrics(
                    query=query,
                    total_time=round(end_rag_time - start_rag_time,2),
                    best_score=round(best_score,2) or 0,
                    worst_score=round(worst_score,2) or 0,
                    mean_score=round(mean_score,2) or 0,
                    chunks_ids=chunks_ids
                )

            collector = MetricsCollector(agent_metrics=req_metrics, rag_metrics=rag_metrics)
            collector.save()

        except Exception as e:
            self.mon_logger.error(f"Error during saving metrics: {e}")
