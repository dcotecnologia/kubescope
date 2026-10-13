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
        <location filename="../log_tab.py" line="46"/>
        <source>No log lines returned.</source>
        <translation>Строки журнала не получены.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="51"/>
        <source>Updated at {time}</source>
        <translation>Обновлено в {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="58"/>
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
        <location filename="../window.py" line="1540"/>
        <location filename="../window.py" line="1569"/>
        <source>TYPE</source>
        <translation>ТИП</translation>
    </message>
    <message>
        <location filename="../window.py" line="1541"/>
        <source>CLUSTER IP</source>
        <translation>CLUSTER IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1542"/>
        <source>EXTERNAL IP</source>
        <translation>EXTERNAL IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1543"/>
        <location filename="../window.py" line="1547"/>
        <location filename="../window.py" line="1555"/>
        <source>PORTS</source>
        <translation>ПОРТЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1546"/>
        <source>ADDRESS TYPE</source>
        <translation>ТИП АДРЕСА</translation>
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
        <translation>КЛАСС</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <source>HOSTS</source>
        <translation>ХОСТЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1554"/>
        <source>ADDRESS</source>
        <translation>АДРЕС</translation>
    </message>
    <message>
        <location filename="../window.py" line="1558"/>
        <source>CONTROLLER</source>
        <translation>КОНТРОЛЛЕР</translation>
    </message>
    <message>
        <location filename="../window.py" line="1559"/>
        <source>PARAMETERS</source>
        <translation>ПАРАМЕТРЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1562"/>
        <source>POD SELECTOR</source>
        <translation>СЕЛЕКТОР ПОДОВ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1563"/>
        <source>POLICY TYPES</source>
        <translation>ТИПЫ ПОЛИТИКИ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1566"/>
        <location filename="../window.py" line="1570"/>
        <source>DATA</source>
        <translation>ДАННЫЕ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1573"/>
        <source>USAGE</source>
        <translation>ИСПОЛЬЗОВАНИЕ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>TYPES</source>
        <translation>ТИПЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1579"/>
        <source>REFERENCE</source>
        <translation>ССЫЛКА</translation>
    </message>
    <message>
        <location filename="../window.py" line="1580"/>
        <source>MIN PODS</source>
        <translation>МИН. ПОДОВ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1581"/>
        <source>MAX PODS</source>
        <translation>МАКС. ПОДОВ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1582"/>
        <source>REPLICAS</source>
        <translation>РЕПЛИКИ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1585"/>
        <source>MIN AVAILABLE</source>
        <translation>МИН. ДОСТУПНО</translation>
    </message>
    <message>
        <location filename="../window.py" line="1586"/>
        <source>MAX UNAVAILABLE</source>
        <translation>МАКС. НЕДОСТУПНО</translation>
    </message>
    <message>
        <location filename="../window.py" line="1587"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>ДОПУСТИМЫЕ ПРЕРЫВАНИЯ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1590"/>
        <source>VALUE</source>
        <translation>ЗНАЧЕНИЕ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1591"/>
        <source>GLOBAL DEFAULT</source>
        <translation>ГЛОБАЛЬНО ПО УМОЛЧАНИЮ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1594"/>
        <source>HANDLER</source>
        <translation>HANDLER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1597"/>
        <source>HOLDER</source>
        <translation>ДЕРЖАТЕЛЬ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1600"/>
        <location filename="../window.py" line="1603"/>
        <source>WEBHOOKS</source>
        <translation>WEBHOOKS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1606"/>
        <location filename="../window.py" line="1613"/>
        <location filename="../window.py" line="1636"/>
        <location filename="../ui/main_window.ui" line="2023"/>
        <location filename="../ui/main_window.ui" line="2547"/>
        <source>STATUS</source>
        <translation>СТАТУС</translation>
    </message>
    <message>
        <location filename="../window.py" line="1607"/>
        <source>INSTANCE TYPES</source>
        <translation>ТИПЫ ЭКЗЕМПЛЯРОВ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <source>NODES</source>
        <translation>УЗЛЫ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1609"/>
        <source>AMI TYPE</source>
        <translation>ТИП AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1610"/>
        <source>AMI VERSION</source>
        <translation>ВЕРСИЯ AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1614"/>
        <location filename="../ui/main_window.ui" line="2557"/>
        <source>VERSION</source>
        <translation>ВЕРСИЯ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1615"/>
        <source>SOURCE</source>
        <translation>ИСТОЧНИК</translation>
    </message>
    <message>
        <location filename="../window.py" line="1625"/>
        <source>COMPLETIONS</source>
        <translation>ЗАВЕРШЕНИЯ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1626"/>
        <source>SCHEDULE</source>
        <translation>РАСПИСАНИЕ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1627"/>
        <location filename="../ui/main_window.ui" line="2018"/>
        <source>READY</source>
        <translation>ГОТОВО</translation>
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
        <translation>ИМЯ</translation>
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
        <translation>ПАМЯТЬ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1639"/>
        <source>RESTARTS</source>
        <translation>ПЕРЕЗАПУСКИ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1640"/>
        <location filename="../window.py" line="1652"/>
        <location filename="../ui/main_window.ui" line="2028"/>
        <location filename="../ui/main_window.ui" line="2577"/>
        <source>AGE</source>
        <translation>ВОЗРАСТ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1649"/>
        <location filename="../ui/main_window.ui" line="2008"/>
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
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1714"/>
        <source>Overview</source>
        <translation>Обзор</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="607"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <source>Cluster</source>
        <translation>Кластер</translation>
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
        <location filename="../ui/main_window.ui" line="1932"/>
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
        <location filename="../ui/main_window.ui" line="1665"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>БЕЗОПАСНЫЙ ДОСТУП
Ресурсы в режиме только чтения</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1721"/>
        <source>Cluster resources and capacity</source>
        <translation>Ресурсы и ёмкость кластера</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1746"/>
        <location filename="../ui/main_window.ui" line="1759"/>
        <location filename="../ui/main_window.ui" line="1772"/>
        <source>Refresh</source>
        <translation>Обновить</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1878"/>
        <source>Search by name or namespace...</source>
        <translation>Поиск по имени или namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1929"/>
        <source>View Pods of the selected workload</source>
        <translation>Показать Pods выбранного workload</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1945"/>
        <source>View JSON details of the selected workload</source>
        <translation>Показать JSON-детали выбранного workload</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1948"/>
        <source>Details</source>
        <translation>Детали</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1961"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Показать журналы Pod выбранного workload</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1964"/>
        <source>Logs</source>
        <translation>Журналы</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2507"/>
        <source>Nodes</source>
        <translation>Узлы</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2542"/>
        <source>NODE</source>
        <translation>УЗЕЛ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2552"/>
        <source>ROLE</source>
        <translation>РОЛЬ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2572"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2590"/>
        <source>Select a context to load workloads</source>
        <translation>Выберите контекст, чтобы загрузить workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2613"/>
        <source>Data fetched from the cluster API</source>
        <translation>Данные получены из API кластера</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2674"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>Открыть сайт DCO Tecnologia</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2694"/>
        <source>MIT License</source>
        <translation>Лицензия MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2697"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope — программное обеспечение с открытым исходным кодом под лицензией MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2733"/>
        <source>Update available</source>
        <translation>Доступно обновление</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2736"/>
        <source>Open the download page of the new version</source>
        <translation>Открыть страницу загрузки новой версии</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Check for updates</source>
        <translation>Проверить обновления</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2784"/>
        <source>Open the project on GitHub</source>
        <translation>Открыть проект на GitHub</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="2030"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>узлов готово</translation>
    </message>
    <message>
        <location filename="../window.py" line="2046"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>ядер запрошено / доступно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2060"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>запрошено / доступно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>в кластере</translation>
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
        <location filename="../window.py" line="3068"/>
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
        <translation>Все namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="832"/>
        <source>Loading contexts...</source>
        <translation>Загрузка контекстов...</translation>
    </message>
    <message>
        <location filename="../window.py" line="841"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>Не удалось загрузить kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="863"/>
        <source>No contexts found in kubeconfig</source>
        <translation>В kubeconfig не найдено контекстов</translation>
    </message>
    <message>
        <location filename="../window.py" line="892"/>
        <location filename="../window.py" line="970"/>
        <source>Unpin from the top</source>
        <translation>Открепить сверху</translation>
    </message>
    <message>
        <location filename="../window.py" line="892"/>
        <source>Pin to the top</source>
        <translation>Закрепить сверху</translation>
    </message>
    <message>
        <location filename="../window.py" line="1008"/>
        <source>Close</source>
        <translation>Закрыть</translation>
    </message>
    <message>
        <location filename="../window.py" line="1055"/>
        <source>Status</source>
        <translation>Статус</translation>
    </message>
    <message>
        <location filename="../window.py" line="1056"/>
        <source>Kubernetes version</source>
        <translation>Версия Kubernetes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1057"/>
        <source>Platform version</source>
        <translation>Версия платформы</translation>
    </message>
    <message>
        <location filename="../window.py" line="1058"/>
        <source>Created</source>
        <translation>Создан</translation>
    </message>
    <message>
        <location filename="../window.py" line="1059"/>
        <source>Provider</source>
        <translation>Провайдер</translation>
    </message>
    <message>
        <location filename="../window.py" line="1062"/>
        <source>API server endpoint</source>
        <translation>Endpoint API-сервера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1063"/>
        <source>Cluster ARN</source>
        <translation>ARN кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1064"/>
        <source>Cluster IAM role ARN</source>
        <translation>ARN IAM-роли кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1065"/>
        <source>OpenID Connect provider URL</source>
        <translation>URL провайдера OpenID Connect</translation>
    </message>
    <message>
        <location filename="../window.py" line="1073"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1074"/>
        <source>Cluster security group</source>
        <translation>Security group кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Additional security groups</source>
        <translation>Дополнительные security groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>None</source>
        <translation>Нет</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>API server endpoint access</source>
        <translation>Доступ к endpoint API-сервера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>Cluster IP address family</source>
        <translation>Семейство IP-адресов кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Service IPv4 range</source>
        <translation>Диапазон IPv4 сервисов</translation>
    </message>
    <message>
        <location filename="../window.py" line="1086"/>
        <source>Public access source allowlist</source>
        <translation>Список источников с публичным доступом</translation>
    </message>
    <message>
        <location filename="../window.py" line="1089"/>
        <source>Subnets</source>
        <translation>Subnets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1099"/>
        <location filename="../window.py" line="2531"/>
        <source>Active</source>
        <translation>Активен</translation>
    </message>
    <message>
        <location filename="../window.py" line="1100"/>
        <source>Creating</source>
        <translation>Создаётся</translation>
    </message>
    <message>
        <location filename="../window.py" line="1101"/>
        <source>Updating</source>
        <translation>Обновляется</translation>
    </message>
    <message>
        <location filename="../window.py" line="1102"/>
        <source>Deleting</source>
        <translation>Удаляется</translation>
    </message>
    <message>
        <location filename="../window.py" line="1103"/>
        <location filename="../window.py" line="2524"/>
        <source>Degraded</source>
        <translation>Ухудшен</translation>
    </message>
    <message>
        <location filename="../window.py" line="1104"/>
        <location filename="../window.py" line="2470"/>
        <location filename="../window.py" line="2528"/>
        <source>Failed</source>
        <translation>Сбой</translation>
    </message>
    <message>
        <location filename="../window.py" line="1105"/>
        <source>Creation failed</source>
        <translation>Сбой создания</translation>
    </message>
    <message>
        <location filename="../window.py" line="1106"/>
        <source>Update failed</source>
        <translation>Сбой обновления</translation>
    </message>
    <message>
        <location filename="../window.py" line="1107"/>
        <source>Deletion failed</source>
        <translation>Сбой удаления</translation>
    </message>
    <message>
        <location filename="../window.py" line="1108"/>
        <location filename="../window.py" line="2468"/>
        <location filename="../window.py" line="2529"/>
        <source>Pending</source>
        <translation>Ожидание</translation>
    </message>
    <message>
        <location filename="../window.py" line="1109"/>
        <source>Deployed</source>
        <translation>Развёрнут</translation>
    </message>
    <message>
        <location filename="../window.py" line="1110"/>
        <source>Superseded</source>
        <translation>Заменён</translation>
    </message>
    <message>
        <location filename="../window.py" line="1111"/>
        <source>Uninstalled</source>
        <translation>Удалён</translation>
    </message>
    <message>
        <location filename="../window.py" line="1112"/>
        <source>Uninstalling</source>
        <translation>Удаляется</translation>
    </message>
    <message>
        <location filename="../window.py" line="1113"/>
        <source>Pending install</source>
        <translation>Установка ожидает</translation>
    </message>
    <message>
        <location filename="../window.py" line="1114"/>
        <source>Pending upgrade</source>
        <translation>Обновление ожидает</translation>
    </message>
    <message>
        <location filename="../window.py" line="1115"/>
        <source>Pending rollback</source>
        <translation>Откат ожидает</translation>
    </message>
    <message>
        <location filename="../window.py" line="1116"/>
        <source>Public</source>
        <translation>Публичный</translation>
    </message>
    <message>
        <location filename="../window.py" line="1117"/>
        <source>Private</source>
        <translation>Приватный</translation>
    </message>
    <message>
        <location filename="../window.py" line="1118"/>
        <source>Public and private</source>
        <translation>Публичный и приватный</translation>
    </message>
    <message>
        <location filename="../window.py" line="1210"/>
        <source>Overview</source>
        <translation>Обзор</translation>
    </message>
    <message>
        <location filename="../window.py" line="1211"/>
        <source>Cluster resources and capacity</source>
        <translation>Ресурсы и ёмкость кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1213"/>
        <source>Details &amp; Logs</source>
        <translation>Детали и журналы</translation>
    </message>
    <message>
        <location filename="../window.py" line="1215"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Детали ресурсов и журналы Pod, по вкладке на каждый</translation>
    </message>
    <message>
        <location filename="../window.py" line="1218"/>
        <source>Settings</source>
        <translation>Настройки</translation>
    </message>
    <message>
        <location filename="../window.py" line="1219"/>
        <source>Preferences and context names</source>
        <translation>Настройки и имена контекстов</translation>
    </message>
    <message>
        <location filename="../window.py" line="1221"/>
        <source>Workloads overview</source>
        <translation>Обзор workloads</translation>
    </message>
    <message>
        <location filename="../window.py" line="1223"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>Состояние каждого вида workload и последние события</translation>
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
        <translation>Pods кластера</translation>
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
        <translation>Deployments кластера</translation>
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
        <translation>StatefulSets кластера</translation>
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
        <translation>DaemonSets кластера</translation>
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
        <translation>ReplicaSets кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1245"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1246"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>ReplicationControllers кластера</translation>
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
        <translation>Jobs кластера</translation>
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
        <translation>CronJobs кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1250"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1250"/>
        <source>Services of the cluster</source>
        <translation>Services кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1252"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1253"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>Endpoint Slices кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1256"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1257"/>
        <source>Endpoints of the cluster</source>
        <translation>Endpoints кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1260"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1261"/>
        <source>Ingresses of the cluster</source>
        <translation>Ingresses кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1264"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1265"/>
        <source>Ingress Classes of the cluster</source>
        <translation>Ingress Classes кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1269"/>
        <source>Network Policies of the cluster</source>
        <translation>Network Policies кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1273"/>
        <source>Config Maps of the cluster</source>
        <translation>Config Maps кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1276"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1277"/>
        <source>Secrets of the cluster</source>
        <translation>Secrets кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1280"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1281"/>
        <source>Resource Quotas of the cluster</source>
        <translation>Resource Quotas кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1284"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1285"/>
        <source>Limit Ranges of the cluster</source>
        <translation>Limit Ranges кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1288"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1289"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>Horizontal Pod Autoscalers кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1292"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1293"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>Pod Disruption Budgets кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1296"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1297"/>
        <source>Priority Classes of the cluster</source>
        <translation>Priority Classes кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1300"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1301"/>
        <source>Runtime Classes of the cluster</source>
        <translation>Runtime Classes кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1304"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1305"/>
        <source>Leases of the cluster</source>
        <translation>Leases кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1308"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1309"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>Mutating Webhook Configurations кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1312"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1313"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>Validating Webhook Configurations кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1316"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1317"/>
        <source>Node Groups of the cluster</source>
        <translation>Node Groups кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1320"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1321"/>
        <source>Add-ons of the cluster</source>
        <translation>Add-ons кластера</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Version {version}</source>
        <translation>Версия {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1333"/>
        <source>Open the project on GitHub</source>
        <translation>Открыть проект на GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="1367"/>
        <source>Up to date</source>
        <translation>Актуальная версия</translation>
    </message>
    <message>
        <location filename="../window.py" line="1368"/>
        <source>Could not check</source>
        <translation>Не удалось проверить</translation>
    </message>
    <message>
        <location filename="../window.py" line="1379"/>
        <source>Check for updates</source>
        <translation>Проверить обновления</translation>
    </message>
    <message>
        <location filename="../window.py" line="1380"/>
        <source>Checking for updates...</source>
        <translation>Проверка обновлений...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1381"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope актуален. Нажмите, чтобы проверить снова.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1382"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>Не удалось проверить обновления. Нажмите, чтобы повторить.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1388"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>Доступно обновление: {version}. Нажмите, чтобы открыть страницу загрузки; правая кнопка — проверить снова.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1396"/>
        <source>Update available</source>
        <translation>Доступно обновление</translation>
    </message>
    <message>
        <location filename="../window.py" line="1398"/>
        <source>Download KubeScope {version}</source>
        <translation>Скачать KubeScope {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1434"/>
        <source>Check for updates again</source>
        <translation>Проверить обновления ещё раз</translation>
    </message>
    <message>
        <location filename="../window.py" line="1531"/>
        <location filename="../window.py" line="2206"/>
        <source>Loading resources...</source>
        <translation>Загрузка ресурсов...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1775"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Настроить учётные данные AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1779"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>Учётные данные AWS для профиля {profile} отсутствуют или недействительны</translation>
    </message>
    <message>
        <location filename="../window.py" line="1784"/>
        <source>Sign in to {provider}</source>
        <translation>Войти в {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1787"/>
        <source>Not signed in to {provider}</source>
        <translation>Вход в {provider} не выполнен</translation>
    </message>
    <message>
        <location filename="../window.py" line="1791"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>Войти в {provider} ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1797"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>Вход в {provider} не выполнен (профиль {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1818"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Завершите в открывшемся терминале, затем нажмите «Обновить».</translation>
    </message>
    <message>
        <location filename="../window.py" line="1837"/>
        <source>Loading workloads...</source>
        <translation>Загрузка workloads...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1898"/>
        <source>Could not read: {names}</source>
        <translation>Не удалось прочитать: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1958"/>
        <source>Loading cluster data...</source>
        <translation>Загрузка данных кластера...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2039"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>запущено · ожидает: {pending} · сбоев: {failed}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2048"/>
        <location filename="../window.py" line="2062"/>
        <source> · usage {value}</source>
        <translation> · использование {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2086"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Реальное использование недоступно: metrics-server не найден.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2111"/>
        <source>Ready</source>
        <translation>Готов</translation>
    </message>
    <message>
        <location filename="../window.py" line="2111"/>
        <source>Not ready</source>
        <translation>Не готов</translation>
    </message>
    <message>
        <location filename="../window.py" line="2223"/>
        <source>Refreshing...</source>
        <translation>Обновление...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2414"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>Services: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2416"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>Endpoint Slices: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2419"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>Endpoints: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2422"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>Ingresses: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2424"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>Ingress Classes в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2426"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>Network Policies: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2429"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>Config Maps: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2431"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>Secrets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2433"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>Resource Quotas: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2436"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>Limit Ranges: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2439"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>Horizontal Pod Autoscalers: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2442"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>Pod Disruption Budgets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2444"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>Leases: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2446"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>Priority Classes в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2448"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>Runtime Classes в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2450"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>Mutating Webhook Configurations в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2453"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>Validating Webhook Configurations в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2455"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>Node Groups в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2456"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>Add-ons в кластере: {count}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2467"/>
        <location filename="../window.py" line="2533"/>
        <source>Running</source>
        <translation>Выполняется</translation>
    </message>
    <message>
        <location filename="../window.py" line="2469"/>
        <source>Succeeded</source>
        <translation>Завершён успешно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2471"/>
        <source>Unknown</source>
        <translation>Неизвестно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2515"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>Pods: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2523"/>
        <source>Healthy</source>
        <translation>Исправно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2525"/>
        <source>Unavailable</source>
        <translation>Недоступно</translation>
    </message>
    <message>
        <location filename="../window.py" line="2526"/>
        <source>Scaled to zero</source>
        <translation>Масштабировано до нуля</translation>
    </message>
    <message>
        <location filename="../window.py" line="2527"/>
        <source>Complete</source>
        <translation>Завершено</translation>
    </message>
    <message>
        <location filename="../window.py" line="2530"/>
        <source>Suspended</source>
        <translation>Приостановлено</translation>
    </message>
    <message>
        <location filename="../window.py" line="2532"/>
        <source>Scheduled</source>
        <translation>Запланировано</translation>
    </message>
    <message>
        <location filename="../window.py" line="2577"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>Deployments: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2580"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>StatefulSets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2583"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>DaemonSets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2586"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>ReplicaSets: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2589"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>ReplicationControllers: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2591"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>Jobs: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2592"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>CronJobs: {count}, namespaces: {namespaces}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2616"/>
        <source>{visible} of {total} Pods</source>
        <translation>Pods: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2617"/>
        <source>{visible} of {total} Deployments</source>
        <translation>Deployments: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2618"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>StatefulSets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2619"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>DaemonSets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2620"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>ReplicaSets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2622"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>ReplicationControllers: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2624"/>
        <source>{visible} of {total} Jobs</source>
        <translation>Jobs: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2625"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>CronJobs: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2626"/>
        <source>{visible} of {total} Services</source>
        <translation>Services: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2627"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>Endpoint Slices: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2628"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>Endpoints: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2629"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>Ingresses: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2630"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>Ingress Classes: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2631"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>Network Policies: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2632"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>Config Maps: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2633"/>
        <source>{visible} of {total} Secrets</source>
        <translation>Secrets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2634"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>Resource Quotas: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2635"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>Limit Ranges: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2637"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2640"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2642"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>Priority Classes: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2643"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>Runtime Classes: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2644"/>
        <source>{visible} of {total} Leases</source>
        <translation>Leases: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2646"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2649"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2651"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>Node Groups: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2652"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>Add-ons: {visible} из {total}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2698"/>
        <source>Loading...</source>
        <translation>Загрузка...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2744"/>
        <location filename="../window.py" line="2836"/>
        <source>Pod: {name}</source>
        <translation>Pod: {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2790"/>
        <source>Pods of {name}</source>
        <translation>Pods для {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2792"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods в {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2857"/>
        <source>No Pods are associated with this workload</source>
        <translation>С этим workload не связано ни одного Pod</translation>
    </message>
    <message>
        <location filename="../window.py" line="2864"/>
        <location filename="../window.py" line="2887"/>
        <source>Logs</source>
        <translation>Журналы</translation>
    </message>
    <message>
        <location filename="../window.py" line="2864"/>
        <source>This workload has no Pods.</source>
        <translation>У этого workload нет Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2873"/>
        <location filename="../window.py" line="2896"/>
        <source>View logs</source>
        <translation>Показать журналы</translation>
    </message>
    <message>
        <location filename="../window.py" line="2874"/>
        <source>Select the Pod:</source>
        <translation>Выберите Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2888"/>
        <source>Pod {name} has no containers.</source>
        <translation>У Pod {name} нет контейнеров.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2897"/>
        <source>Select the container of {name}:</source>
        <translation>Выберите контейнер для {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2923"/>
        <source>Save to a file</source>
        <translation>Сохранить в файл</translation>
    </message>
    <message>
        <location filename="../window.py" line="2934"/>
        <source>Could not save</source>
        <translation>Не удалось сохранить</translation>
    </message>
    <message>
        <location filename="../window.py" line="2935"/>
        <source>The file could not be written: {reason}</source>
        <translation>Не удалось записать файл: {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2981"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Журналы: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3031"/>
        <source>Automatic</source>
        <translation>Автоматически</translation>
    </message>
    <message>
        <location filename="../window.py" line="3044"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>По умолчанию выключено. Когда включено, KubeScope записывает свои действия (но не журналы Pod и не содержимое ресурсов) в {path}. Прочитайте файл, прежде чем делиться: в нём есть имена контекстов.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3075"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>В kubeconfig не найдено контекстов.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3104"/>
        <source>Choose a kubeconfig file</source>
        <translation>Выберите файл kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="3150"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>Команда входа в строке {row} недействительна.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3163"/>
        <source>Light</source>
        <translation>Светлая</translation>
    </message>
    <message>
        <location filename="../window.py" line="3163"/>
        <source>Dark</source>
        <translation>Тёмная</translation>
    </message>
    <message>
        <location filename="../window.py" line="3182"/>
        <source>My theme</source>
        <translation>Моя тема</translation>
    </message>
    <message>
        <location filename="../window.py" line="3226"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>Кеш очищен. Всё загрузится заново, когда понадобится.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3281"/>
        <source>Settings saved.</source>
        <translation>Настройки сохранены.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3320"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>Вашему пользователю не разрешено: {action}. Обратитесь к администратору кластера за доступом.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3325"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>Вашему пользователю это не разрешено. Обратитесь к администратору кластера за доступом.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3344"/>
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
