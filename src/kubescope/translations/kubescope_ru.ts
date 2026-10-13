<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ru">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>Программа входа не найдена</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>Ваш kubeconfig запускает «{tool}» для входа, но программа не установлена или отсутствует в PATH. Установите её и обновите.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>Контекст не найден</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>Этого контекста нет в вашем kubeconfig. Проверьте ~/.kube/config.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>Ошибка аутентификации</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>Срок действия ваших учётных данных мог истечь. Войдите снова (например, «aws sso login», «gcloud auth login» или «az login») и обновите.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Not an Amazon EKS cluster</source>
        <translation>Это не кластер Amazon EKS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Node Groups, Add-ons and the AWS cards of the Overview exist only on Amazon EKS contexts.</source>
        <translation>Node Groups, Add-ons и карточки AWS на странице «Обзор» есть только в контекстах Amazon EKS.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="110"/>
        <source>Unexpected answer from AWS</source>
        <translation>Неожиданный ответ от AWS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="111"/>
        <source>Update the AWS CLI to its latest version and refresh.</source>
        <translation>Обновите AWS CLI до последней версии и обновите данные.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="118"/>
        <location filename="../errors.py" line="128"/>
        <source>Access denied</source>
        <translation>Доступ запрещён</translation>
    </message>
    <message>
        <location filename="../errors.py" line="119"/>
        <source>Your AWS identity is not allowed to read this. The wiki lists the eks: permissions KubeScope needs.</source>
        <translation>Вашей учётной записи AWS не разрешено читать это. Нужные KubeScope разрешения eks: перечислены в вики.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>Вашему пользователю не разрешено читать этот ресурс.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="143"/>
        <source>No network connection</source>
        <translation>Нет подключения к сети</translation>
    </message>
    <message>
        <location filename="../errors.py" line="144"/>
        <source>Check your internet connection or VPN and refresh.</source>
        <translation>Проверьте подключение к интернету или VPN и обновите.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="165"/>
        <source>Cluster unreachable</source>
        <translation>Кластер недоступен</translation>
    </message>
    <message>
        <location filename="../errors.py" line="166"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>Проверьте сеть или VPN и убедитесь, что кластер запущен.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="172"/>
        <source>Something went wrong</source>
        <translation>Что-то пошло не так</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="42"/>
        <source>No log lines returned.</source>
        <translation>Строки журнала не получены.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="47"/>
        <source>Updated at {time}</source>
        <translation>Обновлено в {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="54"/>
        <source>Could not refresh logs: {message}</source>
        <translation>Не удалось обновить журналы: {message}</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>Автообновление</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>Получать новые строки журнала каждые несколько секунд и следить за концом журнала</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>Обновить сейчас</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../window.py" line="1508"/>
        <location filename="../window.py" line="1537"/>
        <source>TYPE</source>
        <translation>ТИП</translation>
    </message>
    <message>
        <location filename="../window.py" line="1509"/>
        <source>CLUSTER IP</source>
        <translation>CLUSTER IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1510"/>
        <source>EXTERNAL IP</source>
        <translation>EXTERNAL IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1511"/>
        <location filename="../window.py" line="1515"/>
        <location filename="../window.py" line="1523"/>
        <source>PORTS</source>
        <translation>ПОРТЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1514"/>
        <source>ADDRESS TYPE</source>
        <translation>ТИП АДРЕСА</translation>
    </message>
    <message>
        <location filename="../window.py" line="1516"/>
        <location filename="../window.py" line="1518"/>
        <source>ENDPOINTS</source>
        <translation>ENDPOINTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1520"/>
        <source>CLASS</source>
        <translation>КЛАСС</translation>
    </message>
    <message>
        <location filename="../window.py" line="1521"/>
        <source>HOSTS</source>
        <translation>ХОСТЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1522"/>
        <source>ADDRESS</source>
        <translation>АДРЕС</translation>
    </message>
    <message>
        <location filename="../window.py" line="1526"/>
        <source>CONTROLLER</source>
        <translation>КОНТРОЛЛЕР</translation>
    </message>
    <message>
        <location filename="../window.py" line="1527"/>
        <source>PARAMETERS</source>
        <translation>ПАРАМЕТРЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1530"/>
        <source>POD SELECTOR</source>
        <translation>СЕЛЕКТОР ПОДОВ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1531"/>
        <source>POLICY TYPES</source>
        <translation>ТИПЫ ПОЛИТИКИ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1534"/>
        <location filename="../window.py" line="1538"/>
        <source>DATA</source>
        <translation>ДАННЫЕ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1541"/>
        <source>USAGE</source>
        <translation>ИСПОЛЬЗОВАНИЕ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1544"/>
        <source>TYPES</source>
        <translation>ТИПЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1547"/>
        <source>REFERENCE</source>
        <translation>ССЫЛКА</translation>
    </message>
    <message>
        <location filename="../window.py" line="1548"/>
        <source>MIN PODS</source>
        <translation>МИН. ПОДОВ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1549"/>
        <source>MAX PODS</source>
        <translation>МАКС. ПОДОВ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1550"/>
        <source>REPLICAS</source>
        <translation>РЕПЛИКИ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <source>MIN AVAILABLE</source>
        <translation>МИН. ДОСТУПНО</translation>
    </message>
    <message>
        <location filename="../window.py" line="1554"/>
        <source>MAX UNAVAILABLE</source>
        <translation>МАКС. НЕДОСТУПНО</translation>
    </message>
    <message>
        <location filename="../window.py" line="1555"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>ДОПУСТИМЫЕ ПРЕРЫВАНИЯ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1558"/>
        <source>VALUE</source>
        <translation>ЗНАЧЕНИЕ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1559"/>
        <source>GLOBAL DEFAULT</source>
        <translation>ГЛОБАЛЬНО ПО УМОЛЧАНИЮ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1562"/>
        <source>HANDLER</source>
        <translation>HANDLER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1565"/>
        <source>HOLDER</source>
        <translation>ДЕРЖАТЕЛЬ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1568"/>
        <location filename="../window.py" line="1571"/>
        <source>WEBHOOKS</source>
        <translation>WEBHOOKS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1574"/>
        <location filename="../window.py" line="1581"/>
        <location filename="../window.py" line="1604"/>
        <location filename="../ui/main_window.ui" line="2054"/>
        <location filename="../ui/main_window.ui" line="2578"/>
        <source>STATUS</source>
        <translation>СТАТУС</translation>
    </message>
    <message>
        <location filename="../window.py" line="1575"/>
        <source>INSTANCE TYPES</source>
        <translation>ТИПЫ ЭКЗЕМПЛЯРОВ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>NODES</source>
        <translation>УЗЛЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1577"/>
        <source>AMI TYPE</source>
        <translation>ТИП AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1578"/>
        <source>AMI VERSION</source>
        <translation>ВЕРСИЯ AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1582"/>
        <location filename="../ui/main_window.ui" line="2588"/>
        <source>VERSION</source>
        <translation>ВЕРСИЯ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1583"/>
        <source>SOURCE</source>
        <translation>ИСТОЧНИК</translation>
    </message>
    <message>
        <location filename="../window.py" line="1593"/>
        <source>COMPLETIONS</source>
        <translation>ЗАВЕРШЕНИЯ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1594"/>
        <source>SCHEDULE</source>
        <translation>РАСПИСАНИЕ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1595"/>
        <location filename="../ui/main_window.ui" line="2049"/>
        <source>READY</source>
        <translation>ГОТОВО</translation>
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
        <translation>ИМЯ</translation>
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
        <translation>ПАМЯТЬ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1607"/>
        <source>RESTARTS</source>
        <translation>ПЕРЕЗАПУСКИ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <location filename="../window.py" line="1620"/>
        <location filename="../ui/main_window.ui" line="2059"/>
        <location filename="../ui/main_window.ui" line="2608"/>
        <source>AGE</source>
        <translation>ВОЗРАСТ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1617"/>
        <location filename="../ui/main_window.ui" line="2039"/>
        <source>KIND</source>
        <translation>ВИД</translation>
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
        <translation>Консоль Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="339"/>
        <source>CONTEXT</source>
        <translation>КОНТЕКСТ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>Контекст Kubernetes из вашего kubeconfig</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="372"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>Войдите через облачный CLI, затем перезагрузите данные кластера</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="375"/>
        <source>Sign in</source>
        <translation>Войти</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="397"/>
        <source>Settings</source>
        <translation>Настройки</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="437"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>В вашем kubeconfig не найдено контекстов кластера. Добавьте кластер в kubeconfig (например, через AWS CLI: aws eks update-kubeconfig) и перезагрузите.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="478"/>
        <source>Dismiss</source>
        <translation>Скрыть</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="569"/>
        <source>MONITORING</source>
        <translation>МОНИТОРИНГ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1745"/>
        <source>Overview</source>
        <translation>Обзор</translation>
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
        <location filename="../ui/main_window.ui" line="721"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="752"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="783"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="814"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="845"/>
        <location filename="../ui/main_window.ui" line="1963"/>
        <source>Pods</source>
        <translation>Pods</translation>
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
        <location filename="../ui/main_window.ui" line="938"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="972"/>
        <source>Network</source>
        <translation>Сеть</translation>
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
        <location filename="../ui/main_window.ui" line="1086"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1117"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1148"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1179"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1213"/>
        <source>Config</source>
        <translation>Конфигурация</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1265"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1296"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1327"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1358"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1389"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1420"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
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
        <location filename="../ui/main_window.ui" line="1513"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1544"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1575"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1606"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1640"/>
        <source>Details &amp;&amp; Logs</source>
        <translation>Детали &amp;&amp; Журналы</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1696"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>БЕЗОПАСНЫЙ ДОСТУП
Ресурсы в режиме только чтения</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1752"/>
        <source>Cluster resources and capacity</source>
        <translation>Ресурсы и ёмкость кластера</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1777"/>
        <location filename="../ui/main_window.ui" line="1790"/>
        <location filename="../ui/main_window.ui" line="1803"/>
        <source>Refresh</source>
        <translation>Обновить</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1909"/>
        <source>Search by name or namespace...</source>
        <translation>Поиск по имени или namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1960"/>
        <source>View Pods of the selected workload</source>
        <translation>Показать Pods выбранного workload</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1976"/>
        <source>View JSON details of the selected workload</source>
        <translation>Показать JSON-детали выбранного workload</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1979"/>
        <source>Details</source>
        <translation>Детали</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1992"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Показать журналы Pod выбранного workload</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1995"/>
        <source>Logs</source>
        <translation>Журналы</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2538"/>
        <source>Nodes</source>
        <translation>Узлы</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2573"/>
        <source>NODE</source>
        <translation>УЗЕЛ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2583"/>
        <source>ROLE</source>
        <translation>РОЛЬ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2603"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2621"/>
        <source>Select a context to load workloads</source>
        <translation>Выберите контекст, чтобы загрузить workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2644"/>
        <source>Data fetched from the cluster API</source>
        <translation>Данные получены из API кластера</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2705"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>Открыть сайт DCO Tecnologia</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2725"/>
        <source>MIT License</source>
        <translation>Лицензия MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2728"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope — программное обеспечение с открытым исходным кодом под лицензией MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Update available</source>
        <translation>Доступно обновление</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2767"/>
        <source>Open the download page of the new version</source>
        <translation>Открыть страницу загрузки новой версии</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2795"/>
        <source>Check for updates</source>
        <translation>Проверить обновления</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2815"/>
        <source>Open the project on GitHub</source>
        <translation>Открыть проект на GitHub</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="1998"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>узлов готово</translation>
    </message>
    <message>
        <location filename="../window.py" line="2014"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>ядер запрошено / доступно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2028"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>запрошено / доступно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2047"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>в кластере</translation>
    </message>
    <message>
        <location filename="../window.py" line="2049"/>
        <location filename="../ui/overview_page.ui" line="510"/>
        <location filename="../ui/overview_page.ui" line="564"/>
        <location filename="../ui/overview_page.ui" line="618"/>
        <source>workloads</source>
        <translation>workloads</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="29"/>
        <source>Cluster resources</source>
        <translation>Ресурсы кластера</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="78"/>
        <source>CLUSTER INFO</source>
        <translation>О КЛАСТЕРЕ</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="125"/>
        <source>NETWORKING</source>
        <translation>СЕТЬ</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="174"/>
        <source>NODES</source>
        <translation>УЗЛЫ</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="228"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="248"/>
        <source>running / capacity</source>
        <translation>запущено / ёмкость</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="295"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="362"/>
        <source>MEMORY</source>
        <translation>ПАМЯТЬ</translation>
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
        <translation>ИМЯ</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>ГОТОВО</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>ФАЗА</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>КОНТЕЙНЕРЫ</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>ВОЗРАСТ</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>Детали Pod</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>Показать журналы</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>Закрыть</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="3038"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>Задайте контекстам понятные имена. Оставьте имя пустым, чтобы сохранить исходное.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>Сохранить изменения</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>ОБЩИЕ</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="107"/>
        <source>Language</source>
        <translation>Язык</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="142"/>
        <source>Theme</source>
        <translation>Тема</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="177"/>
        <source>New theme...</source>
        <translation>Новая тема...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>Изменить тему...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>Открыть папку тем</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>Namespace по умолчанию</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>Namespace, в котором открывается каждый контекст. Оставьте пустым, чтобы показывать все.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>Запоминать последний использованный контекст</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>Проверять новую версию на GitHub при запуске приложения</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>Запрашивает у публичного API GitHub последний релиз и отправляет только версию приложения. Значок в нижней панели проверяет по запросу.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>Режим отладки: записывать файл журнала, которым можно поделиться</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>Открыть папку журналов</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>Очистить кеш</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>Забывает уже загруженные списки и обзоры, а также вход в каждый кластер, поэтому следующий запрос снова выполнит вход и загрузит всё заново. Ваши настройки сохраняются.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>ФАЙЛЫ KUBECONFIG</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>KubeScope читает файлы из переменной KUBECONFIG или ~/.kube/config. Добавьте файлы здесь, чтобы читать их вместо этого. Нажмите «Сохранить», чтобы применить.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>Добавить файл...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>Удалить</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>КОМАНДЫ ВХОДА</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>Для облака, которого KubeScope не знает, укажите программу, которую ваш kubeconfig использует для входа (например, oci), и команду входа (например, oci session authenticate). Кнопка «Войти» запустит её без оболочки. Нажмите «Сохранить», чтобы применить.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>ПРОГРАММА</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>КОМАНДА ВХОДА</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>Добавить строку</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>ИМЕНА КОНТЕКСТОВ</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>КОНТЕКСТ</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>ОТОБРАЖАЕМОЕ ИМЯ</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>Фон страницы</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>Панели и карточки</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>Чередующиеся панели</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>Дорожки индикаторов</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>Границы</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>Верхняя панель</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>Логотип верхней панели</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>Селектор верхней панели</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>Граница селектора верхней панели</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>Выделение верхней панели</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>Текст верхней панели</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>Текст</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>Заголовок боковой панели</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>Вторичный текст</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>Отключённый текст</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>Акцентный текст и ссылки</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>Акцентные кнопки</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>Акцентные кнопки при наведении</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>Акцентные кнопки в отключённом состоянии</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>Фокус и выделение</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>Текст значка</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>Акцентный оттенок</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>Выделение текста</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>Акцентная граница</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>Текст на верхней панели и акцентных кнопках</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>Текст «исправно»</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>Фон «исправно»</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>Текст предупреждения</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>Фон предупреждения</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>Текст сбоя</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>Фон сбоя</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>Текст «простаивает»</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>Фон «простаивает»</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>Строка с проблемой</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>Строка нового Pod</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>Индикатор использования: заполняется</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>Индикатор использования: почти заполнен</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>Индикатор здоровья: исправно</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>Индикатор здоровья: предупреждение</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>Индикатор здоровья: сбой</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>Новая тема</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>Изменить тему: {name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>Название темы</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>Светлая</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>Тёмная</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>Название</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>Основа</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>Цвета</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>Сохранить содержимое этой вкладки в файл</translation>
    </message>
</context>
<context>
    <name>WorkloadWindow</name>
    <message>
        <location filename="../window.py" line="707"/>
        <source>0 Deployments</source>
        <translation>0 Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="723"/>
        <location filename="../window.py" line="2267"/>
        <location filename="../window.py" line="2290"/>
        <location filename="../window.py" line="3276"/>
        <source>All namespaces</source>
        <translation>Все namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="834"/>
        <source>Loading contexts...</source>
        <translation>Загрузка контекстов...</translation>
    </message>
    <message>
        <location filename="../window.py" line="843"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>Не удалось загрузить kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="865"/>
        <source>No contexts found in kubeconfig</source>
        <translation>В kubeconfig не найдено контекстов</translation>
    </message>
    <message>
        <location filename="../window.py" line="894"/>
        <location filename="../window.py" line="972"/>
        <source>Unpin from the top</source>
        <translation>Открепить сверху</translation>
    </message>
    <message>
        <location filename="../window.py" line="894"/>
        <source>Pin to the top</source>
        <translation>Закрепить сверху</translation>
    </message>
    <message>
        <location filename="../window.py" line="1021"/>
        <source>Status</source>
        <translation>Статус</translation>
    </message>
    <message>
        <location filename="../window.py" line="1022"/>
        <source>Kubernetes version</source>
        <translation>Версия Kubernetes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1023"/>
        <source>Platform version</source>
        <translation>Версия платформы</translation>
    </message>
    <message>
        <location filename="../window.py" line="1024"/>
        <source>Created</source>
        <translation>Создан</translation>
    </message>
    <message>
        <location filename="../window.py" line="1025"/>
        <source>Provider</source>
        <translation>Провайдер</translation>
    </message>
    <message>
        <location filename="../window.py" line="1028"/>
        <source>API server endpoint</source>
        <translation>Endpoint API-сервера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1029"/>
        <source>Cluster ARN</source>
        <translation>ARN кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1030"/>
        <source>Cluster IAM role ARN</source>
        <translation>ARN IAM-роли кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1031"/>
        <source>OpenID Connect provider URL</source>
        <translation>URL провайдера OpenID Connect</translation>
    </message>
    <message>
        <location filename="../window.py" line="1039"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1040"/>
        <source>Cluster security group</source>
        <translation>Security group кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1042"/>
        <source>Additional security groups</source>
        <translation>Дополнительные security groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1043"/>
        <source>None</source>
        <translation>Нет</translation>
    </message>
    <message>
        <location filename="../window.py" line="1046"/>
        <source>API server endpoint access</source>
        <translation>Доступ к endpoint API-сервера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1049"/>
        <source>Cluster IP address family</source>
        <translation>Семейство IP-адресов кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1050"/>
        <source>Service IPv4 range</source>
        <translation>Диапазон IPv4 сервисов</translation>
    </message>
    <message>
        <location filename="../window.py" line="1052"/>
        <source>Public access source allowlist</source>
        <translation>Список источников с публичным доступом</translation>
    </message>
    <message>
        <location filename="../window.py" line="1055"/>
        <source>Subnets</source>
        <translation>Subnets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1065"/>
        <location filename="../window.py" line="2499"/>
        <source>Active</source>
        <translation>Активен</translation>
    </message>
    <message>
        <location filename="../window.py" line="1066"/>
        <source>Creating</source>
        <translation>Создаётся</translation>
    </message>
    <message>
        <location filename="../window.py" line="1067"/>
        <source>Updating</source>
        <translation>Обновляется</translation>
    </message>
    <message>
        <location filename="../window.py" line="1068"/>
        <source>Deleting</source>
        <translation>Удаляется</translation>
    </message>
    <message>
        <location filename="../window.py" line="1069"/>
        <location filename="../window.py" line="2492"/>
        <source>Degraded</source>
        <translation>Ухудшен</translation>
    </message>
    <message>
        <location filename="../window.py" line="1070"/>
        <location filename="../window.py" line="2438"/>
        <location filename="../window.py" line="2496"/>
        <source>Failed</source>
        <translation>Сбой</translation>
    </message>
    <message>
        <location filename="../window.py" line="1071"/>
        <source>Creation failed</source>
        <translation>Сбой создания</translation>
    </message>
    <message>
        <location filename="../window.py" line="1072"/>
        <source>Update failed</source>
        <translation>Сбой обновления</translation>
    </message>
    <message>
        <location filename="../window.py" line="1073"/>
        <source>Deletion failed</source>
        <translation>Сбой удаления</translation>
    </message>
    <message>
        <location filename="../window.py" line="1074"/>
        <location filename="../window.py" line="2436"/>
        <location filename="../window.py" line="2497"/>
        <source>Pending</source>
        <translation>Ожидание</translation>
    </message>
    <message>
        <location filename="../window.py" line="1075"/>
        <source>Deployed</source>
        <translation>Развёрнут</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Superseded</source>
        <translation>Заменён</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>Uninstalled</source>
        <translation>Удалён</translation>
    </message>
    <message>
        <location filename="../window.py" line="1078"/>
        <source>Uninstalling</source>
        <translation>Удаляется</translation>
    </message>
    <message>
        <location filename="../window.py" line="1079"/>
        <source>Pending install</source>
        <translation>Установка ожидает</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>Pending upgrade</source>
        <translation>Обновление ожидает</translation>
    </message>
    <message>
        <location filename="../window.py" line="1081"/>
        <source>Pending rollback</source>
        <translation>Откат ожидает</translation>
    </message>
    <message>
        <location filename="../window.py" line="1082"/>
        <source>Public</source>
        <translation>Публичный</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>Private</source>
        <translation>Приватный</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Public and private</source>
        <translation>Публичный и приватный</translation>
    </message>
    <message>
        <location filename="../window.py" line="1177"/>
        <source>Overview</source>
        <translation>Обзор</translation>
    </message>
    <message>
        <location filename="../window.py" line="1178"/>
        <source>Cluster resources and capacity</source>
        <translation>Ресурсы и ёмкость кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1180"/>
        <source>Details &amp; Logs</source>
        <translation>Детали и журналы</translation>
    </message>
    <message>
        <location filename="../window.py" line="1182"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Детали ресурсов и журналы Pod, по вкладке на каждый</translation>
    </message>
    <message>
        <location filename="../window.py" line="1185"/>
        <source>Settings</source>
        <translation>Настройки</translation>
    </message>
    <message>
        <location filename="../window.py" line="1186"/>
        <source>Preferences and context names</source>
        <translation>Настройки и имена контекстов</translation>
    </message>
    <message>
        <location filename="../window.py" line="1188"/>
        <source>Workloads overview</source>
        <translation>Обзор workloads</translation>
    </message>
    <message>
        <location filename="../window.py" line="1190"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>Состояние каждого вида workload и последние события</translation>
    </message>
    <message>
        <location filename="../window.py" line="1194"/>
        <location filename="../window.py" line="1845"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="1194"/>
        <source>Pods of the cluster</source>
        <translation>Pods кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1196"/>
        <location filename="../window.py" line="1846"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="1197"/>
        <source>Deployments of the cluster</source>
        <translation>Deployments кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1200"/>
        <location filename="../window.py" line="1848"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1201"/>
        <source>StatefulSets of the cluster</source>
        <translation>StatefulSets кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1204"/>
        <location filename="../window.py" line="1847"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1205"/>
        <source>DaemonSets of the cluster</source>
        <translation>DaemonSets кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1208"/>
        <location filename="../window.py" line="1849"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1209"/>
        <source>ReplicaSets of the cluster</source>
        <translation>ReplicaSets кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1212"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1213"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>ReplicationControllers кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1215"/>
        <location filename="../window.py" line="1850"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1215"/>
        <source>Jobs of the cluster</source>
        <translation>Jobs кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1216"/>
        <location filename="../window.py" line="1851"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1216"/>
        <source>CronJobs of the cluster</source>
        <translation>CronJobs кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1217"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1217"/>
        <source>Services of the cluster</source>
        <translation>Services кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1219"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1220"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>Endpoint Slices кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1223"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1224"/>
        <source>Endpoints of the cluster</source>
        <translation>Endpoints кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1227"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1228"/>
        <source>Ingresses of the cluster</source>
        <translation>Ingresses кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1231"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1232"/>
        <source>Ingress Classes of the cluster</source>
        <translation>Ingress Classes кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1235"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1236"/>
        <source>Network Policies of the cluster</source>
        <translation>Network Policies кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1239"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1240"/>
        <source>Config Maps of the cluster</source>
        <translation>Config Maps кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1243"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1244"/>
        <source>Secrets of the cluster</source>
        <translation>Secrets кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1247"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1248"/>
        <source>Resource Quotas of the cluster</source>
        <translation>Resource Quotas кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1251"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1252"/>
        <source>Limit Ranges of the cluster</source>
        <translation>Limit Ranges кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1255"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1256"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>Horizontal Pod Autoscalers кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1259"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1260"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>Pod Disruption Budgets кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1263"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1264"/>
        <source>Priority Classes of the cluster</source>
        <translation>Priority Classes кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1267"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>Runtime Classes of the cluster</source>
        <translation>Runtime Classes кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1271"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Leases of the cluster</source>
        <translation>Leases кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1275"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1276"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>Mutating Webhook Configurations кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1279"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1280"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>Validating Webhook Configurations кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1283"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1284"/>
        <source>Node Groups of the cluster</source>
        <translation>Node Groups кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1287"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1288"/>
        <source>Add-ons of the cluster</source>
        <translation>Add-ons кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1297"/>
        <source>Version {version}</source>
        <translation>Версия {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1300"/>
        <source>Open the project on GitHub</source>
        <translation>Открыть проект на GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="1334"/>
        <source>Up to date</source>
        <translation>Актуальная версия</translation>
    </message>
    <message>
        <location filename="../window.py" line="1335"/>
        <source>Could not check</source>
        <translation>Не удалось проверить</translation>
    </message>
    <message>
        <location filename="../window.py" line="1346"/>
        <source>Check for updates</source>
        <translation>Проверить обновления</translation>
    </message>
    <message>
        <location filename="../window.py" line="1347"/>
        <source>Checking for updates...</source>
        <translation>Проверка обновлений...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1348"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope актуален. Нажмите, чтобы проверить снова.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1349"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>Не удалось проверить обновления. Нажмите, чтобы повторить.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1355"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>Доступно обновление: {version}. Нажмите, чтобы открыть страницу загрузки; правая кнопка — проверить снова.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1363"/>
        <source>Update available</source>
        <translation>Доступно обновление</translation>
    </message>
    <message>
        <location filename="../window.py" line="1365"/>
        <source>Download KubeScope {version}</source>
        <translation>Скачать KubeScope {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1401"/>
        <source>Check for updates again</source>
        <translation>Проверить обновления ещё раз</translation>
    </message>
    <message>
        <location filename="../window.py" line="1499"/>
        <location filename="../window.py" line="2174"/>
        <source>Loading resources...</source>
        <translation>Загрузка ресурсов...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1743"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Настроить учётные данные AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1747"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>Учётные данные AWS для профиля {profile} отсутствуют или недействительны</translation>
    </message>
    <message>
        <location filename="../window.py" line="1752"/>
        <source>Sign in to {provider}</source>
        <translation>Войти в {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1755"/>
        <source>Not signed in to {provider}</source>
        <translation>Вход в {provider} не выполнен</translation>
    </message>
    <message>
        <location filename="../window.py" line="1759"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>Войти в {provider} ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1765"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>Вход в {provider} не выполнен (профиль {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1786"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Завершите в открывшемся терминале, затем нажмите «Обновить».</translation>
    </message>
    <message>
        <location filename="../window.py" line="1805"/>
        <source>Loading workloads...</source>
        <translation>Загрузка workloads...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1866"/>
        <source>Could not read: {names}</source>
        <translation>Не удалось прочитать: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1926"/>
        <source>Loading cluster data...</source>
        <translation>Загрузка данных кластера...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2007"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>запущено · ожидает: {pending} · сбоев: {failed}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2016"/>
        <location filename="../window.py" line="2030"/>
        <source> · usage {value}</source>
        <translation> · использование {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2054"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Реальное использование недоступно: metrics-server не найден.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <source>Ready</source>
        <translation>Готов</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <source>Not ready</source>
        <translation>Не готов</translation>
    </message>
    <message>
        <location filename="../window.py" line="2191"/>
        <source>Refreshing...</source>
        <translation>Обновление...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2382"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>Services: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2384"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>Endpoint Slices: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2387"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>Endpoints: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2390"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>Ingresses: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2392"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>Ingress Classes в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2394"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>Network Policies: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2397"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>Config Maps: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2399"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>Secrets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2401"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>Resource Quotas: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2404"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>Limit Ranges: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2407"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>Horizontal Pod Autoscalers: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2410"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>Pod Disruption Budgets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2412"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>Leases: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2414"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>Priority Classes в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2416"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>Runtime Classes в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2418"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>Mutating Webhook Configurations в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2421"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>Validating Webhook Configurations в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2423"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>Node Groups в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2424"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>Add-ons в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2435"/>
        <location filename="../window.py" line="2501"/>
        <source>Running</source>
        <translation>Выполняется</translation>
    </message>
    <message>
        <location filename="../window.py" line="2437"/>
        <source>Succeeded</source>
        <translation>Завершён успешно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2439"/>
        <source>Unknown</source>
        <translation>Неизвестно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2483"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>Pods: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2491"/>
        <source>Healthy</source>
        <translation>Исправно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2493"/>
        <source>Unavailable</source>
        <translation>Недоступно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2494"/>
        <source>Scaled to zero</source>
        <translation>Масштабировано до нуля</translation>
    </message>
    <message>
        <location filename="../window.py" line="2495"/>
        <source>Complete</source>
        <translation>Завершено</translation>
    </message>
    <message>
        <location filename="../window.py" line="2498"/>
        <source>Suspended</source>
        <translation>Приостановлено</translation>
    </message>
    <message>
        <location filename="../window.py" line="2500"/>
        <source>Scheduled</source>
        <translation>Запланировано</translation>
    </message>
    <message>
        <location filename="../window.py" line="2545"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>Deployments: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2548"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>StatefulSets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2551"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>DaemonSets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2554"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>ReplicaSets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2557"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>ReplicationControllers: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2559"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>Jobs: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2560"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>CronJobs: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2584"/>
        <source>{visible} of {total} Pods</source>
        <translation>Pods: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2585"/>
        <source>{visible} of {total} Deployments</source>
        <translation>Deployments: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2586"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>StatefulSets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2587"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>DaemonSets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2588"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>ReplicaSets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2590"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>ReplicationControllers: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2592"/>
        <source>{visible} of {total} Jobs</source>
        <translation>Jobs: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2593"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>CronJobs: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2594"/>
        <source>{visible} of {total} Services</source>
        <translation>Services: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2595"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>Endpoint Slices: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2596"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>Endpoints: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2597"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>Ingresses: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2598"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>Ingress Classes: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2599"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>Network Policies: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2600"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>Config Maps: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2601"/>
        <source>{visible} of {total} Secrets</source>
        <translation>Secrets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2602"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>Resource Quotas: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2603"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>Limit Ranges: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2605"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2608"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2610"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>Priority Classes: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2611"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>Runtime Classes: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2612"/>
        <source>{visible} of {total} Leases</source>
        <translation>Leases: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2614"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2617"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2619"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>Node Groups: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2620"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>Add-ons: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2666"/>
        <source>Loading...</source>
        <translation>Загрузка...</translation>
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
        <translation>Pods для {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2760"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods в {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2825"/>
        <source>No Pods are associated with this workload</source>
        <translation>С этим workload не связано ни одного Pod</translation>
    </message>
    <message>
        <location filename="../window.py" line="2832"/>
        <location filename="../window.py" line="2855"/>
        <source>Logs</source>
        <translation>Журналы</translation>
    </message>
    <message>
        <location filename="../window.py" line="2832"/>
        <source>This workload has no Pods.</source>
        <translation>У этого workload нет Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2841"/>
        <location filename="../window.py" line="2864"/>
        <source>View logs</source>
        <translation>Показать журналы</translation>
    </message>
    <message>
        <location filename="../window.py" line="2842"/>
        <source>Select the Pod:</source>
        <translation>Выберите Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2856"/>
        <source>Pod {name} has no containers.</source>
        <translation>У Pod {name} нет контейнеров.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2865"/>
        <source>Select the container of {name}:</source>
        <translation>Выберите контейнер для {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2891"/>
        <source>Save to a file</source>
        <translation>Сохранить в файл</translation>
    </message>
    <message>
        <location filename="../window.py" line="2902"/>
        <source>Could not save</source>
        <translation>Не удалось сохранить</translation>
    </message>
    <message>
        <location filename="../window.py" line="2903"/>
        <source>The file could not be written: {reason}</source>
        <translation>Не удалось записать файл: {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2951"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Журналы: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3001"/>
        <source>Automatic</source>
        <translation>Автоматически</translation>
    </message>
    <message>
        <location filename="../window.py" line="3014"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>По умолчанию выключено. Когда включено, KubeScope записывает свои действия (но не журналы Pod и не содержимое ресурсов) в {path}. Прочитайте файл, прежде чем делиться: в нём есть имена контекстов.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3045"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>В kubeconfig не найдено контекстов.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3074"/>
        <source>Choose a kubeconfig file</source>
        <translation>Выберите файл kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="3120"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>Команда входа в строке {row} недействительна.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3133"/>
        <source>Light</source>
        <translation>Светлая</translation>
    </message>
    <message>
        <location filename="../window.py" line="3133"/>
        <source>Dark</source>
        <translation>Тёмная</translation>
    </message>
    <message>
        <location filename="../window.py" line="3152"/>
        <source>My theme</source>
        <translation>Моя тема</translation>
    </message>
    <message>
        <location filename="../window.py" line="3196"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>Кеш очищен. Всё загрузится заново, когда понадобится.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3251"/>
        <source>Settings saved.</source>
        <translation>Настройки сохранены.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3290"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>Вашему пользователю не разрешено: {action}. Обратитесь к администратору кластера за доступом.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3295"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>Вашему пользователю это не разрешено. Обратитесь к администратору кластера за доступом.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3314"/>
        <source>Query failed</source>
        <translation>Запрос не выполнен</translation>
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
        <translation>События</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="293"/>
        <source>TYPE</source>
        <translation>ТИП</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="298"/>
        <source>SOURCE</source>
        <translation>ИСТОЧНИК</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>INVOLVED OBJECT</source>
        <translation>СВЯЗАННЫЙ ОБЪЕКТ</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>MESSAGE</source>
        <translation>СООБЩЕНИЕ</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>COUNT</source>
        <translation>КОЛИЧЕСТВО</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>AGE</source>
        <translation>ВОЗРАСТ</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>LAST SEEN</source>
        <translation>ПОСЛЕДНЕЕ</translation>
    </message>
</context>
</TS>
