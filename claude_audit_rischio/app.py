"""
FinSecure Analytics - AI Financial Risk Management Agent
Backend API using Anthropic Claude with tool use
"""

import os
import json
import re
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)

# Initialize Anthropic client (no API key needed in Claude artifacts)
client = anthropic.Anthropic()

# Load financial documents
DOCS_DIR = Path(__file__).parent / "data" / "documents"

def load_documents():
    """Load all financial documents from the data directory."""
    docs = {}
    if DOCS_DIR.exists():
        for f in DOCS_DIR.glob("*.txt"):
            docs[f.stem] = f.read_text(encoding="utf-8")
    return docs

FINANCIAL_DOCS = load_documents()

# ─── Tool Definitions ────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "analyze_financial_report",
        "description": (
            "Analizza un report finanziario per estrarre KPI, identificare anomalie, "
            "calcolare indicatori di rischio e rilevare possibili problemi contabili. "
            "Usa questo strumento per ottenere un'analisi strutturata dei documenti finanziari."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "report_id": {
                    "type": "string",
                    "description": "ID del report da analizzare (es. 'report_Q1_2024', 'report_Q2_2024', 'audit_compliance_H1_2024')"
                },
                "focus_areas": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Aree specifiche su cui concentrare l'analisi: 'kpi', 'rischio_credito', 'rischio_mercato', 'compliance', 'anomalie_contabili', 'liquidita', 'covenant'"
                }
            },
            "required": ["report_id"]
        }
    },
    {
        "name": "simulate_risk_scenario",
        "description": (
            "Simula scenari di rischio finanziario basati sui dati attuali. "
            "Permette di modellare impatti di variazioni di tassi, perdita clienti, "
            "deterioramento crediti, stress test e altri scenari avversi."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "scenario_type": {
                    "type": "string",
                    "enum": ["tasso_interesse", "perdita_clienti", "deterioramento_crediti", "stress_test", "liquidita", "covenant_breach"],
                    "description": "Tipo di scenario da simulare"
                },
                "parameters": {
                    "type": "object",
                    "description": "Parametri dello scenario (es. {'variazione_bps': 200, 'clienti_persi_pct': 15})"
                }
            },
            "required": ["scenario_type"]
        }
    },
    {
        "name": "compare_periods",
        "description": (
            "Confronta indicatori finanziari tra diversi periodi per identificare trend, "
            "deterioramenti o miglioramenti nelle performance e nei profili di rischio."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "period1": {"type": "string", "description": "Primo periodo (es. 'Q1_2024')"},
                "period2": {"type": "string", "description": "Secondo periodo (es. 'Q2_2024')"},
                "metrics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Metriche da confrontare: 'ricavi', 'ebitda', 'leverage', 'liquidita', 'crediti', 'quick_ratio'"
                }
            },
            "required": ["period1", "period2"]
        }
    },
    {
        "name": "get_compliance_status",
        "description": (
            "Recupera lo stato di compliance normativa, i finding dell'audit e "
            "le raccomandazioni per la remediation. Include DORA, MiFID II, AML, IFRS."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "regulation": {
                    "type": "string",
                    "description": "Normativa specifica ('DORA', 'MiFID', 'AML', 'IFRS', 'tutte')",
                    "default": "tutte"
                },
                "severity_filter": {
                    "type": "string",
                    "enum": ["alta", "media", "bassa", "tutte"],
                    "description": "Filtra per severità dei finding"
                }
            }
        }
    },
    {
        "name": "generate_risk_dashboard_data",
        "description": (
            "Genera i dati strutturati per il dashboard di monitoraggio del rischio, "
            "inclusi grafici, semafori e indicatori in tempo reale."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "include_charts": {
                    "type": "boolean",
                    "description": "Includere dati per grafici e visualizzazioni",
                    "default": True
                }
            }
        }
    }
]

# ─── Tool Implementations ─────────────────────────────────────────────────────

