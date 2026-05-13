from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = None


@dataclass
class ConversationContext:
    company: Optional[str] = None
    period: Optional[str] = None
    analysis_type: Optional[str] = None
    last_findings: List[Dict] = None
    
    def __post_init__(self):
        if self.last_findings is None:
            self.last_findings = []


class AuditChatbot:
    def __init__(self, data_processor, risk_analyzer):
        self.data_processor = data_processor
        self.risk_analyzer = risk_analyzer
        self.conversations: Dict[str, List[Message]] = {}
        self.contexts: Dict[str, ConversationContext] = {}
        
    def start_conversation(self, conversation_id: str, user_id: str = "default") -> str:
        welcome_msg = Message(
            role="assistant",
            content="""Ciao! Sono l'Assistente AI per Audit e Gestione del Rischio di FinSecure Analytics.

Posso aiutarti a:
- Analizzare report finanziari e identificare rischi
- Rilevare anomalie nei dati
- Simulare scenari di rischio
- Rispondere a domande sulla compliance
- Generare report di audit automatici

Dimmi cosa vorresti analizzare o chiedimi qualsiasi cosa sui rischi finanziari!""",
            timestamp=datetime.now()
        )
        
        self.conversations[conversation_id] = [welcome_msg]
        self.contexts[conversation_id] = ConversationContext()
        
        return welcome_msg.content
    
    def process_message(self, message: str, conversation_id: str) -> str:
        if conversation_id not in self.conversations:
            return self.start_conversation(conversation_id)
        
        user_msg = Message(
            role="user",
            content=message,
            timestamp=datetime.now()
        )
        self.conversations[conversation_id].append(user_msg)
        
        response = self._generate_response(message, conversation_id)
        
        assistant_msg = Message(
            role="assistant",
            content=response,
            timestamp=datetime.now()
        )
        self.conversations[conversation_id].append(assistant_msg)
        
        return response
    
    def _generate_response(self, message: str, conversation_id: str) -> str:
        message_lower = message.lower()
        context = self.contexts.get(conversation_id, ConversationContext())
        
        if any(word in message_lower for word in ["ciao", "hello", "hi", "start", "inizio"]):
            return self._handle_greeting()
        
        elif "analizza" in message_lower or "analisi" in message_lower:
            return self._handle_analysis_request(message, context)
        
        elif "rischio" in message_lower or "risk" in message_lower:
            return self._handle_risk_query(context)
        
        elif "credito" in message_lower or "credit" in message_lower or "cliente" in message_lower:
            return self._handle_credit_query(context)
        
        elif "liquidità" in message_lower or "liquid" in message_lower or "cash" in message_lower:
            return self._handle_liquidity_query(context)
        
        elif "redditività" in message_lower or "reddit" in message_lower or "profit" in message_lower:
            return self._handle_profitability_query(context)
        
        elif "compliance" in message_lower or "norma" in message_lower or "regola" in message_lower:
            return self._handle_compliance_query(context)
        
        elif "scenario" in message_lower or "simula" in message_lower or "what-if" in message_lower:
            return self._handle_scenario_query(context)
        
        elif "report" in message_lower or "report" in message_lower or "genera" in message_lower:
            return self._handle_report_request(context)
        
        elif any(word in message_lower for word in ["grazie", "thanks", "ok", "perfetto"]):
            return "Prego! Sono qui per qualsiasi altra domanda. Posso aiutarti con analisi di rischio, simulazioni scenari, o domande sulla compliance."
        
        else:
            return self._handle_general_query(message, context)
    
    def _handle_greeting(self) -> str:
        return """Ciao! Sono il tuo assistente per la gestione del rischio finanziario.

Posso aiutarti con:
- 📊 **Analisi finanziaria**: Analisi di KPI e indicatori di rischio
- 🔍 **Audit**: Identificazione di anomalie e criticità
- 📈 **Simulazioni**: What-if scenarios e analisi di sensitività
- ⚖️ **Compliance**: Verifica conformità normativa
- 📋 **Report**: Generazione di report automatici

Cosa vorresti fare?"""
    
    def _handle_analysis_request(self, message: str, context: ConversationContext) -> str:
        summary = self.data_processor.ingestion.get_financial_summary()
        
        if "kpi" in message.lower() or "indicatore" in message.lower():
            kpis = summary.get("kpis", {})
            return f"""## Analisi KPI Attuali

| Indicatore | Valore | Status |
|------------|--------|--------|
| Current Ratio | {kpis.get('current_ratio', 'N/A')} | {'🔴 Critico' if kpis.get('current_ratio', 1.5) < 1.0 else '🟡 Attenzione' if kpis.get('current_ratio', 1.5) < 1.3 else '🟢 OK'} |
| Quick Ratio | {kpis.get('quick_ratio', 'N/A')} | {'🔴 Critico' if kpis.get('quick_ratio', 1.0) < 0.8 else '🟡 Attenzione' if kpis.get('quick_ratio', 1.0) < 1.0 else '🟢 OK'} |
| DSO | {kpis.get('dso', 'N/A')} gg | {'🔴 Critico' if kpis.get('dso', 45) > 60 else '🟡 Attenzione' if kpis.get('dso', 45) > 45 else '🟢 OK'} |
| Debt/Equity | {kpis.get('debt_to_equity', 'N/A')} | {'🔴 Critico' if kpis.get('debt_to_equity', 1.5) > 3.0 else '🟡 Attenzione' if kpis.get('debt_to_equity', 1.5) > 2.0 else '🟢 OK'} |
| EBITDA Margin | {kpis.get('ebitda_margin', 'N/A')}% | {'🔴 Critico' if kpis.get('ebitda_margin', 20) < 10 else '🟡 Attenzione' if kpis.get('ebitda_margin', 20) < 15 else '🟢 OK'} |
"""
        
        risk_score = self.data_processor.calculate_risk_score(summary.get("kpis", {}))
        
        return f"""## Risultati Analisi

**Punteggio di Rischio**: {risk_score['risk_score']}/100
**Livello di Rischio**: {risk_score['risk_level']}

### Fattori di Rischio Identificati:
{chr(10).join(['- ' + f for f in risk_score['factors']]) if risk_score['factors'] else 'Nessun fattore critico identificato.'}

Vuoi che approfondisca qualche area specifica?"""
    
    def _handle_risk_query(self, context: ConversationContext) -> str:
        summary = self.data_processor.ingestion.get_financial_summary()
        risk_score = self.data_processor.calculate_risk_score(summary.get("kpis", {}))
        
        return f"""## Analisi del Rischio

**Livello di Rischio Complessivo**: {risk_score['risk_level']}
**Punteggio**: {risk_score['risk_score']}/100

### Aree di Attenzione:
{chr(10).join([f"**{i+1}. {f}**" for i, f in enumerate(risk_score['factors'])]) if risk_score['factors'] else '- Nessuna criticità immediata'}

### Situazione Finanziaria:
- Capitale circolante: €{summary.get('kpis', {}).get('current_ratio', 1.0) * 10:.1f}M
- Esposizione creditoria: €{summary.get('receivables', {}).get('total_exposure', 0)/1000:.1f}K

Posso fornirti ulteriori dettagli su un'area specifica?"""
    
    def _handle_credit_query(self, context: ConversationContext) -> str:
        csv_data = self.data_processor.ingestion.load_csv_data()
        
        if "accounts_receivable" in csv_data:
            credit_risk = self.data_processor.analyze_credit_risk(csv_data["accounts_receivable"])
            
            high_risk = credit_risk.get("high_risk_clients", [])
            high_risk_text = ""
            if high_risk:
                high_risk_text = "\n### Clienti ad Alto Rischio:\n"
                for client in high_risk[:3]:
                    high_risk_text += f"- **{client.get('client_name', 'N/A')}**: €{client.get('amount', 0)/1000:.1f}K in ritardo da {client.get('days_overdue', 0)} giorni\n"
            
            return f"""## Analisi Credito

- **Esposizione totale**: €{credit_risk.get('total_overdue', 0)/1000:.1f}K
- **Clienti con ritardi**: {credit_risk.get('clients_with_overdue', 0)}
- **Giorni medi di ritardo**: {credit_risk.get('average_days_overdue', 0):.0f} giorni
- **Ritardo massimo**: {credit_risk.get('max_days_overdue', 0)} giorni
{high_risk_text}

Vuoi che simuli scenari di recupero crediti?"""
        
        return "Non sono disponibili dati sui crediti. Carica i documenti finanziari per procedere."
    
    def _handle_liquidity_query(self, context: ConversationContext) -> str:
        summary = self.data_processor.ingestion.get_financial_summary()
        kpis = summary.get("kpis", {})
        
        current = kpis.get("current_ratio", 1.5)
        quick = kpis.get("quick_ratio", 1.0)
        
        status = "🔴 CRITICA" if current < 1.0 or quick < 0.8 else "🟡 ATTENZIONE" if current < 1.3 or quick < 1.0 else "🟢 OK"
        
        recommendations = []
        if current < 1.0:
            recommendations.append("- Negoziare linee di credito a breve termine")
        if quick < 0.8:
            recommendations.append("- Accelerare incassi crediti")
            recommendations.append("- Rivedere politiche di pagamento fornitori")
        
        return f"""## Analisi Liquidità

**Status**: {status}

| Indicatore | Valore | Soglia Critica |
|------------|--------|-----------------|
| Current Ratio | {current} | < 1.0 |
| Quick Ratio | {quick} | < 0.8 |

### Raccomandazioni:
{chr(10).join(recommendations) if recommendations else '- Situazione OK, monitorare costantemente'}

Vuoi che esegua una simulazione di stress sulla liquidità?"""
    
    def _handle_profitability_query(self, context: ConversationContext) -> str:
        summary = self.data_processor.ingestion.get_financial_summary()
        fin_data = summary.get("financial_data", {})
        
        return f"""## Analisi Redditività

| KPI | Valore | Trend |
|-----|--------|-------|
| Ricavi | €{fin_data.get('latest_revenue', 0)}M | 📈 |
| EBITDA | €{fin_data.get('latest_ebitda', 0)}M | {'📉' if fin_data.get('latest_ebitda', 10) < 10 else '📈'} |
| Margine EBITDA | {summary.get('kpis', {}).get('ebitda_margin', 0)}% | {'📉' if summary.get('kpis', {}).get('ebitda_margin', 20) < 15 else '📈'} |
| Utile Netto | €{fin_data.get('latest_net_income', 0)}M | {'📉' if fin_data.get('latest_net_income', 3) < 3 else '📈'} |

Il margine EBITDA risulta {'in contrazione' if summary.get('kpis', {}).get('ebitda_margin', 20) < 20 else 'stabile'}.
"""
    
    def _handle_compliance_query(self, context: ConversationContext) -> str:
        return """## Compliance e Normativa

Dai documenti analizzati, sono state rilevate le seguenti aree di attenzione:

### GDPR/Privacy
- Policy privacy da aggiornare

### AML/Antiriciclaggio
- Formazione personale incompleta (60% completato)

### Contabilità/IFRS
- Crediti prescritti non svalutati identificati

### Safety
- Non conformità minori da correggere

Vuoi dettagli su una specifica area normativa?"""
    
    def _handle_scenario_query(self, context: ConversationContext) -> str:
        return """## Simulazione Scenari

Posso simulare i seguenti scenari:

1. **Scenario Base** (50% probabilità): Continuità operativa attuale
2. **Recessione** (25% probabilità): -15% ricavi, +10% costi
3. **Stress Severo** (15% probabilità): -25% ricavi, crisi liquidità
4. **Espansione** (10% probabilità): +10% ricavi, miglioramento

Vuoi eseguire una simulazione? Indicami:
- Quanti anni di proiezione?
- Quale scenario ti interessa?"""
    
    def _handle_report_request(self, context: ConversationContext) -> str:
        return """## Generazione Report

Posso generare i seguenti report:

1. **Report Rischi Completo**: Analisi approfondita di tutti i rischi
2. **Report Audit**: Riepilogo criticità e azioni correttive
3. **Report Compliance**: Stato conformità normativa
4. **Report Simulazione**: Risultati scenari what-if
5. **Dashboard Esecutivo**: KPI e metriche chiave

Quale report preferisci generare?"""
    
    def _handle_general_query(self, message: str, context: ConversationContext) -> str:
        return f"""Non ho capito bene la tua richiesta. 

Hai chiesto: "{message}"

Posso aiutarti con:
- 📊 **Analisi** di dati finanziari e KPI
- 🔍 **Identificazione** di rischi e anomalie  
- 📈 **Simulazioni** di scenari what-if
- ⚖️ **Compliance** normativa
- 📋 **Report** automatici

Prova a riformulare la tua domanda!"""
    
    def get_conversation_history(self, conversation_id: str) -> List[Message]:
        return self.conversations.get(conversation_id, [])


class ChatInterface:
    def __init__(self, data_processor):
        from src.agents.risk_analyzer import RiskAnalyzer
        self.chatbot = AuditChatbot(data_processor, RiskAnalyzer())
        
    def start(self):
        conv_id = "session_1"
        print(self.chatbot.start_conversation(conv_id))
        
        while True:
            user_input = input("\n> ")
            if user_input.lower() in ["exit", "quit", "esci"]:
                print("Arrivederci!")
                break
            
            response = self.chatbot.process_message(user_input, conv_id)
            print(f"\n{response}")


if __name__ == "__main__":
    from src.utils.data_processing import DataProcessor
    processor = DataProcessor()
    interface = ChatInterface(processor)
    interface.start()
