from typing import List

class ChatMessagesTemplates:

    def __init__(self):
        self.chat_commands = """
            Comandi per le funzionalità:
                - scrivi 'exit' per uscire
                - scrivi 'upload' per caricare un file e generare report
        """

    def welcome_rag_enabled(self):
        return f"""
        "ChatBot avviato!"
        
        ====================

        Il sistema può generare insight sui report finanziari di DataTrust Solutions.
        es: Quali sono i punti principali riguardo area di performance finanziaria degli ultimi anni?

        ====================
        
        {self.chat_commands}

        """

    def welcome_rag_disabled(self):
        return f"""
        "ChatBot avviato!"
        
        ====================

        ATTENZIONE RAG DISABILITATO
        Le risposte saranno basate solo sulla conoscenza del LLM interrogato

        ====================
    
        {self.chat_commands}
        """

    def goodbye(self):
        return "Arrivederci!"

    def wrong_bitch(self):
        return "Bot: Per favore scrivi qualcosa!"

    def no_results(self):
        return "Non ho trovato nulla su questo argomento"

    def bot_answer(self, answer):
        return f"Bot:\n {answer}"

    def no_content_extracted(self):
        return "Non ho trovato contenuti testuali all'interno del file fornito"

    def generic_error(self):
        return "Si è verificato un errore durante l'elaborazione della richiesta. Riprovare."

    def file_format_not_permitted(self, expected_formats: List[str]):
        return f"Formato file caricato non consentito. Permessi file con estensione: {", ".join(expected_formats)}"

    def max_input_tokens(self):
        return "Il file caricato supera il limite di grandezza consentito"
