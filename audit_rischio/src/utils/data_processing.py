import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

try:
    from llama_index import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
    from llama_index.node_parser import SimpleNodeParser
    from llama_index.embeddings import HuggingFaceEmbedding
    LLAMA_INDEX_AVAILABLE = True
except ImportError:
    LLAMA_INDEX_AVAILABLE = False


@dataclass
class FinancialDocument:
    doc_id: str
    title: str
    content: str
    doc_type: str
    date: Optional[str] = None
    company: Optional[str] = None
    metadata: Dict[str, Any] = None


class DataIngestion:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.documents_dir = self.data_dir / "documents"
        self.csv_dir = self.data_dir / "csv"
        self.storage_dir = self.data_dir / "storage"
        
    def load_csv_data(self) -> Dict[str, pd.DataFrame]:
        csv_files = {}
        for csv_file in self.csv_dir.glob("*.csv"):
            df = pd.read_csv(csv_file)
            csv_files[csv_file.stem] = df
        return csv_files
    
    def load_documents(self) -> List[FinancialDocument]:
        docs = []
        for txt_file in self.documents_dir.glob("*.txt"):
            content = txt_file.read_text(encoding='utf-8')
            doc_type = self._classify_document(txt_file.name)
            company = self._extract_company(txt_file.name)
            date = self._extract_date(content)
            
            doc = FinancialDocument(
                doc_id=txt_file.stem,
                title=txt_file.name,
                content=content,
                doc_type=doc_type,
                date=date,
                company=company,
                metadata={}
            )
            docs.append(doc)
        return docs
    
    def _classify_document(self, filename: str) -> str:
        filename_lower = filename.lower()
        if "q1" in filename_lower or "q2" in filename_lower:
            return "quarterly_report"
        elif "audit" in filename_lower:
            return "audit_report"
        elif "risk" in filename_lower:
            return "risk_analysis"
        elif "aml" in filename_lower or "policy" in filename_lower:
            return "compliance_policy"
        return "general"
    
    def _extract_company(self, filename: str) -> Optional[str]:
        name = filename.replace(".txt", "")
        for part in ["Alpha Industries", "Beta Financial", "Gamma Corp", "Delta Financial"]:
            if part.lower() in name.lower():
                return part
        return "Unknown"
    
    def _extract_date(self, content: str) -> Optional[str]:
        lines = content.split('\n')
        for line in lines[:5]:
            if "data" in line.lower() and "2024" in line:
                return line.strip()
        return None
    
    def create_vector_index(self, documents: List[FinancialDocument]) -> Any:
        if not LLAMA_INDEX_AVAILABLE:
            print("LlamaIndex not available, using simple fallback")
            return None
            
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        from llama_index import Document
        llama_docs = [Document(text=doc.content, doc_id=doc.doc_id, 
                              extra_info={"type": doc.doc_type, "company": doc.company})
                      for doc in documents]
        
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        index = VectorStoreIndex.from_documents(
            llama_docs,
            embed_model=embed_model,
            show_progress=True
        )
        
        index.storage_context.persist(persist_dir=str(self.storage_dir))
        return index
    
    def load_vector_index(self) -> Any:
        if not LLAMA_INDEX_AVAILABLE:
            return None
        if not self.storage_dir.exists():
            return None
        return load_index_from_storage(StorageContext.from_defaults(
            persist_dir=str(self.storage_dir)
        ))
    
    def get_financial_summary(self) -> Dict[str, Any]:
        csv_data = self.load_csv_data()
        summary = {}
        
        if "financial_data" in csv_data:
            df = csv_data["financial_data"]
            summary["financial_data"] = {
                "total_quarters": len(df),
                "latest_revenue": float(df.iloc[-1]["revenue"]),
                "latest_ebitda": float(df.iloc[-1]["ebitda"]),
                "latest_net_income": float(df.iloc[-1]["net_income"]),
                "total_assets": float(df.iloc[-1]["total_assets"]),
                "total_liabilities": float(df.iloc[-1]["total_liabilities"]),
                "equity": float(df.iloc[-1]["equity"]),
            }
        
        if "accounts_receivable" in csv_data:
            df = csv_data["accounts_receivable"]
            total_amount = df["amount"].sum()
            overdue = df[df["status"] == "overdue"]["amount"].sum()
            summary["receivables"] = {
                "total_exposure": float(total_amount),
                "overdue_amount": float(overdue),
                "overdue_percentage": float(overdue / total_amount * 100) if total_amount > 0 else 0,
                "unique_clients": df["client_id"].nunique()
            }
        
        if "kpi_trends" in csv_data:
            df = csv_data["kpi_trends"]
            summary["kpis"] = {
                "current_ratio": float(df.iloc[-1]["current_ratio"]),
                "quick_ratio": float(df.iloc[-1]["quick_ratio"]),
                "dso": float(df.iloc[-1]["dso"]),
                "debt_to_equity": float(df.iloc[-1]["debt_to_equity"]),
                "ebitda_margin": float(df.iloc[-1]["ebitda_margin"])
            }
        
        return summary


