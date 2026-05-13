# ARIA — AI Risk Intelligence Agent
### FinSecure Analytics · Gestione del Rischio Finanziario e Audit Interattivi

```
┌─────────────────────────────────────────────────────────┐
│  ARIA  ·  Autonomous Risk Intelligence Agent            │
│  FinSecure Analytics  ·  Powered by Anthropic Claude    │
└─────────────────────────────────────────────────────────┘
```

## Panoramica del Progetto

ARIA è un agente AI avanzato per la gestione del rischio finanziario e gli audit interattivi, sviluppato per FinSecure Analytics. Il sistema combina Large Language Models (Claude di Anthropic) con tool use avanzato per analizzare documenti finanziari, simulare scenari di rischio, e fornire audit interattivi basati su dati reali.

### Architettura

```
┌──────────────────┐    HTTP/JSON    ┌──────────────────────────┐
│   Frontend       │◄───────────────►│   Backend Flask (Python) │
│   (HTML/JS/CSS)  │                 │   app.py                 │
│   index.html     │                 │                          │
│                  │                 │  ┌────────────────────┐  │
│  • Chat UI       │                 │  │  Anthropic Claude  │  │
│  • Dashboard     │                 │  │  (Tool Use Loop)   │  │
│  • Analytics     │                 │  └────────────────────┘  │
└──────────────────┘                 │                          │
                                     │  ┌────────────────────┐  │
                                     │  │  Financial Tools   │  │
                                     │  │  • analyze_report  │  │
                                     │  │  • simulate_risk   │  │
                                     │  │  • compare_periods │  │
                                     │  │  • get_compliance  │  │
                                     │  │  • dashboard_data  │  │
                                     │  └────────────────────┘  │
                                     │                          │
                                     │  ┌────────────────────┐  │
                                     │  │  Documents         │  │
                                     │  │  • report_Q1_2024  │  │
                                     │  │  • report_Q2_2024  │  │
                                     │  │  • audit_H1_2024   │  │
                                     │  └────────────────────┘  │
                                     └──────────────────────────┘
```

## Struttura del Progetto

```
finsecure/
├── app.py                          # Backend Flask + Agente AI
├── requirements.txt                # Dipendenze Python
├── README.md                       # Questo file
│
├── data/
│   └── documents/                  # Documenti finanziari fittizi
│       ├── report_Q1_2024.txt      # Report finanziario Q1 2024
│       ├── report_Q2_2024.txt      # Report finanziario Q2 2024
│       └── audit_compliance_H1_2024.txt  # Audit interno H1 2024
│
└── frontend/
    └── index.html                  # UI completa (single-file SPA)
```

## Installazione e Avvio

