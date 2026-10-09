<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="pt_BR">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="52"/>
        <source>Login tool not found</source>
        <translation>Ferramenta de login não encontrada</translation>
    </message>
    <message>
        <location filename="../errors.py" line="53"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>Seu kubeconfig executa “{tool}” para autenticar, mas ela não está instalada ou não está no PATH. Instale-a e atualize.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="62"/>
        <source>kubectl is missing</source>
        <translation>kubectl não encontrado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="63"/>
        <source>The kubectl bundled with the app was not found. Reinstall it.</source>
        <translation>O kubectl que acompanha o app não foi encontrado. Reinstale o aplicativo.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Context not found</source>
        <translation>Contexto não encontrado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>Este contexto não está no seu kubeconfig. Verifique o ~/.kube/config.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="80"/>
        <source>Authentication failed</source>
        <translation>Falha na autenticação</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”) and refresh.</source>
        <translation>Suas credenciais podem ter expirado. Faça login novamente (por exemplo “aws sso login”) e atualize.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Access denied</source>
        <translation>Acesso negado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>Seu usuário não tem permissão para ler este recurso.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="108"/>
        <source>Cluster unreachable</source>
        <translation>Cluster inacessível</translation>
    </message>
    <message>
        <location filename="../errors.py" line="109"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>Verifique sua rede ou VPN e se o cluster está em execução.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="115"/>
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
        <location filename="../ui/main_window.ui" line="344"/>
        <source>KubeScope</source>
        <translation>KubeScope</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="241"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="254"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>Contexto do Kubernetes do seu kubeconfig</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="287"/>
        <source>READ ONLY</source>
        <translation>SOMENTE LEITURA</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="351"/>
        <source>Kubernetes console</source>
        <translation>Console Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="374"/>
        <source>MONITORING</source>
        <translation>MONITORAMENTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="381"/>
        <location filename="../ui/main_window.ui" line="464"/>
        <location filename="../ui/main_window.ui" line="781"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="412"/>
        <source>Workloads</source>
        <translation>Workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="557"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="588"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="619"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="653"/>
        <source>Details &amp;&amp; Logs</source>
        <translation>Detalhes e Logs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="697"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="732"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>ACESSO SEGURO
