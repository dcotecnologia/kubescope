<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="it">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>Strumento di accesso non trovato</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>Il tuo kubeconfig esegue «{tool}» per accedere, ma non è installato o non è nel PATH. Installalo e aggiorna.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>Contesto non trovato</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>Questo contesto non è nel tuo kubeconfig. Controlla ~/.kube/config.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>Autenticazione non riuscita</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>Le tue credenziali potrebbero essere scadute. Accedi di nuovo (ad esempio con «aws sso login», «gcloud auth login» o «az login») e aggiorna.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Not an Amazon EKS cluster</source>
        <translation>Non è un cluster Amazon EKS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Node Groups, Add-ons and the AWS cards of the Overview exist only on Amazon EKS contexts.</source>
        <translation>Node Groups, Add-ons e le schede AWS della Panoramica esistono solo nei contesti Amazon EKS.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="110"/>
        <source>Unexpected answer from AWS</source>
        <translation>Risposta inattesa da AWS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="111"/>
        <source>Update the AWS CLI to its latest version and refresh.</source>
        <translation>Aggiorna la AWS CLI all&apos;ultima versione e ricarica.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="118"/>
        <location filename="../errors.py" line="128"/>
        <source>Access denied</source>
        <translation>Accesso negato</translation>
    </message>
    <message>
        <location filename="../errors.py" line="119"/>
        <source>Your AWS identity is not allowed to read this. The wiki lists the eks: permissions KubeScope needs.</source>
        <translation>La tua identità AWS non ha il permesso di leggere questo. La wiki elenca i permessi eks: di cui KubeScope ha bisogno.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>Il tuo utente non è autorizzato a leggere questa risorsa.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="143"/>
        <source>No network connection</source>
        <translation>Nessuna connessione di rete</translation>
    </message>
    <message>
        <location filename="../errors.py" line="144"/>
        <source>Check your internet connection or VPN and refresh.</source>
        <translation>Controlla la connessione a internet o la VPN e aggiorna.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="165"/>
        <source>Cluster unreachable</source>
        <translation>Cluster non raggiungibile</translation>
    </message>
    <message>
        <location filename="../errors.py" line="166"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>Controlla la rete o la VPN e che il cluster sia in esecuzione.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="172"/>
        <source>Something went wrong</source>
        <translation>Qualcosa è andato storto</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="42"/>
        <source>No log lines returned.</source>
        <translation>Nessuna riga di log restituita.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="47"/>
        <source>Updated at {time}</source>
        <translation>Aggiornato alle {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="54"/>
        <source>Could not refresh logs: {message}</source>
        <translation>Impossibile aggiornare i log: {message}</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>Aggiornamento automatico</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>Recupera nuove righe di log ogni pochi secondi e segue la fine del log</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>Aggiorna ora</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../window.py" line="1508"/>
        <location filename="../window.py" line="1537"/>
        <source>TYPE</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1509"/>
        <source>CLUSTER IP</source>
        <translation>IP DEL CLUSTER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1510"/>
        <source>EXTERNAL IP</source>
        <translation>IP ESTERNO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1511"/>
        <location filename="../window.py" line="1515"/>
        <location filename="../window.py" line="1523"/>
        <source>PORTS</source>
        <translation>PORTE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1514"/>
        <source>ADDRESS TYPE</source>
        <translation>TIPO DI INDIRIZZO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1516"/>
        <location filename="../window.py" line="1518"/>
        <source>ENDPOINTS</source>
        <translation>ENDPOINT</translation>
    </message>
    <message>
        <location filename="../window.py" line="1520"/>
        <source>CLASS</source>
        <translation>CLASSE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1521"/>
        <source>HOSTS</source>
        <translation>HOST</translation>
    </message>
    <message>
        <location filename="../window.py" line="1522"/>
        <source>ADDRESS</source>
        <translation>INDIRIZZO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1526"/>
        <source>CONTROLLER</source>
        <translation>CONTROLLER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1527"/>
        <source>PARAMETERS</source>
        <translation>PARAMETRI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1530"/>
        <source>POD SELECTOR</source>
        <translation>SELETTORE DEI POD</translation>
    </message>
    <message>
        <location filename="../window.py" line="1531"/>
        <source>POLICY TYPES</source>
        <translation>TIPI DI POLICY</translation>
    </message>
    <message>
        <location filename="../window.py" line="1534"/>
        <location filename="../window.py" line="1538"/>
        <source>DATA</source>
        <translation>DATI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1541"/>
        <source>USAGE</source>
        <translation>UTILIZZO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1544"/>
        <source>TYPES</source>
        <translation>TIPI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1547"/>
        <source>REFERENCE</source>
        <translation>RIFERIMENTO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1548"/>
        <source>MIN PODS</source>
        <translation>MIN POD</translation>
    </message>
    <message>
        <location filename="../window.py" line="1549"/>
        <source>MAX PODS</source>
        <translation>MAX POD</translation>
    </message>
    <message>
        <location filename="../window.py" line="1550"/>
        <source>REPLICAS</source>
        <translation>REPLICHE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <source>MIN AVAILABLE</source>
        <translation>MIN DISPONIBILI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1554"/>
        <source>MAX UNAVAILABLE</source>
        <translation>MAX NON DISPONIBILI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1555"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>INTERRUZIONI CONSENTITE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1558"/>
        <source>VALUE</source>
        <translation>VALORE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1559"/>
        <source>GLOBAL DEFAULT</source>
        <translation>PREDEFINITO GLOBALE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1562"/>
        <source>HANDLER</source>
        <translation>HANDLER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1565"/>
        <source>HOLDER</source>
        <translation>TITOLARE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1568"/>
        <location filename="../window.py" line="1571"/>
        <source>WEBHOOKS</source>
        <translation>WEBHOOKS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1575"/>
        <source>INSTANCE TYPES</source>
        <translation>TIPI DI ISTANZA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>NODES</source>
        <translation>NODI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1577"/>
        <source>AMI TYPE</source>
        <translation>TIPO DI AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1578"/>
        <source>AMI VERSION</source>
        <translation>VERSIONE AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1582"/>
        <location filename="../ui/main_window.ui" line="2588"/>
        <source>VERSION</source>
        <translation>VERSIONE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1583"/>
        <source>SOURCE</source>
        <translation>ORIGINE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1593"/>
        <source>COMPLETIONS</source>
        <translation>COMPLETAMENTI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1594"/>
        <source>SCHEDULE</source>
        <translation>PIANIFICAZIONE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1595"/>
        <location filename="../ui/main_window.ui" line="2049"/>
        <source>READY</source>
        <translation>PRONTI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1600"/>
        <location filename="../window.py" line="1616"/>
        <location filename="../ui/main_window.ui" line="1857"/>
        <location filename="../ui/main_window.ui" line="2034"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1602"/>
        <location filename="../window.py" line="1618"/>
        <location filename="../ui/main_window.ui" line="2044"/>
        <source>NAME</source>
        <translation>NOME</translation>
    </message>
    <message>
        <location filename="../window.py" line="1574"/>
        <location filename="../window.py" line="1581"/>
        <location filename="../window.py" line="1604"/>
        <location filename="../ui/main_window.ui" line="2054"/>
        <location filename="../ui/main_window.ui" line="2578"/>
        <source>STATUS</source>
        <translation>STATO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1605"/>
        <location filename="../ui/main_window.ui" line="2593"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../window.py" line="1606"/>
        <location filename="../ui/main_window.ui" line="2598"/>
        <source>MEMORY</source>
        <translation>MEMORIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1607"/>
        <source>RESTARTS</source>
        <translation>RIAVVII</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <location filename="../window.py" line="1620"/>
        <location filename="../ui/main_window.ui" line="2059"/>
        <location filename="../ui/main_window.ui" line="2608"/>
        <source>AGE</source>
        <translation>ETÀ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1617"/>
        <location filename="../ui/main_window.ui" line="2039"/>
        <source>KIND</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="20"/>
        <location filename="../ui/main_window.ui" line="283"/>
        <source>KubeScope</source>
        <translation>KubeScope</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="293"/>
        <source>Kubernetes console</source>
        <translation>Console Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="339"/>
        <source>CONTEXT</source>
        <translation>CONTESTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>Contesto Kubernetes dal tuo kubeconfig</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="372"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>Accedi con la CLI del cloud, poi ricarica i dati del cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="375"/>
        <source>Sign in</source>
        <translation>Accedi</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="397"/>
        <source>Settings</source>
        <translation>Impostazioni</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="437"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>Nessun contesto di cluster trovato nel tuo kubeconfig. Aggiungi un cluster al kubeconfig (ad esempio con la CLI di AWS: aws eks update-kubeconfig) e ricarica.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="478"/>
        <source>Dismiss</source>
        <translation>Chiudi</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="569"/>
        <source>MONITORING</source>
        <translation>MONITORAGGIO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1745"/>
        <source>Overview</source>
        <translation>Panoramica</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="607"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="638"/>
        <source>Workloads</source>
        <translation>Workload</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="845"/>
        <location filename="../ui/main_window.ui" line="1963"/>
        <source>Pods</source>
        <translation>Pod</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="783"/>
        <source>Deployments</source>
        <translation>Deployment</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="938"/>
        <source>StatefulSets</source>
        <translation>StatefulSet</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="752"/>
        <source>DaemonSets</source>
        <translation>DaemonSet</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="876"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSet</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="907"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationController</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="814"/>
        <source>Jobs</source>
        <translation>Job</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="721"/>
        <source>CronJobs</source>
        <translation>CronJob</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="972"/>
        <source>Network</source>
        <translation>Rete</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1179"/>
        <source>Services</source>
        <translation>Service</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1024"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slice</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1055"/>
        <source>Endpoints</source>
        <translation>Endpoint</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1117"/>
        <source>Ingresses</source>
        <translation>Ingress</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1086"/>
        <source>Ingress Classes</source>
        <translation>Ingress Class</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1148"/>
        <source>Network Policies</source>
        <translation>Network Policy</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1213"/>
        <source>Config</source>
        <translation>Configurazione</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1296"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1575"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1513"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1389"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1327"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1451"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1482"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1544"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1358"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1420"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1606"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1265"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1640"/>
        <source>Details &amp;&amp; Logs</source>
        <translation>Dettagli e log</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1696"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>ACCESSO SICURO
Risorse in modalità sola lettura</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1752"/>
        <source>Cluster resources and capacity</source>
        <translation>Risorse e capacità del cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1909"/>
        <source>Search by name or namespace...</source>
        <translation>Cerca per nome o namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1777"/>
        <location filename="../ui/main_window.ui" line="1790"/>
        <location filename="../ui/main_window.ui" line="1803"/>
        <source>Refresh</source>
        <translation>Aggiorna</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1960"/>
        <source>View Pods of the selected workload</source>
        <translation>Mostra i Pod del workload selezionato</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1976"/>
        <source>View JSON details of the selected workload</source>
        <translation>Mostra i dettagli JSON del workload selezionato</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1979"/>
        <source>Details</source>
        <translation>Dettagli</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1992"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Mostra i log di un Pod del workload selezionato</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1995"/>
        <source>Logs</source>
        <translation>Log</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2538"/>
        <source>Nodes</source>
        <translation>Nodi</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2573"/>
        <source>NODE</source>
        <translation>NODO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2583"/>
        <source>ROLE</source>
        <translation>RUOLO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2603"/>
        <source>PODS</source>
        <translation>POD</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2621"/>
        <source>Select a context to load workloads</source>
        <translation>Seleziona un contesto per caricare i workload</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2644"/>
        <source>Data fetched from the cluster API</source>
        <translation>Dati ottenuti dall&apos;API del cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2705"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>Apri il sito web di DCO Tecnologia</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2725"/>
        <source>MIT License</source>
        <translation>Licenza MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2728"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope è software open source rilasciato con licenza MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Update available</source>
        <translation>Aggiornamento disponibile</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2767"/>
        <source>Open the download page of the new version</source>
        <translation>Apri la pagina di download della nuova versione</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2795"/>
        <source>Check for updates</source>
        <translation>Verifica aggiornamenti</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2815"/>
        <source>Open the project on GitHub</source>
        <translation>Apri il progetto su GitHub</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="1998"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>nodi pronti</translation>
    </message>
    <message>
        <location filename="../window.py" line="2014"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>core richiesti / allocabili</translation>
    </message>
    <message>
        <location filename="../window.py" line="2028"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>richiesti / allocabili</translation>
    </message>
    <message>
        <location filename="../window.py" line="2047"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>nel cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2049"/>
        <location filename="../ui/overview_page.ui" line="510"/>
        <location filename="../ui/overview_page.ui" line="564"/>
        <location filename="../ui/overview_page.ui" line="618"/>
        <source>workloads</source>
        <translation>workload</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="29"/>
        <source>Cluster resources</source>
        <translation>Risorse del cluster</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="78"/>
        <source>CLUSTER INFO</source>
        <translation>INFORMAZIONI SUL CLUSTER</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="125"/>
        <source>NETWORKING</source>
        <translation>RETE</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="174"/>
        <source>NODES</source>
        <translation>NODI</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="228"/>
        <source>PODS</source>
        <translation>POD</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="248"/>
        <source>running / capacity</source>
        <translation>in esecuzione / capacità</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="295"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="362"/>
        <source>MEMORY</source>
        <translation>MEMORIA</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="436"/>
        <source>NAMESPACES</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="490"/>
        <source>DEPLOYMENTS</source>
        <translation>DEPLOYMENT</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="544"/>
        <source>STATEFULSETS</source>
        <translation>STATEFULSET</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="598"/>
        <source>DAEMONSETS</source>
        <translation>DAEMONSET</translation>
    </message>
</context>
<context>
    <name>PodsDialog</name>
    <message>
        <location filename="../ui/pods_dialog.ui" line="12"/>
        <source>Pods</source>
        <translation>Pod</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="41"/>
        <source>NAME</source>
        <translation>NOME</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>PRONTI</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>FASE</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>CONTAINER</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>ETÀ</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>Dettagli del Pod</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>Mostra i log</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>Chiudi</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="3038"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>Dai ai tuoi contesti nomi più semplici. Lascia un nome vuoto per mantenere quello originale.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>Salva le modifiche</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>GENERALE</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="107"/>
        <source>Language</source>
        <translation>Lingua</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="142"/>
        <source>Theme</source>
        <translation>Tema</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="177"/>
        <source>New theme...</source>
        <translation>Nuovo tema...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>Modifica tema...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>Apri la cartella dei temi</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>Namespace predefinito</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>Il namespace su cui si apre ogni contesto. Lascia vuoto per mostrarli tutti.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>Ricorda l&apos;ultimo contesto usato</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>Cerca una nuova versione su GitHub all&apos;avvio dell&apos;app</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>Interroga l&apos;API pubblica di GitHub per l&apos;ultima versione e non invia altro che la versione dell&apos;app. L&apos;icona nel piè di pagina controlla su richiesta.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>Modalità debug: scrivi un file di log da poter condividere</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>Apri la cartella dei log</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>Svuota la cache</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>Dimentica gli elenchi e le panoramiche già caricati e l&apos;accesso di ogni cluster, così la richiesta successiva accede e carica di nuovo tutto. Le tue impostazioni vengono mantenute.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>FILE KUBECONFIG</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>KubeScope legge i file della variabile KUBECONFIG, oppure ~/.kube/config. Aggiungi qui dei file per leggere quelli al loro posto. Premi Salva per applicare.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>Aggiungi file...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>Rimuovi</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>COMANDI DI ACCESSO</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>Per un cloud che KubeScope non conosce, indica il programma che il tuo kubeconfig usa per accedere (ad esempio oci) e il comando che effettua l&apos;accesso (ad esempio oci session authenticate). Il pulsante Accedi lo esegue, senza shell. Premi Salva per applicare.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>PROGRAMMA</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>COMANDO DI ACCESSO</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>Aggiungi riga</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>NOMI DEI CONTESTI</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>CONTESTO</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>NOME VISUALIZZATO</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>Sfondo della pagina</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>Pannelli e schede</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>Pannelli alternati</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>Tracce delle barre</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>Bordi</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>Barra superiore</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>Logo della barra superiore</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>Selettore della barra superiore</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>Bordo del selettore della barra superiore</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>Selezione della barra superiore</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>Testo della barra superiore</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>Testo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>Titolo della barra laterale</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>Testo secondario</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>Testo disabilitato</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>Testo di accento e link</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>Pulsanti di accento</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>Pulsanti di accento al passaggio del mouse</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>Pulsanti di accento disabilitati</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>Focus ed evidenziazioni</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>Testo del badge</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>Tinta di accento</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>Selezione del testo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>Bordo di accento</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>Testo sulla barra superiore e sui pulsanti di accento</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>Testo integro</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>Sfondo integro</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>Testo di avviso</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>Sfondo di avviso</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>Testo di errore</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>Sfondo di errore</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>Testo inattivo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>Sfondo inattivo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>Riga con un problema</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>Riga di un Pod recente</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>Barra di utilizzo, quasi piena</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>Barra di utilizzo, piena</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>Barra di salute, integro</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>Barra di salute, avviso</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>Barra di salute, errore</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>Nuovo tema</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>Modifica tema: {name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>Nome del tema</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>Chiaro</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>Scuro</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>Nome</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>Parte da</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>Colori</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>Salva in un file ciò che mostra questa scheda</translation>
    </message>
</context>
<context>
    <name>WorkloadWindow</name>
    <message>
        <location filename="../window.py" line="707"/>
        <source>0 Deployments</source>
        <translation>0 Deployment</translation>
    </message>
    <message>
        <location filename="../window.py" line="723"/>
        <location filename="../window.py" line="2267"/>
        <location filename="../window.py" line="2290"/>
        <location filename="../window.py" line="3276"/>
        <source>All namespaces</source>
        <translation>Tutti i namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="834"/>
        <source>Loading contexts...</source>
        <translation>Caricamento dei contesti...</translation>
    </message>
    <message>
        <location filename="../window.py" line="843"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>Impossibile caricare il kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="865"/>
        <source>No contexts found in kubeconfig</source>
        <translation>Nessun contesto trovato nel kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="894"/>
        <location filename="../window.py" line="972"/>
        <source>Unpin from the top</source>
        <translation>Rimuovi dall&apos;alto</translation>
    </message>
    <message>
        <location filename="../window.py" line="894"/>
        <source>Pin to the top</source>
        <translation>Fissa in alto</translation>
    </message>
    <message>
        <location filename="../window.py" line="1021"/>
        <source>Status</source>
        <translation>Stato</translation>
    </message>
    <message>
        <location filename="../window.py" line="1022"/>
        <source>Kubernetes version</source>
        <translation>Versione di Kubernetes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1023"/>
        <source>Platform version</source>
        <translation>Versione della piattaforma</translation>
    </message>
    <message>
        <location filename="../window.py" line="1024"/>
        <source>Created</source>
        <translation>Creato</translation>
    </message>
    <message>
        <location filename="../window.py" line="1025"/>
        <source>Provider</source>
        <translation>Provider</translation>
    </message>
    <message>
        <location filename="../window.py" line="1028"/>
        <source>API server endpoint</source>
        <translation>Endpoint del server API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1029"/>
        <source>Cluster ARN</source>
        <translation>ARN del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1030"/>
        <source>Cluster IAM role ARN</source>
        <translation>ARN del ruolo IAM del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1031"/>
        <source>OpenID Connect provider URL</source>
        <translation>URL del provider OpenID Connect</translation>
    </message>
    <message>
        <location filename="../window.py" line="1039"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1040"/>
        <source>Cluster security group</source>
        <translation>Security group del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1042"/>
        <source>Additional security groups</source>
        <translation>Security group aggiuntivi</translation>
    </message>
    <message>
        <location filename="../window.py" line="1043"/>
        <source>None</source>
        <translation>Nessuno</translation>
    </message>
    <message>
        <location filename="../window.py" line="1046"/>
        <source>API server endpoint access</source>
        <translation>Accesso all&apos;endpoint del server API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1049"/>
        <source>Cluster IP address family</source>
        <translation>Famiglia di indirizzi IP del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1050"/>
        <source>Service IPv4 range</source>
        <translation>Intervallo IPv4 dei servizi</translation>
    </message>
    <message>
        <location filename="../window.py" line="1052"/>
        <source>Public access source allowlist</source>
        <translation>Origini consentite per l&apos;accesso pubblico</translation>
    </message>
    <message>
        <location filename="../window.py" line="1055"/>
        <source>Subnets</source>
        <translation>Subnet</translation>
    </message>
    <message>
        <location filename="../window.py" line="1066"/>
        <source>Creating</source>
        <translation>In creazione</translation>
    </message>
    <message>
        <location filename="../window.py" line="1067"/>
        <source>Updating</source>
        <translation>In aggiornamento</translation>
    </message>
    <message>
        <location filename="../window.py" line="1068"/>
        <source>Deleting</source>
        <translation>In eliminazione</translation>
    </message>
    <message>
        <location filename="../window.py" line="1071"/>
        <source>Creation failed</source>
        <translation>Creazione non riuscita</translation>
    </message>
    <message>
        <location filename="../window.py" line="1072"/>
        <source>Update failed</source>
        <translation>Aggiornamento non riuscito</translation>
    </message>
    <message>
        <location filename="../window.py" line="1073"/>
        <source>Deletion failed</source>
        <translation>Eliminazione non riuscita</translation>
    </message>
    <message>
        <location filename="../window.py" line="1075"/>
        <source>Deployed</source>
        <translation>Distribuito</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Superseded</source>
        <translation>Sostituito</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>Uninstalled</source>
        <translation>Disinstallato</translation>
    </message>
    <message>
        <location filename="../window.py" line="1078"/>
        <source>Uninstalling</source>
        <translation>In disinstallazione</translation>
    </message>
    <message>
        <location filename="../window.py" line="1079"/>
        <source>Pending install</source>
        <translation>Installazione in sospeso</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>Pending upgrade</source>
        <translation>Aggiornamento in sospeso</translation>
    </message>
    <message>
        <location filename="../window.py" line="1081"/>
        <source>Pending rollback</source>
        <translation>Rollback in sospeso</translation>
    </message>
    <message>
        <location filename="../window.py" line="1082"/>
        <source>Public</source>
        <translation>Pubblico</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>Private</source>
        <translation>Privato</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Public and private</source>
        <translation>Pubblico e privato</translation>
    </message>
    <message>
        <location filename="../window.py" line="1177"/>
        <source>Overview</source>
        <translation>Panoramica</translation>
    </message>
    <message>
        <location filename="../window.py" line="1178"/>
        <source>Cluster resources and capacity</source>
        <translation>Risorse e capacità del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1180"/>
        <source>Details &amp; Logs</source>
        <translation>Dettagli e log</translation>
    </message>
    <message>
        <location filename="../window.py" line="1182"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Dettagli della risorsa e log dei Pod, una scheda ciascuno</translation>
    </message>
    <message>
        <location filename="../window.py" line="1185"/>
        <source>Settings</source>
        <translation>Impostazioni</translation>
    </message>
    <message>
        <location filename="../window.py" line="1186"/>
        <source>Preferences and context names</source>
        <translation>Preferenze e nomi dei contesti</translation>
    </message>
    <message>
        <location filename="../window.py" line="1188"/>
        <source>Workloads overview</source>
        <translation>Panoramica dei workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="1190"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>Stato di ogni tipo di workload e ultimi eventi</translation>
    </message>
    <message>
        <location filename="../window.py" line="1194"/>
        <location filename="../window.py" line="1845"/>
        <source>Pods</source>
        <translation>Pod</translation>
    </message>
    <message>
        <location filename="../window.py" line="1194"/>
        <source>Pods of the cluster</source>
        <translation>Pod del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1196"/>
        <location filename="../window.py" line="1846"/>
        <source>Deployments</source>
        <translation>Deployment</translation>
    </message>
    <message>
        <location filename="../window.py" line="1197"/>
        <source>Deployments of the cluster</source>
        <translation>Deployment del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1200"/>
        <location filename="../window.py" line="1848"/>
        <source>StatefulSets</source>
        <translation>StatefulSet</translation>
    </message>
    <message>
        <location filename="../window.py" line="1201"/>
        <source>StatefulSets of the cluster</source>
        <translation>StatefulSet del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1204"/>
        <location filename="../window.py" line="1847"/>
        <source>DaemonSets</source>
        <translation>DaemonSet</translation>
    </message>
    <message>
        <location filename="../window.py" line="1205"/>
        <source>DaemonSets of the cluster</source>
        <translation>DaemonSet del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1208"/>
        <location filename="../window.py" line="1849"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSet</translation>
    </message>
    <message>
        <location filename="../window.py" line="1209"/>
        <source>ReplicaSets of the cluster</source>
        <translation>ReplicaSet del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1212"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationController</translation>
    </message>
    <message>
        <location filename="../window.py" line="1213"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>ReplicationController del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1215"/>
        <location filename="../window.py" line="1850"/>
        <source>Jobs</source>
        <translation>Job</translation>
    </message>
    <message>
        <location filename="../window.py" line="1215"/>
        <source>Jobs of the cluster</source>
        <translation>Job del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1216"/>
        <location filename="../window.py" line="1851"/>
        <source>CronJobs</source>
        <translation>CronJob</translation>
    </message>
    <message>
        <location filename="../window.py" line="1216"/>
        <source>CronJobs of the cluster</source>
        <translation>CronJob del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1217"/>
        <source>Services</source>
        <translation>Service</translation>
    </message>
    <message>
        <location filename="../window.py" line="1217"/>
        <source>Services of the cluster</source>
        <translation>Service del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1219"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slice</translation>
    </message>
    <message>
        <location filename="../window.py" line="1220"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>Endpoint Slice del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1223"/>
        <source>Endpoints</source>
        <translation>Endpoint</translation>
    </message>
    <message>
        <location filename="../window.py" line="1224"/>
        <source>Endpoints of the cluster</source>
        <translation>Endpoint del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1227"/>
        <source>Ingresses</source>
        <translation>Ingress</translation>
    </message>
    <message>
        <location filename="../window.py" line="1228"/>
        <source>Ingresses of the cluster</source>
        <translation>Ingress del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1231"/>
        <source>Ingress Classes</source>
        <translation>Ingress Class</translation>
    </message>
    <message>
        <location filename="../window.py" line="1232"/>
        <source>Ingress Classes of the cluster</source>
        <translation>Ingress Class del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1235"/>
        <source>Network Policies</source>
        <translation>Network Policy</translation>
    </message>
    <message>
        <location filename="../window.py" line="1236"/>
        <source>Network Policies of the cluster</source>
        <translation>Network Policy del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1239"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1240"/>
        <source>Config Maps of the cluster</source>
        <translation>Config Maps del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1243"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1244"/>
        <source>Secrets of the cluster</source>
        <translation>Secrets del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1247"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1248"/>
        <source>Resource Quotas of the cluster</source>
        <translation>Resource Quotas del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1251"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1252"/>
        <source>Limit Ranges of the cluster</source>
        <translation>Limit Ranges del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1255"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1256"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>Horizontal Pod Autoscalers del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1259"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1260"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>Pod Disruption Budgets del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1263"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1264"/>
        <source>Priority Classes of the cluster</source>
        <translation>Priority Classes del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1267"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>Runtime Classes of the cluster</source>
        <translation>Runtime Classes del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1271"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Leases of the cluster</source>
        <translation>Leases del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1275"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1276"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>Mutating Webhook Configurations del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1279"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1280"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>Validating Webhook Configurations del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1283"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1284"/>
        <source>Node Groups of the cluster</source>
        <translation>Node Groups del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1287"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1288"/>
        <source>Add-ons of the cluster</source>
        <translation>Add-ons del cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1297"/>
        <source>Version {version}</source>
        <translation>Versione {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1300"/>
        <source>Open the project on GitHub</source>
        <translation>Apri il progetto su GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="1334"/>
        <source>Up to date</source>
        <translation>Aggiornato</translation>
    </message>
    <message>
        <location filename="../window.py" line="1335"/>
        <source>Could not check</source>
        <translation>Verifica non riuscita</translation>
    </message>
    <message>
        <location filename="../window.py" line="1346"/>
        <source>Check for updates</source>
        <translation>Verifica aggiornamenti</translation>
    </message>
    <message>
        <location filename="../window.py" line="1347"/>
        <source>Checking for updates...</source>
        <translation>Verifica degli aggiornamenti...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1348"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope è aggiornato. Fai clic per verificare di nuovo.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1349"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>Impossibile verificare gli aggiornamenti. Fai clic per riprovare.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1355"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>Aggiornamento disponibile: {version}. Fai clic per aprire la pagina di download; clic destro per verificare di nuovo.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1363"/>
        <source>Update available</source>
        <translation>Aggiornamento disponibile</translation>
    </message>
    <message>
        <location filename="../window.py" line="1365"/>
        <source>Download KubeScope {version}</source>
        <translation>Scarica KubeScope {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1401"/>
        <source>Check for updates again</source>
        <translation>Verifica di nuovo gli aggiornamenti</translation>
    </message>
    <message>
        <location filename="../window.py" line="1499"/>
        <location filename="../window.py" line="2174"/>
        <source>Loading resources...</source>
        <translation>Caricamento delle risorse...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1743"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Configura le credenziali AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1747"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>Le credenziali AWS del profilo {profile} mancano o non sono valide</translation>
    </message>
    <message>
        <location filename="../window.py" line="1752"/>
        <source>Sign in to {provider}</source>
        <translation>Accedi a {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1755"/>
        <source>Not signed in to {provider}</source>
        <translation>Accesso a {provider} non effettuato</translation>
    </message>
    <message>
        <location filename="../window.py" line="1759"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>Accedi a {provider} ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1765"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>Accesso a {provider} non effettuato (profilo {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1786"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Termina nel terminale che si è aperto, poi premi Aggiorna.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1805"/>
        <source>Loading workloads...</source>
        <translation>Caricamento dei workload...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1866"/>
        <source>Could not read: {names}</source>
        <translation>Impossibile leggere: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1926"/>
        <source>Loading cluster data...</source>
        <translation>Caricamento dei dati del cluster...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2007"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>in esecuzione · {pending} in attesa · {failed} in errore</translation>
    </message>
    <message>
        <location filename="../window.py" line="2016"/>
        <location filename="../window.py" line="2030"/>
        <source> · usage {value}</source>
        <translation> · utilizzo {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <source>Ready</source>
        <translation>Pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <source>Not ready</source>
        <translation>Non pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="2054"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Utilizzo reale non disponibile: metrics-server non trovato.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2191"/>
        <source>Refreshing...</source>
        <translation>Aggiornamento...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2382"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{count} Service in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2384"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{count} Endpoint Slice in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2387"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{count} Endpoint in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2390"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{count} Ingress in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2392"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>{count} Ingress Class nel cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2394"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{count} Network Policy in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2397"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>{count} Config Maps in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2399"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>{count} Secrets in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2401"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>{count} Resource Quotas in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2404"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>{count} Limit Ranges in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2407"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>{count} Horizontal Pod Autoscalers in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2410"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>{count} Pod Disruption Budgets in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2412"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>{count} Leases in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2414"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>{count} Priority Classes nel cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2416"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>{count} Runtime Classes nel cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2418"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>{count} Mutating Webhook Configurations nel cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2421"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>{count} Validating Webhook Configurations nel cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2423"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>{count} Node Groups nel cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2424"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>{count} Add-ons nel cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2435"/>
        <location filename="../window.py" line="2501"/>
        <source>Running</source>
        <translation>In esecuzione</translation>
    </message>
    <message>
        <location filename="../window.py" line="1074"/>
        <location filename="../window.py" line="2436"/>
        <location filename="../window.py" line="2497"/>
        <source>Pending</source>
        <translation>In attesa</translation>
    </message>
    <message>
        <location filename="../window.py" line="2437"/>
        <source>Succeeded</source>
        <translation>Riuscito</translation>
    </message>
    <message>
        <location filename="../window.py" line="1070"/>
        <location filename="../window.py" line="2438"/>
        <location filename="../window.py" line="2496"/>
        <source>Failed</source>
        <translation>Fallito</translation>
    </message>
    <message>
        <location filename="../window.py" line="2439"/>
        <source>Unknown</source>
        <translation>Sconosciuto</translation>
    </message>
    <message>
        <location filename="../window.py" line="2483"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pod in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2491"/>
        <source>Healthy</source>
        <translation>Integro</translation>
    </message>
    <message>
        <location filename="../window.py" line="1069"/>
        <location filename="../window.py" line="2492"/>
        <source>Degraded</source>
        <translation>Degradato</translation>
    </message>
    <message>
        <location filename="../window.py" line="2493"/>
        <source>Unavailable</source>
        <translation>Non disponibile</translation>
    </message>
    <message>
        <location filename="../window.py" line="2494"/>
        <source>Scaled to zero</source>
        <translation>Ridotto a zero</translation>
    </message>
    <message>
        <location filename="../window.py" line="2495"/>
        <source>Complete</source>
        <translation>Completato</translation>
    </message>
    <message>
        <location filename="../window.py" line="2498"/>
        <source>Suspended</source>
        <translation>Sospeso</translation>
    </message>
    <message>
        <location filename="../window.py" line="1065"/>
        <location filename="../window.py" line="2499"/>
        <source>Active</source>
        <translation>Attivo</translation>
    </message>
    <message>
        <location filename="../window.py" line="2500"/>
        <source>Scheduled</source>
        <translation>Pianificato</translation>
    </message>
    <message>
        <location filename="../window.py" line="2545"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployment in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2548"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{count} StatefulSet in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2551"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{count} DaemonSet in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2554"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{count} ReplicaSet in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2557"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{count} ReplicationController in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2559"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{count} Job in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2560"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{count} CronJob in {namespaces} namespace</translation>
    </message>
    <message>
        <location filename="../window.py" line="2584"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} di {total} Pod</translation>
    </message>
    <message>
        <location filename="../window.py" line="2585"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} di {total} Deployment</translation>
    </message>
    <message>
        <location filename="../window.py" line="2586"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{visible} di {total} StatefulSet</translation>
    </message>
    <message>
        <location filename="../window.py" line="2587"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{visible} di {total} DaemonSet</translation>
    </message>
    <message>
        <location filename="../window.py" line="2588"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{visible} di {total} ReplicaSet</translation>
    </message>
    <message>
        <location filename="../window.py" line="2590"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{visible} di {total} ReplicationController</translation>
    </message>
    <message>
        <location filename="../window.py" line="2592"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{visible} di {total} Job</translation>
    </message>
    <message>
        <location filename="../window.py" line="2593"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{visible} di {total} CronJob</translation>
    </message>
    <message>
        <location filename="../window.py" line="2594"/>
        <source>{visible} of {total} Services</source>
        <translation>{visible} di {total} Service</translation>
    </message>
    <message>
        <location filename="../window.py" line="2595"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{visible} di {total} Endpoint Slice</translation>
    </message>
    <message>
        <location filename="../window.py" line="2596"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{visible} di {total} Endpoint</translation>
    </message>
    <message>
        <location filename="../window.py" line="2597"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{visible} di {total} Ingress</translation>
    </message>
    <message>
        <location filename="../window.py" line="2598"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{visible} di {total} Ingress Class</translation>
    </message>
    <message>
        <location filename="../window.py" line="2599"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{visible} di {total} Network Policy</translation>
    </message>
    <message>
        <location filename="../window.py" line="2600"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>{visible} di {total} Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="2601"/>
        <source>{visible} of {total} Secrets</source>
        <translation>{visible} di {total} Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2602"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>{visible} di {total} Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="2603"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>{visible} di {total} Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="2605"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>{visible} di {total} Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2608"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>{visible} di {total} Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2610"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>{visible} di {total} Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2611"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>{visible} di {total} Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2612"/>
        <source>{visible} of {total} Leases</source>
        <translation>{visible} di {total} Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="2614"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>{visible} di {total} Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2617"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>{visible} di {total} Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2619"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>{visible} di {total} Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="2620"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>{visible} di {total} Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="2666"/>
        <source>Loading...</source>
        <translation>Caricamento...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2712"/>
        <location filename="../window.py" line="2804"/>
        <source>Pod: {name}</source>
        <translation>Pod: {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2758"/>
        <source>Pods of {name}</source>
        <translation>Pod di {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2760"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pod in {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2825"/>
        <source>No Pods are associated with this workload</source>
        <translation>Nessun Pod è associato a questo workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="2832"/>
        <location filename="../window.py" line="2855"/>
        <source>Logs</source>
        <translation>Log</translation>
    </message>
    <message>
        <location filename="../window.py" line="2832"/>
        <source>This workload has no Pods.</source>
        <translation>Questo workload non ha Pod.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2841"/>
        <location filename="../window.py" line="2864"/>
        <source>View logs</source>
        <translation>Mostra i log</translation>
    </message>
    <message>
        <location filename="../window.py" line="2842"/>
        <source>Select the Pod:</source>
        <translation>Seleziona il Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2856"/>
        <source>Pod {name} has no containers.</source>
        <translation>Il Pod {name} non ha container.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2865"/>
        <source>Select the container of {name}:</source>
        <translation>Seleziona il container di {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2891"/>
        <source>Save to a file</source>
        <translation>Salva in un file</translation>
    </message>
    <message>
        <location filename="../window.py" line="2902"/>
        <source>Could not save</source>
        <translation>Impossibile salvare</translation>
    </message>
    <message>
        <location filename="../window.py" line="2903"/>
        <source>The file could not be written: {reason}</source>
        <translation>Impossibile scrivere il file: {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2951"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Log: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3001"/>
        <source>Automatic</source>
        <translation>Automatico</translation>
    </message>
    <message>
        <location filename="../window.py" line="3014"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>Disattivata per impostazione predefinita. Quando è attiva, KubeScope scrive ciò che fa, mai i log dei Pod né il contenuto delle risorse, in {path}. Leggilo prima di condividerlo: include i nomi dei contesti.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3045"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>Nessun contesto trovato nel kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3074"/>
        <source>Choose a kubeconfig file</source>
        <translation>Scegli un file kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="3120"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>Il comando di accesso della riga {row} non è valido.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3133"/>
        <source>Light</source>
        <translation>Chiaro</translation>
    </message>
    <message>
        <location filename="../window.py" line="3133"/>
        <source>Dark</source>
        <translation>Scuro</translation>
    </message>
    <message>
        <location filename="../window.py" line="3152"/>
        <source>My theme</source>
        <translation>Il mio tema</translation>
    </message>
    <message>
        <location filename="../window.py" line="3196"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>Cache svuotata. Tutto viene caricato di nuovo la prossima volta che serve.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3251"/>
        <source>Settings saved.</source>
        <translation>Impostazioni salvate.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3290"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>Il tuo utente non è autorizzato a eseguire questa azione ({action}). Chiedi l&apos;accesso all&apos;amministratore del cluster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3295"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>Il tuo utente non è autorizzato a farlo. Chiedi l&apos;accesso all&apos;amministratore del cluster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3314"/>
        <source>Query failed</source>
        <translation>Richiesta non riuscita</translation>
    </message>
</context>
<context>
    <name>WorkloadsOverviewPage</name>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="29"/>
        <source>Workloads</source>
        <translation>Workload</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="78"/>
        <source>Pods</source>
        <translation>Pod</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="100"/>
        <source>Deployments</source>
        <translation>Deployment</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="122"/>
        <source>DaemonSets</source>
        <translation>DaemonSet</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="144"/>
        <source>StatefulSets</source>
        <translation>StatefulSet</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="166"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSet</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="188"/>
        <source>Jobs</source>
        <translation>Job</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="210"/>
        <source>CronJobs</source>
        <translation>CronJob</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="258"/>
        <source>Events</source>
        <translation>Eventi</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="293"/>
        <source>TYPE</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="298"/>
        <source>SOURCE</source>
        <translation>ORIGINE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>INVOLVED OBJECT</source>
        <translation>OGGETTO COINVOLTO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>MESSAGE</source>
        <translation>MESSAGGIO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>COUNT</source>
        <translation>CONTEGGIO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>AGE</source>
        <translation>ETÀ</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>LAST SEEN</source>
        <translation>ULTIMA VOLTA</translation>
    </message>
</context>
</TS>