def analyze_financial_report(report_id: str, focus_areas: list = None) -> dict:
    """Extract and analyze financial data from documents."""
    if report_id not in FINANCIAL_DOCS:
        available = list(FINANCIAL_DOCS.keys())
        return {"error": f"Report '{report_id}' non trovato. Disponibili: {available}"}
    
    doc = FINANCIAL_DOCS[report_id]
    
    # Parse key data from documents
    result = {
        "report_id": report_id,
        "document_content": doc,
        "focus_areas": focus_areas or ["kpi", "rischio", "anomalie"],
        "analysis_note": "Documento caricato per analisi AI approfondita"
    }
    
    # Add structured KPI data based on report
    if "Q1_2024" in report_id:
        result["kpi_estratti"] = {
            "ricavi": 42.3, "ebitda_margin": 23.2, "leverage": 3.49,
            "quick_ratio": 0.97, "crediti_scaduti_90gg_pct": 5.9,
            "concentrazione_top5_pct": 55.6, "var_95_10gg": 1.84
        }
        result["alert_count"] = {"alta": 3, "media": 2, "bassa": 1}
    elif "Q2_2024" in report_id:
        result["kpi_estratti"] = {
            "ricavi": 40.1, "ebitda_margin": 20.7, "leverage": 3.73,
            "quick_ratio": 0.91, "crediti_scaduti_90gg_pct": 8.4,
            "dso_giorni": 67, "liquidita": 0.5
        }
        result["alert_count"] = {"alta": 5, "media": 3, "bassa": 2}
        result["covenant_breach"] = True
    elif "audit" in report_id:
        result["audit_score"] = {
            "compliance": 48, "controlli_interni": 61, "risk_management": 44
        }
        result["findings_total"] = 12
    
    return result


def simulate_risk_scenario(scenario_type: str, parameters: dict = None) -> dict:
    """Simulate financial risk scenarios."""
    params = parameters or {}
    base_data = {
        "debito_variabile": 21.3,  # M€
        "ebitda_annualizzato": (8.3 * 4),  # Q2 annualizzato
        "ricavi_h1": 82.4,
        "crediti_totali": 21.4,
        "patrimonio_netto": 89.2
    }
    
    if scenario_type == "tasso_interesse":
        bps = params.get("variazione_bps", 100)
        impatto_annuo = base_data["debito_variabile"] * (bps / 10000)
        copertura = 0.35  # 35% hedge ratio attuale
        impatto_netto = impatto_annuo * (1 - copertura)
        return {
            "scenario": f"Aumento tassi +{bps}bps",
            "impatto_costo_debito_lordo_M": round(impatto_annuo, 3),
            "impatto_netto_dopo_hedge_M": round(impatto_netto, 3),
            "impatto_su_utile_netto_pct": round((impatto_netto / 7.8) * 100, 1),
            "hedge_ratio_attuale": "35%",
            "raccomandazione": "Aumentare copertura al 60-70% prima di ulteriori rialzi",
            "severita": "ALTA" if bps >= 200 else "MEDIA"
        }
    
    elif scenario_type == "perdita_clienti":
        pct = params.get("clienti_persi_pct", 10)
        impatto_ricavi = base_data["ricavi_h1"] * 2 * (pct / 100)
        nuovo_leverage = (base_data["debito_variabile"] + 15.5) / max((base_data["ebitda_annualizzato"] - impatto_ricavi * 0.25), 1)
        return {
            "scenario": f"Perdita {pct}% base clienti",
            "impatto_ricavi_annuo_M": round(impatto_ricavi, 2),
            "impatto_ebitda_M": round(impatto_ricavi * 0.25, 2),
            "nuovo_leverage_stimato": round(nuovo_leverage, 2),
            "covenant_breach": nuovo_leverage > 3.5,
            "severita": "CRITICA" if pct > 15 else "ALTA"
        }
    
    elif scenario_type == "deterioramento_crediti":
        pct_insoluti = params.get("percentuale_insoluti", 10)
        perdita = base_data["crediti_totali"] * (pct_insoluti / 100)
        return {
            "scenario": f"Deterioramento crediti: {pct_insoluti}% insoluti",
            "esposizione_totale_M": base_data["crediti_totali"],
            "perdita_stimata_M": round(perdita, 2),
            "fondo_attuale_M": 1.1,
            "gap_copertura_M": round(max(perdita - 1.1, 0), 2),
            "impatto_patrimonio_pct": round((perdita / base_data["patrimonio_netto"]) * 100, 1),
            "severita": "CRITICA" if pct_insoluti > 15 else "ALTA"
        }
    
    elif scenario_type == "stress_test":
        return {
            "scenario": "Stress Test Combinato (scenario avverso)",
            "assunzioni": {
                "calo_ricavi_pct": -12,
                "aumento_tassi_bps": 200,
                "deterioramento_crediti_pct": 8,
                "svalutazione_portafoglio_pct": -15
            },
            "impatti": {
                "perdita_ricavi_M": -19.8,
                "impatto_tassi_M": -0.86,
                "perdita_crediti_M": -1.71,
                "svalutazione_investimenti_M": -3.05
            },
            "impatto_totale_M": -25.42,
            "leverage_post_stress": 5.2,
            "patrimonio_post_stress_M": 63.8,
            "covenant_breach": True,
            "necessita_capitale_M": 15,
            "severita": "CRITICA",
            "probabilita": "20%"
        }
    
    elif scenario_type == "liquidita":
        return {
            "scenario": "Analisi Liquidità",
            "liquidita_attuale_M": 0.5,
            "soglia_covenant_M": 5.0,
            "deficit_strutturale_M": 4.5,
            "revolving_utilizzato_M": 4.5,
            "revolving_disponibile_M": 0.5,
            "cash_runway_giorni": 18,
            "fabbisogno_30gg_M": 6.2,
            "gap_liquidita_M": 5.7,
            "severita": "CRITICA"
        }
    
    elif scenario_type == "covenant_breach":
        return {
            "scenario": "Analisi Breach Covenant",
            "covenant_violati": [
                {"covenant": "Leverage Ratio max 3.5x", "attuale": 3.73, "status": "BREACH"},
                {"covenant": "Interest Coverage min 3.0x", "attuale": 2.8, "status": "BREACH"},
                {"covenant": "Minimum Liquidity €5M", "attuale": "0.5M (formale: OK)", "status": "A RISCHIO"}
            ],
            "conseguenze_potenziali": [
                "Accelerazione rimborso debiti (€15-20M entro 6 mesi)",
                "Cross-default su altre linee di credito",
                "Aumento spread su debito esistente (+80-150bps)",
                "Richiesta garanzie aggiuntive"
            ],
            "waiver_status": "In negoziazione",
            "probabilita_waiver": "65%",
            "piano_b": "Dismissione asset non-core e/o aumento di capitale",
            "severita": "CRITICA"
        }
    
    return {"error": f"Scenario '{scenario_type}' non riconosciuto"}


