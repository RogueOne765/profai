from typing import List

class MessagePrinter:

    def __init__(self):
        self.chat_commands = """
            Comandi per le funzionalità:
                - scrivi 'exit' per uscire
                - scrivi 'upload' per caricare un file e generare report
        """

    def welcome_rag_enabled(self):
        print(f"""
        "ChatBot avviato!"
        
        ====================

        Il sistema può rispondere su vari domini:
            - guida generale allo studente (es. come cambiare sede o corso, inizio lezioni etc.)
            - come avviare procedure tirocinio (marketing)
            - elenco enti disponibili per tirocinio (marketing)
            - linee guida elaborazione e stesura tesi (giurisprudenza)

        es: Come avviare procedura per inizio tirocinio?

        ====================
        
        {self.chat_commands}

        """)

    def welcome_rag_disabled(self):
        print(f"""
        "ChatBot avviato!"
        
        ====================

        ATTENZIONE RAG DISABILITATO
        Le risposte saranno basate solo sulla conoscenza del LLM interrogato

        ====================
    
        {self.chat_commands}
        """)

    def goodbye(self):
        print("Arrivederci!")

    def wrong_bitch(self):
        print("Bot: Per favore scrivi qualcosa!")

    def no_results(self):
        print("Non ho trovato nulla su questo argomento")

    def bot_answer(self, answer):
        print(f"Bot: {answer}")

    def no_content_extracted(self):
        print("Non ho trovato contenuti testuali all'interno del file fornito")

    def generic_error(self):
        print("Si è verificato un errore durante l'elaborazione della richiesta. Riprovare.")

    def file_format_not_permitted(self, expected_formats: List[str]):
        print(f"Formato file caricato non consentito. Permessi file con estensione: {", ".join(expected_formats)}")

    def max_input_tokens(self):
        print("Il file caricato supera il limite di grandezza consentito")
