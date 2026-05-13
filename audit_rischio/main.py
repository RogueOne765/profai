import os
import sys
from typing import Optional, List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.data_processing import DataProcessor, DataIngestion
from src.agents.risk_analyzer import RiskAnalyzer, ReportGenerator
from src.agents.scenario_simulator import RiskSimulator


class FinancialRiskAgent:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.processor = DataProcessor()
        self.ingestion = self.processor.ingestion
        self.risk_analyzer = RiskAnalyzer()
        
    def initialize(self) -> Dict[str, Any]:
        summary = self.ingestion.get_financial_summary()
        
        documents = self.ingestion.load_documents()
        
        return {
            "status": "initialized",
            "documents_loaded": len(documents),
            "summary": summary
        }
    
    def analyze_risks(self) -> Dict[str, Any]:
        summary = self.ingestion.get_financial_summary()
        kpis = summary.get("kpis", {})
        
        findings = self.risk_analyzer.analyze_financial_health(kpis)
        risk_score = self.processor.calculate_risk_score(kpis)
        
        csv_data = self.ingestion.load_csv_data()
        credit_risk = {}
        if "accounts_receivable" in csv_data:
            credit_risk = self.processor.analyze_credit_risk(csv_data["accounts_receivable"])
        
        return {
            "risk_score": risk_score,
            "findings": [
                {
                    "finding": f.finding,
                    "risk_level": f.risk_level.value,
                    "category": f.category,
                    "recommendation": f.recommendation
                }
                for f in findings
            ],
            "credit_risk": credit_risk
        }
    
    def run_scenario_simulation(self, baseline: Optional[Dict] = None) -> Dict[str, Any]:
        if baseline is None:
            summary = self.ingestion.get_financial_summary()
            baseline = {
                "revenue": summary.get("financial_data", {}).get("latest_revenue", 45.0),
                "ebitda": summary.get("financial_data", {}).get("latest_ebitda", 9.3),
                "ebitda_margin": summary.get("kpis", {}).get("ebitda_margin", 19.0) / 100,
                "total_liabilities": summary.get("financial_data", {}).get("total_liabilities", 40.0),
                "current_ratio": summary.get("kpis", {}).get("current_ratio", 1.14),
                "quick_ratio": summary.get("kpis", {}).get("quick_ratio", 0.72)
            }
        
        simulator = RiskSimulator(baseline)
        results = simulator.simulate(3)
        
        default_prob = simulator.calculate_default_probability(results)
        var = simulator.get_value_at_risk(results)
        monte_carlo = simulator.monte_carlo_simulation(1000)
        
        return {
            "baseline": baseline,
            "scenarios": simulator.export_results(results, "json"),
            "default_probability": default_prob,
            "value_at_risk": var,
            "monte_carlo": monte_carlo
        }
    
    def generate_report(self) -> str:
        summary = self.ingestion.get_financial_summary()
        risk_analysis = self.analyze_risks()
        
        report_gen = ReportGenerator()
        
        findings = self.risk_analyzer.analyze_financial_health(summary.get("kpis", {}))
        report = report_gen.generate_report(
            financial_data=summary.get("kpis", {}),
            risk_findings=findings if findings else [],
            compliance_gaps={}
        )
        
        return report
    
    def query_documents(self, query: str) -> List[Dict[str, Any]]:
        documents = self.ingestion.load_documents()
        
        results = []
        query_lower = query.lower()
        
        for doc in documents:
            if query_lower in doc.content.lower():
                start = doc.content.lower().find(query_lower)
                context = doc.content[max(0, start-100):start+200]
                results.append({
                    "document": doc.title,
                    "type": doc.doc_type,
                    "company": doc.company,
                    "context": context
                })
        
        return results


def main():
    print("=" * 60)
    print("FinSecure Analytics - Agente AI per Gestione Rischio")
    print("=" * 60)
    
    agent = FinancialRiskAgent()
    
    print("\n[1] Inizializzazione...")
    init_result = agent.initialize()
    print(f"   Status: {init_result['status']}")
    print(f"   Documenti caricati: {init_result['documents_loaded']}")
    
    print("\n[2] Analisi dei Rischi...")
    risk_analysis = agent.analyze_risks()
    print(f"   Risk Score: {risk_analysis['risk_score']['risk_score']}/100")
    print(f"   Livello: {risk_analysis['risk_score']['risk_level']}")
    print(f"   Criticità trovate: {len(risk_analysis['findings'])}")
    
    print("\n[3] Simulazione Scenari...")
    simulation = agent.run_scenario_simulation()
    print(f"   Probabilità default: {simulation['default_probability']}%")
    print(f"   VaR (EBITDA): €{simulation['value_at_risk']['var_ebitda']}M")
    
    print("\n[4] Query Documenti...")
    docs = agent.query_documents("credito")
    print(f"   Risultati trovati: {len(docs)}")
    
    print("\n" + "=" * 60)
    print("Inizializzazione completata!")
    print("Per avviare la dashboard: streamlit run src/dashboard/dashboard.py")
    print("Per il chatbot interattivo: python -m src.chatbot.audit_chatbot")
    print("=" * 60)


if __name__ == "__main__":
    main()