def compare_periods(period1: str, period2: str, metrics: list = None) -> dict:
    """Compare financial metrics between periods."""
    data = {
        "Q1_2024": {
            "ricavi": 42.3, "ebitda": 9.8, "ebitda_margin": 23.2,
            "leverage": 3.49, "quick_ratio": 0.97, "liquidita": 6.1,
            "crediti_90gg_pct": 5.9, "dso": 58, "roe": 5.84
        },
        "Q2_2024": {
            "ricavi": 40.1, "ebitda": 8.3, "ebitda_margin": 20.7,
            "leverage": 3.73, "quick_ratio": 0.91, "liquidita": 0.5,
            "crediti_90gg_pct": 8.4, "dso": 67, "roe": 4.37
        },
        "Q2_2023": {
            "ricavi": 42.3, "ebitda": 9.9, "ebitda_margin": 23.5,
            "leverage": 2.9, "quick_ratio": 1.15, "liquidita": 9.2,
            "crediti_90gg_pct": 3.1, "dso": 48, "roe": 7.2
        }
    }
    
    p1 = period1.replace("report_", "").upper()
    p2 = period2.replace("report_", "").upper()
    
    if p1 not in data or p2 not in data:
        return {"error": f"Periodo non trovato. Disponibili: {list(data.keys())}"}
    
    d1, d2 = data[p1], data[p2]
    selected_metrics = metrics or list(d1.keys())
    
    comparison = {}
    for m in selected_metrics:
        if m in d1 and m in d2:
            v1, v2 = d1[m], d2[m]
            delta = v2 - v1
            delta_pct = (delta / v1 * 100) if v1 != 0 else 0
            # Determine if change is positive or negative for risk
            risk_metrics = ["leverage", "crediti_90gg_pct", "dso"]
            is_deterioramento = (delta > 0 and m in risk_metrics) or (delta < 0 and m not in risk_metrics)
            comparison[m] = {
                p1: v1, p2: v2,
                "delta": round(delta, 3),
                "delta_pct": round(delta_pct, 1),
                "trend": "⬇️ DETERIORAMENTO" if is_deterioramento else "⬆️ MIGLIORAMENTO"
            }
    
    return {
        "period1": p1, "period2": p2,
        "comparison": comparison,
        "summary": f"Confronto {p1} vs {p2}: {sum(1 for v in comparison.values() if 'DETERIORAMENTO' in v['trend'])} metriche in deterioramento su {len(comparison)}"
    }