### Prerequisiti
- Python 3.10+
- API Key Anthropic (da https://console.anthropic.com)
- Browser moderno (Chrome, Firefox, Safari, Edge)

### 1. Installazione dipendenze

```bash
cd finsecure
pip install -r requirements.txt
```

### 2. Configurazione API Key

```bash
# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-..."

# Oppure crea un file .env nella cartella finsecure/
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### 3. Avvio Backend

```bash
python app.py
```

Il backend sarà disponibile su `http://localhost:5000`

**Verifica:**
```bash
curl http://localhost:5000/health
# {"status": "ok", "documents_loaded": 3}
```

### 4. Apertura Frontend

Apri il file `frontend/index.html` nel browser.

> **Nota:** Per la comunicazione con il backend in locale, il frontend usa `USE_MOCK = false` (da impostare in `index.html` se si usa il backend reale) oppure funziona con risposte mock per demo/sviluppo con `USE_MOCK = true`.

Per abilitare il backend reale, nel file `frontend/index.html` cambia:
```javascript
const USE_MOCK = false; // Abilita comunicazione con backend Flask
```

## Funzionalità Principali

### 🤖 Agente AI con Tool Use

L'agente utilizza il framework di **Tool Use** di Anthropic Claude in un loop agentivo:

```
Utente → Claude analizza → Decide quale tool usare → 
Esegue tool → Ottiene dati → Formula risposta → Utente
```

**Tools disponibili:**

| Tool | Descrizione |
|------|-------------|
| `analyze_financial_report` | Estrae KPI, identifica anomalie dai report |
| `simulate_risk_scenario` | Simula scenari: tassi, liquidità, crediti, stress test |
| `compare_periods` | Confronta metriche tra periodi diversi |
| `get_compliance_status` | Stato compliance IFRS, DORA, MiFID, AML |
| `generate_risk_dashboard_data` | Dati per il dashboard di monitoraggio |

### 📊 Dashboard di Monitoraggio

Il pannello destro mostra in tempo reale:
- **Risk Score Globale** (28/100 — Critico)
- **Semafori KPI** (Leverage, Liquidità, Quick Ratio, etc.)
- **Covenant Breach Alert** (2 breach attivi)
- **Azioni Urgenti** (lista prioritizzata)

### 💬 Audit Interattivo

Chat conversazionale con ARIA per:
- Domande in linguaggio naturale sui dati finanziari
- Richieste di simulazioni e stress test
- Analisi di compliance normativa
- Identificazione di anomalie contabili

### 📈 Analytics

Grafici interattivi (Chart.js):
- Trend ricavi ultimi 5 trimestri
- Evoluzione leverage vs soglia covenant
- Distribuzione portafoglio crediti per scadenza

## Documenti Fittizi Inclusi

### `report_Q1_2024.txt`
Report finanziario Q1 2024 con:
- KPI: Ricavi €42.3M, EBITDA 23.2%, Leverage 3.49x
- **Anomalie:** Ricavi anticipati IFRS 15 (€2.1M), fondo rischi sottostimato
- **Alert:** Leverage vicino al covenant (margine <1%)

### `report_Q2_2024.txt`
Report Q2 2024 con deterioramento significativo:
- **Breach covenant** confermato (Leverage 3.73x, Coverage 2.8x)
- Liquidità crollata da €6.1M a €0.5M
- Perdita cliente strategico (€3.2M/anno)

### `audit_compliance_H1_2024.txt`
Audit interno con 12 finding:
- 5 finding di **ALTA criticità** (FR-01, FR-02, AML-01, DORA-01, DORA-02)
- Compliance score: **48/100** (insufficiente)
- Budget remediation: €4.8-6.2M

## API Endpoints

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/chat` | POST | Chat con l'agente AI |
| `/api/dashboard` | GET | Dati dashboard risk monitor |
| `/api/documents` | GET | Lista documenti disponibili |
| `/health` | GET | Health check |

### Esempio chiamata API

```python
import requests

response = requests.post('http://localhost:5000/api/chat', json={
    "messages": [
        {
            "role": "user",
            "content": "Analizza il rischio di liquidità nel Q2 2024"
        }
    ]
})

print(response.json()['response'])
```

## Scenari di Simulazione Disponibili

```python
# Via API o conversazione con ARIA:

# Rialzo tassi di interesse
simulate_risk_scenario("tasso_interesse", {"variazione_bps": 200})

# Perdita base clienti
simulate_risk_scenario("perdita_clienti", {"clienti_persi_pct": 15})

# Deterioramento crediti
simulate_risk_scenario("deterioramento_crediti", {"percentuale_insoluti": 10})

# Stress test combinato
simulate_risk_scenario("stress_test")

# Analisi liquidità
simulate_risk_scenario("liquidita")

# Breach covenant
simulate_risk_scenario("covenant_breach")
```

## Tecnologie Utilizzate

| Componente | Tecnologia |
|-----------|------------|
| AI Agent | Anthropic Claude (claude-sonnet-4-20250514) |
| Tool Use | Anthropic Messages API con agentic loop |
| Backend | Python + Flask + Flask-CORS |
| Frontend | HTML5 + CSS3 + Vanilla JavaScript |
| Grafici | Chart.js 4.4.1 |
| Tipografia | IBM Plex Mono + IBM Plex Sans |
| Deploy | Local (estensibile a Docker/Cloud) |

## Estensioni Future

- [ ] Integrazione con database reale (PostgreSQL)
- [ ] Import automatico dati da ERP/CRM aziendale
- [ ] LlamaIndex per indicizzazione documenti avanzata
- [ ] LangChain per catene di ragionamento complesse
- [ ] RAG (Retrieval Augmented Generation) su archivio storico
- [ ] Export report PDF automatizzato
- [ ] Notifiche alert via email/Slack
- [ ] Multi-tenancy per più aziende clienti
- [ ] Autenticazione e RBAC (Role Based Access Control)

## Note di Sicurezza

> ⚠️ Questo progetto usa documenti **fittizi** a scopo dimostrativo.
> In produzione, assicurarsi di:
> - Non esporre l'API key Anthropic lato frontend
> - Implementare autenticazione per tutti gli endpoint
> - Cifrare i documenti finanziari sensibili
> - Implementare audit log di tutte le query
> - Rispettare GDPR per eventuali dati personali

---

*ARIA — Autonomous Risk Intelligence Agent*
*FinSecure Analytics © 2024*
