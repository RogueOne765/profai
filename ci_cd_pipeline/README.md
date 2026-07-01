- creare nodo in dashboard jenkins
- copiare nome e secret del nodo creato e inserirli nel file .env
- riavviare il container dell'agente jenkins
- nella configurazione del nodo "master", abbassare numero esecutori a 0


### Railway
- creare account
- creare nuovo progetto
- creare nuovo servizio "Empty
- collegare repository github https://github.com/RogueOne765/profai e configurare root directory ci_cd_pipeline/api
- in network generare dominio random di railway e nelle configurazioni indicare porta 8000
- come modalità build lasciare railway container (troverà automaticamente il Dockerfile da compilare)
- da impostazioni progetto, creare token
- da pannello env del servizio recuperare project_id e service_id

### Step finale jenkins
- In sezione credentials aggiungere RAILWAY_TOKEN, RAILWAY_PROJECT_ID, RAILWAY_SERVICE_ID
