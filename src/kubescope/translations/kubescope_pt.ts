<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="pt_BR">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>Ferramenta de login não encontrada</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>Seu kubeconfig executa “{tool}” para autenticar, mas ela não está instalada ou não está no PATH. Instale-a e atualize.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>Contexto não encontrado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>Este contexto não está no seu kubeconfig. Verifique o ~/.kube/config.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>Falha na autenticação</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>Suas credenciais podem ter expirado. Faça login novamente (por exemplo com “aws sso login”, “gcloud auth login” ou “az login”) e atualize.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Not an Amazon EKS cluster</source>
        <translation>Não é um cluster Amazon EKS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Node Groups, Add-ons and the AWS cards of the Overview exist only on Amazon EKS contexts.</source>
        <translation>Node Groups, Add-ons e os cards da AWS na Visão geral existem apenas em contextos Amazon EKS.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="110"/>
        <source>Unexpected answer from AWS</source>
        <translation>Resposta inesperada da AWS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="111"/>
        <source>Update the AWS CLI to its latest version and refresh.</source>
        <translation>Atualize a AWS CLI para a versão mais recente e recarregue.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="118"/>
        <location filename="../errors.py" line="128"/>
        <source>Access denied</source>
        <translation>Acesso negado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="119"/>
        <source>Your AWS identity is not allowed to read this. The wiki lists the eks: permissions KubeScope needs.</source>
        <translation>Sua identidade da AWS não tem permissão para ler isto. A wiki lista as permissões eks: que o KubeScope precisa.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>Seu usuário não tem permissão para ler este recurso.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="143"/>
        <source>No network connection</source>
        <translation>Sem conexão de rede</translation>
    </message>
    <message>
        <location filename="../errors.py" line="144"/>
        <source>Check your internet connection or VPN and refresh.</source>
        <translation>Verifique sua conexão com a internet ou VPN e atualize.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="165"/>
        <source>Cluster unreachable</source>
        <translation>Cluster inacessível</translation>
    </message>
    <message>
        <location filename="../errors.py" line="166"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>Verifique sua rede ou VPN e se o cluster está em execução.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="172"/>
        <source>Something went wrong</source>
        <translation>Algo deu errado</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>Atualizar automaticamente</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>Busca novas linhas de log a cada poucos segundos e acompanha o fim do log</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>Atualizar agora</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="46"/>
        <source>No log lines returned.</source>
        <translation>Nenhuma linha de log retornada.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="51"/>
        <source>Updated at {time}</source>
        <translation>Atualizado às {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="58"/>
        <source>Could not refresh logs: {message}</source>
        <translation>Não foi possível atualizar os logs: {message}</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../ui/main_window.ui" line="20"/>
        <location filename="../ui/main_window.ui" line="283"/>
        <source>KubeScope</source>
        <translation>KubeScope</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="339"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>Contexto do Kubernetes do seu kubeconfig</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="437"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>Nenhum contexto de cluster foi encontrado no seu kubeconfig. Adicione um cluster ao kubeconfig (por exemplo, com a AWS CLI: aws eks update-kubeconfig) e recarregue.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="293"/>
        <source>Kubernetes console</source>
        <translation>Console Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="372"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>Faça login com a CLI da nuvem e recarregue os dados do cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="375"/>
        <source>Sign in</source>
        <translation>Entrar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="478"/>
        <source>Dismiss</source>
        <translation>Dispensar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="569"/>
        <source>MONITORING</source>
        <translation>MONITORAMENTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1714"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
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
        <translation>Rede</translation>
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
        <translation>Configuração</translation>
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
        <location filename="../ui/main_window.ui" line="397"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <source>Cluster</source>
        <translation>Cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1665"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>ACESSO SEGURO
Recursos em modo somente leitura</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1721"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2507"/>
        <source>Nodes</source>
        <translation>Nós</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2542"/>
        <source>NODE</source>
        <translation>NÓ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2552"/>
        <source>ROLE</source>
        <translation>FUNÇÃO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2572"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2613"/>
        <source>Data fetched from the cluster API</source>
        <translation>Dados consultados na API do cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2674"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>Abrir o site da DCO Tecnologia</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2694"/>
        <source>MIT License</source>
        <translation>Licença MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2733"/>
        <source>Update available</source>
        <translation>Atualização disponível</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2736"/>
        <source>Open the download page of the new version</source>
        <translation>Abrir a página de download da nova versão</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Check for updates</source>
        <translation>Verificar atualizações</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2784"/>
        <source>Open the project on GitHub</source>
        <translation>Abrir o projeto no GitHub</translation>
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
        <location filename="../ui/main_window.ui" line="1878"/>
        <source>Search by name or namespace...</source>
        <translation>Buscar por nome ou namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1746"/>
        <location filename="../ui/main_window.ui" line="1759"/>
        <location filename="../ui/main_window.ui" line="1772"/>
        <source>Refresh</source>
        <translation>Atualizar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1929"/>
        <source>View Pods of the selected workload</source>
        <translation>Ver Pods do workload selecionado</translation>
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
        <location filename="../ui/main_window.ui" line="1945"/>
        <source>View JSON details of the selected workload</source>
        <translation>Ver os detalhes JSON do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1948"/>
        <source>Details</source>
        <translation>Detalhes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1961"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Ver logs de um Pod do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1964"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1649"/>
        <location filename="../ui/main_window.ui" line="2008"/>
        <source>KIND</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1634"/>
        <location filename="../window.py" line="1650"/>
        <location filename="../ui/main_window.ui" line="2013"/>
        <source>NAME</source>
        <translation>NOME</translation>
    </message>
    <message>
        <location filename="../window.py" line="1627"/>
        <location filename="../ui/main_window.ui" line="2018"/>
        <source>READY</source>
        <translation>PRONTOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1625"/>
        <source>COMPLETIONS</source>
        <translation>CONCLUSÕES</translation>
    </message>
    <message>
        <location filename="../window.py" line="1540"/>
        <location filename="../window.py" line="1569"/>
        <source>TYPE</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1541"/>
        <source>CLUSTER IP</source>
        <translation>CLUSTER IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1542"/>
        <source>EXTERNAL IP</source>
        <translation>IP EXTERNO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1543"/>
        <location filename="../window.py" line="1547"/>
        <location filename="../window.py" line="1555"/>
        <source>PORTS</source>
        <translation>PORTAS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1546"/>
        <source>ADDRESS TYPE</source>
        <translation>TIPO DE ENDEREÇO</translation>
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
        <translation>HOSTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1554"/>
        <source>ADDRESS</source>
        <translation>ENDEREÇO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1558"/>
        <source>CONTROLLER</source>
        <translation>CONTROLADOR</translation>
    </message>
    <message>
        <location filename="../window.py" line="1559"/>
        <source>PARAMETERS</source>
        <translation>PARÂMETROS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1562"/>
        <source>POD SELECTOR</source>
        <translation>SELETOR DE POD</translation>
    </message>
    <message>
        <location filename="../window.py" line="1563"/>
        <source>POLICY TYPES</source>
        <translation>TIPOS DE POLÍTICA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1566"/>
        <location filename="../window.py" line="1570"/>
        <source>DATA</source>
        <translation>DADOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1573"/>
        <source>USAGE</source>
        <translation>USO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>TYPES</source>
        <translation>TIPOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1579"/>
        <source>REFERENCE</source>
        <translation>REFERÊNCIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1580"/>
        <source>MIN PODS</source>
        <translation>MÍN. PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1581"/>
        <source>MAX PODS</source>
        <translation>MÁX. PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1582"/>
        <source>REPLICAS</source>
        <translation>RÉPLICAS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1585"/>
        <source>MIN AVAILABLE</source>
        <translation>MÍN. DISPONÍVEL</translation>
    </message>
    <message>
        <location filename="../window.py" line="1586"/>
        <source>MAX UNAVAILABLE</source>
        <translation>MÁX. INDISPONÍVEL</translation>
    </message>
    <message>
        <location filename="../window.py" line="1587"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>INTERRUPÇÕES PERMITIDAS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1590"/>
        <source>VALUE</source>
        <translation>VALOR</translation>
    </message>
    <message>
        <location filename="../window.py" line="1591"/>
        <source>GLOBAL DEFAULT</source>
        <translation>PADRÃO GLOBAL</translation>
    </message>
    <message>
        <location filename="../window.py" line="1594"/>
        <source>HANDLER</source>
        <translation>HANDLER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1597"/>
        <source>HOLDER</source>
        <translation>TITULAR</translation>
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
        <translation>TIPOS DE INSTÂNCIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <source>NODES</source>
        <translation>NÓS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1609"/>
        <source>AMI TYPE</source>
        <translation>TIPO DE AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1610"/>
        <source>AMI VERSION</source>
        <translation>VERSÃO DA AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1614"/>
        <location filename="../ui/main_window.ui" line="2557"/>
        <source>VERSION</source>
        <translation>VERSÃO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1615"/>
        <source>SOURCE</source>
        <translation>ORIGEM</translation>
    </message>
    <message>
        <location filename="../window.py" line="1626"/>
        <source>SCHEDULE</source>
        <translation>AGENDA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1606"/>
        <location filename="../window.py" line="1613"/>
        <location filename="../window.py" line="1636"/>
        <location filename="../ui/main_window.ui" line="2023"/>
        <location filename="../ui/main_window.ui" line="2547"/>
        <source>STATUS</source>
        <translation>STATUS</translation>
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
        <translation>MEMÓRIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1639"/>
        <source>RESTARTS</source>
        <translation>REINÍCIOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1640"/>
        <location filename="../window.py" line="1652"/>
        <location filename="../ui/main_window.ui" line="2028"/>
        <location filename="../ui/main_window.ui" line="2577"/>
        <source>AGE</source>
        <translation>IDADE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2590"/>
        <source>Select a context to load workloads</source>
        <translation>Selecione um contexto para carregar os workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2697"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>O KubeScope é software de código aberto, distribuído sob a Licença MIT</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="2030"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>nós prontos</translation>
    </message>
    <message>
        <location filename="../window.py" line="2046"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>cores requisitados / alocáveis</translation>
    </message>
    <message>
        <location filename="../window.py" line="2060"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>requisitada / alocável</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>no cluster</translation>
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
        <translation>Recursos do cluster</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="78"/>
        <source>CLUSTER INFO</source>
        <translation>INFORMAÇÕES DO CLUSTER</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="125"/>
        <source>NETWORKING</source>
        <translation>REDE</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="174"/>
        <source>NODES</source>
        <translation>NÓS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="228"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="248"/>
        <source>running / capacity</source>
        <translation>em execução / capacidade</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="295"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="362"/>
        <source>MEMORY</source>
        <translation>MEMÓRIA</translation>
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
        <translation>NOME</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>PRONTOS</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>FASE</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>CONTAINERS</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>IDADE</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>Detalhes do Pod</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>Ver logs</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>Fechar</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="3068"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>Dê nomes mais amigáveis aos seus contextos. Deixe o nome vazio para manter o original.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>Salvar alterações</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>GERAL</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="107"/>
        <source>Language</source>
        <translation>Idioma</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="142"/>
        <source>Theme</source>
        <translation>Tema</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="177"/>
        <source>New theme...</source>
        <translation>Novo tema...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>Editar tema...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>Abrir a pasta de temas</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>Namespace padrão</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>O namespace em que cada contexto abre. Deixe vazio para mostrar todos.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>Lembrar o último contexto usado</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>Procurar uma nova versão no GitHub ao abrir o app</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>Consulta a API pública do GitHub pela última versão e envia apenas a versão do app. O ícone do rodapé verifica sob demanda.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>Modo debug: gravar um arquivo de log que eu possa compartilhar</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>Abrir a pasta de logs</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>Limpar o cache</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>Esquece as listas e visões gerais já carregadas e o login de cada cluster; a próxima requisição entra de novo e carrega tudo outra vez. Suas configurações são mantidas.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>ARQUIVOS KUBECONFIG</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>O KubeScope lê os arquivos da variável KUBECONFIG, ou ~/.kube/config. Adicione arquivos aqui para ler esses no lugar. Clique em Salvar para aplicar.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>Adicionar arquivo...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>Remover</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>COMANDOS DE LOGIN</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>Para uma nuvem que o KubeScope não conhece, informe o programa que seu kubeconfig usa para entrar (por exemplo oci) e o comando que faz o login (por exemplo oci session authenticate). O botão de login o executa, sem shell. Clique em Salvar para aplicar.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>PROGRAMA</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>COMANDO DE LOGIN</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>Adicionar linha</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>NOMES DOS CONTEXTOS</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>NOME EXIBIDO</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>Fundo da página</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>Painéis e cartões</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>Painéis alternados</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>Trilhas das barras</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>Bordas</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>Barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>Logo da barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>Seletor da barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>Borda do seletor da barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>Seleção na barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>Texto da barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>Texto</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>Título da barra lateral</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>Texto secundário</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>Texto desabilitado</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>Texto de destaque e links</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>Botões de destaque</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>Botões de destaque ao passar o mouse</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>Botões de destaque desabilitados</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>Foco e realces</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>Texto do selo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>Tom de destaque</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>Seleção de texto</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>Borda de destaque</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>Texto na barra superior e nos botões de destaque</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>Texto saudável</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>Fundo saudável</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>Texto de aviso</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>Fundo de aviso</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>Texto com falha</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>Fundo com falha</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>Texto ocioso</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>Fundo ocioso</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>Linha com problema</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>Linha de um Pod novo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>Barra de uso, ficando cheia</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>Barra de uso, quase cheia</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>Barra de saúde, saudável</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>Barra de saúde, aviso</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>Barra de saúde, com falha</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>Novo tema</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>Editar tema: {name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>Nome do tema</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>Claro</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>Escuro</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>Nome</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>Parte de</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>Cores</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>Salvar em um arquivo o que esta aba mostra</translation>
    </message>
</context>
<context>
    <name>WorkloadWindow</name>
    <message>
        <location filename="../window.py" line="722"/>
        <location filename="../window.py" line="2299"/>
        <location filename="../window.py" line="2322"/>
        <location filename="../window.py" line="3306"/>
        <source>All namespaces</source>
        <translation>Todos os namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="832"/>
        <source>Loading contexts...</source>
        <translation>Carregando contextos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="841"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>Não foi possível carregar o kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="863"/>
        <source>No contexts found in kubeconfig</source>
        <translation>Nenhum contexto encontrado no kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="1210"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
    </message>
    <message>
        <location filename="../window.py" line="1211"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1213"/>
        <source>Details &amp; Logs</source>
        <translation>Detalhes e Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1215"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Detalhes de recursos e logs de Pods, uma aba para cada</translation>
    </message>
    <message>
        <location filename="../window.py" line="1218"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../window.py" line="1219"/>
        <source>Preferences and context names</source>
        <translation>Preferências e nomes dos contextos</translation>
    </message>
    <message>
        <location filename="../window.py" line="1221"/>
        <source>Workloads overview</source>
        <translation>Visão geral das cargas de trabalho</translation>
    </message>
    <message>
        <location filename="../window.py" line="1223"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>Saúde de cada tipo de carga e os eventos mais recentes</translation>
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
        <translation>StatefulSets do cluster</translation>
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
        <translation>Jobs do cluster</translation>
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
        <translation>CronJobs do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Version {version}</source>
        <translation>Versão {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1333"/>
        <source>Open the project on GitHub</source>
        <translation>Abrir o projeto no GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="1837"/>
        <source>Loading workloads...</source>
        <translation>Carregando cargas de trabalho...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1237"/>
        <location filename="../window.py" line="1879"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1241"/>
        <location filename="../window.py" line="1881"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1898"/>
        <source>Could not read: {names}</source>
        <translation>Não foi possível ler: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1958"/>
        <source>Loading cluster data...</source>
        <translation>Carregando dados do cluster...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2039"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>em execução · {pending} pendentes · {failed} com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="2048"/>
        <location filename="../window.py" line="2062"/>
        <source> · usage {value}</source>
        <translation> · uso {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2111"/>
        <source>Ready</source>
        <translation>Pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="2111"/>
        <source>Not ready</source>
        <translation>Não pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="2086"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Uso real indisponível: metrics-server não encontrado.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1531"/>
        <location filename="../window.py" line="2206"/>
        <source>Loading resources...</source>
        <translation>Carregando recursos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1367"/>
        <source>Up to date</source>
        <translation>Atualizado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1368"/>
        <source>Could not check</source>
        <translation>Não foi possível verificar</translation>
    </message>
    <message>
        <location filename="../window.py" line="1388"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>Atualização disponível: {version}. Clique para abrir a página de download; clique com o botão direito para verificar de novo.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1784"/>
        <source>Sign in to {provider}</source>
        <translation>Entrar no {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1787"/>
        <source>Not signed in to {provider}</source>
        <translation>Sem login no {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1791"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>Entrar no {provider} ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1797"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>Sem login no {provider} (perfil {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="2223"/>
        <source>Refreshing...</source>
        <translation>Atualizando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2467"/>
        <location filename="../window.py" line="2533"/>
        <source>Running</source>
        <translation>Em execução</translation>
    </message>
    <message>
        <location filename="../window.py" line="1108"/>
        <location filename="../window.py" line="2468"/>
        <location filename="../window.py" line="2529"/>
        <source>Pending</source>
        <translation>Pendente</translation>
    </message>
    <message>
        <location filename="../window.py" line="2469"/>
        <source>Succeeded</source>
        <translation>Concluído</translation>
    </message>
    <message>
        <location filename="../window.py" line="1104"/>
        <location filename="../window.py" line="2470"/>
        <location filename="../window.py" line="2528"/>
        <source>Failed</source>
        <translation>Com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="2471"/>
        <source>Unknown</source>
        <translation>Desconhecido</translation>
    </message>
    <message>
        <location filename="../window.py" line="2523"/>
        <source>Healthy</source>
        <translation>Saudável</translation>
    </message>
    <message>
        <location filename="../window.py" line="1103"/>
        <location filename="../window.py" line="2524"/>
        <source>Degraded</source>
        <translation>Degradado</translation>
    </message>
    <message>
        <location filename="../window.py" line="2525"/>
        <source>Unavailable</source>
        <translation>Indisponível</translation>
    </message>
    <message>
        <location filename="../window.py" line="2526"/>
        <source>Scaled to zero</source>
        <translation>Zero réplicas</translation>
    </message>
    <message>
        <location filename="../window.py" line="2527"/>
        <source>Complete</source>
        <translation>Concluído</translation>
    </message>
    <message>
        <location filename="../window.py" line="2530"/>
        <source>Suspended</source>
        <translation>Suspenso</translation>
    </message>
    <message>
        <location filename="../window.py" line="1099"/>
        <location filename="../window.py" line="2531"/>
        <source>Active</source>
        <translation>Ativo</translation>
    </message>
    <message>
        <location filename="../window.py" line="2532"/>
        <source>Scheduled</source>
        <translation>Agendado</translation>
    </message>
    <message>
        <location filename="../window.py" line="2580"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{count} StatefulSets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2591"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{count} Jobs em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2592"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{count} CronJobs em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2618"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{visible} de {total} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2624"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{visible} de {total} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2625"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{visible} de {total} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2698"/>
        <source>Loading...</source>
        <translation>Carregando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2790"/>
        <source>Pods of {name}</source>
        <translation>Pods de {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2792"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods em {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2744"/>
        <location filename="../window.py" line="2836"/>
        <source>Pod: {name}</source>
        <translation>Pod: {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="706"/>
        <source>0 Deployments</source>
        <translation>0 Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="892"/>
        <location filename="../window.py" line="970"/>
        <source>Unpin from the top</source>
        <translation>Desafixar do topo</translation>
    </message>
    <message>
        <location filename="../window.py" line="892"/>
        <source>Pin to the top</source>
        <translation>Fixar no topo</translation>
    </message>
    <message>
        <location filename="../window.py" line="1008"/>
        <source>Close</source>
        <translation>Fechar</translation>
    </message>
    <message>
        <location filename="../window.py" line="1055"/>
        <source>Status</source>
        <translation>Status</translation>
    </message>
    <message>
        <location filename="../window.py" line="1056"/>
        <source>Kubernetes version</source>
        <translation>Versão do Kubernetes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1057"/>
        <source>Platform version</source>
        <translation>Versão da plataforma</translation>
    </message>
    <message>
        <location filename="../window.py" line="1058"/>
        <source>Created</source>
        <translation>Criado em</translation>
    </message>
    <message>
        <location filename="../window.py" line="1059"/>
        <source>Provider</source>
        <translation>Provedor</translation>
    </message>
    <message>
        <location filename="../window.py" line="1062"/>
        <source>API server endpoint</source>
        <translation>Endpoint do servidor da API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1063"/>
        <source>Cluster ARN</source>
        <translation>ARN do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1064"/>
        <source>Cluster IAM role ARN</source>
        <translation>ARN da role IAM do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1065"/>
        <source>OpenID Connect provider URL</source>
        <translation>URL do provedor OpenID Connect</translation>
    </message>
    <message>
        <location filename="../window.py" line="1073"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1074"/>
        <source>Cluster security group</source>
        <translation>Security group do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Additional security groups</source>
        <translation>Security groups adicionais</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>None</source>
        <translation>Nenhum</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>API server endpoint access</source>
        <translation>Acesso ao endpoint do servidor da API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>Cluster IP address family</source>
        <translation>Família de endereços IP do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Service IPv4 range</source>
        <translation>Faixa IPv4 dos serviços</translation>
    </message>
    <message>
        <location filename="../window.py" line="1086"/>
        <source>Public access source allowlist</source>
        <translation>Lista de origens com acesso público</translation>
    </message>
    <message>
        <location filename="../window.py" line="1089"/>
        <source>Subnets</source>
        <translation>Subnets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1100"/>
        <source>Creating</source>
        <translation>Criando</translation>
    </message>
    <message>
        <location filename="../window.py" line="1101"/>
        <source>Updating</source>
        <translation>Atualizando</translation>
    </message>
    <message>
        <location filename="../window.py" line="1102"/>
        <source>Deleting</source>
        <translation>Excluindo</translation>
    </message>
    <message>
        <location filename="../window.py" line="1105"/>
        <source>Creation failed</source>
        <translation>Falha na criação</translation>
    </message>
    <message>
        <location filename="../window.py" line="1106"/>
        <source>Update failed</source>
        <translation>Falha na atualização</translation>
    </message>
    <message>
        <location filename="../window.py" line="1107"/>
        <source>Deletion failed</source>
        <translation>Falha na exclusão</translation>
    </message>
    <message>
        <location filename="../window.py" line="1109"/>
        <source>Deployed</source>
        <translation>Implantado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1110"/>
        <source>Superseded</source>
        <translation>Substituído</translation>
    </message>
    <message>
        <location filename="../window.py" line="1111"/>
        <source>Uninstalled</source>
        <translation>Desinstalado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1112"/>
        <source>Uninstalling</source>
        <translation>Desinstalando</translation>
    </message>
    <message>
        <location filename="../window.py" line="1113"/>
        <source>Pending install</source>
        <translation>Instalação pendente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1114"/>
        <source>Pending upgrade</source>
        <translation>Atualização pendente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1115"/>
        <source>Pending rollback</source>
        <translation>Reversão pendente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1116"/>
        <source>Public</source>
        <translation>Público</translation>
    </message>
    <message>
        <location filename="../window.py" line="1117"/>
        <source>Private</source>
        <translation>Privado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1118"/>
        <source>Public and private</source>
        <translation>Público e privado</translation>
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
        <translation>Pods do cluster</translation>
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
        <translation>Deployments do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1238"/>
        <source>DaemonSets of the cluster</source>
        <translation>DaemonSets do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1242"/>
        <source>ReplicaSets of the cluster</source>
        <translation>ReplicaSets do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1245"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1246"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>ReplicationControllers do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1250"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1250"/>
        <source>Services of the cluster</source>
        <translation>Services do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1252"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1253"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>Endpoint Slices do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1256"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1257"/>
        <source>Endpoints of the cluster</source>
        <translation>Endpoints do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1260"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1261"/>
        <source>Ingresses of the cluster</source>
        <translation>Ingresses do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1264"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1265"/>
        <source>Ingress Classes of the cluster</source>
        <translation>Ingress Classes do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1269"/>
        <source>Network Policies of the cluster</source>
        <translation>Network Policies do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1273"/>
        <source>Config Maps of the cluster</source>
        <translation>Config Maps do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1276"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1277"/>
        <source>Secrets of the cluster</source>
        <translation>Secrets do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1280"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1281"/>
        <source>Resource Quotas of the cluster</source>
        <translation>Resource Quotas do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1284"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1285"/>
        <source>Limit Ranges of the cluster</source>
        <translation>Limit Ranges do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1288"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1289"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>Horizontal Pod Autoscalers do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1292"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1293"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>Pod Disruption Budgets do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1296"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1297"/>
        <source>Priority Classes of the cluster</source>
        <translation>Priority Classes do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1300"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1301"/>
        <source>Runtime Classes of the cluster</source>
        <translation>Runtime Classes do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1304"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1305"/>
        <source>Leases of the cluster</source>
        <translation>Leases do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1308"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1309"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>Mutating Webhook Configurations do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1312"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1313"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>Validating Webhook Configurations do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1316"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1317"/>
        <source>Node Groups of the cluster</source>
        <translation>Node Groups do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1320"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1321"/>
        <source>Add-ons of the cluster</source>
        <translation>Add-ons do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1379"/>
        <source>Check for updates</source>
        <translation>Verificar atualizações</translation>
    </message>
    <message>
        <location filename="../window.py" line="1380"/>
        <source>Checking for updates...</source>
        <translation>Verificando atualizações...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1381"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>O KubeScope está atualizado. Clique para verificar de novo.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1382"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>Não foi possível verificar atualizações. Clique para tentar de novo.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1396"/>
        <source>Update available</source>
        <translation>Atualização disponível</translation>
    </message>
    <message>
        <location filename="../window.py" line="1398"/>
        <source>Download KubeScope {version}</source>
        <translation>Baixar o KubeScope {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1434"/>
        <source>Check for updates again</source>
        <translation>Verificar atualizações de novo</translation>
    </message>
    <message>
        <location filename="../window.py" line="1775"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Configurar credenciais da AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1779"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>As credenciais da AWS do perfil {profile} estão ausentes ou inválidas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1818"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Conclua no terminal que abriu e depois clique em Atualizar.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2414"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{count} Services em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2416"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{count} Endpoint Slices em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2419"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{count} Endpoints em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2422"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{count} Ingresses em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2424"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>{count} Ingress Classes no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2426"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{count} Network Policies em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2429"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>{count} Config Maps em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2431"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>{count} Secrets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2433"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>{count} Resource Quotas em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2436"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>{count} Limit Ranges em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2439"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>{count} Horizontal Pod Autoscalers em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2442"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>{count} Pod Disruption Budgets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2444"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>{count} Leases em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2446"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>{count} Priority Classes no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2448"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>{count} Runtime Classes no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2450"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>{count} Mutating Webhook Configurations no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2453"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>{count} Validating Webhook Configurations no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2455"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>{count} Node Groups no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2456"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>{count} Add-ons no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2515"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pods em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2577"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployments em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2583"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{count} DaemonSets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2586"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{count} ReplicaSets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2589"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{count} ReplicationControllers em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2616"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} de {total} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2617"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} de {total} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2619"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{visible} de {total} DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2620"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{visible} de {total} ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2622"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{visible} de {total} ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2626"/>
        <source>{visible} of {total} Services</source>
        <translation>{visible} de {total} Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="2627"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{visible} de {total} Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="2628"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{visible} de {total} Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="2629"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{visible} de {total} Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="2630"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{visible} de {total} Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2631"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{visible} de {total} Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="2632"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>{visible} de {total} Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="2633"/>
        <source>{visible} of {total} Secrets</source>
        <translation>{visible} de {total} Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2634"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>{visible} de {total} Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="2635"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>{visible} de {total} Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="2637"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>{visible} de {total} Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2640"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>{visible} de {total} Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2642"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>{visible} de {total} Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2643"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>{visible} de {total} Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2644"/>
        <source>{visible} of {total} Leases</source>
        <translation>{visible} de {total} Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="2646"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>{visible} de {total} Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2649"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>{visible} de {total} Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2651"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>{visible} de {total} Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="2652"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>{visible} de {total} Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="2857"/>
        <source>No Pods are associated with this workload</source>
        <translation>Nenhum Pod associado a este workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="2864"/>
        <location filename="../window.py" line="2887"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2864"/>
        <source>This workload has no Pods.</source>
        <translation>Este workload não possui Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2873"/>
        <location filename="../window.py" line="2896"/>
        <source>View logs</source>
        <translation>Ver logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2874"/>
        <source>Select the Pod:</source>
        <translation>Selecione o Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2888"/>
        <source>Pod {name} has no containers.</source>
        <translation>O Pod {name} não possui containers.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2897"/>
        <source>Select the container of {name}:</source>
        <translation>Selecione o container de {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2923"/>
        <source>Save to a file</source>
        <translation>Salvar em um arquivo</translation>
    </message>
    <message>
        <location filename="../window.py" line="2934"/>
        <source>Could not save</source>
        <translation>Não foi possível salvar</translation>
    </message>
    <message>
        <location filename="../window.py" line="2935"/>
        <source>The file could not be written: {reason}</source>
        <translation>Não foi possível gravar o arquivo: {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2981"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Logs: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3031"/>
        <source>Automatic</source>
        <translation>Automático</translation>
    </message>
    <message>
        <location filename="../window.py" line="3104"/>
        <source>Choose a kubeconfig file</source>
        <translation>Escolha um arquivo kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="3150"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>O comando de login da linha {row} não é válido.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3163"/>
        <source>Light</source>
        <translation>Claro</translation>
    </message>
    <message>
        <location filename="../window.py" line="3163"/>
        <source>Dark</source>
        <translation>Escuro</translation>
    </message>
    <message>
        <location filename="../window.py" line="3044"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>Desligado por padrão. Quando ligado, o KubeScope registra o que faz, nunca logs de Pods nem o conteúdo de recursos, em {path}. Leia antes de compartilhar: ele inclui nomes de contextos.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3075"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>Nenhum contexto foi encontrado no kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3182"/>
        <source>My theme</source>
        <translation>Meu tema</translation>
    </message>
    <message>
        <location filename="../window.py" line="3226"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>Cache limpo. Tudo é carregado de novo na próxima vez que for preciso.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3281"/>
        <source>Settings saved.</source>
        <translation>Configurações salvas.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3320"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>Seu usuário não tem permissão para {action}. Peça acesso ao administrador do cluster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3325"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>Seu usuário não tem permissão para fazer isso. Peça acesso ao administrador do cluster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3344"/>
        <source>Query failed</source>
        <translation>Falha na consulta</translation>
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
        <translation>Eventos</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="293"/>
        <source>TYPE</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="298"/>
        <source>SOURCE</source>
        <translation>ORIGEM</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>INVOLVED OBJECT</source>
        <translation>OBJETO ENVOLVIDO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>MESSAGE</source>
        <translation>MENSAGEM</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>COUNT</source>
        <translation>QTD.</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>AGE</source>
        <translation>IDADE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>LAST SEEN</source>
        <translation>VISTO POR ÚLTIMO</translation>
    </message>
</context>
</TS>
