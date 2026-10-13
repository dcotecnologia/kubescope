<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="fr">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>Outil de connexion introuvable</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>Votre kubeconfig exécute « {tool} » pour se connecter, mais il n&apos;est pas installé ou n&apos;est pas dans le PATH. Installez-le puis actualisez.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>Contexte introuvable</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>Ce contexte n&apos;est pas dans votre kubeconfig. Vérifiez ~/.kube/config.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>Échec de l&apos;authentification</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>Vos identifiants ont peut-être expiré. Reconnectez-vous (par exemple avec « aws sso login », « gcloud auth login » ou « az login ») puis actualisez.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Not an Amazon EKS cluster</source>
        <translation>Ce n&apos;est pas un cluster Amazon EKS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Node Groups, Add-ons and the AWS cards of the Overview exist only on Amazon EKS contexts.</source>
        <translation>Les Node Groups, les Add-ons et les cartes AWS de la Vue d&apos;ensemble n&apos;existent que sur les contextes Amazon EKS.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="110"/>
        <source>Unexpected answer from AWS</source>
        <translation>Réponse inattendue d&apos;AWS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="111"/>
        <source>Update the AWS CLI to its latest version and refresh.</source>
        <translation>Mettez à jour l&apos;AWS CLI vers la dernière version puis actualisez.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="118"/>
        <location filename="../errors.py" line="128"/>
        <source>Access denied</source>
        <translation>Accès refusé</translation>
    </message>
    <message>
        <location filename="../errors.py" line="119"/>
        <source>Your AWS identity is not allowed to read this. The wiki lists the eks: permissions KubeScope needs.</source>
        <translation>Votre identité AWS n&apos;est pas autorisée à lire ceci. Le wiki liste les autorisations eks: dont KubeScope a besoin.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>Votre utilisateur n&apos;est pas autorisé à lire cette ressource.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="143"/>
        <source>No network connection</source>
        <translation>Pas de connexion réseau</translation>
    </message>
    <message>
        <location filename="../errors.py" line="144"/>
        <source>Check your internet connection or VPN and refresh.</source>
        <translation>Vérifiez votre connexion internet ou VPN, puis actualisez.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="165"/>
        <source>Cluster unreachable</source>
        <translation>Cluster inaccessible</translation>
    </message>
    <message>
        <location filename="../errors.py" line="166"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>Vérifiez votre réseau ou votre VPN, et que le cluster est en cours d&apos;exécution.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="172"/>
        <source>Something went wrong</source>
        <translation>Une erreur est survenue</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="46"/>
        <source>No log lines returned.</source>
        <translation>Aucune ligne de journal renvoyée.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="51"/>
        <source>Updated at {time}</source>
        <translation>Mis à jour à {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="58"/>
        <source>Could not refresh logs: {message}</source>
        <translation>Impossible d&apos;actualiser les journaux : {message}</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>Actualisation automatique</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>Récupère de nouvelles lignes de journal toutes les quelques secondes et suit la fin du journal</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>Actualiser maintenant</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../window.py" line="1540"/>
        <location filename="../window.py" line="1569"/>
        <source>TYPE</source>
        <translation>TYPE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1541"/>
        <source>CLUSTER IP</source>
        <translation>IP DU CLUSTER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1542"/>
        <source>EXTERNAL IP</source>
        <translation>IP EXTERNE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1543"/>
        <location filename="../window.py" line="1547"/>
        <location filename="../window.py" line="1555"/>
        <source>PORTS</source>
        <translation>PORTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1546"/>
        <source>ADDRESS TYPE</source>
        <translation>TYPE D&apos;ADRESSE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1548"/>
        <location filename="../window.py" line="1550"/>
        <source>ENDPOINTS</source>
        <translation>ENDPOINTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1552"/>
        <source>CLASS</source>
        <translation>CLASSE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <source>HOSTS</source>
        <translation>HÔTES</translation>
    </message>
    <message>
        <location filename="../window.py" line="1554"/>
        <source>ADDRESS</source>
        <translation>ADRESSE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1558"/>
        <source>CONTROLLER</source>
        <translation>CONTRÔLEUR</translation>
    </message>
    <message>
        <location filename="../window.py" line="1559"/>
        <source>PARAMETERS</source>
        <translation>PARAMÈTRES</translation>
    </message>
    <message>
        <location filename="../window.py" line="1562"/>
        <source>POD SELECTOR</source>
        <translation>SÉLECTEUR DE PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1563"/>
        <source>POLICY TYPES</source>
        <translation>TYPES DE POLITIQUE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1566"/>
        <location filename="../window.py" line="1570"/>
        <source>DATA</source>
        <translation>DONNÉES</translation>
    </message>
    <message>
        <location filename="../window.py" line="1573"/>
        <source>USAGE</source>
        <translation>UTILISATION</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>TYPES</source>
        <translation>TYPES</translation>
    </message>
    <message>
        <location filename="../window.py" line="1579"/>
        <source>REFERENCE</source>
        <translation>RÉFÉRENCE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1580"/>
        <source>MIN PODS</source>
        <translation>MIN PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1581"/>
        <source>MAX PODS</source>
        <translation>MAX PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1582"/>
        <source>REPLICAS</source>
        <translation>RÉPLIQUES</translation>
    </message>
    <message>
        <location filename="../window.py" line="1585"/>
        <source>MIN AVAILABLE</source>
        <translation>MIN DISPONIBLE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1586"/>
        <source>MAX UNAVAILABLE</source>
        <translation>MAX INDISPONIBLE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1587"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>INTERRUPTIONS AUTORISÉES</translation>
    </message>
    <message>
        <location filename="../window.py" line="1590"/>
        <source>VALUE</source>
        <translation>VALEUR</translation>
    </message>
    <message>
        <location filename="../window.py" line="1591"/>
        <source>GLOBAL DEFAULT</source>
        <translation>DÉFAUT GLOBAL</translation>
    </message>
    <message>
        <location filename="../window.py" line="1594"/>
        <source>HANDLER</source>
        <translation>HANDLER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1597"/>
        <source>HOLDER</source>
        <translation>DÉTENTEUR</translation>
    </message>
    <message>
        <location filename="../window.py" line="1600"/>
        <location filename="../window.py" line="1603"/>
        <source>WEBHOOKS</source>
        <translation>WEBHOOKS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1607"/>
        <source>INSTANCE TYPES</source>
        <translation>TYPES D&apos;INSTANCE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <source>NODES</source>
        <translation>NŒUDS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1609"/>
        <source>AMI TYPE</source>
        <translation>TYPE D&apos;AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1610"/>
        <source>AMI VERSION</source>
        <translation>VERSION DE L&apos;AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1614"/>
        <location filename="../ui/main_window.ui" line="2557"/>
        <source>VERSION</source>
        <translation>VERSION</translation>
    </message>
    <message>
        <location filename="../window.py" line="1615"/>
        <source>SOURCE</source>
        <translation>SOURCE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1625"/>
        <source>COMPLETIONS</source>
        <translation>TERMINÉS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1626"/>
        <source>SCHEDULE</source>
        <translation>PLANIFICATION</translation>
    </message>
    <message>
        <location filename="../window.py" line="1627"/>
        <location filename="../ui/main_window.ui" line="2018"/>
        <source>READY</source>
        <translation>PRÊTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1632"/>
        <location filename="../window.py" line="1648"/>
        <location filename="../ui/main_window.ui" line="1826"/>
        <location filename="../ui/main_window.ui" line="2003"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1634"/>
        <location filename="../window.py" line="1650"/>
        <location filename="../ui/main_window.ui" line="2013"/>
        <source>NAME</source>
        <translation>NOM</translation>
    </message>
    <message>
        <location filename="../window.py" line="1606"/>
        <location filename="../window.py" line="1613"/>
        <location filename="../window.py" line="1636"/>
        <location filename="../ui/main_window.ui" line="2023"/>
        <location filename="../ui/main_window.ui" line="2547"/>
        <source>STATUS</source>
        <translation>STATUT</translation>
    </message>
    <message>
        <location filename="../window.py" line="1637"/>
        <location filename="../ui/main_window.ui" line="2562"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../window.py" line="1638"/>
        <location filename="../ui/main_window.ui" line="2567"/>
        <source>MEMORY</source>
        <translation>MÉMOIRE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1639"/>
        <source>RESTARTS</source>
        <translation>REDÉMARRAGES</translation>
    </message>
    <message>
        <location filename="../window.py" line="1640"/>
        <location filename="../window.py" line="1652"/>
        <location filename="../ui/main_window.ui" line="2028"/>
        <location filename="../ui/main_window.ui" line="2577"/>
        <source>AGE</source>
        <translation>ÂGE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1649"/>
        <location filename="../ui/main_window.ui" line="2008"/>
        <source>KIND</source>
        <translation>KIND</translation>
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
        <translation>CONTEXTE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>Contexte Kubernetes de votre kubeconfig</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="372"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>Connectez-vous avec la CLI du cloud, puis rechargez les données du cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="375"/>
        <source>Sign in</source>
        <translation>Se connecter</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="397"/>
        <source>Settings</source>
        <translation>Paramètres</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="437"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>Aucun contexte de cluster trouvé dans votre kubeconfig. Ajoutez un cluster à votre kubeconfig (par exemple avec la CLI AWS : aws eks update-kubeconfig) puis rechargez.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="478"/>
        <source>Dismiss</source>
        <translation>Fermer</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="569"/>
        <source>MONITORING</source>
        <translation>SUPERVISION</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1714"/>
        <source>Overview</source>
        <translation>Vue d&apos;ensemble</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="607"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="638"/>
        <source>Workloads</source>
        <translation>Workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="845"/>
        <location filename="../ui/main_window.ui" line="1932"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="783"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="938"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="752"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="876"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="907"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="814"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="721"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="972"/>
        <source>Network</source>
        <translation>Réseau</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1179"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1024"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1055"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1117"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1086"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1148"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1213"/>
        <source>Config</source>
        <translation>Configuration</translation>
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
        <location filename="../ui/main_window.ui" line="1665"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>ACCÈS SÉCURISÉ
Ressources en mode lecture seule</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1721"/>
        <source>Cluster resources and capacity</source>
        <translation>Ressources et capacité du cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1878"/>
        <source>Search by name or namespace...</source>
        <translation>Rechercher par nom ou namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1746"/>
        <location filename="../ui/main_window.ui" line="1759"/>
        <location filename="../ui/main_window.ui" line="1772"/>
        <source>Refresh</source>
        <translation>Actualiser</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <source>Cluster</source>
        <translation>Cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1929"/>
        <source>View Pods of the selected workload</source>
        <translation>Afficher les Pods du workload sélectionné</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1945"/>
        <source>View JSON details of the selected workload</source>
        <translation>Afficher les détails JSON du workload sélectionné</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1948"/>
        <source>Details</source>
        <translation>Détails</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1961"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Afficher les journaux d&apos;un Pod du workload sélectionné</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1964"/>
        <source>Logs</source>
        <translation>Journaux</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2507"/>
        <source>Nodes</source>
        <translation>Nœuds</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2542"/>
        <source>NODE</source>
        <translation>NŒUD</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2552"/>
        <source>ROLE</source>
        <translation>RÔLE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2572"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2590"/>
        <source>Select a context to load workloads</source>
        <translation>Sélectionnez un contexte pour charger les workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2613"/>
        <source>Data fetched from the cluster API</source>
        <translation>Données obtenues depuis l&apos;API du cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2674"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>Ouvrir le site web de DCO Tecnologia</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2694"/>
        <source>MIT License</source>
        <translation>Licence MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2697"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope est un logiciel libre publié sous licence MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2733"/>
        <source>Update available</source>
        <translation>Mise à jour disponible</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2736"/>
        <source>Open the download page of the new version</source>
        <translation>Ouvrir la page de téléchargement de la nouvelle version</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Check for updates</source>
        <translation>Rechercher des mises à jour</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2784"/>
        <source>Open the project on GitHub</source>
        <translation>Ouvrir le projet sur GitHub</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="2030"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>nœuds prêts</translation>
    </message>
    <message>
        <location filename="../window.py" line="2046"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>cœurs demandés / allouables</translation>
    </message>
    <message>
        <location filename="../window.py" line="2060"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>demandé / allouable</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>dans le cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2081"/>
        <location filename="../ui/overview_page.ui" line="510"/>
        <location filename="../ui/overview_page.ui" line="564"/>
        <location filename="../ui/overview_page.ui" line="618"/>
        <source>workloads</source>
        <translation>workloads</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="29"/>
        <source>Cluster resources</source>
        <translation>Ressources du cluster</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="78"/>
        <source>CLUSTER INFO</source>
        <translation>INFORMATIONS SUR LE CLUSTER</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="125"/>
        <source>NETWORKING</source>
        <translation>RÉSEAU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="174"/>
        <source>NODES</source>
        <translation>NŒUDS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="228"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="248"/>
        <source>running / capacity</source>
        <translation>en cours d&apos;exécution / capacité</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="295"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="362"/>
        <source>MEMORY</source>
        <translation>MÉMOIRE</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="436"/>
        <source>NAMESPACES</source>
        <translation>NAMESPACES</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="490"/>
        <source>DEPLOYMENTS</source>
        <translation>DEPLOYMENTS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="544"/>
        <source>STATEFULSETS</source>
        <translation>STATEFULSETS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="598"/>
        <source>DAEMONSETS</source>
        <translation>DAEMONSETS</translation>
    </message>
</context>
<context>
    <name>PodsDialog</name>
    <message>
        <location filename="../ui/pods_dialog.ui" line="12"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="41"/>
        <source>NAME</source>
        <translation>NOM</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>PRÊTS</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>PHASE</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>CONTENEURS</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>ÂGE</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>Détails du Pod</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>Afficher les journaux</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>Fermer</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="3068"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>Donnez des noms plus simples à vos contextes. Laissez un nom vide pour conserver l&apos;original.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>Enregistrer les modifications</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>GÉNÉRAL</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="107"/>
        <source>Language</source>
        <translation>Langue</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="142"/>
        <source>Theme</source>
        <translation>Thème</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="177"/>
        <source>New theme...</source>
        <translation>Nouveau thème...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>Modifier le thème...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>Ouvrir le dossier des thèmes</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>Namespace par défaut</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>Le namespace sur lequel s&apos;ouvre chaque contexte. Laissez vide pour tous les afficher.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>Mémoriser le dernier contexte utilisé</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>Rechercher une nouvelle version sur GitHub au démarrage de l&apos;application</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>Interroge l&apos;API publique de GitHub pour connaître la dernière version et n&apos;envoie rien d&apos;autre que la version de l&apos;application. L&apos;icône du pied de page vérifie à la demande.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>Mode débogage : écrire un fichier journal que je peux partager</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>Ouvrir le dossier des journaux</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>Vider le cache</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>Oublie les listes et vues d&apos;ensemble déjà chargées ainsi que la connexion de chaque cluster : la prochaine requête se reconnecte et recharge tout. Vos paramètres sont conservés.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>FICHIERS KUBECONFIG</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>KubeScope lit les fichiers de la variable KUBECONFIG, ou ~/.kube/config. Ajoutez ici des fichiers pour lire ceux-là à la place. Cliquez sur Enregistrer pour appliquer.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>Ajouter un fichier...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>Retirer</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>COMMANDES DE CONNEXION</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>Pour un cloud que KubeScope ne connaît pas, indiquez le programme que votre kubeconfig utilise pour se connecter (par exemple oci) et la commande qui vous connecte (par exemple oci session authenticate). Le bouton Se connecter l&apos;exécute, sans shell. Cliquez sur Enregistrer pour appliquer.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>PROGRAMME</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>COMMANDE DE CONNEXION</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>Ajouter une ligne</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>NOMS DES CONTEXTES</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>CONTEXTE</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>NOM AFFICHÉ</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>Arrière-plan de la page</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>Panneaux et cartes</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>Panneaux alternés</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>Rails des barres</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>Bordures</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>Barre supérieure</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>Logo de la barre supérieure</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>Sélecteur de la barre supérieure</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>Bordure du sélecteur de la barre supérieure</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>Sélection de la barre supérieure</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>Texte de la barre supérieure</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>Texte</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>Titre de la barre latérale</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>Texte secondaire</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>Texte désactivé</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>Texte d&apos;accent et liens</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>Boutons d&apos;accent</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>Boutons d&apos;accent au survol</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>Boutons d&apos;accent désactivés</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>Focus et surbrillances</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>Texte du badge</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>Teinte d&apos;accent</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>Sélection du texte</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>Bordure d&apos;accent</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>Texte de la barre supérieure et des boutons d&apos;accent</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>Texte sain</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>Arrière-plan sain</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>Texte d&apos;avertissement</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>Arrière-plan d&apos;avertissement</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>Texte d&apos;échec</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>Arrière-plan d&apos;échec</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>Texte inactif</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>Arrière-plan inactif</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>Ligne avec un problème</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>Ligne d&apos;un Pod récent</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>Barre d&apos;utilisation, qui se remplit</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>Barre d&apos;utilisation, presque pleine</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>Barre de santé, sain</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>Barre de santé, avertissement</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>Barre de santé, échec</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>Nouveau thème</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>Modifier le thème : {name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>Nom du thème</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>Clair</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>Sombre</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>Nom</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>Basé sur</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>Couleurs</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>Enregistre dans un fichier ce que montre cet onglet</translation>
    </message>
</context>
<context>
    <name>WorkloadWindow</name>
    <message>
        <location filename="../window.py" line="706"/>
        <source>0 Deployments</source>
        <translation>0 Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="722"/>
        <location filename="../window.py" line="2299"/>
        <location filename="../window.py" line="2322"/>
        <location filename="../window.py" line="3306"/>
        <source>All namespaces</source>
        <translation>Tous les namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="832"/>
        <source>Loading contexts...</source>
        <translation>Chargement des contextes...</translation>
    </message>
    <message>
        <location filename="../window.py" line="841"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>Impossible de charger le kubeconfig : {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="863"/>
        <source>No contexts found in kubeconfig</source>
        <translation>Aucun contexte trouvé dans le kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="892"/>
        <location filename="../window.py" line="970"/>
        <source>Unpin from the top</source>
        <translation>Retirer du haut</translation>
    </message>
    <message>
        <location filename="../window.py" line="892"/>
        <source>Pin to the top</source>
        <translation>Épingler en haut</translation>
    </message>
    <message>
        <location filename="../window.py" line="1008"/>
        <source>Close</source>
        <translation>Fermer</translation>
    </message>
    <message>
        <location filename="../window.py" line="1055"/>
        <source>Status</source>
        <translation>Statut</translation>
    </message>
    <message>
        <location filename="../window.py" line="1056"/>
        <source>Kubernetes version</source>
        <translation>Version de Kubernetes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1057"/>
        <source>Platform version</source>
        <translation>Version de la plateforme</translation>
    </message>
    <message>
        <location filename="../window.py" line="1058"/>
        <source>Created</source>
        <translation>Créé</translation>
    </message>
    <message>
        <location filename="../window.py" line="1059"/>
        <source>Provider</source>
        <translation>Fournisseur</translation>
    </message>
    <message>
        <location filename="../window.py" line="1062"/>
        <source>API server endpoint</source>
        <translation>Point de terminaison du serveur d&apos;API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1063"/>
        <source>Cluster ARN</source>
        <translation>ARN du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1064"/>
        <source>Cluster IAM role ARN</source>
        <translation>ARN du rôle IAM du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1065"/>
        <source>OpenID Connect provider URL</source>
        <translation>URL du fournisseur OpenID Connect</translation>
    </message>
    <message>
        <location filename="../window.py" line="1073"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1074"/>
        <source>Cluster security group</source>
        <translation>Security group du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Additional security groups</source>
        <translation>Security groups supplémentaires</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>None</source>
        <translation>Aucun</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>API server endpoint access</source>
        <translation>Accès au endpoint du serveur d&apos;API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>Cluster IP address family</source>
        <translation>Famille d&apos;adresses IP du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Service IPv4 range</source>
        <translation>Plage IPv4 des services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1086"/>
        <source>Public access source allowlist</source>
        <translation>Liste d&apos;origines autorisées en accès public</translation>
    </message>
    <message>
        <location filename="../window.py" line="1089"/>
        <source>Subnets</source>
        <translation>Subnets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1100"/>
        <source>Creating</source>
        <translation>Création</translation>
    </message>
    <message>
        <location filename="../window.py" line="1101"/>
        <source>Updating</source>
        <translation>Mise à jour</translation>
    </message>
    <message>
        <location filename="../window.py" line="1102"/>
        <source>Deleting</source>
        <translation>Suppression</translation>
    </message>
    <message>
        <location filename="../window.py" line="1105"/>
        <source>Creation failed</source>
        <translation>Échec de la création</translation>
    </message>
    <message>
        <location filename="../window.py" line="1106"/>
        <source>Update failed</source>
        <translation>Échec de la mise à jour</translation>
    </message>
    <message>
        <location filename="../window.py" line="1107"/>
        <source>Deletion failed</source>
        <translation>Échec de la suppression</translation>
    </message>
    <message>
        <location filename="../window.py" line="1109"/>
        <source>Deployed</source>
        <translation>Déployé</translation>
    </message>
    <message>
        <location filename="../window.py" line="1110"/>
        <source>Superseded</source>
        <translation>Remplacé</translation>
    </message>
    <message>
        <location filename="../window.py" line="1111"/>
        <source>Uninstalled</source>
        <translation>Désinstallé</translation>
    </message>
    <message>
        <location filename="../window.py" line="1112"/>
        <source>Uninstalling</source>
        <translation>Désinstallation</translation>
    </message>
    <message>
        <location filename="../window.py" line="1113"/>
        <source>Pending install</source>
        <translation>Installation en attente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1114"/>
        <source>Pending upgrade</source>
        <translation>Mise à jour en attente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1115"/>
        <source>Pending rollback</source>
        <translation>Retour arrière en attente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1116"/>
        <source>Public</source>
        <translation>Public</translation>
    </message>
    <message>
        <location filename="../window.py" line="1117"/>
        <source>Private</source>
        <translation>Privé</translation>
    </message>
    <message>
        <location filename="../window.py" line="1118"/>
        <source>Public and private</source>
        <translation>Public et privé</translation>
    </message>
    <message>
        <location filename="../window.py" line="1210"/>
        <source>Overview</source>
        <translation>Vue d&apos;ensemble</translation>
    </message>
    <message>
        <location filename="../window.py" line="1211"/>
        <source>Cluster resources and capacity</source>
        <translation>Ressources et capacité du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1213"/>
        <source>Details &amp; Logs</source>
        <translation>Détails et journaux</translation>
    </message>
    <message>
        <location filename="../window.py" line="1215"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Détails de la ressource et journaux du Pod, un onglet chacun</translation>
    </message>
    <message>
        <location filename="../window.py" line="1218"/>
        <source>Settings</source>
        <translation>Paramètres</translation>
    </message>
    <message>
        <location filename="../window.py" line="1219"/>
        <source>Preferences and context names</source>
        <translation>Préférences et noms des contextes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1221"/>
        <source>Workloads overview</source>
        <translation>Vue d&apos;ensemble des workloads</translation>
    </message>
    <message>
        <location filename="../window.py" line="1223"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>Santé de chaque type de workload et derniers événements</translation>
    </message>
    <message>
        <location filename="../window.py" line="1227"/>
        <location filename="../window.py" line="1877"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="1227"/>
        <source>Pods of the cluster</source>
        <translation>Pods du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1229"/>
        <location filename="../window.py" line="1878"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="1230"/>
        <source>Deployments of the cluster</source>
        <translation>Deployments du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1233"/>
        <location filename="../window.py" line="1880"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1234"/>
        <source>StatefulSets of the cluster</source>
        <translation>StatefulSets du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1237"/>
        <location filename="../window.py" line="1879"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1238"/>
        <source>DaemonSets of the cluster</source>
        <translation>DaemonSets du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1241"/>
        <location filename="../window.py" line="1881"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1242"/>
        <source>ReplicaSets of the cluster</source>
        <translation>ReplicaSets du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1245"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1246"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>ReplicationControllers du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1248"/>
        <location filename="../window.py" line="1882"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1248"/>
        <source>Jobs of the cluster</source>
        <translation>Jobs du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1249"/>
        <location filename="../window.py" line="1883"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1249"/>
        <source>CronJobs of the cluster</source>
        <translation>CronJobs du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1250"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1250"/>
        <source>Services of the cluster</source>
        <translation>Services du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1252"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1253"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>Endpoint Slices du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1256"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1257"/>
        <source>Endpoints of the cluster</source>
        <translation>Endpoints du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1260"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1261"/>
        <source>Ingresses of the cluster</source>
        <translation>Ingresses du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1264"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1265"/>
        <source>Ingress Classes of the cluster</source>
        <translation>Ingress Classes du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1269"/>
        <source>Network Policies of the cluster</source>
        <translation>Network Policies du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1273"/>
        <source>Config Maps of the cluster</source>
        <translation>Config Maps du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1276"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1277"/>
        <source>Secrets of the cluster</source>
        <translation>Secrets du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1280"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1281"/>
        <source>Resource Quotas of the cluster</source>
        <translation>Resource Quotas du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1284"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1285"/>
        <source>Limit Ranges of the cluster</source>
        <translation>Limit Ranges du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1288"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1289"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>Horizontal Pod Autoscalers du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1292"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1293"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>Pod Disruption Budgets du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1296"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1297"/>
        <source>Priority Classes of the cluster</source>
        <translation>Priority Classes du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1300"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1301"/>
        <source>Runtime Classes of the cluster</source>
        <translation>Runtime Classes du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1304"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1305"/>
        <source>Leases of the cluster</source>
        <translation>Leases du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1308"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1309"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>Mutating Webhook Configurations du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1312"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1313"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>Validating Webhook Configurations du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1316"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1317"/>
        <source>Node Groups of the cluster</source>
        <translation>Node Groups du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1320"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1321"/>
        <source>Add-ons of the cluster</source>
        <translation>Add-ons du cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Version {version}</source>
        <translation>Version {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1333"/>
        <source>Open the project on GitHub</source>
        <translation>Ouvrir le projet sur GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="1367"/>
        <source>Up to date</source>
        <translation>À jour</translation>
    </message>
    <message>
        <location filename="../window.py" line="1368"/>
        <source>Could not check</source>
        <translation>Vérification impossible</translation>
    </message>
    <message>
        <location filename="../window.py" line="1379"/>
        <source>Check for updates</source>
        <translation>Rechercher des mises à jour</translation>
    </message>
    <message>
        <location filename="../window.py" line="1380"/>
        <source>Checking for updates...</source>
        <translation>Recherche de mises à jour...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1381"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope est à jour. Cliquez pour vérifier à nouveau.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1382"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>Impossible de rechercher des mises à jour. Cliquez pour réessayer.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1388"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>Mise à jour disponible : {version}. Cliquez pour ouvrir la page de téléchargement ; clic droit pour vérifier à nouveau.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1396"/>
        <source>Update available</source>
        <translation>Mise à jour disponible</translation>
    </message>
    <message>
        <location filename="../window.py" line="1398"/>
        <source>Download KubeScope {version}</source>
        <translation>Télécharger KubeScope {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1434"/>
        <source>Check for updates again</source>
        <translation>Rechercher à nouveau des mises à jour</translation>
    </message>
    <message>
        <location filename="../window.py" line="1531"/>
        <location filename="../window.py" line="2206"/>
        <source>Loading resources...</source>
        <translation>Chargement des ressources...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1775"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Configurer les identifiants AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1779"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>Les identifiants AWS du profil {profile} sont manquants ou invalides</translation>
    </message>
    <message>
        <location filename="../window.py" line="1784"/>
        <source>Sign in to {provider}</source>
        <translation>Se connecter à {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1787"/>
        <source>Not signed in to {provider}</source>
        <translation>Non connecté à {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1791"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>Se connecter à {provider} ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1797"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>Non connecté à {provider} (profil {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1818"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Terminez dans le terminal qui s&apos;est ouvert, puis cliquez sur Actualiser.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1837"/>
        <source>Loading workloads...</source>
        <translation>Chargement des workloads...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1898"/>
        <source>Could not read: {names}</source>
        <translation>Lecture impossible : {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1958"/>
        <source>Loading cluster data...</source>
        <translation>Chargement des données du cluster...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2039"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>en cours d&apos;exécution · {pending} en attente · {failed} en échec</translation>
    </message>
    <message>
        <location filename="../window.py" line="2048"/>
        <location filename="../window.py" line="2062"/>
        <source> · usage {value}</source>
        <translation> · utilisation {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2111"/>
        <source>Ready</source>
        <translation>Prêt</translation>
    </message>
    <message>
        <location filename="../window.py" line="2111"/>
        <source>Not ready</source>
        <translation>Non prêt</translation>
    </message>
    <message>
        <location filename="../window.py" line="2086"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Utilisation réelle indisponible : metrics-server introuvable.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2223"/>
        <source>Refreshing...</source>
        <translation>Actualisation...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2414"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{count} Services dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2416"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{count} Endpoint Slices dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2419"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{count} Endpoints dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2422"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{count} Ingresses dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2424"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>{count} Ingress Classes dans le cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2426"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{count} Network Policies dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2429"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>{count} Config Maps dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2431"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>{count} Secrets dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2433"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>{count} Resource Quotas dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2436"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>{count} Limit Ranges dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2439"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>{count} Horizontal Pod Autoscalers dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2442"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>{count} Pod Disruption Budgets dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2444"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>{count} Leases dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2446"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>{count} Priority Classes dans le cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2448"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>{count} Runtime Classes dans le cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2450"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>{count} Mutating Webhook Configurations dans le cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2453"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>{count} Validating Webhook Configurations dans le cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2455"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>{count} Node Groups dans le cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2456"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>{count} Add-ons dans le cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2467"/>
        <location filename="../window.py" line="2533"/>
        <source>Running</source>
        <translation>En cours d&apos;exécution</translation>
    </message>
    <message>
        <location filename="../window.py" line="1108"/>
        <location filename="../window.py" line="2468"/>
        <location filename="../window.py" line="2529"/>
        <source>Pending</source>
        <translation>En attente</translation>
    </message>
    <message>
        <location filename="../window.py" line="2469"/>
        <source>Succeeded</source>
        <translation>Réussi</translation>
    </message>
    <message>
        <location filename="../window.py" line="1104"/>
        <location filename="../window.py" line="2470"/>
        <location filename="../window.py" line="2528"/>
        <source>Failed</source>
        <translation>Échoué</translation>
    </message>
    <message>
        <location filename="../window.py" line="2471"/>
        <source>Unknown</source>
        <translation>Inconnu</translation>
    </message>
    <message>
        <location filename="../window.py" line="2515"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pods dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2523"/>
        <source>Healthy</source>
        <translation>Sain</translation>
    </message>
    <message>
        <location filename="../window.py" line="1103"/>
        <location filename="../window.py" line="2524"/>
        <source>Degraded</source>
        <translation>Dégradé</translation>
    </message>
    <message>
        <location filename="../window.py" line="2525"/>
        <source>Unavailable</source>
        <translation>Indisponible</translation>
    </message>
    <message>
        <location filename="../window.py" line="2526"/>
        <source>Scaled to zero</source>
        <translation>Réduit à zéro</translation>
    </message>
    <message>
        <location filename="../window.py" line="2527"/>
        <source>Complete</source>
        <translation>Terminé</translation>
    </message>
    <message>
        <location filename="../window.py" line="2530"/>
        <source>Suspended</source>
        <translation>Suspendu</translation>
    </message>
    <message>
        <location filename="../window.py" line="1099"/>
        <location filename="../window.py" line="2531"/>
        <source>Active</source>
        <translation>Actif</translation>
    </message>
    <message>
        <location filename="../window.py" line="2532"/>
        <source>Scheduled</source>
        <translation>Planifié</translation>
    </message>
    <message>
        <location filename="../window.py" line="2577"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployments dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2580"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{count} StatefulSets dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2583"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{count} DaemonSets dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2586"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{count} ReplicaSets dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2589"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{count} ReplicationControllers dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2591"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{count} Jobs dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2592"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{count} CronJobs dans {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2616"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} sur {total} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2617"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} sur {total} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2618"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{visible} sur {total} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2619"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{visible} sur {total} DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2620"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{visible} sur {total} ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2622"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{visible} sur {total} ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2624"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{visible} sur {total} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2625"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{visible} sur {total} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2626"/>
        <source>{visible} of {total} Services</source>
        <translation>{visible} sur {total} Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="2627"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{visible} sur {total} Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="2628"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{visible} sur {total} Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="2629"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{visible} sur {total} Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="2630"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{visible} sur {total} Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2631"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{visible} sur {total} Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="2632"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>{visible} sur {total} Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="2633"/>
        <source>{visible} of {total} Secrets</source>
        <translation>{visible} sur {total} Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2634"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>{visible} sur {total} Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="2635"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>{visible} sur {total} Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="2637"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>{visible} sur {total} Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2640"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>{visible} sur {total} Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2642"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>{visible} sur {total} Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2643"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>{visible} sur {total} Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2644"/>
        <source>{visible} of {total} Leases</source>
        <translation>{visible} sur {total} Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="2646"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>{visible} sur {total} Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2649"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>{visible} sur {total} Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2651"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>{visible} sur {total} Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="2652"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>{visible} sur {total} Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="2698"/>
        <source>Loading...</source>
        <translation>Chargement...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2744"/>
        <location filename="../window.py" line="2836"/>
        <source>Pod: {name}</source>
        <translation>Pod : {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2790"/>
        <source>Pods of {name}</source>
        <translation>Pods de {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2792"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods dans {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2857"/>
        <source>No Pods are associated with this workload</source>
        <translation>Aucun Pod n&apos;est associé à ce workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="2864"/>
        <location filename="../window.py" line="2887"/>
        <source>Logs</source>
        <translation>Journaux</translation>
    </message>
    <message>
        <location filename="../window.py" line="2864"/>
        <source>This workload has no Pods.</source>
        <translation>Ce workload n&apos;a aucun Pod.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2873"/>
        <location filename="../window.py" line="2896"/>
        <source>View logs</source>
        <translation>Afficher les journaux</translation>
    </message>
    <message>
        <location filename="../window.py" line="2874"/>
        <source>Select the Pod:</source>
        <translation>Sélectionnez le Pod :</translation>
    </message>
    <message>
        <location filename="../window.py" line="2888"/>
        <source>Pod {name} has no containers.</source>
        <translation>Le Pod {name} n&apos;a aucun conteneur.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2897"/>
        <source>Select the container of {name}:</source>
        <translation>Sélectionnez le conteneur de {name} :</translation>
    </message>
    <message>
        <location filename="../window.py" line="2923"/>
        <source>Save to a file</source>
        <translation>Enregistrer dans un fichier</translation>
    </message>
    <message>
        <location filename="../window.py" line="2934"/>
        <source>Could not save</source>
        <translation>Enregistrement impossible</translation>
    </message>
    <message>
        <location filename="../window.py" line="2935"/>
        <source>The file could not be written: {reason}</source>
        <translation>Le fichier n&apos;a pas pu être écrit : {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2981"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Journaux : {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3031"/>
        <source>Automatic</source>
        <translation>Automatique</translation>
    </message>
    <message>
        <location filename="../window.py" line="3044"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>Désactivé par défaut. Lorsqu&apos;il est activé, KubeScope écrit ce qu&apos;il fait, jamais les journaux des Pods ni le contenu des ressources, dans {path}. Relisez-le avant de le partager : il contient les noms des contextes.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3075"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>Aucun contexte trouvé dans le kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3104"/>
        <source>Choose a kubeconfig file</source>
        <translation>Choisissez un fichier kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="3150"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>La commande de connexion de la ligne {row} n&apos;est pas valide.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3163"/>
        <source>Light</source>
        <translation>Clair</translation>
    </message>
    <message>
        <location filename="../window.py" line="3163"/>
        <source>Dark</source>
        <translation>Sombre</translation>
    </message>
    <message>
        <location filename="../window.py" line="3182"/>
        <source>My theme</source>
        <translation>Mon thème</translation>
    </message>
    <message>
        <location filename="../window.py" line="3226"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>Cache vidé. Tout est rechargé la prochaine fois que c&apos;est nécessaire.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3281"/>
        <source>Settings saved.</source>
        <translation>Paramètres enregistrés.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3320"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>Votre utilisateur n&apos;est pas autorisé à effectuer cette action ({action}). Demandez l&apos;accès à l&apos;administrateur de votre cluster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3325"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>Votre utilisateur n&apos;est pas autorisé à faire cela. Demandez l&apos;accès à l&apos;administrateur de votre cluster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3344"/>
        <source>Query failed</source>
        <translation>Échec de la requête</translation>
    </message>
</context>
<context>
    <name>WorkloadsOverviewPage</name>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="29"/>
        <source>Workloads</source>
        <translation>Workloads</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="78"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="100"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="122"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="144"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="166"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="188"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="210"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="258"/>
        <source>Events</source>
        <translation>Événements</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="293"/>
        <source>TYPE</source>
        <translation>TYPE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="298"/>
        <source>SOURCE</source>
        <translation>SOURCE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>INVOLVED OBJECT</source>
        <translation>OBJET CONCERNÉ</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>MESSAGE</source>
        <translation>MESSAGE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>COUNT</source>
        <translation>NOMBRE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>AGE</source>
        <translation>ÂGE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>LAST SEEN</source>
        <translation>DERNIÈRE FOIS</translation>
    </message>
</context>
</TS>