Recursos em modo somente leitura</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="788"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="646"/>
        <location filename="../ui/main_window.ui" line="863"/>
        <location filename="../ui/main_window.ui" line="1049"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="915"/>
        <source>Search by name or namespace...</source>
        <translation>Buscar por nome ou namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="938"/>
        <source>Refresh</source>
        <translation>Atualizar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="975"/>
        <source>View Pods of the selected workload</source>
        <translation>Ver Pods do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="495"/>
        <location filename="../ui/main_window.ui" line="978"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="526"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="991"/>
        <source>View JSON details of the selected workload</source>
        <translation>Ver os detalhes JSON do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="994"/>
        <source>Details</source>
        <translation>Detalhes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1007"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Ver logs de um Pod do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1010"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1054"/>
        <source>KIND</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../window.py" line="648"/>
        <location filename="../ui/main_window.ui" line="1059"/>
        <source>NAME</source>
        <translation>NOME</translation>
    </message>
    <message>
        <location filename="../window.py" line="641"/>
        <location filename="../ui/main_window.ui" line="1064"/>
        <source>READY</source>
        <translation>PRONTOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="639"/>
        <source>COMPLETIONS</source>
        <translation>CONCLUSÕES</translation>
    </message>
    <message>
        <location filename="../window.py" line="640"/>
        <source>SCHEDULE</source>
        <translation>AGENDA</translation>
    </message>
    <message>
        <location filename="../window.py" line="650"/>
        <location filename="../ui/main_window.ui" line="1069"/>
        <source>STATUS</source>
        <translation>STATUS</translation>
    </message>
    <message>
        <location filename="../window.py" line="651"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../window.py" line="652"/>
        <source>MEMORY</source>
        <translation>MEMÓRIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="653"/>
        <source>RESTARTS</source>
        <translation>REINÍCIOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="654"/>
        <location filename="../ui/main_window.ui" line="1074"/>
        <source>AGE</source>
        <translation>IDADE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1552"/>
        <source>Select a context to load workloads</source>
        <translation>Selecione um contexto para carregar os workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="274"/>
        <source>Sign in with the AWS CLI, then reload the cluster data</source>
        <translation>Autenticar com a AWS CLI e recarregar os dados do cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="277"/>
        <source>Sign in to AWS</source>
        <translation>Autenticar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1575"/>
        <source>Data fetched via kubectl</source>
        <translation>Dados consultados via kubectl</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1626"/>
        <source>© 2026 DCO Tecnologia · MIT License</source>
        <translation>© 2026 DCO Tecnologia · Licença MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1629"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>O KubeScope é software de código aberto, distribuído sob a Licença MIT</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="955"/>
        <location filename="../ui/overview_page.ui" line="110"/>
        <source>nodes ready</source>
        <translation>nós prontos</translation>
    </message>
    <message>
        <location filename="../window.py" line="971"/>
        <location filename="../ui/overview_page.ui" line="231"/>
        <source>cores requested / allocatable</source>
        <translation>cores requisitados / alocáveis</translation>
    </message>
    <message>
        <location filename="../window.py" line="985"/>
        <location filename="../ui/overview_page.ui" line="298"/>
        <source>requested / allocatable</source>
        <translation>requisitada / alocável</translation>
    </message>
    <message>
        <location filename="../window.py" line="1004"/>
        <location filename="../ui/overview_page.ui" line="372"/>
        <source>in the cluster</source>
        <translation>no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1006"/>
        <location filename="../ui/overview_page.ui" line="426"/>
        <location filename="../ui/overview_page.ui" line="480"/>
        <location filename="../ui/overview_page.ui" line="534"/>
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
        <location filename="../ui/overview_page.ui" line="90"/>
        <source>NODES</source>
        <translation>NÓS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="144"/>
        <location filename="../ui/overview_page.ui" line="611"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="164"/>
        <source>running / capacity</source>
        <translation>em execução / capacidade</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="211"/>
        <location filename="../ui/overview_page.ui" line="601"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="278"/>
        <location filename="../ui/overview_page.ui" line="606"/>
        <source>MEMORY</source>
        <translation>MEMÓRIA</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="352"/>
        <source>NAMESPACES</source>
        <translation>NAMESPACES</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="406"/>
        <source>DEPLOYMENTS</source>
        <translation>DEPLOYMENTS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="460"/>
        <source>STATEFULSETS</source>
        <translation>STATEFULSETS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="514"/>
        <source>DAEMONSETS</source>
        <translation>DAEMONSETS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="549"/>
        <source>Nodes</source>
        <translation>Nós</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="581"/>
        <source>NODE</source>
        <translation>NÓ</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="586"/>
        <source>STATUS</source>
        <translation>STATUS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="591"/>
        <source>ROLE</source>
        <translation>FUNÇÃO</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="596"/>
        <source>VERSION</source>
        <translation>VERSÃO</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="616"/>
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
        <location filename="../window.py" line="1717"/>
        <location filename="../ui/settings_page.ui" line="166"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>Dê nomes mais amigáveis aos seus contextos. Deixe o nome vazio para manter o original.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>Salvar alterações</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="61"/>
        <source>GENERAL</source>
        <translation>GERAL</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="79"/>
        <source>Language</source>
        <translation>Idioma</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="114"/>
        <source>Remember the last used context</source>
        <translation>Lembrar o último contexto usado</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="124"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>Modo debug: gravar um arquivo de log que eu possa compartilhar</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="147"/>
        <source>Open the log folder</source>
        <translation>Abrir a pasta de logs</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="156"/>
        <source>CONTEXT NAMES</source>
        <translation>NOMES DOS CONTEXTOS</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="195"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="200"/>
        <source>DISPLAY NAME</source>
        <translation>NOME EXIBIDO</translation>
    </message>