def get_compliance_status(regulation: str = "tutte", severity_filter: str = "tutte") -> dict:
    """Get compliance status and audit findings."""
    findings = {
        "IFRS": [
            {"id": "FR-01", "severity": "alta", "desc": "Riconoscimento anticipato ricavi (€2.77M)", "deadline": "30 giorni"},
            {"id": "FR-02", "severity": "alta", "desc": "Fondo rischi sottostimato (-€0.8M)", "deadline": "30 giorni"},
            {"id": "FR-03", "severity": "media", "desc": "Disclosure covenant waiver inadeguata (IAS 1)", "deadline": "60 giorni"},
            {"id": "FR-04", "severity": "media", "desc": "Cambio valutazione fondi senza disclosure (IFRS 13)", "deadline": "60 giorni"},
            {"id": "FR-05", "severity": "bassa", "desc": "Capitalizzazione ricorrente costi ristrutturazione", "deadline": "90 giorni"},
        ],
        "AML": [
            {"id": "AML-01", "severity": "alta", "desc": "KYC incompleto su 12 clienti istituzionali (13.5%)", "deadline": "60 giorni"},
            {"id": "AML-02", "severity": "media", "desc": "Transaction monitoring non aggiornato (2022)", "deadline": "90 giorni"},
            {"id": "AML-03", "severity": "bassa", "desc": "Formazione personale AML: 34% non completata", "deadline": "30 giorni"},
        ],
        "DORA": [
            {"id": "DORA-01", "severity": "alta", "desc": "ICT Risk Framework incompleto (40% gap), test mancanti", "deadline": "Q4 2024"},
            {"id": "DORA-02", "severity": "alta", "desc": "Incident reporting non conforme (4h deadline a rischio)", "deadline": "Urgente"},
            {"id": "DORA-03", "severity": "media", "desc": "8 fornitori critici senza assessment DORA", "deadline": "Q3 2024"},
        ],
        "MiFID": [
            {"id": "MIFID-01", "severity": "bassa", "desc": "Review trimestrale Best Execution non documentata", "deadline": "45 giorni"},
            {"id": "MIFID-02", "severity": "bassa", "desc": "Target market assessment 4 prodotti da aggiornare", "deadline": "45 giorni"},
        ]
    }
    
    if regulation != "tutte":
        reg_key = regulation.upper().replace("MIFID II", "MiFID").replace("MIFIDII", "MiFID")
        findings_filtered = {k: v for k, v in findings.items() if k.upper() == reg_key.upper()}
    else:
        findings_filtered = findings
    
    if severity_filter != "tutte":
        findings_filtered = {
            k: [f for f in v if f["severity"] == severity_filter]
            for k, v in findings_filtered.items()
        }
    
    scores = {"compliance": 48, "controlli_interni": 61, "risk_management": 44}
    total_findings = sum(len(v) for v in findings_filtered.values())
    high_findings = sum(len([f for f in v if f["severity"] == "alta"]) for v in findings_filtered.values())
    
    return {
        "scores": scores,
        "rating_complessivo": "INSUFFICIENTE" if scores["compliance"] < 60 else "SUFFICIENTE",
        "findings": findings_filtered,
        "totale_findings": total_findings,
        "finding_alta_criticita": high_findings,
        "escalation_richiesta": all(s < 60 for s in scores.values()),
        "budget_remediation_M": "4.8-6.2"
    }


def generate_risk_dashboard_data(include_charts: bool = True) -> dict:
    """Generate dashboard data for risk monitoring."""
    return {
        "semafori": {
            "leverage": {"valore": 3.73, "soglia": 3.5, "status": "🔴 CRITICO", "breach": True},
            "liquidita": {"valore": 0.5, "soglia": 5.0, "status": "🔴 CRITICO", "breach": True},
            "quick_ratio": {"valore": 0.91, "soglia": 1.0, "status": "🟡 ATTENZIONE"},
            "dso": {"valore": 67, "soglia": 55, "status": "🟡 ATTENZIONE"},
            "concentrazione_crediti": {"valore": 55.6, "soglia": 40, "status": "🔴 CRITICO"},
            "compliance_score": {"valore": 48, "soglia": 60, "status": "🔴 CRITICO"},
            "interest_coverage": {"valore": 2.8, "soglia": 3.0, "status": "🔴 CRITICO", "breach": True},
        },
        "trend_ricavi": [
            {"periodo": "Q2 2023", "valore": 42.3},
            {"periodo": "Q3 2023", "valore": 43.1},
            {"periodo": "Q4 2023", "valore": 41.8},
            {"periodo": "Q1 2024", "valore": 42.3},
            {"periodo": "Q2 2024", "valore": 40.1},
        ],
        "trend_leverage": [
            {"periodo": "Q2 2023", "valore": 2.9},
            {"periodo": "Q3 2023", "valore": 3.1},
            {"periodo": "Q4 2023", "valore": 3.3},
            {"periodo": "Q1 2024", "valore": 3.49},
            {"periodo": "Q2 2024", "valore": 3.73},
        ],
        "distribuzione_crediti": [
            {"fascia": "0-30 gg", "percentuale": 55.1, "importo_M": 11.8},
            {"fascia": "31-60 gg", "percentuale": 22.9, "importo_M": 4.9},
            {"fascia": "61-90 gg", "percentuale": 13.6, "importo_M": 2.9},
            {"fascia": ">90 gg", "percentuale": 8.4, "importo_M": 1.8},
        ],
        "risk_score_globale": 28,  # out of 100 (higher = safer)
        "alert_attivi": 7,
        "covenant_breach_count": 2,
        "azioni_urgenti": 5
    }


