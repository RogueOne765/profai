import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from langchain_openai import ChatOpenAI
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


class RiskLevel(Enum):
    LOW = "BASSO"
    MEDIUM = "MEDIO"
    HIGH = "ALTO"
    CRITICAL = "CRITICO"


@dataclass
class AnalysisResult:
    finding: str
    risk_level: RiskLevel
    category: str
    recommendation: str
    evidence: List[str]


class RiskAnalyzer:
    def __init__(self, llm: Optional[Any] = None):
        self.llm = llm
        self.findings = []
        
    def analyze_financial_health(self, financial_data: Dict) -> List[AnalysisResult]:
        findings = []
        
        if financial_data.get("current_ratio", 1.5) < 1.0:
            findings.append(AnalysisResult(
                finding="Current ratio sotto la soglia critica",
                risk_level=RiskLevel.CRITICAL,
                category="Liquidità",
                recommendation="Implementare piano emergenza liquidità. Negoziare linee di credito aggiuntive.",
                evidence=[f"Current ratio: {financial_data.get('current_ratio')}"]
            ))
        
        if financial_data.get("quick_ratio", 1.0) < 0.8:
            findings.append(AnalysisResult(
                finding="Quick ratio critico - scarsa liquidità immediata",
                risk_level=RiskLevel.CRITICAL,
                category="Liquidità",
                recommendation="Accelerare incassi crediti, rinegoziare debiti a breve termine.",
                evidence=[f"Quick ratio: {financial_data.get('quick_ratio')}"]
            ))
        
        if financial_data.get("dso", 45) > 60:
            findings.append(AnalysisResult(
                finding="DSO eccessivo - slow collection",
                risk_level=RiskLevel.HIGH,
                category="Credito",
                recommendation="Implementare solleciti automatici, rivedere politiche di credito.",
                evidence=[f"DSO: {financial_data.get('dso')} giorni"]
            ))
        
        if financial_data.get("debt_to_equity", 1.5) > 3.0:
            findings.append(AnalysisResult(
                finding="Eccessivo indebitamento",
                risk_level=RiskLevel.HIGH,
                category="Struttura finanziaria",
                recommendation="Piano di rientro del debito, valutare aumenti di capitale.",
                evidence=[f"Debt/Equity: {financial_data.get('debt_to_equity')}"]
            ))
        
        if financial_data.get("ebitda_margin", 20) < 10:
            findings.append(AnalysisResult(
                finding="Margine EBITDA critico",
                risk_level=RiskLevel.CRITICAL,
                category="Redditività",
                recommendation="Ridurre costi operativi, rivedere pricing strategy.",
                evidence=[f"EBITDA margin: {financial_data.get('ebitda_margin')}%"]
            ))
        
        return findings
    
    def analyze_audit_findings(self, audit_text: str) -> List[AnalysisResult]:
        findings = []
        
        keywords_critical = ["criticità alta", "allarme", "rischio elevato", "non conforme"]
        keywords_high = ["attenzione", "migliorare", "non completamente"]
        keywords_medium = ["correzione", "da verificare"]
        
        for keyword in keywords_critical:
            if keyword.lower() in audit_text.lower():
                findings.append(AnalysisResult(
                    finding=f"Rischio critico rilevato: {keyword}",
                    risk_level=RiskLevel.CRITICAL,
                    category="Audit",
                    recommendation="Intervento immediato richiesto",
                    evidence=[f"Riferimento trovato nel testo: {keyword}"]
                ))
        
        for keyword in keywords_high:
            if keyword.lower() in audit_text.lower():
                findings.append(AnalysisResult(
                    finding=f"Area da migliorare: {keyword}",
                    risk_level=RiskLevel.HIGH,
                    category="Audit",
                    recommendation="Piano correttivo entro 30 giorni",
                    evidence=[f"Riferimento trovato nel testo: {keyword}"]
                ))
        
        return findings
    
    def identify_compliance_gaps(self, documents: List[str]) -> Dict[str, List[str]]:
        gaps = {
            "GDPR": [],
            "AML": [],
            "IFRS": [],
            "Safety": []
        }
        
        for doc in documents:
            doc_lower = doc.lower()
            
            if "gdpr" in doc_lower or "privacy" in doc_lower:
                if "non conforme" in doc_lower or "da aggiornare" in doc_lower:
                    gaps["GDPR"].append("Policy privacy non aggiornata o non conforme")
            
            if "aml" in doc_lower or "riciclaggio" in doc_lower:
                if "60%" in doc_lower or "formazione" in doc_lower:
                    gaps["AML"].append("Formazione AML incompleta")
            
            if "ifrs" in doc_lower or "contabile" in doc_lower:
                if "errore" in doc_lower or "rettifica" in doc_lower:
                    gaps["IFRS"].append("Possibili errori contabili rilevati")
        
        return gaps


class ReportGenerator:
    def __init__(self):
        self.template = """
        # Rapporto di Analisi del Rischio
        
        ## Sommario Esecutivo
        {executive_summary}
        
        ## Dettaglio Risultati
        
        ### Indicatori Chiave
        {kpi_summary}
        
        ### Risultati Analisi
        {findings}
        
        ## Raccomandazioni
        {recommendations}
        
        ## Prossimi Passi
        {next_steps}
        """
    
    def generate_report(self, 
                       financial_data: Dict,
                       risk_findings: List[AnalysisResult],
                       compliance_gaps: Dict) -> str:
        
        kpi_lines = []
        for key, value in financial_data.items():
            kpi_lines.append(f"- {key}: {value}")
        kpi_summary = "\n".join(kpi_lines)
        
        findings_lines = []
        for finding in risk_findings:
            findings_lines.append(f"### {finding.category} - {finding.risk_level.value}")
            findings_lines.append(f"**Reperto**: {finding.finding}")
            findings_lines.append(f"**Raccomandazione**: {finding.recommendation}")
            findings_lines.append("")
        findings_summary = "\n".join(findings_lines)
        
        rec_lines = []
        for finding in risk_findings:
            rec_lines.append(f"- [{finding.risk_level.value}] {finding.recommendation}")
        recommendations = "\n".join(rec_lines)
        
        gaps_lines = []
        for area, issues in compliance_gaps.items():
            if issues:
                gaps_lines.append(f"### {area}")
                for issue in issues:
                    gaps_lines.append(f"- {issue}")
        gaps_summary = "\n".join(gaps_lines) if gaps_lines else "Nessuna criticità rilevata"
        
        report = self.template.format(
            executive_summary=f"Analisi completata con {len(risk_findings)} criticità rilevate.",
            kpi_summary=kpi_summary,
            findings=findings_summary,
            recommendations=recommendations,
            next_steps=f"Follow-up previsto entro 30 giorni. Aree critiche: {gaps_summary}"
        )
        
        return report


if __name__ == "__main__":
    test_data = {
        "current_ratio": 0.95,
        "quick_ratio": 0.72,
        "dso": 65,
        "debt_to_equity": 1.35,
        "ebitda_margin": 19.0
    }
    
    analyzer = RiskAnalyzer()
    findings = analyzer.analyze_financial_health(test_data)
    
    for f in findings:
        print(f"[{f.risk_level.value}] {f.finding}")
        print(f"   -> {f.recommendation}")
