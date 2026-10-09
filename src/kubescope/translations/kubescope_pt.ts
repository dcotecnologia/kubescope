<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="pt_BR">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="47"/>
        <source>Login tool not found</source>
        <translation>Ferramenta de login não encontrada</translation>
    </message>
    <message>
        <location filename="../errors.py" line="48"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>Seu kubeconfig executa “{tool}” para autenticar, mas ela não está instalada ou não está no PATH. Instale-a e atualize.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="57"/>
        <source>kubectl is missing</source>
        <translation>kubectl não encontrado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="58"/>
        <source>The kubectl bundled with the app was not found. Reinstall it.</source>
        <translation>O kubectl que acompanha o app não foi encontrado. Reinstale o aplicativo.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="66"/>
        <source>Context not found</source>
        <translation>Contexto não encontrado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="67"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>Este contexto não está no seu kubeconfig. Verifique o ~/.kube/config.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="75"/>
        <source>Authentication failed</source>
        <translation>Falha na autenticação</translation>
    </message>
    <message>
        <location filename="../errors.py" line="76"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”) and refresh.</source>
        <translation>Suas credenciais podem ter expirado. Faça login novamente (por exemplo “aws sso login”) e atualize.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="85"/>
        <source>Access denied</source>
        <translation>Acesso negado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="86"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>Seu usuário não tem permissão para ler este recurso.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="103"/>
        <source>Cluster unreachable</source>
        <translation>Cluster inacessível</translation>
    </message>
    <message>
        <location filename="../errors.py" line="104"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>Verifique sua rede ou VPN e se o cluster está em execução.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="113"/>
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
        <location filename="../ui/main_window.ui" line="322"/>
        <source>KubeScope</source>
        <translation>KubeScope</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="235"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="248"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>Contexto do Kubernetes do seu kubeconfig</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="265"/>
        <source>READ ONLY</source>
        <translation>SOMENTE LEITURA</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="329"/>
        <source>Kubernetes console</source>
        <translation>Console Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>MONITORING</source>
        <translation>MONITORAMENTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="359"/>
        <location filename="../ui/main_window.ui" line="635"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="390"/>
        <source>Workloads</source>
        <translation>Workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="507"/>
        <source>Details &amp;&amp; Logs</source>
        <translation>Detalhes e Logs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="551"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="586"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>ACESSO SEGURO
Recursos em modo somente leitura</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="642"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="548"/>
        <location filename="../ui/main_window.ui" line="717"/>
        <location filename="../ui/main_window.ui" line="903"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="769"/>
        <source>Search by name or namespace...</source>
        <translation>Buscar por nome ou namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="792"/>
        <source>Refresh</source>
        <translation>Atualizar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="829"/>
        <source>View Pods of the selected workload</source>
        <translation>Ver Pods do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="442"/>
        <location filename="../ui/main_window.ui" line="832"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="473"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="845"/>
        <source>View JSON details of the selected workload</source>
        <translation>Ver os detalhes JSON do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="848"/>
        <source>Details</source>
        <translation>Detalhes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="861"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Ver logs de um Pod do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="864"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="908"/>
        <source>KIND</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../window.py" line="550"/>
        <location filename="../ui/main_window.ui" line="913"/>
        <source>NAME</source>
        <translation>NOME</translation>
    </message>
    <message>
        <location filename="../window.py" line="551"/>
        <location filename="../ui/main_window.ui" line="918"/>
        <source>READY</source>
        <translation>PRONTOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="552"/>
        <location filename="../ui/main_window.ui" line="923"/>
        <source>STATUS</source>
        <translation>STATUS</translation>
    </message>
    <message>
        <location filename="../window.py" line="553"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../window.py" line="554"/>
        <source>MEMORY</source>
        <translation>MEMÓRIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="555"/>
        <source>RESTARTS</source>
        <translation>REINÍCIOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="556"/>
        <location filename="../ui/main_window.ui" line="928"/>
        <source>AGE</source>
        <translation>IDADE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1406"/>
        <source>Select a context to load workloads</source>
        <translation>Selecione um contexto para carregar os workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1419"/>
        <source>Sign in with the AWS CLI, then reload the cluster data</source>
        <translation>Entrar com a AWS CLI e recarregar os dados do cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1422"/>
        <source>Sign in to AWS</source>
        <translation>Entrar na AWS</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1445"/>
        <source>Data fetched via kubectl</source>
        <translation>Dados consultados via kubectl</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1495"/>
        <source>© 2026 DCO Tecnologia · MIT License</source>
        <translation>© 2026 DCO Tecnologia · Licença MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1498"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>O KubeScope é software de código aberto, distribuído sob a Licença MIT</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="744"/>
        <location filename="../ui/overview_page.ui" line="110"/>
        <source>nodes ready</source>
        <translation>nós prontos</translation>
    </message>
    <message>
        <location filename="../window.py" line="760"/>
        <location filename="../ui/overview_page.ui" line="231"/>
        <source>cores requested / allocatable</source>
        <translation>cores requisitados / alocáveis</translation>
    </message>
    <message>
        <location filename="../window.py" line="774"/>
        <location filename="../ui/overview_page.ui" line="298"/>
        <source>requested / allocatable</source>
        <translation>requisitada / alocável</translation>
    </message>
    <message>
        <location filename="../window.py" line="793"/>
        <location filename="../ui/overview_page.ui" line="372"/>
        <source>in the cluster</source>
        <translation>no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="795"/>
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
        <location filename="../window.py" line="1447"/>
        <location filename="../ui/settings_page.ui" line="136"/>
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
        <location filename="../ui/settings_page.ui" line="126"/>
        <source>CONTEXT NAMES</source>
        <translation>NOMES DOS CONTEXTOS</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="165"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="170"/>
        <source>DISPLAY NAME</source>
        <translation>NOME EXIBIDO</translation>
    </message>