# ─── Tool Executor ────────────────────────────────────────────────────────────

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool and return JSON result."""
    try:
        if tool_name == "analyze_financial_report":
            result = analyze_financial_report(**tool_input)
        elif tool_name == "simulate_risk_scenario":
            result = simulate_risk_scenario(**tool_input)
        elif tool_name == "compare_periods":
            result = compare_periods(**tool_input)
        elif tool_name == "get_compliance_status":
            result = get_compliance_status(**tool_input)
        elif tool_name == "generate_risk_dashboard_data":
            result = generate_risk_dashboard_data(**tool_input)
        else:
            result = {"error": f"Tool '{tool_name}' non riconosciuto"}
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── System Prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Sei ARIA (Autonomous Risk Intelligence Agent), l'agente AI specializzato in gestione del rischio finanziario e audit per FinSecure Analytics.

Il tuo ruolo è supportare il team finanziario con:
- Analisi approfondite dei report finanziari (KPI, anomalie, rischi)
- Simulazioni di scenari di rischio e stress test
- Audit interattivi su compliance normativa (IFRS, DORA, MiFID II, AML)
- Identificazione di omissioni, inesattezze e interpretazioni erronee
- Raccomandazioni concrete e prioritizzate per la remediation

Documenti disponibili nel sistema:
- report_Q1_2024: Report finanziario Q1 2024
- report_Q2_2024: Report finanziario Q2 2024  
- audit_compliance_H1_2024: Audit interno compliance H1 2024

Linee guida operative:
1. Usa sempre i tool disponibili per accedere ai dati prima di rispondere
2. Sii preciso, quantitativo e basato sui dati reali dei documenti
3. Evidenzia chiaramente i rischi critici (🔴), le attenzioni (🟡) e le situazioni ok (🟢)
4. Fornisci sempre raccomandazioni concrete con priorità e timeline
5. Segnala proattivamente anomalie e possibili interpretazioni erronee
6. Rispondi in italiano con terminologia finanziaria professionale

Situazione attuale CRITICA (da conoscere):
- Breach di 2 covenant bancari (Leverage 3.73x vs max 3.5x; Interest Coverage 2.8x vs min 3.0x)
- Liquidità strutturale critica (€0.5M vs €5M covenant)
- Compliance score insufficiente (48/100)
- 5 finding di alta criticità nell'ultimo audit

Sei proattivo: se non hai informazioni sufficienti, usa i tool per recuperarle prima di rispondere."""


# ─── Main Chat Endpoint ───────────────────────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    
    if not messages:
        return jsonify({"error": "Nessun messaggio fornito"}), 400
    
    # Agentic loop
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )
        
        # Check if we need to execute tools
        if response.stop_reason == "tool_use":
            # Add assistant's response to messages
            messages.append({"role": "assistant", "content": response.content})
            
            # Execute all requested tools
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            
            # Add tool results and continue loop
            messages.append({"role": "user", "content": tool_results})
        
        else:
            # Final response
            text_content = ""
            for block in response.content:
                if hasattr(block, "text"):
                    text_content += block.text
            
            return jsonify({
                "response": text_content,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            })


@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    """Return dashboard data directly."""
    data = generate_risk_dashboard_data(include_charts=True)
    return jsonify(data)


@app.route("/api/documents", methods=["GET"])
def list_documents():
    """List available documents."""
    return jsonify({"documents": list(FINANCIAL_DOCS.keys())})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "documents_loaded": len(FINANCIAL_DOCS)})


if __name__ == "__main__":
    print(f"📄 Documenti caricati: {list(FINANCIAL_DOCS.keys())}")
    app.run(host="0.0.0.0", port=5000, debug=False)
