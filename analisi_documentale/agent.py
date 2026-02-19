from rag.rag_system import RAGSystem
from langchain_core.prompts import ChatPromptTemplate
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

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Sei un assistente utile. Usa il seguente contesto per rispondere alla domanda. Se non conosci la risposta, di' semplicemente che non la sai, non provare a inventarne una."),
            ("human", "Contesto: {context}\nDomanda: {question}"),
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()


    def start_chatbot(self):
        """Avvia chat con l'utente"""

        self._print_welcome_message()

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

    def _print_welcome_message(self):
        print("ChatBot avviato!")
        print("""

        ====================

        Il sistema può rispondere su vari domini:
            - guida generale allo studente (es. come cambiare sede o corso, inizio lezioni etc.)
            - come avviare procedure tirocinio (marketing)
            - elenco enti disponibili per tirocinio (marketing)
            - linee guida elaborazione e stesura tesi (giurisprudenza)

        es1: Quali sono gli elementi principali per creare Backend API in python?
        es2: Come avviare procedura per inizio tirocinio?

        ====================

        """)
        print("(scrivi 'exit' per uscire)")

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

            if (len(context_results) == 0):
                return "Non ho trovato nulla su questo argomento"

            context_prompt = "\n---\n".join([res.text for res in context_results])
            answer = self.chain.invoke({"context": context_prompt, "question": query})

            return answer

        except Exception as e:
            raise Exception(f"Error asking agent: {e}")
            return "Errore nell'elaborazione della richiesta."
