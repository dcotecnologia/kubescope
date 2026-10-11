<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="pt_BR">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="64"/>
        <source>Login tool not found</source>
        <translation>Ferramenta de login não encontrada</translation>
    </message>
    <message>
        <location filename="../errors.py" line="65"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>Seu kubeconfig executa “{tool}” para autenticar, mas ela não está instalada ou não está no PATH. Instale-a e atualize.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="74"/>
        <source>kubectl is missing</source>
        <translation>kubectl não encontrado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="75"/>
        <source>The kubectl bundled with the app was not found. Reinstall it.</source>
        <translation>O kubectl que acompanha o app não foi encontrado. Reinstale o aplicativo.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="83"/>
        <source>Context not found</source>
        <translation>Contexto não encontrado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="84"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>Este contexto não está no seu kubeconfig. Verifique o ~/.kube/config.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="92"/>
        <source>Authentication failed</source>
        <translation>Falha na autenticação</translation>
    </message>
    <message>
        <location filename="../errors.py" line="93"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”) and refresh.</source>
        <translation>Suas credenciais podem ter expirado. Faça login novamente (por exemplo “aws sso login”) e atualize.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="102"/>
        <source>Access denied</source>
        <translation>Acesso negado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="103"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>Seu usuário não tem permissão para ler este recurso.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="120"/>
        <source>Cluster unreachable</source>
        <translation>Cluster inacessível</translation>
    </message>
    <message>
        <location filename="../errors.py" line="121"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>Verifique sua rede ou VPN e se o cluster está em execução.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="127"/>
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
        <location filename="../log_tab.py" line="41"/>
        <source>No log lines returned.</source>
        <translation>Nenhuma linha de log retornada.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="46"/>
        <source>Updated at {time}</source>
        <translation>Atualizado às {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="53"/>
        <source>Could not refresh logs: {message}</source>
        <translation>Não foi possível atualizar os logs: {message}</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../ui/main_window.ui" line="20"/>
        <location filename="../ui/main_window.ui" line="276"/>
        <source>KubeScope</source>
        <translation>KubeScope</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="308"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="321"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>Contexto do Kubernetes do seu kubeconfig</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="406"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>Nenhum contexto de cluster foi encontrado no seu kubeconfig. Adicione um cluster ao kubeconfig (por exemplo, com a AWS CLI: aws eks update-kubeconfig) e recarregue.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="286"/>
        <source>Kubernetes console</source>
        <translation>Console Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="447"/>
        <source>Dismiss</source>
        <translation>Dispensar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="538"/>
        <source>MONITORING</source>
        <translation>MONITORAMENTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="545"/>
        <location filename="../ui/main_window.ui" line="628"/>
        <location filename="../ui/main_window.ui" line="1256"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <source>Workloads</source>
        <translation>Workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="721"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="752"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="783"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="814"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="845"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="876"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="910"/>
        <source>Network</source>
        <translation>Rede</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="962"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="993"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1024"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1055"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1086"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1117"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1151"/>
        <source>Details &amp;&amp; Logs</source>
        <translation>Detalhes e Logs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="366"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1207"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>ACESSO SEGURO
Recursos em modo somente leitura</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1263"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2114"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>Abrir o site da DCO Tecnologia</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2134"/>
        <source>MIT License</source>
        <translation>Licença MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2173"/>
        <source>Open the project on GitHub</source>
        <translation>Abrir o projeto no GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="922"/>
        <location filename="../window.py" line="938"/>
        <location filename="../ui/main_window.ui" line="1338"/>
        <location filename="../ui/main_window.ui" line="1527"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1390"/>
        <source>Search by name or namespace...</source>
        <translation>Buscar por nome ou namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1413"/>
        <source>Refresh</source>
        <translation>Atualizar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1453"/>
        <source>View Pods of the selected workload</source>
        <translation>Ver Pods do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="659"/>
        <location filename="../ui/main_window.ui" line="1456"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="690"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1469"/>
        <source>View JSON details of the selected workload</source>
        <translation>Ver os detalhes JSON do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1472"/>
        <source>Details</source>
        <translation>Detalhes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1485"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Ver logs de um Pod do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1488"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="939"/>
        <location filename="../ui/main_window.ui" line="1532"/>
        <source>KIND</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../window.py" line="924"/>
        <location filename="../window.py" line="940"/>
        <location filename="../ui/main_window.ui" line="1537"/>
        <source>NAME</source>
        <translation>NOME</translation>
    </message>
    <message>
        <location filename="../window.py" line="917"/>
        <location filename="../ui/main_window.ui" line="1542"/>
        <source>READY</source>
        <translation>PRONTOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="915"/>
        <source>COMPLETIONS</source>
        <translation>CONCLUSÕES</translation>
    </message>
    <message>
        <location filename="../window.py" line="882"/>
        <source>TYPE</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../window.py" line="883"/>
        <source>CLUSTER IP</source>
        <translation>CLUSTER IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="884"/>
        <source>EXTERNAL IP</source>
        <translation>IP EXTERNO</translation>
    </message>
    <message>
        <location filename="../window.py" line="885"/>
        <location filename="../window.py" line="889"/>
        <location filename="../window.py" line="897"/>
        <source>PORTS</source>
        <translation>PORTAS</translation>
    </message>
    <message>
        <location filename="../window.py" line="888"/>
        <source>ADDRESS TYPE</source>
        <translation>TIPO DE ENDEREÇO</translation>
    </message>
    <message>
        <location filename="../window.py" line="890"/>
        <location filename="../window.py" line="892"/>
        <source>ENDPOINTS</source>
        <translation>ENDPOINTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="894"/>
        <source>CLASS</source>
        <translation>CLASSE</translation>
    </message>
    <message>
        <location filename="../window.py" line="895"/>
        <source>HOSTS</source>
        <translation>HOSTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="896"/>
        <source>ADDRESS</source>
        <translation>ENDEREÇO</translation>
    </message>
    <message>
        <location filename="../window.py" line="900"/>
        <source>CONTROLLER</source>
        <translation>CONTROLADOR</translation>
    </message>
    <message>
        <location filename="../window.py" line="901"/>
        <source>PARAMETERS</source>
        <translation>PARÂMETROS</translation>
    </message>
    <message>
        <location filename="../window.py" line="904"/>
        <source>POD SELECTOR</source>
        <translation>SELETOR DE POD</translation>
    </message>
    <message>
        <location filename="../window.py" line="905"/>
        <source>POLICY TYPES</source>
        <translation>TIPOS DE POLÍTICA</translation>
    </message>
    <message>
        <location filename="../window.py" line="916"/>
        <source>SCHEDULE</source>
        <translation>AGENDA</translation>
    </message>
    <message>
        <location filename="../window.py" line="926"/>
        <location filename="../ui/main_window.ui" line="1547"/>
        <source>STATUS</source>
        <translation>STATUS</translation>
    </message>
    <message>
        <location filename="../window.py" line="927"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../window.py" line="928"/>
        <source>MEMORY</source>
        <translation>MEMÓRIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="929"/>
        <source>RESTARTS</source>
        <translation>REINÍCIOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="930"/>
        <location filename="../window.py" line="942"/>
        <location filename="../ui/main_window.ui" line="1552"/>
        <source>AGE</source>
        <translation>IDADE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2030"/>
        <source>Select a context to load workloads</source>
        <translation>Selecione um contexto para carregar os workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="341"/>
        <source>Sign in with the AWS CLI, then reload the cluster data</source>
        <translation>Autenticar com a AWS CLI e recarregar os dados do cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="344"/>
        <source>Sign in to AWS</source>
        <translation>Autenticar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2053"/>
        <source>Data fetched via kubectl</source>
        <translation>Dados consultados via kubectl</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2137"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>O KubeScope é software de código aberto, distribuído sob a Licença MIT</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="1272"/>
        <location filename="../ui/overview_page.ui" line="113"/>
        <source>nodes ready</source>
        <translation>nós prontos</translation>
    </message>
    <message>
        <location filename="../window.py" line="1288"/>
        <location filename="../ui/overview_page.ui" line="234"/>
        <source>cores requested / allocatable</source>
        <translation>cores requisitados / alocáveis</translation>
    </message>
    <message>
        <location filename="../window.py" line="1302"/>
        <location filename="../ui/overview_page.ui" line="301"/>
        <source>requested / allocatable</source>
        <translation>requisitada / alocável</translation>
    </message>
    <message>
        <location filename="../window.py" line="1321"/>
        <location filename="../ui/overview_page.ui" line="375"/>
        <source>in the cluster</source>
        <translation>no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1323"/>
        <location filename="../ui/overview_page.ui" line="429"/>
        <location filename="../ui/overview_page.ui" line="483"/>
        <location filename="../ui/overview_page.ui" line="537"/>
        <source>workloads</source>
        <translation>workloads</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="29"/>
        <source>Cluster resources</source>
        <translation>Recursos do cluster</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="52"/>
        <source>Refresh</source>
        <translation>Atualizar</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="93"/>
        <source>NODES</source>
        <translation>NÓS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="147"/>
        <location filename="../ui/overview_page.ui" line="614"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="167"/>
        <source>running / capacity</source>
        <translation>em execução / capacidade</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="214"/>
        <location filename="../ui/overview_page.ui" line="604"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="281"/>
        <location filename="../ui/overview_page.ui" line="609"/>
        <source>MEMORY</source>
        <translation>MEMÓRIA</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="355"/>
        <source>NAMESPACES</source>
        <translation>NAMESPACES</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="409"/>
        <source>DEPLOYMENTS</source>
        <translation>DEPLOYMENTS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="463"/>
        <source>STATEFULSETS</source>
        <translation>STATEFULSETS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="517"/>
        <source>DAEMONSETS</source>
        <translation>DAEMONSETS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="552"/>
        <source>Nodes</source>
        <translation>Nós</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="584"/>
        <source>NODE</source>
        <translation>NÓ</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="589"/>
        <source>STATUS</source>
        <translation>STATUS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="594"/>
        <source>ROLE</source>
        <translation>FUNÇÃO</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="599"/>
        <source>VERSION</source>
        <translation>VERSÃO</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="619"/>
        <source>AGE</source>
        <translation>IDADE</translation>
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
        <location filename="../window.py" line="2163"/>
        <location filename="../ui/settings_page.ui" line="294"/>
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
        <source>Remember the last used context</source>
        <translation>Lembrar o último contexto usado</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="232"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>Modo debug: gravar um arquivo de log que eu possa compartilhar</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="257"/>
        <source>Open the log folder</source>
        <translation>Abrir a pasta de logs</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="284"/>
        <source>CONTEXT NAMES</source>
        <translation>NOMES DOS CONTEXTOS</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="329"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="334"/>
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
    <name>WorkloadWindow</name>
    <message>
        <location filename="../window.py" line="552"/>
        <location filename="../window.py" line="1506"/>
        <location filename="../window.py" line="2282"/>
        <source>All namespaces</source>
        <translation>Todos os namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="631"/>
        <source>Loading contexts...</source>
        <translation>Carregando contextos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="640"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>Não foi possível carregar o kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="661"/>
        <source>No contexts found in kubeconfig</source>
        <translation>Nenhum contexto encontrado no kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="728"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
    </message>
    <message>
        <location filename="../window.py" line="729"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="731"/>
        <source>Details &amp; Logs</source>
        <translation>Detalhes e Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="733"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Detalhes de recursos e logs de Pods, uma aba para cada</translation>
    </message>
    <message>
        <location filename="../window.py" line="736"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../window.py" line="737"/>
        <source>Preferences and context names</source>
        <translation>Preferências e nomes dos contextos</translation>
    </message>
    <message>
        <location filename="../window.py" line="739"/>
        <source>Workloads overview</source>
        <translation>Visão geral das cargas de trabalho</translation>
    </message>
    <message>
        <location filename="../window.py" line="741"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>Saúde de cada tipo de carga e os eventos mais recentes</translation>
    </message>
    <message>
        <location filename="../window.py" line="751"/>
        <location filename="../window.py" line="1140"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="752"/>
        <source>StatefulSets of the cluster</source>
        <translation>StatefulSets do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="766"/>
        <location filename="../window.py" line="1142"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="766"/>
        <source>Jobs of the cluster</source>
        <translation>Jobs do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="767"/>
        <location filename="../window.py" line="1143"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="767"/>
        <source>CronJobs of the cluster</source>
        <translation>CronJobs do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="796"/>
        <source>Version {version}</source>
        <translation>Versão {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="799"/>
        <source>Open the project on GitHub</source>
        <translation>Abrir o projeto no GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="1098"/>
        <source>Loading workloads...</source>
        <translation>Carregando cargas de trabalho...</translation>
    </message>
    <message>
        <location filename="../window.py" line="755"/>
        <location filename="../window.py" line="1139"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="759"/>
        <location filename="../window.py" line="1141"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1158"/>
        <source>Could not read: {names}</source>
        <translation>Não foi possível ler: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1201"/>
        <source>Loading cluster data...</source>
        <translation>Carregando dados do cluster...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1281"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>em execução · {pending} pendentes · {failed} com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="1290"/>
        <location filename="../window.py" line="1304"/>
        <source> · usage {value}</source>
        <translation> · uso {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Ready</source>
        <translation>Pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Not ready</source>
        <translation>Não pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="1355"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Uso real indisponível: metrics-server não encontrado.</translation>
    </message>
    <message>
        <location filename="../window.py" line="873"/>
        <location filename="../window.py" line="1429"/>
        <source>Loading resources...</source>
        <translation>Carregando recursos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1446"/>
        <source>Refreshing...</source>
        <translation>Atualizando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1617"/>
        <location filename="../window.py" line="1683"/>
        <source>Running</source>
        <translation>Em execução</translation>
    </message>
    <message>
        <location filename="../window.py" line="1618"/>
        <location filename="../window.py" line="1679"/>
        <source>Pending</source>
        <translation>Pendente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1619"/>
        <source>Succeeded</source>
        <translation>Concluído</translation>
    </message>
    <message>
        <location filename="../window.py" line="1620"/>
        <location filename="../window.py" line="1678"/>
        <source>Failed</source>
        <translation>Com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="1621"/>
        <source>Unknown</source>
        <translation>Desconhecido</translation>
    </message>
    <message>
        <location filename="../window.py" line="1673"/>
        <source>Healthy</source>
        <translation>Saudável</translation>
    </message>
    <message>
        <location filename="../window.py" line="1674"/>
        <source>Degraded</source>
        <translation>Degradado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1675"/>
        <source>Unavailable</source>
        <translation>Indisponível</translation>
    </message>
    <message>
        <location filename="../window.py" line="1676"/>
        <source>Scaled to zero</source>
        <translation>Zero réplicas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1677"/>
        <source>Complete</source>
        <translation>Concluído</translation>
    </message>
    <message>
        <location filename="../window.py" line="1680"/>
        <source>Suspended</source>
        <translation>Suspenso</translation>
    </message>
    <message>
        <location filename="../window.py" line="1681"/>
        <source>Active</source>
        <translation>Ativo</translation>
    </message>
    <message>
        <location filename="../window.py" line="1682"/>
        <source>Scheduled</source>
        <translation>Agendado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1730"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{count} StatefulSets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1741"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{count} Jobs em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1742"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{count} CronJobs em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1764"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{visible} de {total} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1770"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{visible} de {total} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1771"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{visible} de {total} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1823"/>
        <source>Loading...</source>
        <translation>Carregando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1915"/>
        <source>Pods of {name}</source>
        <translation>Pods de {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1917"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods em {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1869"/>
        <location filename="../window.py" line="1961"/>
        <source>Pod: {name}</source>
        <translation>Pod: {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="536"/>
        <source>0 Deployments</source>
        <translation>0 Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="745"/>
        <location filename="../window.py" line="1137"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="745"/>
        <source>Pods of the cluster</source>
        <translation>Pods do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="747"/>
        <location filename="../window.py" line="1138"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="748"/>
        <source>Deployments of the cluster</source>
        <translation>Deployments do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="756"/>
        <source>DaemonSets of the cluster</source>
        <translation>DaemonSets do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="760"/>
        <source>ReplicaSets of the cluster</source>
        <translation>ReplicaSets do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="763"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="764"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>ReplicationControllers do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="768"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="768"/>
        <source>Services of the cluster</source>
        <translation>Services do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="770"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="771"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>Endpoint Slices do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="774"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="775"/>
        <source>Endpoints of the cluster</source>
        <translation>Endpoints do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="778"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="779"/>
        <source>Ingresses of the cluster</source>
        <translation>Ingresses do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="782"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="783"/>
        <source>Ingress Classes of the cluster</source>
        <translation>Ingress Classes do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="786"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="787"/>
        <source>Network Policies of the cluster</source>
        <translation>Network Policies do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1045"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Configurar credenciais da AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1049"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>As credenciais da AWS do perfil {profile} estão ausentes ou inválidas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1054"/>
        <source>Sign in to AWS ({profile})</source>
        <translation>Autenticar ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1057"/>
        <source>Not signed in to AWS (profile {profile})</source>
        <translation>Sem login na AWS (perfil {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1079"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Conclua no terminal que abriu e depois clique em Atualizar.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1593"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{count} Services em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1595"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{count} Endpoint Slices em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1598"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{count} Endpoints em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1601"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{count} Ingresses em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1603"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>{count} Ingress Classes no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1605"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{count} Network Policies em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1665"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pods em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1727"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployments em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1733"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{count} DaemonSets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1736"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{count} ReplicaSets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1739"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{count} ReplicationControllers em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1762"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} de {total} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="1763"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} de {total} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="1765"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{visible} de {total} DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1766"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{visible} de {total} ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1768"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{visible} de {total} ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1772"/>
        <source>{visible} of {total} Services</source>
        <translation>{visible} de {total} Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1773"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{visible} de {total} Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1774"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{visible} de {total} Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1775"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{visible} de {total} Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1776"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{visible} de {total} Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1777"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{visible} de {total} Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1982"/>
        <source>No Pods are associated with this workload</source>
        <translation>Nenhum Pod associado a este workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="1989"/>
        <location filename="../window.py" line="2012"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1989"/>
        <source>This workload has no Pods.</source>
        <translation>Este workload não possui Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1998"/>
        <location filename="../window.py" line="2021"/>
        <source>View logs</source>
        <translation>Ver logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1999"/>
        <source>Select the Pod:</source>
        <translation>Selecione o Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2013"/>
        <source>Pod {name} has no containers.</source>
        <translation>O Pod {name} não possui containers.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2022"/>
        <source>Select the container of {name}:</source>
        <translation>Selecione o container de {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2078"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Logs: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2128"/>
        <source>Automatic</source>
        <translation>Automático</translation>
    </message>
    <message>
        <location filename="../window.py" line="2178"/>
        <source>Light</source>
        <translation>Claro</translation>
    </message>
    <message>
        <location filename="../window.py" line="2178"/>
        <source>Dark</source>
        <translation>Escuro</translation>
    </message>
    <message>
        <location filename="../window.py" line="2139"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>Desligado por padrão. Quando ligado, o KubeScope registra o que faz, nunca logs de Pods nem o conteúdo de recursos, em {path}. Leia antes de compartilhar: ele inclui nomes de contextos.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2170"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>Nenhum contexto foi encontrado no kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2196"/>
        <source>My theme</source>
        <translation>Meu tema</translation>
    </message>
    <message>
        <location filename="../window.py" line="2262"/>
        <source>Settings saved.</source>
        <translation>Configurações salvas.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2296"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>Seu usuário não tem permissão para {action}. Peça acesso ao administrador do cluster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2301"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>Seu usuário não tem permissão para fazer isso. Peça acesso ao administrador do cluster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2320"/>
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
        <location filename="../ui/workloads_overview_page.ui" line="52"/>
        <source>Refresh</source>
        <translation>Atualizar</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="91"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="113"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="135"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="157"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="179"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="201"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="223"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="271"/>
        <source>Events</source>
        <translation>Eventos</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="306"/>
        <source>TYPE</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="311"/>
        <source>SOURCE</source>
        <translation>ORIGEM</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="316"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="321"/>
        <source>INVOLVED OBJECT</source>
        <translation>OBJETO ENVOLVIDO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="326"/>
        <source>MESSAGE</source>
        <translation>MENSAGEM</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="331"/>
        <source>COUNT</source>
        <translation>QTD.</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="336"/>
        <source>AGE</source>
        <translation>IDADE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="341"/>
        <source>LAST SEEN</source>
        <translation>VISTO POR ÚLTIMO</translation>
    </message>
</context>
</TS>
