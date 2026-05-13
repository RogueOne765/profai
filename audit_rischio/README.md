# FinSecure Analytics - Agente AI per la Gestione del Rischio Finanziario

Sistema di AI per l'analisi del rischio finanziario e audit interattivi per FinSecure Analytics.

## Struttura del Progetto

```
audit_rischio/
├── data/
│   ├── documents/          # Documenti finanziari fittizi
│   │   ├── alpha_industries_q1_2025.txt
│   │   ├── alpha_industries_q2_2025.txt
│   │   ├── beta_financial_audit_2024.txt
│   │   ├── gamma_corp_risk_analysis_2025.txt
│   │   └── delta_financial_aml_policy.txt
│   ├── csv/               # Dati strutturati
│   │   ├── financial_data.csv
│   │   ├── accounts_receivable.csv
│   │   └── kpi_trends.csv
│   └── storage/           # Indice vettoriale (generato)
├── src/
│   ├── agents/
│   │   ├── risk_analyzer.py      # Analisi rischi
│   │   └── scenario_simulator.py # Simulazione scenari
│   ├── chatbot/
│   │   └── audit_chatbot.py      # Chatbot interattivo
│   ├── dashboard/
│   │   └── dashboard.py          # Dashboard Streamlit
│   └── utils/
│       └── data_processing.py    # Processing dati e ingestion
├── main.py               # Entry point principale
└── requirements.txt      # Dipendenze
```

## Installazione

```bash
pip install -r requirements.txt
```

## Utilizzo

### 1. Dashboard Interattiva (Streamlit)

```bash
streamlit run src/dashboard/dashboard.py
```

La dashboard include:
- KPI cards con indicatori di rischio
- Gauge del risk score
- Trend finanziari interattivi
- Analisi crediti
- Simulazione scenari what-if
- Panel compliance

### 2. Chatbot Interattivo

```bash
python -m src.chatbot.audit_chatbot
```

Il chatbot risponde a domande su:
- Analisi rischi
- Situazione crediti
- Liquidità
- Redditività
- Compliance
- Simulazione scenari

### 3. API da riga di comando

```bash
python main.py
```

Esegue l'analisi completa e stampa i risultati.

## Funzionalità

### Analisi Rischi
- Calcolo risk score (0-100)
- Identificazione automatica criticità
- Analisi KPI finanziari (Current Ratio, Quick Ratio, DSO, etc.)

### Simulazione Scenari
- 4 scenari: Base, Recessione, Stress, Espansione
- Proiezioni multi-anno
- Monte Carlo simulation
- Value at Risk (VaR)
- Probabilità di default

### Chatbot Audit
- Interfaccia conversazionale
- Analisi documenti
- Raccomandazioni automatiche

### Dashboard
- Visualizzazione KPI real-time
- Grafici interattivi Plotly
- Simulazione scenari what-if

## Dati di Esempio

Il progetto include documenti fittizi che simulano:
- Report trimestrali Alpha Industries (Q1-Q2 2025)
- Report audit Beta Financial Services
- Analisi rischi Gamma Corp
- Policy AML Delta Financial

## Tecnologie

- **LangChain**: Agenti AI e RAG
- **LlamaIndex**: Indicizzazione documenti
- **Streamlit**: Dashboard interattiva
- **Plotly**: Visualizzazioni
- **Pandas/NumPy**: Analisi dati

## Licenza

Progetto didattico - FinSecure Analytics
