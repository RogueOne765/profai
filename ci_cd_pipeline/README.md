### Jenkins
- setup di base iniziale (primo accesso e creazione utenza) e installazione plugin raccomandati
- installare plugin Copy Artifacts (https://plugins.jenkins.io/copyartifact/)
- creare due nodi in dashboard jenkins, uno per esecuzione python(label=python-exec) ed uno per esecuzione node(label=node-exec)
- copiare nome e secret del nodo creato e inserirli nel file .env
- riavviare i container dei nodi agente jenkins
- nella configurazione del nodo "master", abbassare numero esecutori a 0
- importare configurazione job presente in config/config.xml

### Railway
- creare account (free tier disponibile)
- creare nuovo progetto
- creare nuovo servizio "Empty"
- collegare repository github di interesse (in questo caso https://github.com/RogueOne765/profai) e configurare root directory ci_cd_pipeline/api
- in network generare dominio random  e nelle configurazioni indicare porta 8000
- come modalità build lasciare railway container (troverà automaticamente il Dockerfile da compilare)
- da impostazioni progetto creare un nuovo token
- da pannello env del servizio recuperare service_id

### Step finale jenkins
- In sezione credentials aggiungere RAILWAY_TOKEN, RAILWAY_SERVICE_ID recuperati da dashboard railway
