<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="es">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>Herramienta de inicio de sesión no encontrada</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>Su kubeconfig ejecuta «{tool}» para iniciar sesión, pero no está instalada o no está en el PATH. Instálela y actualice.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>Contexto no encontrado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>Este contexto no está en su kubeconfig. Revise ~/.kube/config.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>Falló la autenticación</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>Sus credenciales pueden haber caducado. Inicie sesión de nuevo (por ejemplo con «aws sso login», «gcloud auth login» o «az login») y actualice.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Not an Amazon EKS cluster</source>
        <translation>No es un clúster de Amazon EKS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Node Groups, Add-ons and the AWS cards of the Overview exist only on Amazon EKS contexts.</source>
        <translation>Node Groups, Add-ons y las tarjetas de AWS de la Vista general existen solo en contextos de Amazon EKS.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="110"/>
        <source>Unexpected answer from AWS</source>
        <translation>Respuesta inesperada de AWS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="111"/>
        <source>Update the AWS CLI to its latest version and refresh.</source>
        <translation>Actualiza la AWS CLI a la última versión y recarga.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="118"/>
        <location filename="../errors.py" line="128"/>
        <source>Access denied</source>
        <translation>Acceso denegado</translation>
    </message>
    <message>
        <location filename="../errors.py" line="119"/>
        <source>Your AWS identity is not allowed to read this. The wiki lists the eks: permissions KubeScope needs.</source>
        <translation>Tu identidad de AWS no tiene permiso para leer esto. La wiki enumera los permisos eks: que KubeScope necesita.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>Su usuario no tiene permiso para leer este recurso.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="143"/>
        <source>No network connection</source>
        <translation>Sin conexión de red</translation>
    </message>
    <message>
        <location filename="../errors.py" line="144"/>
        <source>Check your internet connection or VPN and refresh.</source>
        <translation>Comprueba tu conexión a internet o VPN y actualiza.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="165"/>
        <source>Cluster unreachable</source>
        <translation>Clúster inaccesible</translation>
    </message>
    <message>
        <location filename="../errors.py" line="166"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>Revise su red o VPN y que el clúster esté en ejecución.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="172"/>
        <source>Something went wrong</source>
        <translation>Algo salió mal</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="46"/>
        <source>No log lines returned.</source>
        <translation>No se devolvieron líneas de registro.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="51"/>
        <source>Updated at {time}</source>
        <translation>Actualizado a las {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="58"/>
        <source>Could not refresh logs: {message}</source>
        <translation>No se pudieron actualizar los registros: {message}</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>Actualización automática</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>Obtiene nuevas líneas de registro cada pocos segundos y sigue el final del registro</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>Actualizar ahora</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../window.py" line="1562"/>
        <location filename="../window.py" line="1591"/>
        <source>TYPE</source>
        <translation>TIPO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1563"/>
        <source>CLUSTER IP</source>
        <translation>IP DEL CLÚSTER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1564"/>
        <source>EXTERNAL IP</source>
        <translation>IP EXTERNA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1565"/>
        <location filename="../window.py" line="1569"/>
        <location filename="../window.py" line="1577"/>
        <source>PORTS</source>
        <translation>PUERTOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1568"/>
        <source>ADDRESS TYPE</source>
        <translation>TIPO DE DIRECCIÓN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1570"/>
        <location filename="../window.py" line="1572"/>
        <source>ENDPOINTS</source>
        <translation>ENDPOINTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1574"/>
        <source>CLASS</source>
        <translation>CLASE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1575"/>
        <source>HOSTS</source>
        <translation>HOSTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>ADDRESS</source>
        <translation>DIRECCIÓN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1580"/>
        <source>CONTROLLER</source>
        <translation>CONTROLADOR</translation>
    </message>
    <message>
        <location filename="../window.py" line="1581"/>
        <source>PARAMETERS</source>
        <translation>PARÁMETROS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1584"/>
        <source>POD SELECTOR</source>
        <translation>SELECTOR DE PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1585"/>
        <source>POLICY TYPES</source>
        <translation>TIPOS DE POLÍTICA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1588"/>
        <location filename="../window.py" line="1592"/>
        <source>DATA</source>
        <translation>DATOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1595"/>
        <source>USAGE</source>
        <translation>USO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1598"/>
        <source>TYPES</source>
        <translation>TIPOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1601"/>
        <source>REFERENCE</source>
        <translation>REFERENCIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1602"/>
        <source>MIN PODS</source>
        <translation>MÍN. PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1603"/>
        <source>MAX PODS</source>
        <translation>MÁX. PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1604"/>
        <source>REPLICAS</source>
        <translation>RÉPLICAS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1607"/>
        <source>MIN AVAILABLE</source>
        <translation>MÍN. DISPONIBLE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <source>MAX UNAVAILABLE</source>
        <translation>MÁX. NO DISPONIBLE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1609"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>INTERRUPCIONES PERMITIDAS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1612"/>
        <source>VALUE</source>
        <translation>VALOR</translation>
    </message>
    <message>
        <location filename="../window.py" line="1613"/>
        <source>GLOBAL DEFAULT</source>
        <translation>PREDETERMINADO GLOBAL</translation>
    </message>
    <message>
        <location filename="../window.py" line="1616"/>
        <source>HANDLER</source>
        <translation>HANDLER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1619"/>
        <source>HOLDER</source>
        <translation>TITULAR</translation>
    </message>
    <message>
        <location filename="../window.py" line="1622"/>
        <location filename="../window.py" line="1625"/>
        <source>WEBHOOKS</source>
        <translation>WEBHOOKS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1629"/>
        <source>INSTANCE TYPES</source>
        <translation>TIPOS DE INSTANCIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1630"/>
        <source>NODES</source>
        <translation>NODOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1631"/>
        <source>AMI TYPE</source>
        <translation>TIPO DE AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1632"/>
        <source>AMI VERSION</source>
        <translation>VERSIÓN DE AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1636"/>
        <location filename="../ui/main_window.ui" line="2557"/>
        <source>VERSION</source>
        <translation>VERSIÓN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1637"/>
        <source>SOURCE</source>
        <translation>ORIGEN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1647"/>
        <source>COMPLETIONS</source>
        <translation>COMPLETADOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1648"/>
        <source>SCHEDULE</source>
        <translation>PROGRAMACIÓN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1649"/>
        <location filename="../ui/main_window.ui" line="2018"/>
        <source>READY</source>
        <translation>LISTOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1654"/>
        <location filename="../window.py" line="1670"/>
        <location filename="../ui/main_window.ui" line="1826"/>
        <location filename="../ui/main_window.ui" line="2003"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1656"/>
        <location filename="../window.py" line="1672"/>
        <location filename="../ui/main_window.ui" line="2013"/>
        <source>NAME</source>
        <translation>NOMBRE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1628"/>
        <location filename="../window.py" line="1635"/>
        <location filename="../window.py" line="1658"/>
        <location filename="../ui/main_window.ui" line="2023"/>
        <location filename="../ui/main_window.ui" line="2547"/>
        <source>STATUS</source>
        <translation>ESTADO</translation>
    </message>
    <message>
        <location filename="../window.py" line="1659"/>
        <location filename="../ui/main_window.ui" line="2562"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../window.py" line="1660"/>
        <location filename="../ui/main_window.ui" line="2567"/>
        <source>MEMORY</source>
        <translation>MEMORIA</translation>
    </message>
    <message>
        <location filename="../window.py" line="1661"/>
        <source>RESTARTS</source>
        <translation>REINICIOS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1662"/>
        <location filename="../window.py" line="1674"/>
        <location filename="../ui/main_window.ui" line="2028"/>
        <location filename="../ui/main_window.ui" line="2577"/>
        <source>AGE</source>
        <translation>EDAD</translation>
    </message>
    <message>
        <location filename="../window.py" line="1671"/>
        <location filename="../ui/main_window.ui" line="2008"/>
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
        <translation>Consola de Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="339"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>Contexto de Kubernetes de su kubeconfig</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="372"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>Inicie sesión con la CLI de la nube y recargue los datos del clúster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="375"/>
        <source>Sign in</source>
        <translation>Iniciar sesión</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="397"/>
        <source>Settings</source>
        <translation>Ajustes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="437"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>No se encontraron contextos de clúster en su kubeconfig. Añada un clúster a su kubeconfig (por ejemplo con la CLI de AWS: aws eks update-kubeconfig) y recargue.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="478"/>
        <source>Dismiss</source>
        <translation>Descartar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="569"/>
        <source>MONITORING</source>
        <translation>MONITORIZACIÓN</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1714"/>
        <source>Overview</source>
        <translation>Resumen</translation>
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
        <translation>Red</translation>
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
        <translation>Configuración</translation>
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
        <translation>ACCESO SEGURO
Recursos en modo de solo lectura</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1721"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos y capacidad del clúster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1878"/>
        <source>Search by name or namespace...</source>
        <translation>Buscar por nombre o namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1746"/>
        <location filename="../ui/main_window.ui" line="1759"/>
        <location filename="../ui/main_window.ui" line="1772"/>
        <source>Refresh</source>
        <translation>Actualizar</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <source>Cluster</source>
        <translation>Clúster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1929"/>
        <source>View Pods of the selected workload</source>
        <translation>Ver los Pods del workload seleccionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1945"/>
        <source>View JSON details of the selected workload</source>
        <translation>Ver los detalles JSON del workload seleccionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1948"/>
        <source>Details</source>
        <translation>Detalles</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1961"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>Ver los registros de un Pod del workload seleccionado</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1964"/>
        <source>Logs</source>
        <translation>Registros</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2507"/>
        <source>Nodes</source>
        <translation>Nodos</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2542"/>
        <source>NODE</source>
        <translation>NODO</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2552"/>
        <source>ROLE</source>
        <translation>ROL</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2572"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2590"/>
        <source>Select a context to load workloads</source>
        <translation>Seleccione un contexto para cargar los workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2613"/>
        <source>Data fetched from the cluster API</source>
        <translation>Datos obtenidos de la API del clúster</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2674"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>Abrir el sitio web de DCO Tecnologia</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2694"/>
        <source>MIT License</source>
        <translation>Licencia MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2697"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope es software de código abierto publicado bajo la licencia MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2733"/>
        <source>Update available</source>
        <translation>Actualización disponible</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2736"/>
        <source>Open the download page of the new version</source>
        <translation>Abrir la página de descarga de la nueva versión</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Check for updates</source>
        <translation>Buscar actualizaciones</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2784"/>
        <source>Open the project on GitHub</source>
        <translation>Abrir el proyecto en GitHub</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="2052"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>nodos listos</translation>
    </message>
    <message>
        <location filename="../window.py" line="2068"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>núcleos solicitados / asignables</translation>
    </message>
    <message>
        <location filename="../window.py" line="2082"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>solicitado / asignable</translation>
    </message>
    <message>
        <location filename="../window.py" line="2101"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>en el clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2103"/>
        <location filename="../ui/overview_page.ui" line="510"/>
        <location filename="../ui/overview_page.ui" line="564"/>
        <location filename="../ui/overview_page.ui" line="618"/>
        <source>workloads</source>
        <translation>workloads</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="29"/>
        <source>Cluster resources</source>
        <translation>Recursos del clúster</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="78"/>
        <source>CLUSTER INFO</source>
        <translation>INFORMACIÓN DEL CLÚSTER</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="125"/>
        <source>NETWORKING</source>
        <translation>RED</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="174"/>
        <source>NODES</source>
        <translation>NODOS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="228"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="248"/>
        <source>running / capacity</source>
        <translation>en ejecución / capacidad</translation>
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
        <translation>NOMBRE</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>LISTOS</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>FASE</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>CONTENEDORES</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>EDAD</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>Detalles del Pod</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>Ver registros</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>Cerrar</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="3090"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>Dé nombres más amigables a sus contextos. Deje un nombre vacío para conservar el original.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>Guardar cambios</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>GENERAL</translation>
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
        <translation>Nuevo tema...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>Editar tema...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>Abrir la carpeta de temas</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>Namespace predeterminado</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>El namespace en el que se abre cada contexto. Déjelo vacío para mostrarlos todos.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>Recordar el último contexto usado</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>Buscar una nueva versión en GitHub al iniciar la aplicación</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>Consulta la API pública de GitHub para obtener la última versión y no envía nada más que la versión de la aplicación. El icono del pie de página busca bajo demanda.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>Modo de depuración: escribir un archivo de registro que pueda compartir</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>Abrir la carpeta de registros</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>Vaciar la caché</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>Olvida las listas y los resúmenes ya cargados y el inicio de sesión de cada clúster, de modo que la siguiente solicitud inicia sesión y carga todo de nuevo. Sus ajustes se conservan.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>ARCHIVOS KUBECONFIG</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>KubeScope lee los archivos de la variable KUBECONFIG, o ~/.kube/config. Añada archivos aquí para leer esos en su lugar. Pulse Guardar para aplicar.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>Añadir archivo...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>Quitar</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>COMANDOS DE INICIO DE SESIÓN</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>Para una nube que KubeScope no conoce, indique el programa que su kubeconfig usa para iniciar sesión (por ejemplo oci) y el comando que inicia sesión (por ejemplo oci session authenticate). El botón Iniciar sesión lo ejecuta, sin shell. Pulse Guardar para aplicar.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>PROGRAMA</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>COMANDO DE INICIO DE SESIÓN</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>Añadir fila</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>NOMBRES DE CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>CONTEXTO</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>NOMBRE MOSTRADO</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>Fondo de la página</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>Paneles y tarjetas</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>Paneles alternos</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>Pistas de las barras</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>Bordes</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>Barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>Logotipo de la barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>Selector de la barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>Borde del selector de la barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>Selección de la barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>Texto de la barra superior</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>Texto</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>Título de la barra lateral</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>Texto secundario</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>Texto deshabilitado</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>Texto de acento y enlaces</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>Botones de acento</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>Botones de acento al pasar el cursor</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>Botones de acento deshabilitados</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>Foco y resaltados</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>Texto de la insignia</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>Tinte de acento</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>Selección de texto</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>Borde de acento</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>Texto de la barra superior y de los botones de acento</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>Texto saludable</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>Fondo saludable</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>Texto de advertencia</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>Fondo de advertencia</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>Texto de fallo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>Fondo de fallo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>Texto inactivo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>Fondo inactivo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>Fila con un problema</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>Fila de un Pod joven</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>Barra de uso, llenándose</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>Barra de uso, casi llena</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>Barra de salud, saludable</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>Barra de salud, advertencia</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>Barra de salud, fallo</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>Nuevo tema</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>Editar tema: {name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>Nombre del tema</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>Claro</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>Oscuro</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>Nombre</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>Parte de</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>Colores</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>Guarda en un archivo lo que muestra esta pestaña</translation>
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
        <location filename="../window.py" line="2321"/>
        <location filename="../window.py" line="2344"/>
        <location filename="../window.py" line="3328"/>
        <source>All namespaces</source>
        <translation>Todos los namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="832"/>
        <source>Loading contexts...</source>
        <translation>Cargando contextos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="841"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>No se pudo cargar el kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="863"/>
        <source>No contexts found in kubeconfig</source>
        <translation>No se encontraron contextos en el kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="913"/>
        <location filename="../window.py" line="991"/>
        <source>Unpin from the top</source>
        <translation>Quitar de arriba</translation>
    </message>
    <message>
        <location filename="../window.py" line="913"/>
        <source>Pin to the top</source>
        <translation>Fijar arriba</translation>
    </message>
    <message>
        <location filename="../window.py" line="1029"/>
        <source>Close</source>
        <translation>Cerrar</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Status</source>
        <translation>Estado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>Kubernetes version</source>
        <translation>Versión de Kubernetes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1078"/>
        <source>Platform version</source>
        <translation>Versión de la plataforma</translation>
    </message>
    <message>
        <location filename="../window.py" line="1079"/>
        <source>Created</source>
        <translation>Creado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>Provider</source>
        <translation>Proveedor</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>API server endpoint</source>
        <translation>Endpoint del servidor de la API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Cluster ARN</source>
        <translation>ARN del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1085"/>
        <source>Cluster IAM role ARN</source>
        <translation>ARN del rol de IAM del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1086"/>
        <source>OpenID Connect provider URL</source>
        <translation>URL del proveedor de OpenID Connect</translation>
    </message>
    <message>
        <location filename="../window.py" line="1094"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1095"/>
        <source>Cluster security group</source>
        <translation>Security group del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1097"/>
        <source>Additional security groups</source>
        <translation>Security groups adicionales</translation>
    </message>
    <message>
        <location filename="../window.py" line="1098"/>
        <source>None</source>
        <translation>Ninguno</translation>
    </message>
    <message>
        <location filename="../window.py" line="1101"/>
        <source>API server endpoint access</source>
        <translation>Acceso al endpoint del servidor de la API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1104"/>
        <source>Cluster IP address family</source>
        <translation>Familia de direcciones IP del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1105"/>
        <source>Service IPv4 range</source>
        <translation>Rango IPv4 de servicios</translation>
    </message>
    <message>
        <location filename="../window.py" line="1107"/>
        <source>Public access source allowlist</source>
        <translation>Lista de orígenes con acceso público</translation>
    </message>
    <message>
        <location filename="../window.py" line="1110"/>
        <source>Subnets</source>
        <translation>Subnets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1121"/>
        <source>Creating</source>
        <translation>Creando</translation>
    </message>
    <message>
        <location filename="../window.py" line="1122"/>
        <source>Updating</source>
        <translation>Actualizando</translation>
    </message>
    <message>
        <location filename="../window.py" line="1123"/>
        <source>Deleting</source>
        <translation>Eliminando</translation>
    </message>
    <message>
        <location filename="../window.py" line="1126"/>
        <source>Creation failed</source>
        <translation>Error de creación</translation>
    </message>
    <message>
        <location filename="../window.py" line="1127"/>
        <source>Update failed</source>
        <translation>Error de actualización</translation>
    </message>
    <message>
        <location filename="../window.py" line="1128"/>
        <source>Deletion failed</source>
        <translation>Error de eliminación</translation>
    </message>
    <message>
        <location filename="../window.py" line="1130"/>
        <source>Deployed</source>
        <translation>Desplegado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1131"/>
        <source>Superseded</source>
        <translation>Reemplazado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1132"/>
        <source>Uninstalled</source>
        <translation>Desinstalado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1133"/>
        <source>Uninstalling</source>
        <translation>Desinstalando</translation>
    </message>
    <message>
        <location filename="../window.py" line="1134"/>
        <source>Pending install</source>
        <translation>Instalación pendiente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1135"/>
        <source>Pending upgrade</source>
        <translation>Actualización pendiente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1136"/>
        <source>Pending rollback</source>
        <translation>Reversión pendiente</translation>
    </message>
    <message>
        <location filename="../window.py" line="1137"/>
        <source>Public</source>
        <translation>Público</translation>
    </message>
    <message>
        <location filename="../window.py" line="1138"/>
        <source>Private</source>
        <translation>Privado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1139"/>
        <source>Public and private</source>
        <translation>Público y privado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1232"/>
        <source>Overview</source>
        <translation>Resumen</translation>
    </message>
    <message>
        <location filename="../window.py" line="1233"/>
        <source>Cluster resources and capacity</source>
        <translation>Recursos y capacidad del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1235"/>
        <source>Details &amp; Logs</source>
        <translation>Detalles y registros</translation>
    </message>
    <message>
        <location filename="../window.py" line="1237"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>Detalles del recurso y registros del Pod, una pestaña cada uno</translation>
    </message>
    <message>
        <location filename="../window.py" line="1240"/>
        <source>Settings</source>
        <translation>Ajustes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1241"/>
        <source>Preferences and context names</source>
        <translation>Preferencias y nombres de contexto</translation>
    </message>
    <message>
        <location filename="../window.py" line="1243"/>
        <source>Workloads overview</source>
        <translation>Resumen de workloads</translation>
    </message>
    <message>
        <location filename="../window.py" line="1245"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>Estado de cada tipo de workload y los últimos eventos</translation>
    </message>
    <message>
        <location filename="../window.py" line="1249"/>
        <location filename="../window.py" line="1899"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="1249"/>
        <source>Pods of the cluster</source>
        <translation>Pods del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1251"/>
        <location filename="../window.py" line="1900"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="1252"/>
        <source>Deployments of the cluster</source>
        <translation>Deployments del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1255"/>
        <location filename="../window.py" line="1902"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1256"/>
        <source>StatefulSets of the cluster</source>
        <translation>StatefulSets del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1259"/>
        <location filename="../window.py" line="1901"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1260"/>
        <source>DaemonSets of the cluster</source>
        <translation>DaemonSets del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1263"/>
        <location filename="../window.py" line="1903"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1264"/>
        <source>ReplicaSets of the cluster</source>
        <translation>ReplicaSets del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1267"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>ReplicationControllers del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1270"/>
        <location filename="../window.py" line="1904"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1270"/>
        <source>Jobs of the cluster</source>
        <translation>Jobs del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1271"/>
        <location filename="../window.py" line="1905"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1271"/>
        <source>CronJobs of the cluster</source>
        <translation>CronJobs del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Services of the cluster</source>
        <translation>Services del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1274"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1275"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>Endpoint Slices del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1278"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1279"/>
        <source>Endpoints of the cluster</source>
        <translation>Endpoints del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1282"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1283"/>
        <source>Ingresses of the cluster</source>
        <translation>Ingresses del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1286"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1287"/>
        <source>Ingress Classes of the cluster</source>
        <translation>Ingress Classes del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1290"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1291"/>
        <source>Network Policies of the cluster</source>
        <translation>Network Policies del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1294"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1295"/>
        <source>Config Maps of the cluster</source>
        <translation>Config Maps del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1298"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1299"/>
        <source>Secrets of the cluster</source>
        <translation>Secrets del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1302"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1303"/>
        <source>Resource Quotas of the cluster</source>
        <translation>Resource Quotas del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1306"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1307"/>
        <source>Limit Ranges of the cluster</source>
        <translation>Limit Ranges del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1310"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1311"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>Horizontal Pod Autoscalers del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1314"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1315"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>Pod Disruption Budgets del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1318"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1319"/>
        <source>Priority Classes of the cluster</source>
        <translation>Priority Classes del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1322"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1323"/>
        <source>Runtime Classes of the cluster</source>
        <translation>Runtime Classes del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1326"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1327"/>
        <source>Leases of the cluster</source>
        <translation>Leases del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1331"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>Mutating Webhook Configurations del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1334"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1335"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>Validating Webhook Configurations del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1338"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1339"/>
        <source>Node Groups of the cluster</source>
        <translation>Node Groups del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1342"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1343"/>
        <source>Add-ons of the cluster</source>
        <translation>Add-ons del clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="1352"/>
        <source>Version {version}</source>
        <translation>Versión {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1355"/>
        <source>Open the project on GitHub</source>
        <translation>Abrir el proyecto en GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="1389"/>
        <source>Up to date</source>
        <translation>Actualizado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1390"/>
        <source>Could not check</source>
        <translation>No se pudo comprobar</translation>
    </message>
    <message>
        <location filename="../window.py" line="1401"/>
        <source>Check for updates</source>
        <translation>Buscar actualizaciones</translation>
    </message>
    <message>
        <location filename="../window.py" line="1402"/>
        <source>Checking for updates...</source>
        <translation>Buscando actualizaciones...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1403"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope está actualizado. Haga clic para comprobar de nuevo.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1404"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>No se pudo buscar actualizaciones. Haga clic para reintentar.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1410"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>Actualización disponible: {version}. Haga clic para abrir la página de descarga; clic derecho para comprobar de nuevo.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1418"/>
        <source>Update available</source>
        <translation>Actualización disponible</translation>
    </message>
    <message>
        <location filename="../window.py" line="1420"/>
        <source>Download KubeScope {version}</source>
        <translation>Descargar KubeScope {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1456"/>
        <source>Check for updates again</source>
        <translation>Buscar actualizaciones de nuevo</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <location filename="../window.py" line="2228"/>
        <source>Loading resources...</source>
        <translation>Cargando recursos...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1797"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>Configurar credenciales de AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1801"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>Las credenciales de AWS del perfil {profile} faltan o no son válidas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1806"/>
        <source>Sign in to {provider}</source>
        <translation>Iniciar sesión en {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1809"/>
        <source>Not signed in to {provider}</source>
        <translation>Sin sesión en {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1813"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>Iniciar sesión en {provider} ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1819"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>Sin sesión en {provider} (perfil {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1840"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>Termine en la terminal que se abrió y luego pulse Actualizar.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1859"/>
        <source>Loading workloads...</source>
        <translation>Cargando workloads...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1920"/>
        <source>Could not read: {names}</source>
        <translation>No se pudo leer: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1980"/>
        <source>Loading cluster data...</source>
        <translation>Cargando datos del clúster...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2061"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>en ejecución · {pending} pendientes · {failed} con fallo</translation>
    </message>
    <message>
        <location filename="../window.py" line="2070"/>
        <location filename="../window.py" line="2084"/>
        <source> · usage {value}</source>
        <translation> · uso {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2133"/>
        <source>Ready</source>
        <translation>Listo</translation>
    </message>
    <message>
        <location filename="../window.py" line="2133"/>
        <source>Not ready</source>
        <translation>No listo</translation>
    </message>
    <message>
        <location filename="../window.py" line="2108"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>Uso real no disponible: no se encontró metrics-server.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2245"/>
        <source>Refreshing...</source>
        <translation>Actualizando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2436"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{count} Services en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2438"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{count} Endpoint Slices en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2441"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{count} Endpoints en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2444"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{count} Ingresses en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2446"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>{count} Ingress Classes en el clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2448"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{count} Network Policies en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2451"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>{count} Config Maps en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2453"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>{count} Secrets en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2455"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>{count} Resource Quotas en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2458"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>{count} Limit Ranges en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2461"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>{count} Horizontal Pod Autoscalers en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2464"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>{count} Pod Disruption Budgets en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2466"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>{count} Leases en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2468"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>{count} Priority Classes en el clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2470"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>{count} Runtime Classes en el clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2472"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>{count} Mutating Webhook Configurations en el clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2475"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>{count} Validating Webhook Configurations en el clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2477"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>{count} Node Groups en el clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2478"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>{count} Add-ons en el clúster</translation>
    </message>
    <message>
        <location filename="../window.py" line="2489"/>
        <location filename="../window.py" line="2555"/>
        <source>Running</source>
        <translation>En ejecución</translation>
    </message>
    <message>
        <location filename="../window.py" line="1129"/>
        <location filename="../window.py" line="2490"/>
        <location filename="../window.py" line="2551"/>
        <source>Pending</source>
        <translation>Pendiente</translation>
    </message>
    <message>
        <location filename="../window.py" line="2491"/>
        <source>Succeeded</source>
        <translation>Completado</translation>
    </message>
    <message>
        <location filename="../window.py" line="1125"/>
        <location filename="../window.py" line="2492"/>
        <location filename="../window.py" line="2550"/>
        <source>Failed</source>
        <translation>Fallido</translation>
    </message>
    <message>
        <location filename="../window.py" line="2493"/>
        <source>Unknown</source>
        <translation>Desconocido</translation>
    </message>
    <message>
        <location filename="../window.py" line="2537"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pods en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2545"/>
        <source>Healthy</source>
        <translation>Saludable</translation>
    </message>
    <message>
        <location filename="../window.py" line="1124"/>
        <location filename="../window.py" line="2546"/>
        <source>Degraded</source>
        <translation>Degradado</translation>
    </message>
    <message>
        <location filename="../window.py" line="2547"/>
        <source>Unavailable</source>
        <translation>No disponible</translation>
    </message>
    <message>
        <location filename="../window.py" line="2548"/>
        <source>Scaled to zero</source>
        <translation>Escalado a cero</translation>
    </message>
    <message>
        <location filename="../window.py" line="2549"/>
        <source>Complete</source>
        <translation>Completo</translation>
    </message>
    <message>
        <location filename="../window.py" line="2552"/>
        <source>Suspended</source>
        <translation>Suspendido</translation>
    </message>
    <message>
        <location filename="../window.py" line="1120"/>
        <location filename="../window.py" line="2553"/>
        <source>Active</source>
        <translation>Activo</translation>
    </message>
    <message>
        <location filename="../window.py" line="2554"/>
        <source>Scheduled</source>
        <translation>Programado</translation>
    </message>
    <message>
        <location filename="../window.py" line="2599"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployments en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2602"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{count} StatefulSets en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2605"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{count} DaemonSets en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2608"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{count} ReplicaSets en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2611"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{count} ReplicationControllers en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2613"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{count} Jobs en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2614"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{count} CronJobs en {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2638"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} de {total} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2639"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} de {total} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2640"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{visible} de {total} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2641"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{visible} de {total} DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2642"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{visible} de {total} ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2644"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{visible} de {total} ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2646"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{visible} de {total} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2647"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{visible} de {total} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2648"/>
        <source>{visible} of {total} Services</source>
        <translation>{visible} de {total} Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="2649"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{visible} de {total} Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="2650"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{visible} de {total} Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="2651"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{visible} de {total} Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="2652"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{visible} de {total} Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2653"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{visible} de {total} Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="2654"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>{visible} de {total} Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="2655"/>
        <source>{visible} of {total} Secrets</source>
        <translation>{visible} de {total} Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2656"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>{visible} de {total} Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="2657"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>{visible} de {total} Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="2659"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>{visible} de {total} Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2662"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>{visible} de {total} Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2664"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>{visible} de {total} Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2665"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>{visible} de {total} Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2666"/>
        <source>{visible} of {total} Leases</source>
        <translation>{visible} de {total} Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="2668"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>{visible} de {total} Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2671"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>{visible} de {total} Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2673"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>{visible} de {total} Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="2674"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>{visible} de {total} Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="2720"/>
        <source>Loading...</source>
        <translation>Cargando...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2766"/>
        <location filename="../window.py" line="2858"/>
        <source>Pod: {name}</source>
        <translation>Pod: {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2812"/>
        <source>Pods of {name}</source>
        <translation>Pods de {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2814"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods en {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2879"/>
        <source>No Pods are associated with this workload</source>
        <translation>Ningún Pod está asociado a este workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="2886"/>
        <location filename="../window.py" line="2909"/>
        <source>Logs</source>
        <translation>Registros</translation>
    </message>
    <message>
        <location filename="../window.py" line="2886"/>
        <source>This workload has no Pods.</source>
        <translation>Este workload no tiene Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2895"/>
        <location filename="../window.py" line="2918"/>
        <source>View logs</source>
        <translation>Ver registros</translation>
    </message>
    <message>
        <location filename="../window.py" line="2896"/>
        <source>Select the Pod:</source>
        <translation>Seleccione el Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2910"/>
        <source>Pod {name} has no containers.</source>
        <translation>El Pod {name} no tiene contenedores.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2919"/>
        <source>Select the container of {name}:</source>
        <translation>Seleccione el contenedor de {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2945"/>
        <source>Save to a file</source>
        <translation>Guardar en un archivo</translation>
    </message>
    <message>
        <location filename="../window.py" line="2956"/>
        <source>Could not save</source>
        <translation>No se pudo guardar</translation>
    </message>
    <message>
        <location filename="../window.py" line="2957"/>
        <source>The file could not be written: {reason}</source>
        <translation>No se pudo escribir el archivo: {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3003"/>
        <source>Logs: {pod} / {container}</source>
        <translation>Registros: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3053"/>
        <source>Automatic</source>
        <translation>Automático</translation>
    </message>
    <message>
        <location filename="../window.py" line="3066"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>Desactivado por defecto. Al activarlo, KubeScope escribe lo que hace, nunca los registros de los Pods ni el contenido de los recursos, en {path}. Léalo antes de compartirlo: incluye nombres de contexto.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3097"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>No se encontraron contextos en el kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3126"/>
        <source>Choose a kubeconfig file</source>
        <translation>Elija un archivo kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="3172"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>El comando de inicio de sesión de la fila {row} no es válido.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3185"/>
        <source>Light</source>
        <translation>Claro</translation>
    </message>
    <message>
        <location filename="../window.py" line="3185"/>
        <source>Dark</source>
        <translation>Oscuro</translation>
    </message>
    <message>
        <location filename="../window.py" line="3204"/>
        <source>My theme</source>
        <translation>Mi tema</translation>
    </message>
    <message>
        <location filename="../window.py" line="3248"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>Caché vaciada. Todo se carga de nuevo la próxima vez que haga falta.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3303"/>
        <source>Settings saved.</source>
        <translation>Ajustes guardados.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3342"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>Su usuario no tiene permiso para realizar esta acción ({action}). Pida acceso al administrador de su clúster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3347"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>Su usuario no tiene permiso para hacer esto. Pida acceso al administrador de su clúster.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3366"/>
        <source>Query failed</source>
        <translation>Error en la consulta</translation>
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
        <translation>ORIGEN</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>INVOLVED OBJECT</source>
        <translation>OBJETO INVOLUCRADO</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>MESSAGE</source>
        <translation>MENSAJE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>COUNT</source>
        <translation>CONTADOR</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>AGE</source>
        <translation>EDAD</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>LAST SEEN</source>
        <translation>ÚLTIMA VEZ</translation>
    </message>
</context>
</TS>
