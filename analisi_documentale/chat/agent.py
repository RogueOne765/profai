from chat.standard_messages import StandardMessages
from prompt import ChainPrompt
from rag.rag_system import RAGSystem
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser


class ChatAgent():
    """
    Classe per interfaccia sistema RAG->LLM
    """
    def __init__(self, rag_system: RAGSystem):
        """
        Inizializza client LLM e chain con LangChain
        """
        if not isinstance(rag_system, RAGSystem):
            raise ValueError("rag_system must be a RAGSystem object")

        self.rag_system = rag_system

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )

        self.prompts = ChainPrompt()

        self.messages = StandardMessages()

    def start_chatbot(self):
        """Avvia chat con l'utente"""

        self.messages.welcome()

        while True:
            question = input("Tu: ").strip()

            if question.lower() in ['exit', 'quit', 'esci']:
                print("Arrivederci!")
                break

            if not question:
                print("Bot: Per favore scrivi qualcosa!")
                continue

            answer = self.ask_agent(question)
            print(f"Bot: {answer}")

    def ask_agent(self, query):
        """
        Metodo che gestisce retrieval e chiamata verso llm
        """
        if not isinstance(query, str):
            raise ValueError("query must be a string")
        if not query:
            raise ValueError("query must not be empty")

        try:
            context_results = self.rag_system.retrieve(query)

            if len(context_results) == 0:
                return "Non ho trovato nulla su questo argomento"

            context = "\n---\n".join([res.text for res in context_results])

            chain = self.prompts.simple_query() | self.llm | StrOutputParser()
            answer = chain.invoke({"context": context, "question": query})

            return answer

        except Exception as e:
            raise Exception(f"Error asking agent: {e}")

    def generate_report(self, file):
        """ Metodo per generazione report strutturato a partire da file """
        if not file:
            raise ValueError("file must be provided")

        try:
            chain = self.prompts.report() | self.llm | StrOutputParser()
            answer = chain.invoke({"file": file})

            return answer

        except Exception as e:
            raise Exception(f"Error during report generation: {e}")
