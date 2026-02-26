test_questions = [
    "Quali sono i principali punti chiave nell'area performance finanziaria riguardo i report finanziari degli ultimi anni?",
    "Quali sono i punti principali riguardo le implementazioni per migliorare l'area compliance?",
]

ground_truth_answers = [
    """
    **Principali punti chiave della **Performance Finanziaria** nei report degli ultimi anni (2024‑2026)**  

    | Anno | Indicatori principali | Trend / Insight |
    |------|----------------------|-----------------|
    | **2024** | • Ricavi: **27,5 M €**  <br>• EBITDA: **6,95 M €**  <br>• EBIT: **5,6 M €**  <br>• Utile netto: **3,75 M €**  <br>• Costi operativi: **20,55 M €** | Base di partenza per il periodo di analisi. |
    | **2025** | • Ricavi: **32,4 M €**  (+18 % vs 2024)  <br>• EBITDA: **8,9 M €**  (+28 % vs 2024)  <br>• EBIT: **7,2 M €**  (+29 % vs 2024)  <br>• Utile netto: **4,85 M €**  (+29 % vs 2024)  <br>• Costi operativi: **23,5 M €** (+14 % vs 2024)  <br>• Margine EBITDA: **25,9 %** (↑ 2,1 pp)  <br>• ROE: **18,3 %** (↑ 2,2 pp)  <br>• Patrimonio netto: **47,5 M €** (+15 % vs 2024)  <br>• Liquidità corrente: **2,8 x** | **Crescita robusta dei ricavi** trainata da advisory regolatoria e servizi SaaS. <br>**Miglioramento della marginalità** grazie a automazione dei processi documentali e razionalizzazione dei costi di consulenza esterna. <br>**Solidità patrimoniale** con aumento del patrimonio netto e buona capacità di investimento. |
    | **2026** | • Ricavi: **37,26 M €** (+15 % vs 2025)  <br>• EBITDA: **10,15 M €** (+14 % vs 2025)  <br>• EBIT: **8,35 M €** (+16 % vs 2025)  <br>• Utile netto: **5,48 M €** (+13 % vs 2025)  <br>• Costi operativi: **27,11 M €** (+15 % vs 2025)  <br>• Margine EBITDA: **≈27 %** (obiettivo 27‑28 %)  <br>• ROE: **≈20 %** (in crescita)  <br>• Posizione finanziaria netta: **18,3 M €** (↑ ≈ 3,6 M €) | **Continua crescita dei ricavi**, soprattutto da soluzioni SaaS di compliance. <br>**Margine EBITDA stabile** nonostante l’aumento dei costi operativi legati a investimenti in tecnologia e personale qualificato. <br>**Focus su automazione avanzata** (AI, RPA) per mantenere la redditività. <br>**Obiettivi KPI 2026**: crescita ricavi 13‑17 %, margine EBITDA 27‑28 %, retention clienti 95 %, NPS ≥ 65. |
    
    ### Sintesi dei punti chiave
    
    1. **Crescita dei ricavi**: +18 % (2024→2025) e +15 % (2025→2026), trainata da advisory regolatoria, servizi di compliance SaaS e tecnologie AI.  
    2. **Miglioramento della redditività**: EBITDA +28 % (2024→2025) e +14 % (2025→2026); margine EBITDA passato dal 23,8 % al 25,9 % (2025) e previsto intorno al 27 % (2026).  
    3. **Utile netto in aumento**: +29 % (2024→2025) e +13 % (2025→2026), dimostrando capacità di convertire la crescita dei ricavi in profitto.  
    4. **Controllo dei costi operativi**: aumento moderato (+14 % nel 2025, +15 % nel 2026) rispetto al più rapido incremento dei ricavi, grazie a razionalizzazione e automazione.  
    5. **Solidità patrimoniale e liquidità**: patrimonio netto +15 % (2025), liquidità corrente 2,8 x, posizione finanziaria netta positiva e in crescita.  
    6. **Indicatori di performance**: ROE in crescita (16,1 % → 18,3 % → ~20 %), margine EBITDA in miglioramento costante, KPI strategici (revenue growth, EBITDA margin, client retention, NPS) definiti per il 2026.  
    7. **Strategia di investimento**: focus su AI generativa, automazione dei report di compliance e ampliamento dell’offerta SaaS per sostenere la crescita futura.  
    
    Questi elementi costituiscono i punti chiave della sezione “Performance Finanziaria” dei report di DataTrust Solutions per gli ultimi tre esercizi.
    """,
    """
    **Punti principali delle implementazioni per potenziare l’area compliance (estratti dal documento)**  
    
    | Area | Implementazione | Obiettivo / risultato atteso |
    |------|----------------|------------------------------|
    | **Infrastruttura di controllo** | Integrazione di sistemi predittivi per l’identificazione preventiva di rischi regolatori | Anticipare le violazioni e ridurre l’esposizione a sanzioni |
    | **Audit** | Riduzione del 22 % dei tempi di audit interni (e 35 % dei tempi di revisione documentale grazie a AI) | Accelerare i controlli e aumentare l’efficienza operativa |
    | **Monitoraggio normativo** | Sistema di monitoraggio multi‑giurisdizione + dashboard KPI real‑time | Coprire le normative di UE, USA e altri mercati in modo continuo |
    | **Certificazioni** | Ottenimento e rinnovo ISO 27001 (sicurezza delle informazioni) e ISO 9001 (quality management) | Garantire standard internazionali di sicurezza e qualità |
    | **Policy interne** | Aggiornamento continuo delle policy in linea con le normative UE (es. GDPR) | Mantenere la conformità alle evoluzioni legislative |
    | **Investimenti tecnologici (2025‑2026)** | • €2,1 M in piattaforme per l’automazione dell’analisi documentale  <br>• €1,4 M in infrastrutture di cybersecurity e data‑protection  <br>• €0,8 M in formazione specialistica su normative emergenti  <br>• €0,5 M in licenze software per compliance monitoring & reporting | Potenziare l’automazione, la sicurezza e le competenze del personale |
    | **Framework di compliance** | Framework multi‑livello che integra GDPR, Sarbanes‑Oxley (SOX), Basel III, AML/BSA, IFRS 18 (pre‑implementazione) | Coprire tutti i principali requisiti normativi del settore finanziario |
    | **Ruoli di governance** | Chief Compliance Officer (CCO), Data Protection Officer (DPO), Compliance Committee, Risk Management Team | Struttura di governance chiara con escalation diretta al CEO e al Consiglio |
    | **Tecnologie emergenti** | • NLP per analisi semantica di documenti e verbali  <br>• Predictive analytics per anticipare cambi normativi  <br>• RPA per automatizzare KYC, reporting periodico  <br>• Blockchain/Smart‑contracts per tracciabilità immutabile  <br>• Generative AI per produzione automatica di report di compliance | Incrementare l’efficacia, l’accuratezza (target ≥ 96 % di accuracy) e la scalabilità dei processi di compliance |
    | **Continuous compliance monitoring** | Implementazione di dashboard KPI (es. “Compliance Incidents” < 2) e monitoraggio mensile dei KPI di efficienza documentale | Garantire visibilità costante e interventi correttivi rapidi |
    | **Formazione e talent development** | Creazione di una corporate academy per competenze ibride compliance‑tech | Ridurre dipendenza da recruiting esterno e colmare lo shortage di talenti AI/compliance |
    | **Strategie di mercato** | Lancio di “Compliance‑as‑a‑Service” platform, mobile app con alert in tempo reale, marketplace per reg‑tech | Estendere l’offerta a piccole/medie istituzioni finanziarie e a terze parti |
    
    **Sintesi**  
    Le implementazioni chiave per migliorare la compliance di DataTrust Solutions consistono in: potenziare l’infrastruttura di controllo con sistemi predittivi; automatizzare audit e revisione documentale tramite AI, NLP e RPA; adottare un monitoraggio normativo multi‑giurisdizione con dashboard KPI; certificare ISO 27001/9001; aggiornare costantemente le policy (es. GDPR); investire in cybersecurity, formazione e licenze software specifiche; consolidare un framework di compliance che copra GDPR, SOX, Basel III, AML/BSA e IFRS 18; rafforzare la governance con CCO, DPO e comitati dedicati; e introdurre tecnologie emergenti (blockchain, generative AI, predictive analytics) per garantire una compliance continua, scalabile e proattiva.

    """
]