class DataProcessor:
    def __init__(self):
        self.ingestion = DataIngestion()
        
    def calculate_risk_score(self, kpi_data: Dict) -> Dict[str, Any]:
        score = 0
        factors = []
        
        current_ratio = kpi_data.get("current_ratio", 1.5)
        if current_ratio < 1.0:
            score += 30
            factors.append("Current ratio critico (<1.0)")
        elif current_ratio < 1.3:
            score += 15
            factors.append("Current ratio basso (<1.3)")
        
        quick_ratio = kpi_data.get("quick_ratio", 1.0)
        if quick_ratio < 0.8:
            score += 25
            factors.append("Quick ratio critico (<0.8)")
        elif quick_ratio < 1.0:
            score += 10
            factors.append("Quick ratio basso (<1.0)")
        
        dso = kpi_data.get("dso", 45)
        if dso > 60:
            score += 25
            factors.append("DSO critico (>60 giorni)")
        elif dso > 45:
            score += 10
            factors.append("DSO elevato (>45 giorni)")
        
        debt_to_equity = kpi_data.get("debt_to_equity", 1.5)
        if debt_to_equity > 3.0:
            score += 20
            factors.append("Elevato indebitamento (>3.0)")
        
        ebitda_margin = kpi_data.get("ebitda_margin", 20)
        if ebitda_margin < 10:
            score += 20
            factors.append("Margine EBITDA critico (<10%)")
        elif ebitda_margin < 15:
            score += 10
            factors.append("Margine EBITDA basso (<15%)")
        
        if score >= 70:
            risk_level = "CRITICO"
        elif score >= 50:
            risk_level = "ALTO"
        elif score >= 30:
            risk_level = "MEDIO"
        else:
            risk_level = "BASSO"
        
        return {
            "risk_score": score,
            "risk_level": risk_level,
            "factors": factors,
            "timestamp": datetime.now().isoformat()
        }
    
    def detect_anomalies(self, time_series_data: pd.DataFrame, column: str) -> List[Dict]:
        if column not in time_series_data.columns:
            return []
        
        data = time_series_data[column]
        mean = data.mean()
        std = data.std()
        
        anomalies = []
        for idx, value in enumerate(data):
            z_score = (value - mean) / std if std > 0 else 0
            if abs(z_score) > 2:
                quarter = time_series_data.iloc[idx]["quarter"]
                anomalies.append({
                    "quarter": quarter,
                    "value": float(value),
                    "z_score": float(z_score),
                    "deviation": "positive" if z_score > 0 else "negative"
                })
        
        return anomalies
    
    def analyze_credit_risk(self, receivables_df: pd.DataFrame) -> Dict:
        overdue = receivables_df[receivables_df["status"] == "overdue"]
        
        risk_by_client = overdue.groupby("client_id").agg({
            "amount": "sum",
            "days_overdue": "max",
            "client_name": "first",
            "risk_score": "first"
        }).reset_index()
        
        risk_by_client = risk_by_client.sort_values("amount", ascending=False)
        
        return {
            "total_overdue": float(overdue["amount"].sum()),
            "clients_with_overdue": overdue["client_id"].nunique(),
            "max_days_overdue": int(overdue["days_overdue"].max()) if len(overdue) > 0 else 0,
            "high_risk_clients": risk_by_client[risk_by_client["risk_score"] == "High"].to_dict("records"),
            "average_days_overdue": float(overdue["days_overdue"].mean()) if len(overdue) > 0 else 0
        }


if __name__ == "__main__":
    processor = DataProcessor()
    summary = processor.ingestion.get_financial_summary()
    print(json.dumps(summary, indent=2))
