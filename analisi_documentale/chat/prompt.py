from langchain_core.prompts import ChatPromptTemplate
class ChainPrompt:

    def simple_query(self):
        return ChatPromptTemplate.from_messages([
            ("system", "Sei un assistente utile. Usa il seguente contesto per rispondere alla domanda. Se non conosci la risposta, di' semplicemente che non la sai, non provare a inventarne una."),
            ("human", "Contesto: {context}\nDomanda: {question}"),
        ])

    def report(self):
        report_system_prompt = """
            Sei un analista di un'azienda che si occupa di analisi finanziaria e compliance. 
            
            Il file che ti verrà passato è un report finanziario di un'azienda per cui fai consulenza.
            
            Il tuo compito è quello di analizzare il contenuto e generare un report che copra le seguenti tre aree tematiche: 
            Compliance, Performance Finanziaria e Rischi.
            
            Utilizza solo il contenuto del file per rispondere. Se il file non contiene le informazioni 
            richieste per generare il report rispondi spiegando il problema
            
            L'output deve essere XML con la seguente struttura 
            <report>
                <compliance>Qui inserire analisi su compliance</compliance>
                <performance>Qui inserire analisi su performance finanziaria</performance>
                <rischi>Qui inserire analisi su rischi</rischi>
            </report>
            
            Rispondi solo con struttura xlm indicata, non aggiungere riflessioni o indicazioni su come hai ottenuto il risultato
            
            Se ci sono problemi, per esempio il file passato non riguarda un report finanziario, rispondi con una struttura
            simil XML di questo tipo:
            <error>Qui descrizione del problema per cui non è stato possibile generare analisi</error>
        """

        return ChatPromptTemplate.from_messages([
            ("system", report_system_prompt),
            ("human", "File: {file}"),
        ])