</context>
<context>
    <name>WorkloadWindow</name>
    <message>
        <location filename="../window.py" line="397"/>
        <location filename="../window.py" line="1140"/>
        <location filename="../window.py" line="1776"/>
        <source>All namespaces</source>
        <translation>Todos os namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="478"/>
        <source>Loading contexts...</source>
        <translation>Carregando contextos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="487"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>Não foi possível carregar o kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="507"/>
        <source>No contexts found in kubeconfig</source>
        <translation>Nenhum contexto encontrado no kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="574"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
    </message>
    <message>
        <location filename="../window.py" line="575"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="577"/>
        <source>Details &amp; Logs</source>
        <translation>Detalhes e Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="579"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Detalhes de recursos e logs de Pods, uma aba para cada</translation>
    </message>
    <message>
        <location filename="../window.py" line="582"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../window.py" line="583"/>
        <source>Preferences and context names</source>
        <translation>Preferências e nomes dos contextos</translation>
    </message>
    <message>
        <location filename="../window.py" line="585"/>
        <source>Workloads overview</source>
        <translation>Visão geral das cargas de trabalho</translation>
    </message>
    <message>
        <location filename="../window.py" line="587"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>Saúde de cada tipo de carga e os eventos mais recentes</translation>
    </message>
    <message>
        <location filename="../window.py" line="597"/>
        <location filename="../window.py" line="832"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="598"/>
        <source>StatefulSets of the cluster</source>
        <translation>StatefulSets do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="600"/>
        <location filename="../window.py" line="834"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="600"/>
        <source>Jobs of the cluster</source>
        <translation>Jobs do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="601"/>
        <location filename="../window.py" line="835"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="601"/>
        <source>CronJobs of the cluster</source>
        <translation>CronJobs do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="787"/>
        <source>Loading workloads...</source>
        <translation>Carregando cargas de trabalho...</translation>
    </message>
    <message>
        <location filename="../window.py" line="831"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="833"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="850"/>
        <source>Could not read: {names}</source>
        <translation>Não foi possível ler: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="889"/>
        <source>Loading cluster data...</source>
        <translation>Carregando dados do cluster...</translation>
    </message>
    <message>
        <location filename="../window.py" line="964"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>em execução · {pending} pendentes · {failed} com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="973"/>
        <location filename="../window.py" line="987"/>
        <source> · usage {value}</source>
        <translation> · uso {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1013"/>
        <source>Ready</source>
        <translation>Pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="1013"/>
        <source>Not ready</source>
        <translation>Não pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="1036"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Uso real indisponível: metrics-server não encontrado.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1098"/>
        <source>Loading resources...</source>
        <translation>Carregando recursos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1101"/>
        <source>Refreshing...</source>
        <translation>Atualizando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1201"/>
        <location filename="../window.py" line="1264"/>
        <source>Running</source>
        <translation>Em execução</translation>
    </message>
    <message>
        <location filename="../window.py" line="1202"/>
        <location filename="../window.py" line="1260"/>
        <source>Pending</source>
        <translation>Pendente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1203"/>
        <source>Succeeded</source>
        <translation>Concluído</translation>
    </message>
    <message>
        <location filename="../window.py" line="1204"/>
        <location filename="../window.py" line="1259"/>
        <source>Failed</source>
        <translation>Com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="1205"/>
        <source>Unknown</source>
        <translation>Desconhecido</translation>
    </message>
    <message>
        <location filename="../window.py" line="1254"/>
        <source>Healthy</source>
        <translation>Saudável</translation>
    </message>
    <message>
        <location filename="../window.py" line="1255"/>
        <source>Degraded</source>
        <translation>Degradado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1256"/>
        <source>Unavailable</source>
        <translation>Indisponível</translation>
    </message>
    <message>
        <location filename="../window.py" line="1257"/>
        <source>Scaled to zero</source>
        <translation>Zero réplicas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1258"/>
        <source>Complete</source>
        <translation>Concluído</translation>
    </message>
    <message>
        <location filename="../window.py" line="1261"/>
        <source>Suspended</source>
        <translation>Suspenso</translation>
    </message>
    <message>
        <location filename="../window.py" line="1262"/>
        <source>Active</source>
        <translation>Ativo</translation>
    </message>
    <message>
        <location filename="../window.py" line="1263"/>
        <source>Scheduled</source>
        <translation>Agendado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1311"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{count} StatefulSets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1313"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{count} Jobs em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1314"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{count} CronJobs em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1336"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{visible} de {total} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1337"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{visible} de {total} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1338"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{visible} de {total} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1378"/>
        <source>Loading...</source>
        <translation>Carregando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1470"/>
        <source>Pods of {name}</source>
        <translation>Pods de {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1472"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods em {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1424"/>
        <location filename="../window.py" line="1516"/>
        <source>Pod: {name}</source>
        <translation>Pod: {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="381"/>
        <source>0 Deployments</source>
        <translation>0 Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="591"/>
        <location filename="../window.py" line="829"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="591"/>
        <source>Pods of the cluster</source>
        <translation>Pods do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="593"/>
        <location filename="../window.py" line="830"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="594"/>
        <source>Deployments of the cluster</source>
        <translation>Deployments do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="734"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Configurar credenciais da AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="738"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>As credenciais da AWS do perfil {profile} estão ausentes ou inválidas</translation>
    </message>
    <message>
        <location filename="../window.py" line="743"/>
        <source>Sign in to AWS ({profile})</source>
        <translation>Autenticar ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="746"/>
        <source>Not signed in to AWS (profile {profile})</source>
        <translation>Sem login na AWS (perfil {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="768"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Conclua no terminal que abriu e depois clique em Atualizar.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1246"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pods em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1308"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployments em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1334"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} de {total} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="1335"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} de {total} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="1537"/>
        <source>No Pods are associated with this workload</source>
        <translation>Nenhum Pod associado a este workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="1544"/>
        <location filename="../window.py" line="1567"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1544"/>
        <source>This workload has no Pods.</source>
        <translation>Este workload não possui Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <location filename="../window.py" line="1576"/>
        <source>View logs</source>
        <translation>Ver logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1554"/>
        <source>Select the Pod:</source>
        <translation>Selecione o Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="1568"/>
        <source>Pod {name} has no containers.</source>
        <translation>O Pod {name} não possui containers.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1577"/>
        <source>Select the container of {name}:</source>
        <translation>Selecione o container de {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="1630"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Logs: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1681"/>
        <source>Automatic</source>
        <translation>Automático</translation>
    </message>
    <message>
        <location filename="../window.py" line="1693"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>Desligado por padrão. Quando ligado, o KubeScope registra o que faz, nunca logs de Pods nem o conteúdo de recursos, em {path}. Leia antes de compartilhar: ele inclui nomes de contextos.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1723"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>Nenhum contexto foi encontrado no kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1757"/>
        <source>Settings saved.</source>
        <translation>Configurações salvas.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1792"/>
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
        <location filename="../ui/workloads_overview_page.ui" line="88"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="110"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="132"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="154"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="176"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="198"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="220"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="268"/>
        <source>Events</source>
        <translation>Eventos</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>TYPE</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>SOURCE</source>
        <translation>ORIGEM</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>INVOLVED OBJECT</source>
        <translation>OBJETO ENVOLVIDO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>MESSAGE</source>
        <translation>MENSAGEM</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>COUNT</source>
        <translation>QTD.</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="333"/>
        <source>AGE</source>
        <translation>IDADE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="338"/>
        <source>LAST SEEN</source>
        <translation>VISTO POR ÚLTIMO</translation>
    </message>
</context>
</TS>