</context>
<context>
    <name>WorkloadWindow</name>
    <message>
        <location filename="../window.py" line="338"/>
        <location filename="../window.py" line="913"/>
        <location filename="../window.py" line="1492"/>
        <source>All namespaces</source>
        <translation>Todos os namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="408"/>
        <source>Loading contexts...</source>
        <translation>Carregando contextos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="416"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>Não foi possível carregar o kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="435"/>
        <source>No contexts found in kubeconfig</source>
        <translation>Nenhum contexto encontrado no kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="499"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
    </message>
    <message>
        <location filename="../window.py" line="500"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="502"/>
        <source>Details &amp; Logs</source>
        <translation>Detalhes e Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="504"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Detalhes de recursos e logs de Pods, uma aba para cada</translation>
    </message>
    <message>
        <location filename="../window.py" line="507"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../window.py" line="508"/>
        <source>Preferences and context names</source>
        <translation>Preferências e nomes dos contextos</translation>
    </message>
    <message>
        <location filename="../window.py" line="684"/>
        <source>Loading cluster data...</source>
        <translation>Carregando dados do cluster...</translation>
    </message>
    <message>
        <location filename="../window.py" line="753"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>em execução · {pending} pendentes · {failed} com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="762"/>
        <location filename="../window.py" line="776"/>
        <source> · usage {value}</source>
        <translation> · uso {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="802"/>
        <source>Ready</source>
        <translation>Pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="802"/>
        <source>Not ready</source>
        <translation>Não pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="825"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Uso real indisponível: metrics-server não encontrado.</translation>
    </message>
    <message>
        <location filename="../window.py" line="880"/>
        <source>Loading resources...</source>
        <translation>Carregando recursos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="883"/>
        <source>Refreshing...</source>
        <translation>Atualizando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="974"/>
        <source>Running</source>
        <translation>Em execução</translation>
    </message>
    <message>
        <location filename="../window.py" line="975"/>
        <source>Pending</source>
        <translation>Pendente</translation>
    </message>
    <message>
        <location filename="../window.py" line="976"/>
        <source>Succeeded</source>
        <translation>Concluído</translation>
    </message>
    <message>
        <location filename="../window.py" line="977"/>
        <source>Failed</source>
        <translation>Com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="978"/>
        <source>Unknown</source>
        <translation>Desconhecido</translation>
    </message>
    <message>
        <location filename="../window.py" line="1027"/>
        <source>Healthy</source>
        <translation>Saudável</translation>
    </message>
    <message>
        <location filename="../window.py" line="1028"/>
        <source>Degraded</source>
        <translation>Degradado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1029"/>
        <source>Unavailable</source>
        <translation>Indisponível</translation>
    </message>
    <message>
        <location filename="../window.py" line="1030"/>
        <source>Scaled to zero</source>
        <translation>Zero réplicas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1117"/>
        <source>Loading...</source>
        <translation>Carregando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1208"/>
        <source>Pods of {name}</source>
        <translation>Pods de {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1210"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods em {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1162"/>
        <location filename="../window.py" line="1254"/>
        <source>Pod: {name}</source>
        <translation>Pod: {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="322"/>
        <source>0 Deployments</source>
        <translation>0 Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="510"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="511"/>
        <source>Pods of the cluster</source>
        <translation>Pods do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="513"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="514"/>
        <source>Deployments of the cluster</source>
        <translation>Deployments do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="632"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Configurar credenciais da AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="636"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>As credenciais da AWS do perfil {profile} estão ausentes ou inválidas</translation>
    </message>
    <message>
        <location filename="../window.py" line="641"/>
        <source>Sign in to AWS ({profile})</source>
        <translation>Entrar na AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="644"/>
        <source>Not signed in to AWS (profile {profile})</source>
        <translation>Sem login na AWS (perfil {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="665"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Conclua no terminal que abriu e depois clique em Atualizar.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1019"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pods em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1060"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployments em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} de {total} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="1078"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} de {total} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="1275"/>
        <source>No Pods are associated with this workload</source>
        <translation>Nenhum Pod associado a este workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="1282"/>
        <location filename="../window.py" line="1305"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1282"/>
        <source>This workload has no Pods.</source>
        <translation>Este workload não possui Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1291"/>
        <location filename="../window.py" line="1314"/>
        <source>View logs</source>
        <translation>Ver logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1292"/>
        <source>Select the Pod:</source>
        <translation>Selecione o Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="1306"/>
        <source>Pod {name} has no containers.</source>
        <translation>O Pod {name} não possui containers.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1315"/>
        <source>Select the container of {name}:</source>
        <translation>Selecione o container de {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="1368"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Logs: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1419"/>
        <source>Automatic</source>
        <translation>Automático</translation>
    </message>
    <message>
        <location filename="../window.py" line="1453"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>Nenhum contexto foi encontrado no kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1476"/>
        <source>Settings saved.</source>
        <translation>Configurações salvas.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1506"/>
        <source>Query failed</source>
        <translation>Falha na consulta</translation>
    </message>
    <message>
        <location filename="../window.py" line="1536"/>
        <source>Finishing the current cluster request...</source>
        <translation>Finalizando a consulta atual ao cluster...</translation>
    </message>
</context>
</TS>
