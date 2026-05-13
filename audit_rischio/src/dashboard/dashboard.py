import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Dashboard:
    def __init__(self, data_processor, risk_simulator):
        self.data_processor = data_processor
        self.risk_simulator = risk_simulator
        self.summary = data_processor.ingestion.get_financial_summary()
        
    def render_header(self):
        st.set_page_config(
            page_title="FinSecure Analytics - Dashboard Rischio Finanziario",
            page_icon="📊",
            layout="wide"
        )
        
        st.title("📊 FinSecure Analytics")
        st.markdown("### Dashboard di Gestione del Rischio Finanziario e Audit")
        st.markdown("---")
    
    def render_kpi_cards(self):
        kpis = self.summary.get("kpis", {})
        fin_data = self.summary.get("financial_data", {})
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            current_ratio = kpis.get("current_ratio", 0)
            color = "🔴" if current_ratio < 1.0 else "🟡" if current_ratio < 1.3 else "🟢"
            st.metric("Current Ratio", f"{current_ratio:.2f}", delta_color="inverse")
        
        with col2:
            quick_ratio = kpis.get("quick_ratio", 0)
            color = "🔴" if quick_ratio < 0.8 else "🟡" if quick_ratio < 1.0 else "🟢"
            st.metric("Quick Ratio", f"{quick_ratio:.2f}", delta_color="inverse")
        
        with col3:
            dso = kpis.get("dso", 0)
            color = "🔴" if dso > 60 else "🟡" if dso > 45 else "🟢"
            st.metric("DSO (gg)", f"{dso:.0f}", delta_color="inverse")
        
        with col4:
            debt_eq = kpis.get("debt_to_equity", 0)
            color = "🔴" if debt_eq > 3.0 else "🟡" if debt_eq > 2.0 else "🟢"
            st.metric("Debt/Equity", f"{debt_eq:.2f}", delta_color="inverse")
        
        with col5:
            ebitda = kpis.get("ebitda_margin", 0)
            color = "🔴" if ebitda < 10 else "🟡" if ebitda < 15 else "🟢"
            st.metric("EBITDA Margin", f"{ebitda:.1f}%")
    
    def render_risk_score(self):
        risk_score = self.data_processor.calculate_risk_score(self.summary.get("kpis", {}))
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            score = risk_score["risk_score"]
            if score >= 70:
                color = "#ff4b4b"
                status = "CRITICO"
            elif score >= 50:
                color = "#ffa500"
                status = "ALTO"
            elif score >= 30:
                color = "#ffff00"
                status = "MEDIO"
            else:
                color = "#00cc66"
                status = "BASSO"
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f"Livello Rischio: {status}"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 30], 'color': "#e8f5e9"},
                        {'range': [30, 50], 'color': "#fff3e0"},
                        {'range': [50, 70], 'color': "#ffebee"},
                        {'range': [70, 100], 'color': "#ffcdd2"}
                    ]
                }
            ))
            fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Fattori di Rischio")
            if risk_score["factors"]:
                for f in risk_score["factors"]:
                    st.warning(f"⚠️ {f}")
            else:
                st.success("✅ Nessun fattore critico rilevato")
    
    def render_financial_trends(self):
        csv_data = self.data_processor.ingestion.load_csv_data()
        
        if "kpi_trends" in csv_data:
            df = csv_data["kpi_trends"]
            
            tab1, tab2, tab3 = st.tabs(["📈 Redditività", "💰 Liquidità", "⚖️ Struttura"])
            
            with tab1:
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(
                    go.Bar(x=df["quarter"], y=df["ebitda_margin"], name="EBITDA Margin %"),
                    secondary_y=False
                )
                fig.add_trace(
                    go.Line(x=df["quarter"], y=df["net_profit_margin"], name="Net Profit Margin %"),
                    secondary_y=True
                )
                fig.update_layout(title="Trend Redditività", height=350)
                fig.update_yaxes(title="%", secondary_y=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df["quarter"], y=df["current_ratio"], name="Current Ratio", line=dict(color="blue")))
                fig.add_trace(go.Scatter(x=df["quarter"], y=df["quick_ratio"], name="Quick Ratio", line=dict(color="red")))
                fig.add_hline(y=1.0, line_dash="dash", annotation_text="Soglia Critica")
                fig.update_layout(title="Trend Liquidità", height=350)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df["quarter"], y=df["debt_to_equity"], name="Debt/Equity"))
                fig.update_layout(title="Trend Indebitamento", height=350)
                st.plotly_chart(fig, use_container_width=True)
    
    def render_credit_analysis(self):
        csv_data = self.data_processor.ingestion.load_csv_data()
        
        if "accounts_receivable" in csv_data:
            df = csv_data["accounts_receivable"]
            credit_risk = self.data_processor.analyze_credit_risk(df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Crediti Scaduti")
                overdue_df = df[df["status"] == "overdue"]
                
                fig = px.bar(
                    overdue_df.groupby("client_name")["amount"].sum().reset_index(),
                    x="client_name",
                    y="amount",
                    title="Crediti Scaduti per Cliente",
                    color="amount",
                    color_continuous_scale="Reds"
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Distribuzione Ritardi")
                status_counts = df["status"].value_counts()
                fig = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Stato Crediti",
                    color_discrete_map={"paid": "#00cc66", "overdue": "#ff4b4b"}
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            st.metric("Totale Crediti Scaduti", f"€{credit_risk.get('total_overdue', 0):,.0f}")
    
    def render_scenario_analysis(self):
        st.subheader("🔮 Simulazione Scenari")
        
        col1, col2 = st.columns(2)
        
        with col1:
            scenario_type = st.selectbox(
                "Seleziona Scenario",
                ["base", "recession", "stress", "expansion"],
                format_func=lambda x: {
                    "base": "📊 Base (50%)",
                    "recession": "📉 Recessione (25%)",
                    "stress": "⚠️ Stress Severo (15%)",
                    "expansion": "📈 Espansione (10%)"
                }[x]
            )
        
        with col2:
            years = st.slider("Anni di proiezione", 1, 5, 3)
        
        if st.button("Esegui Simulazione"):
            baseline = {
                "revenue": self.summary.get("financial_data", {}).get("latest_revenue", 45.0),
                "ebitda": self.summary.get("financial_data", {}).get("latest_ebitda", 9.3),
                "ebitda_margin": self.summary.get("kpis", {}).get("ebitda_margin", 19.0) / 100,
                "total_liabilities": self.summary.get("financial_data", {}).get("total_liabilities", 40.0),
                "current_ratio": self.summary.get("kpis", {}).get("current_ratio", 1.14),
                "quick_ratio": self.summary.get("kpis", {}).get("quick_ratio", 0.72)
            }
            
            self.risk_simulator = self.risk_simulator.__class__(baseline)
            results = self.risk_simulator.simulate(years)
            
            scenario_results = results.get(scenario_type, [])
            
            df = pd.DataFrame([{
                "Anno": r.year,
                "Ricavi": r.revenue,
                "EBITDA": r.ebitda,
                "Utile Netto": r.net_income,
                "Debito": r.debt,
                "Current Ratio": r.current_ratio,
                "Quick Ratio": r.quick_ratio
            } for r in scenario_results])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["Anno"], y=df["Ricavi"], name="Ricavi", line=dict(color="blue")))
            fig.add_trace(go.Scatter(x=df["Anno"], y=df["EBITDA"], name="EBITDA", line=dict(color="green")))
            fig.add_trace(go.Scatter(x=df["Anno"], y=df["Utile Netto"], name="Utile Netto", line=dict(color="orange")))
            fig.update_layout(title=f"Proiezione - Scenario {scenario_type.title()}", height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df, use_container_width=True)
    
    def render_compliance_panel(self):
        st.subheader("⚖️ Compliance e Audit")
        
        compliance_data = {
            "Area": ["GDPR", "AML/FT", "IFRS", "Sicurezza Lavoro", "Antifrode"],
            "Status": ["🟡 Da aggiornare", "🟢 Conforme", "🟡 Review richiesta", "🟡 Non conformità", "🟢 Conforme"],
            "Rischio": ["Medio", "Basso", "Medio", "Medio", "Basso"]
        }
        
        df = pd.DataFrame(compliance_data)
        st.table(df)
    
    def render(self):
        self.render_header()
        
        st.sidebar.title("Navigazione")
        page = st.sidebar.radio(
            "Vai a:",
            ["Dashboard", "Analisi Dettagliata", "Simulazioni", "Crediti", "Compliance"]
        )
        
        if page == "Dashboard":
            self.render_kpi_cards()
            st.markdown("### Valutazione Rischio Complessivo")
            self.render_risk_score()
            st.markdown("### Trend Finanziari")
            self.render_financial_trends()
        
        elif page == "Analisi Dettagliata":
            self.render_kpi_cards()
            self.render_risk_score()
            self.render_financial_trends()
        
        elif page == "Simulazioni":
            self.render_scenario_analysis()
        
        elif page == "Crediti":
            self.render_credit_analysis()
        
        elif page == "Compliance":
            self.render_compliance_panel()


def run_dashboard():
    from src.utils.data_processing import DataProcessor
    from src.agents.scenario_simulator import RiskSimulator
    
    processor = DataProcessor()
    simulator = RiskSimulator({
        "revenue": 45.0,
        "ebitda": 9.3,
        "ebitda_margin": 0.19,
        "total_liabilities": 40.0,
        "current_ratio": 1.14,
        "quick_ratio": 0.72
    })
    
    dashboard = Dashboard(processor, simulator)
    dashboard.render()


if __name__ == "__main__":
    run_dashboard()
