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
        <location filename="../ui/main_window.ui" line="383"/>
        <source>KubeScope</source>
        <translation>KubeScope</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="249"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="262"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>Contexto do Kubernetes do seu kubeconfig</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="295"/>
        <source>READ ONLY</source>
        <translation>SOMENTE LEITURA</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="323"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>Nenhum contexto de cluster foi encontrado no seu kubeconfig. Adicione um cluster ao kubeconfig (por exemplo, com a AWS CLI: aws eks update-kubeconfig) e recarregue.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="390"/>
        <source>Kubernetes console</source>
        <translation>Console Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="413"/>
        <source>MONITORING</source>
        <translation>MONITORAMENTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="420"/>
        <location filename="../ui/main_window.ui" line="503"/>
        <location filename="../ui/main_window.ui" line="820"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="451"/>
        <source>Workloads</source>
        <translation>Workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="596"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="627"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="658"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="692"/>
        <source>Details &amp;&amp; Logs</source>
        <translation>Detalhes e Logs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="736"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="771"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>ACESSO SEGURO
Recursos em modo somente leitura</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="827"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1701"/>
        <source>Open the project on GitHub</source>
        <translation>Abrir o projeto no GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="701"/>
        <location filename="../ui/main_window.ui" line="902"/>
        <location filename="../ui/main_window.ui" line="1091"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="954"/>
        <source>Search by name or namespace...</source>
        <translation>Buscar por nome ou namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="977"/>
        <source>Refresh</source>
        <translation>Atualizar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1017"/>
        <source>View Pods of the selected workload</source>
        <translation>Ver Pods do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="534"/>
        <location filename="../ui/main_window.ui" line="1020"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="565"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1033"/>
        <source>View JSON details of the selected workload</source>
        <translation>Ver os detalhes JSON do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1036"/>
        <source>Details</source>
        <translation>Detalhes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1049"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Ver logs de um Pod do workload selecionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1052"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1096"/>
        <source>KIND</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../window.py" line="703"/>
        <location filename="../ui/main_window.ui" line="1101"/>
        <source>NAME</source>
        <translation>NOME</translation>
    </message>
    <message>
        <location filename="../window.py" line="696"/>
        <location filename="../ui/main_window.ui" line="1106"/>
        <source>READY</source>
        <translation>PRONTOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="694"/>
        <source>COMPLETIONS</source>
        <translation>CONCLUSÕES</translation>
    </message>
    <message>
        <location filename="../window.py" line="695"/>
        <source>SCHEDULE</source>
        <translation>AGENDA</translation>
    </message>
    <message>
        <location filename="../window.py" line="705"/>
        <location filename="../ui/main_window.ui" line="1111"/>
        <source>STATUS</source>
        <translation>STATUS</translation>
    </message>
    <message>
        <location filename="../window.py" line="706"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../window.py" line="707"/>
        <source>MEMORY</source>
        <translation>MEMÓRIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="708"/>
        <source>RESTARTS</source>
        <translation>REINÍCIOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="709"/>
        <location filename="../ui/main_window.ui" line="1116"/>
        <source>AGE</source>
        <translation>IDADE</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1594"/>
        <source>Select a context to load workloads</source>
        <translation>Selecione um contexto para carregar os workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="282"/>
        <source>Sign in with the AWS CLI, then reload the cluster data</source>
        <translation>Autenticar com a AWS CLI e recarregar os dados do cluster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="285"/>
        <source>Sign in to AWS</source>
        <translation>Autenticar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1617"/>
        <source>Data fetched via kubectl</source>
        <translation>Dados consultados via kubectl</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1668"/>
        <source>© 2026 DCO Tecnologia · MIT License</source>
        <translation>© 2026 DCO Tecnologia · Licença MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1671"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>O KubeScope é software de código aberto, distribuído sob a Licença MIT</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="1016"/>
        <location filename="../ui/overview_page.ui" line="113"/>
        <source>nodes ready</source>
        <translation>nós prontos</translation>
    </message>
    <message>
        <location filename="../window.py" line="1032"/>
        <location filename="../ui/overview_page.ui" line="234"/>
        <source>cores requested / allocatable</source>
        <translation>cores requisitados / alocáveis</translation>
    </message>
    <message>
        <location filename="../window.py" line="1046"/>
        <location filename="../ui/overview_page.ui" line="301"/>
        <source>requested / allocatable</source>
        <translation>requisitada / alocável</translation>
    </message>
    <message>
        <location filename="../window.py" line="1065"/>
        <location filename="../ui/overview_page.ui" line="375"/>
        <source>in the cluster</source>
        <translation>no cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1067"/>
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
        <location filename="../window.py" line="1785"/>
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
        <location filename="../window.py" line="420"/>
        <location filename="../window.py" line="1204"/>
        <location filename="../window.py" line="1904"/>
        <source>All namespaces</source>
        <translation>Todos os namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="496"/>
        <source>Loading contexts...</source>
        <translation>Carregando contextos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="505"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>Não foi possível carregar o kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="526"/>
        <source>No contexts found in kubeconfig</source>
        <translation>Nenhum contexto encontrado no kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="593"/>
        <source>Overview</source>
        <translation>Visão geral</translation>
    </message>
    <message>
        <location filename="../window.py" line="594"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos e capacidade do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="596"/>
        <source>Details &amp; Logs</source>
        <translation>Detalhes e Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="598"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Detalhes de recursos e logs de Pods, uma aba para cada</translation>
    </message>
    <message>
        <location filename="../window.py" line="601"/>
        <source>Settings</source>
        <translation>Configurações</translation>
    </message>
    <message>
        <location filename="../window.py" line="602"/>
        <source>Preferences and context names</source>
        <translation>Preferências e nomes dos contextos</translation>
    </message>
    <message>
        <location filename="../window.py" line="604"/>
        <source>Workloads overview</source>
        <translation>Visão geral das cargas de trabalho</translation>
    </message>
    <message>
        <location filename="../window.py" line="606"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>Saúde de cada tipo de carga e os eventos mais recentes</translation>
    </message>
    <message>
        <location filename="../window.py" line="616"/>
        <location filename="../window.py" line="884"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="617"/>
        <source>StatefulSets of the cluster</source>
        <translation>StatefulSets do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="619"/>
        <location filename="../window.py" line="886"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="619"/>
        <source>Jobs of the cluster</source>
        <translation>Jobs do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="620"/>
        <location filename="../window.py" line="887"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="620"/>
        <source>CronJobs of the cluster</source>
        <translation>CronJobs do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="628"/>
        <source>Version {version}</source>
        <translation>Versão {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="631"/>
        <source>Open the project on GitHub</source>
        <translation>Abrir o projeto no GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="842"/>
        <source>Loading workloads...</source>
        <translation>Carregando cargas de trabalho...</translation>
    </message>
    <message>
        <location filename="../window.py" line="883"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="885"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="902"/>
        <source>Could not read: {names}</source>
        <translation>Não foi possível ler: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="945"/>
        <source>Loading cluster data...</source>
        <translation>Carregando dados do cluster...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1025"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>em execução · {pending} pendentes · {failed} com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="1034"/>
        <location filename="../window.py" line="1048"/>
        <source> · usage {value}</source>
        <translation> · uso {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1074"/>
        <source>Ready</source>
        <translation>Pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="1074"/>
        <source>Not ready</source>
        <translation>Não pronto</translation>
    </message>
    <message>
        <location filename="../window.py" line="1099"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Uso real indisponível: metrics-server não encontrado.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1162"/>
        <source>Loading resources...</source>
        <translation>Carregando recursos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1165"/>
        <source>Refreshing...</source>
        <translation>Atualizando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1265"/>
        <location filename="../window.py" line="1331"/>
        <source>Running</source>
        <translation>Em execução</translation>
    </message>
    <message>
        <location filename="../window.py" line="1266"/>
        <location filename="../window.py" line="1327"/>
        <source>Pending</source>
        <translation>Pendente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1267"/>
        <source>Succeeded</source>
        <translation>Concluído</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <location filename="../window.py" line="1326"/>
        <source>Failed</source>
        <translation>Com falha</translation>
    </message>
    <message>
        <location filename="../window.py" line="1269"/>
        <source>Unknown</source>
        <translation>Desconhecido</translation>
    </message>
    <message>
        <location filename="../window.py" line="1321"/>
        <source>Healthy</source>
        <translation>Saudável</translation>
    </message>
    <message>
        <location filename="../window.py" line="1322"/>
        <source>Degraded</source>
        <translation>Degradado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1323"/>
        <source>Unavailable</source>
        <translation>Indisponível</translation>
    </message>
    <message>
        <location filename="../window.py" line="1324"/>
        <source>Scaled to zero</source>
        <translation>Zero réplicas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1325"/>
        <source>Complete</source>
        <translation>Concluído</translation>
    </message>
    <message>
        <location filename="../window.py" line="1328"/>
        <source>Suspended</source>
        <translation>Suspenso</translation>
    </message>
    <message>
        <location filename="../window.py" line="1329"/>
        <source>Active</source>
        <translation>Ativo</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Scheduled</source>
        <translation>Agendado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1378"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{count} StatefulSets em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1380"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{count} Jobs em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1381"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{count} CronJobs em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1403"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{visible} de {total} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1404"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{visible} de {total} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1405"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{visible} de {total} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1445"/>
        <source>Loading...</source>
        <translation>Carregando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1537"/>
        <source>Pods of {name}</source>
        <translation>Pods de {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1539"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods em {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1491"/>
        <location filename="../window.py" line="1583"/>
        <source>Pod: {name}</source>
        <translation>Pod: {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="404"/>
        <source>0 Deployments</source>
        <translation>0 Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="610"/>
        <location filename="../window.py" line="881"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="610"/>
        <source>Pods of the cluster</source>
        <translation>Pods do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="612"/>
        <location filename="../window.py" line="882"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="613"/>
        <source>Deployments of the cluster</source>
        <translation>Deployments do cluster</translation>
    </message>
    <message>
        <location filename="../window.py" line="789"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Configurar credenciais da AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="793"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>As credenciais da AWS do perfil {profile} estão ausentes ou inválidas</translation>
    </message>
    <message>
        <location filename="../window.py" line="798"/>
        <source>Sign in to AWS ({profile})</source>
        <translation>Autenticar ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="801"/>
        <source>Not signed in to AWS (profile {profile})</source>
        <translation>Sem login na AWS (perfil {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="823"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Conclua no terminal que abriu e depois clique em Atualizar.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1313"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pods em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1375"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployments em {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1401"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} de {total} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="1402"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} de {total} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="1604"/>
        <source>No Pods are associated with this workload</source>
        <translation>Nenhum Pod associado a este workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="1611"/>
        <location filename="../window.py" line="1634"/>
        <source>Logs</source>
        <translation>Logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1611"/>
        <source>This workload has no Pods.</source>
        <translation>Este workload não possui Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1620"/>
        <location filename="../window.py" line="1643"/>
        <source>View logs</source>
        <translation>Ver logs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1621"/>
        <source>Select the Pod:</source>
        <translation>Selecione o Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="1635"/>
        <source>Pod {name} has no containers.</source>
        <translation>O Pod {name} não possui containers.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1644"/>
        <source>Select the container of {name}:</source>
        <translation>Selecione o container de {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="1700"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Logs: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1750"/>
        <source>Automatic</source>
        <translation>Automático</translation>
    </message>
    <message>
        <location filename="../window.py" line="1800"/>
        <source>Light</source>
        <translation>Claro</translation>
    </message>
    <message>
        <location filename="../window.py" line="1800"/>
        <source>Dark</source>
        <translation>Escuro</translation>
    </message>
    <message>
        <location filename="../window.py" line="1761"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>Desligado por padrão. Quando ligado, o KubeScope registra o que faz, nunca logs de Pods nem o conteúdo de recursos, em {path}. Leia antes de compartilhar: ele inclui nomes de contextos.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1792"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>Nenhum contexto foi encontrado no kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1818"/>
        <source>My theme</source>
        <translation>Meu tema</translation>
    </message>
    <message>
        <location filename="../window.py" line="1884"/>
        <source>Settings saved.</source>
        <translation>Configurações salvas.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1920"/>
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
