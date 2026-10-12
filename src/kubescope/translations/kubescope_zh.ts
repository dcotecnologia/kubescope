<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="zh">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>未找到登录工具</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>您的 kubeconfig 运行“{tool}”来登录，但它没有安装或不在 PATH 中。请安装后刷新。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>未找到上下文</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>此上下文不在您的 kubeconfig 中。请检查 ~/.kube/config。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>身份验证失败</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>您的凭据可能已过期。请重新登录（例如使用“aws sso login”、“gcloud auth login”或“az login”）后刷新。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Not an Amazon EKS cluster</source>
        <translation>不是 Amazon EKS 集群</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Node Groups, Add-ons and the AWS cards of the Overview exist only on Amazon EKS contexts.</source>
        <translation>Node Groups、Add-ons 以及概览中的 AWS 卡片仅存在于 Amazon EKS 上下文。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="110"/>
        <source>Unexpected answer from AWS</source>
        <translation>AWS 返回了意外的响应</translation>
    </message>
    <message>
        <location filename="../errors.py" line="111"/>
        <source>Update the AWS CLI to its latest version and refresh.</source>
        <translation>请将 AWS CLI 更新到最新版本后刷新。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="118"/>
        <location filename="../errors.py" line="128"/>
        <source>Access denied</source>
        <translation>访问被拒绝</translation>
    </message>
    <message>
        <location filename="../errors.py" line="119"/>
        <source>Your AWS identity is not allowed to read this. The wiki lists the eks: permissions KubeScope needs.</source>
        <translation>您的 AWS 身份无权读取此内容。Wiki 列出了 KubeScope 所需的 eks: 权限。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>您的用户无权读取此资源。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="150"/>
        <source>Cluster unreachable</source>
        <translation>无法连接集群</translation>
    </message>
    <message>
        <location filename="../errors.py" line="151"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>请检查您的网络或 VPN，并确认集群正在运行。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="157"/>
        <source>Something went wrong</source>
        <translation>出了点问题</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="42"/>
        <source>No log lines returned.</source>
        <translation>没有返回日志行。</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="47"/>
        <source>Updated at {time}</source>
        <translation>更新于 {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="54"/>
        <source>Could not refresh logs: {message}</source>
        <translation>无法刷新日志：{message}</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>自动刷新</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>每隔几秒获取新的日志行，并跟随日志末尾</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>立即刷新</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../window.py" line="1508"/>
        <location filename="../window.py" line="1537"/>
        <source>TYPE</source>
        <translation>类型</translation>
    </message>
    <message>
        <location filename="../window.py" line="1509"/>
        <source>CLUSTER IP</source>
        <translation>集群 IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1510"/>
        <source>EXTERNAL IP</source>
        <translation>外部 IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1511"/>
        <location filename="../window.py" line="1515"/>
        <location filename="../window.py" line="1523"/>
        <source>PORTS</source>
        <translation>端口</translation>
    </message>
    <message>
        <location filename="../window.py" line="1514"/>
        <source>ADDRESS TYPE</source>
        <translation>地址类型</translation>
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
        <translation>类</translation>
    </message>
    <message>
        <location filename="../window.py" line="1521"/>
        <source>HOSTS</source>
        <translation>主机</translation>
    </message>
    <message>
        <location filename="../window.py" line="1522"/>
        <source>ADDRESS</source>
        <translation>地址</translation>
    </message>
    <message>
        <location filename="../window.py" line="1526"/>
        <source>CONTROLLER</source>
        <translation>控制器</translation>
    </message>
    <message>
        <location filename="../window.py" line="1527"/>
        <source>PARAMETERS</source>
        <translation>参数</translation>
    </message>
    <message>
        <location filename="../window.py" line="1530"/>
        <source>POD SELECTOR</source>
        <translation>POD 选择器</translation>
    </message>
    <message>
        <location filename="../window.py" line="1531"/>
        <source>POLICY TYPES</source>
        <translation>策略类型</translation>
    </message>
    <message>
        <location filename="../window.py" line="1534"/>
        <location filename="../window.py" line="1538"/>
        <source>DATA</source>
        <translation>数据</translation>
    </message>
    <message>
        <location filename="../window.py" line="1541"/>
        <source>USAGE</source>
        <translation>用量</translation>
    </message>
    <message>
        <location filename="../window.py" line="1544"/>
        <source>TYPES</source>
        <translation>类型</translation>
    </message>
    <message>
        <location filename="../window.py" line="1547"/>
        <source>REFERENCE</source>
        <translation>引用</translation>
    </message>
    <message>
        <location filename="../window.py" line="1548"/>
        <source>MIN PODS</source>
        <translation>最小 POD 数</translation>
    </message>
    <message>
        <location filename="../window.py" line="1549"/>
        <source>MAX PODS</source>
        <translation>最大 POD 数</translation>
    </message>
    <message>
        <location filename="../window.py" line="1550"/>
        <source>REPLICAS</source>
        <translation>副本</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <source>MIN AVAILABLE</source>
        <translation>最小可用</translation>
    </message>
    <message>
        <location filename="../window.py" line="1554"/>
        <source>MAX UNAVAILABLE</source>
        <translation>最大不可用</translation>
    </message>
    <message>
        <location filename="../window.py" line="1555"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>允许的中断</translation>
    </message>
    <message>
        <location filename="../window.py" line="1558"/>
        <source>VALUE</source>
        <translation>值</translation>
    </message>
    <message>
        <location filename="../window.py" line="1559"/>
        <source>GLOBAL DEFAULT</source>
        <translation>全局默认</translation>
    </message>
    <message>
        <location filename="../window.py" line="1562"/>
        <source>HANDLER</source>
        <translation>处理程序</translation>
    </message>
    <message>
        <location filename="../window.py" line="1565"/>
        <source>HOLDER</source>
        <translation>持有者</translation>
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
        <translation>实例类型</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>NODES</source>
        <translation>节点数</translation>
    </message>
    <message>
        <location filename="../window.py" line="1577"/>
        <source>AMI TYPE</source>
        <translation>AMI 类型</translation>
    </message>
    <message>
        <location filename="../window.py" line="1578"/>
        <source>AMI VERSION</source>
        <translation>AMI 版本</translation>
    </message>
    <message>
        <location filename="../window.py" line="1582"/>
        <location filename="../ui/main_window.ui" line="2588"/>
        <source>VERSION</source>
        <translation>版本</translation>
    </message>
    <message>
        <location filename="../window.py" line="1583"/>
        <source>SOURCE</source>
        <translation>来源</translation>
    </message>
    <message>
        <location filename="../window.py" line="1593"/>
        <source>COMPLETIONS</source>
        <translation>完成数</translation>
    </message>
    <message>
        <location filename="../window.py" line="1594"/>
        <source>SCHEDULE</source>
        <translation>计划</translation>
    </message>
    <message>
        <location filename="../window.py" line="1595"/>
        <location filename="../ui/main_window.ui" line="2049"/>
        <source>READY</source>
        <translation>就绪</translation>
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
        <translation>名称</translation>
    </message>
    <message>
        <location filename="../window.py" line="1574"/>
        <location filename="../window.py" line="1581"/>
        <location filename="../window.py" line="1604"/>
        <location filename="../ui/main_window.ui" line="2054"/>
        <location filename="../ui/main_window.ui" line="2578"/>
        <source>STATUS</source>
        <translation>状态</translation>
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
        <translation>内存</translation>
    </message>
    <message>
        <location filename="../window.py" line="1607"/>
        <source>RESTARTS</source>
        <translation>重启次数</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <location filename="../window.py" line="1620"/>
        <location filename="../ui/main_window.ui" line="2059"/>
        <location filename="../ui/main_window.ui" line="2608"/>
        <source>AGE</source>
        <translation>存在时间</translation>
    </message>
    <message>
        <location filename="../window.py" line="1617"/>
        <location filename="../ui/main_window.ui" line="2039"/>
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
        <translation>Kubernetes 控制台</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="339"/>
        <source>CONTEXT</source>
        <translation>上下文</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>来自您的 kubeconfig 的 Kubernetes 上下文</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="372"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>使用云 CLI 登录，然后重新加载集群数据</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="375"/>
        <source>Sign in</source>
        <translation>登录</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="397"/>
        <source>Settings</source>
        <translation>设置</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="437"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>在您的 kubeconfig 中未找到集群上下文。请将集群添加到 kubeconfig（例如使用 AWS CLI：aws eks update-kubeconfig）后重新加载。</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="478"/>
        <source>Dismiss</source>
        <translation>关闭</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="569"/>
        <source>MONITORING</source>
        <translation>监控</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1745"/>
        <source>Overview</source>
        <translation>概览</translation>
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
        <location filename="../ui/main_window.ui" line="1963"/>
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
        <translation>网络</translation>
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
        <translation>配置</translation>
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
        <translation>详情与日志</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1696"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>安全访问
资源为只读模式</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1752"/>
        <source>Cluster resources and capacity</source>
        <translation>集群资源与容量</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1909"/>
        <source>Search by name or namespace...</source>
        <translation>按名称或 namespace 搜索...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1777"/>
        <location filename="../ui/main_window.ui" line="1790"/>
        <location filename="../ui/main_window.ui" line="1803"/>
        <source>Refresh</source>
        <translation>刷新</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1960"/>
        <source>View Pods of the selected workload</source>
        <translation>查看所选 workload 的 Pods</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1976"/>
        <source>View JSON details of the selected workload</source>
        <translation>查看所选 workload 的 JSON 详情</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1979"/>
        <source>Details</source>
        <translation>详情</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1992"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>查看所选 workload 某个 Pod 的日志</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1995"/>
        <source>Logs</source>
        <translation>日志</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2538"/>
        <source>Nodes</source>
        <translation>节点</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2573"/>
        <source>NODE</source>
        <translation>节点</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2583"/>
        <source>ROLE</source>
        <translation>角色</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2603"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2621"/>
        <source>Select a context to load workloads</source>
        <translation>选择上下文以加载 workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2644"/>
        <source>Data fetched from the cluster API</source>
        <translation>数据来自集群 API</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2705"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>打开 DCO Tecnologia 网站</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2725"/>
        <source>MIT License</source>
        <translation>MIT 许可证</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2728"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope 是以 MIT 许可证发布的开源软件</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Update available</source>
        <translation>有可用更新</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2767"/>
        <source>Open the download page of the new version</source>
        <translation>打开新版本的下载页面</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2795"/>
        <source>Check for updates</source>
        <translation>检查更新</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2815"/>
        <source>Open the project on GitHub</source>
        <translation>在 GitHub 上打开项目</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="1998"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>个节点就绪</translation>
    </message>
    <message>
        <location filename="../window.py" line="2014"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>已请求 / 可分配核心数</translation>
    </message>
    <message>
        <location filename="../window.py" line="2028"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>已请求 / 可分配</translation>
    </message>
    <message>
        <location filename="../window.py" line="2047"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>在集群中</translation>
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
        <translation>集群资源</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="78"/>
        <source>CLUSTER INFO</source>
        <translation>集群信息</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="125"/>
        <source>NETWORKING</source>
        <translation>网络</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="174"/>
        <source>NODES</source>
        <translation>节点</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="228"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="248"/>
        <source>running / capacity</source>
        <translation>运行中 / 容量</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="295"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="362"/>
        <source>MEMORY</source>
        <translation>内存</translation>
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
        <translation>名称</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>就绪</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>阶段</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>容器</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>存在时间</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>Pod 详情</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>查看日志</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>关闭</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="3038"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>为您的上下文起更易读的名称。名称留空则保留原名。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>保存更改</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>常规</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="107"/>
        <source>Language</source>
        <translation>语言</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="142"/>
        <source>Theme</source>
        <translation>主题</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="177"/>
        <source>New theme...</source>
        <translation>新建主题...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>编辑主题...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>打开主题文件夹</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>默认 namespace</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>每个上下文打开时所在的 namespace。留空则显示全部。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>记住上次使用的上下文</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>应用启动时在 GitHub 上检查新版本</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>向 GitHub 公共 API 查询最新版本，只发送应用版本号。页脚的图标可按需检查。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>调试模式：写入可分享的日志文件</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>打开日志文件夹</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>清除缓存</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>忘记已加载的列表和概览以及每个集群的登录状态，因此下次请求会重新登录并重新加载所有内容。您的设置会保留。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>KUBECONFIG 文件</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>KubeScope 读取 KUBECONFIG 变量中的文件，或 ~/.kube/config。在此添加文件即可改为读取这些文件。点击“保存”以应用。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>添加文件...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>移除</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>登录命令</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>对于 KubeScope 不认识的云，请填写您的 kubeconfig 用来登录的程序（例如 oci）以及执行登录的命令（例如 oci session authenticate）。“登录”按钮会运行该命令，不使用 shell。点击“保存”以应用。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>程序</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>登录命令</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>添加行</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>上下文名称</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>上下文</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>显示名称</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>页面背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>面板和卡片</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>交替面板</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>进度条轨道</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>边框</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>顶部栏</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>顶部栏徽标</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>顶部栏选择器</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>顶部栏选择器边框</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>顶部栏选中项</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>顶部栏文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>侧边栏标题</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>次要文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>禁用文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>强调文字和链接</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>强调按钮</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>悬停时的强调按钮</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>禁用时的强调按钮</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>焦点和高亮</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>徽章文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>强调色调</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>文字选中</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>强调边框</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>顶部栏和强调按钮上的文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>正常状态文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>正常状态背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>警告文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>警告背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>失败文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>失败背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>空闲文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>空闲背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>有问题的行</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>新建 Pod 的行</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>用量条，接近占满</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>用量条，几乎占满</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>健康条，正常</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>健康条，警告</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>健康条，失败</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>新建主题</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>编辑主题：{name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>主题名称</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>浅色</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>深色</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>名称</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>基于</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>颜色</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>将此标签页显示的内容保存到文件</translation>
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
        <translation>所有 namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="834"/>
        <source>Loading contexts...</source>
        <translation>正在加载上下文...</translation>
    </message>
    <message>
        <location filename="../window.py" line="843"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>无法加载 kubeconfig：{error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="865"/>
        <source>No contexts found in kubeconfig</source>
        <translation>在 kubeconfig 中未找到上下文</translation>
    </message>
    <message>
        <location filename="../window.py" line="894"/>
        <location filename="../window.py" line="972"/>
        <source>Unpin from the top</source>
        <translation>从顶部取消固定</translation>
    </message>
    <message>
        <location filename="../window.py" line="894"/>
        <source>Pin to the top</source>
        <translation>固定到顶部</translation>
    </message>
    <message>
        <location filename="../window.py" line="1021"/>
        <source>Status</source>
        <translation>状态</translation>
    </message>
    <message>
        <location filename="../window.py" line="1022"/>
        <source>Kubernetes version</source>
        <translation>Kubernetes 版本</translation>
    </message>
    <message>
        <location filename="../window.py" line="1023"/>
        <source>Platform version</source>
        <translation>平台版本</translation>
    </message>
    <message>
        <location filename="../window.py" line="1024"/>
        <source>Created</source>
        <translation>创建时间</translation>
    </message>
    <message>
        <location filename="../window.py" line="1025"/>
        <source>Provider</source>
        <translation>提供商</translation>
    </message>
    <message>
        <location filename="../window.py" line="1028"/>
        <source>API server endpoint</source>
        <translation>API 服务器端点</translation>
    </message>
    <message>
        <location filename="../window.py" line="1029"/>
        <source>Cluster ARN</source>
        <translation>集群 ARN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1030"/>
        <source>Cluster IAM role ARN</source>
        <translation>集群 IAM 角色 ARN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1031"/>
        <source>OpenID Connect provider URL</source>
        <translation>OpenID Connect 提供商 URL</translation>
    </message>
    <message>
        <location filename="../window.py" line="1039"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1040"/>
        <source>Cluster security group</source>
        <translation>集群安全组</translation>
    </message>
    <message>
        <location filename="../window.py" line="1042"/>
        <source>Additional security groups</source>
        <translation>附加安全组</translation>
    </message>
    <message>
        <location filename="../window.py" line="1043"/>
        <source>None</source>
        <translation>无</translation>
    </message>
    <message>
        <location filename="../window.py" line="1046"/>
        <source>API server endpoint access</source>
        <translation>API 服务器端点访问</translation>
    </message>
    <message>
        <location filename="../window.py" line="1049"/>
        <source>Cluster IP address family</source>
        <translation>集群 IP 地址族</translation>
    </message>
    <message>
        <location filename="../window.py" line="1050"/>
        <source>Service IPv4 range</source>
        <translation>服务 IPv4 范围</translation>
    </message>
    <message>
        <location filename="../window.py" line="1052"/>
        <source>Public access source allowlist</source>
        <translation>公共访问来源允许列表</translation>
    </message>
    <message>
        <location filename="../window.py" line="1055"/>
        <source>Subnets</source>
        <translation>子网</translation>
    </message>
    <message>
        <location filename="../window.py" line="1066"/>
        <source>Creating</source>
        <translation>创建中</translation>
    </message>
    <message>
        <location filename="../window.py" line="1067"/>
        <source>Updating</source>
        <translation>更新中</translation>
    </message>
    <message>
        <location filename="../window.py" line="1068"/>
        <source>Deleting</source>
        <translation>删除中</translation>
    </message>
    <message>
        <location filename="../window.py" line="1071"/>
        <source>Creation failed</source>
        <translation>创建失败</translation>
    </message>
    <message>
        <location filename="../window.py" line="1072"/>
        <source>Update failed</source>
        <translation>更新失败</translation>
    </message>
    <message>
        <location filename="../window.py" line="1073"/>
        <source>Deletion failed</source>
        <translation>删除失败</translation>
    </message>
    <message>
        <location filename="../window.py" line="1075"/>
        <source>Deployed</source>
        <translation>已部署</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Superseded</source>
        <translation>已被取代</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>Uninstalled</source>
        <translation>已卸载</translation>
    </message>
    <message>
        <location filename="../window.py" line="1078"/>
        <source>Uninstalling</source>
        <translation>卸载中</translation>
    </message>
    <message>
        <location filename="../window.py" line="1079"/>
        <source>Pending install</source>
        <translation>等待安装</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>Pending upgrade</source>
        <translation>等待升级</translation>
    </message>
    <message>
        <location filename="../window.py" line="1081"/>
        <source>Pending rollback</source>
        <translation>等待回滚</translation>
    </message>
    <message>
        <location filename="../window.py" line="1082"/>
        <source>Public</source>
        <translation>公开</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>Private</source>
        <translation>私有</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Public and private</source>
        <translation>公开和私有</translation>
    </message>
    <message>
        <location filename="../window.py" line="1177"/>
        <source>Overview</source>
        <translation>概览</translation>
    </message>
    <message>
        <location filename="../window.py" line="1178"/>
        <source>Cluster resources and capacity</source>
        <translation>集群资源与容量</translation>
    </message>
    <message>
        <location filename="../window.py" line="1180"/>
        <source>Details &amp; Logs</source>
        <translation>详情与日志</translation>
    </message>
    <message>
        <location filename="../window.py" line="1182"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>资源详情和 Pod 日志，各占一个标签页</translation>
    </message>
    <message>
        <location filename="../window.py" line="1185"/>
        <source>Settings</source>
        <translation>设置</translation>
    </message>
    <message>
        <location filename="../window.py" line="1186"/>
        <source>Preferences and context names</source>
        <translation>偏好设置和上下文名称</translation>
    </message>
    <message>
        <location filename="../window.py" line="1188"/>
        <source>Workloads overview</source>
        <translation>Workloads 概览</translation>
    </message>
    <message>
        <location filename="../window.py" line="1190"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>每种 workload 的健康状况和最新事件</translation>
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
        <translation>集群的 Pods</translation>
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
        <translation>集群的 Deployments</translation>
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
        <translation>集群的 StatefulSets</translation>
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
        <translation>集群的 DaemonSets</translation>
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
        <translation>集群的 ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1212"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1213"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>集群的 ReplicationControllers</translation>
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
        <translation>集群的 Jobs</translation>
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
        <translation>集群的 CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1217"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1217"/>
        <source>Services of the cluster</source>
        <translation>集群的 Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1219"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1220"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>集群的 Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1223"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1224"/>
        <source>Endpoints of the cluster</source>
        <translation>集群的 Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1227"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1228"/>
        <source>Ingresses of the cluster</source>
        <translation>集群的 Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1231"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1232"/>
        <source>Ingress Classes of the cluster</source>
        <translation>集群的 Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1235"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1236"/>
        <source>Network Policies of the cluster</source>
        <translation>集群的 Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1239"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1240"/>
        <source>Config Maps of the cluster</source>
        <translation>集群的 Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1243"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1244"/>
        <source>Secrets of the cluster</source>
        <translation>集群的 Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1247"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1248"/>
        <source>Resource Quotas of the cluster</source>
        <translation>集群的 Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1251"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1252"/>
        <source>Limit Ranges of the cluster</source>
        <translation>集群的 Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1255"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1256"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>集群的 Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1259"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1260"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>集群的 Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1263"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1264"/>
        <source>Priority Classes of the cluster</source>
        <translation>集群的 Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1267"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>Runtime Classes of the cluster</source>
        <translation>集群的 Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1271"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Leases of the cluster</source>
        <translation>集群的 Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1275"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1276"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>集群的 Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1279"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1280"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>集群的 Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1283"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1284"/>
        <source>Node Groups of the cluster</source>
        <translation>集群的 Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1287"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1288"/>
        <source>Add-ons of the cluster</source>
        <translation>集群的 Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1297"/>
        <source>Version {version}</source>
        <translation>版本 {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1300"/>
        <source>Open the project on GitHub</source>
        <translation>在 GitHub 上打开项目</translation>
    </message>
    <message>
        <location filename="../window.py" line="1334"/>
        <source>Up to date</source>
        <translation>已是最新</translation>
    </message>
    <message>
        <location filename="../window.py" line="1335"/>
        <source>Could not check</source>
        <translation>无法检查</translation>
    </message>
    <message>
        <location filename="../window.py" line="1346"/>
        <source>Check for updates</source>
        <translation>检查更新</translation>
    </message>
    <message>
        <location filename="../window.py" line="1347"/>
        <source>Checking for updates...</source>
        <translation>正在检查更新...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1348"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope 已是最新版本。点击可再次检查。</translation>
    </message>
    <message>
        <location filename="../window.py" line="1349"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>无法检查更新。点击重试。</translation>
    </message>
    <message>
        <location filename="../window.py" line="1355"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>有可用更新：{version}。点击打开下载页面；右键再次检查。</translation>
    </message>
    <message>
        <location filename="../window.py" line="1363"/>
        <source>Update available</source>
        <translation>有可用更新</translation>
    </message>
    <message>
        <location filename="../window.py" line="1365"/>
        <source>Download KubeScope {version}</source>
        <translation>下载 KubeScope {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1401"/>
        <source>Check for updates again</source>
        <translation>再次检查更新</translation>
    </message>
    <message>
        <location filename="../window.py" line="1499"/>
        <location filename="../window.py" line="2174"/>
        <source>Loading resources...</source>
        <translation>正在加载资源...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1743"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>配置 AWS 凭据（{profile}）</translation>
    </message>
    <message>
        <location filename="../window.py" line="1747"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>配置文件 {profile} 的 AWS 凭据缺失或无效</translation>
    </message>
    <message>
        <location filename="../window.py" line="1752"/>
        <source>Sign in to {provider}</source>
        <translation>登录 {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1755"/>
        <source>Not signed in to {provider}</source>
        <translation>未登录 {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1759"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>登录 {provider}（{profile}）</translation>
    </message>
    <message>
        <location filename="../window.py" line="1765"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>未登录 {provider}（配置文件 {profile}）</translation>
    </message>
    <message>
        <location filename="../window.py" line="1786"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>请在打开的终端中完成，然后点击“刷新”。</translation>
    </message>
    <message>
        <location filename="../window.py" line="1805"/>
        <source>Loading workloads...</source>
        <translation>正在加载 workloads...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1866"/>
        <source>Could not read: {names}</source>
        <translation>无法读取：{names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1926"/>
        <source>Loading cluster data...</source>
        <translation>正在加载集群数据...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2007"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>运行中 · {pending} 个等待中 · {failed} 个失败</translation>
    </message>
    <message>
        <location filename="../window.py" line="2016"/>
        <location filename="../window.py" line="2030"/>
        <source> · usage {value}</source>
        <translation> · 用量 {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <source>Ready</source>
        <translation>就绪</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <source>Not ready</source>
        <translation>未就绪</translation>
    </message>
    <message>
        <location filename="../window.py" line="2054"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>无法获取实际用量：未找到 metrics-server。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2191"/>
        <source>Refreshing...</source>
        <translation>正在刷新...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2382"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="2384"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="2387"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="2390"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="2392"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>集群中共 {count} 个 Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2394"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="2397"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="2399"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2401"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="2404"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="2407"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2410"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2412"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="2414"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>集群中共 {count} 个 Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2416"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>集群中共 {count} 个 Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2418"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>集群中共 {count} 个 Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2421"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>集群中共 {count} 个 Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2423"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>集群中共 {count} 个 Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="2424"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>集群中共 {count} 个 Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="2435"/>
        <location filename="../window.py" line="2501"/>
        <source>Running</source>
        <translation>运行中</translation>
    </message>
    <message>
        <location filename="../window.py" line="1074"/>
        <location filename="../window.py" line="2436"/>
        <location filename="../window.py" line="2497"/>
        <source>Pending</source>
        <translation>等待中</translation>
    </message>
    <message>
        <location filename="../window.py" line="2437"/>
        <source>Succeeded</source>
        <translation>已成功</translation>
    </message>
    <message>
        <location filename="../window.py" line="1070"/>
        <location filename="../window.py" line="2438"/>
        <location filename="../window.py" line="2496"/>
        <source>Failed</source>
        <translation>已失败</translation>
    </message>
    <message>
        <location filename="../window.py" line="2439"/>
        <source>Unknown</source>
        <translation>未知</translation>
    </message>
    <message>
        <location filename="../window.py" line="2483"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2491"/>
        <source>Healthy</source>
        <translation>正常</translation>
    </message>
    <message>
        <location filename="../window.py" line="1069"/>
        <location filename="../window.py" line="2492"/>
        <source>Degraded</source>
        <translation>降级</translation>
    </message>
    <message>
        <location filename="../window.py" line="2493"/>
        <source>Unavailable</source>
        <translation>不可用</translation>
    </message>
    <message>
        <location filename="../window.py" line="2494"/>
        <source>Scaled to zero</source>
        <translation>已缩容至零</translation>
    </message>
    <message>
        <location filename="../window.py" line="2495"/>
        <source>Complete</source>
        <translation>已完成</translation>
    </message>
    <message>
        <location filename="../window.py" line="2498"/>
        <source>Suspended</source>
        <translation>已暂停</translation>
    </message>
    <message>
        <location filename="../window.py" line="1065"/>
        <location filename="../window.py" line="2499"/>
        <source>Active</source>
        <translation>活动</translation>
    </message>
    <message>
        <location filename="../window.py" line="2500"/>
        <source>Scheduled</source>
        <translation>已计划</translation>
    </message>
    <message>
        <location filename="../window.py" line="2545"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2548"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2551"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2554"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2557"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2559"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2560"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{namespaces} 个 namespaces 中共 {count} 个 CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2584"/>
        <source>{visible} of {total} Pods</source>
        <translation>{total} 个 Pods 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2585"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{total} 个 Deployments 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2586"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{total} 个 StatefulSets 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2587"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{total} 个 DaemonSets 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2588"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{total} 个 ReplicaSets 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2590"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{total} 个 ReplicationControllers 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2592"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{total} 个 Jobs 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2593"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{total} 个 CronJobs 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2594"/>
        <source>{visible} of {total} Services</source>
        <translation>{total} 个 Services 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2595"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{total} 个 Endpoint Slices 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2596"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{total} 个 Endpoints 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2597"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{total} 个 Ingresses 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2598"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{total} 个 Ingress Classes 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2599"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{total} 个 Network Policies 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2600"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>{total} 个 Config Maps 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2601"/>
        <source>{visible} of {total} Secrets</source>
        <translation>{total} 个 Secrets 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2602"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>{total} 个 Resource Quotas 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2603"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>{total} 个 Limit Ranges 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2605"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>{total} 个 Horizontal Pod Autoscalers 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2608"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>{total} 个 Pod Disruption Budgets 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2610"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>{total} 个 Priority Classes 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2611"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>{total} 个 Runtime Classes 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2612"/>
        <source>{visible} of {total} Leases</source>
        <translation>{total} 个 Leases 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2614"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>{total} 个 Mutating Webhook Configurations 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2617"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>{total} 个 Validating Webhook Configurations 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2619"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>{total} 个 Node Groups 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2620"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>{total} 个 Add-ons 中的 {visible} 个</translation>
    </message>
    <message>
        <location filename="../window.py" line="2666"/>
        <source>Loading...</source>
        <translation>正在加载...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2712"/>
        <location filename="../window.py" line="2804"/>
        <source>Pod: {name}</source>
        <translation>Pod：{name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2758"/>
        <source>Pods of {name}</source>
        <translation>{name} 的 Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2760"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{namespace} / {name} 中共 {count} 个 Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2825"/>
        <source>No Pods are associated with this workload</source>
        <translation>此 workload 没有关联的 Pod</translation>
    </message>
    <message>
        <location filename="../window.py" line="2832"/>
        <location filename="../window.py" line="2855"/>
        <source>Logs</source>
        <translation>日志</translation>
    </message>
    <message>
        <location filename="../window.py" line="2832"/>
        <source>This workload has no Pods.</source>
        <translation>此 workload 没有 Pod。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2841"/>
        <location filename="../window.py" line="2864"/>
        <source>View logs</source>
        <translation>查看日志</translation>
    </message>
    <message>
        <location filename="../window.py" line="2842"/>
        <source>Select the Pod:</source>
        <translation>选择 Pod：</translation>
    </message>
    <message>
        <location filename="../window.py" line="2856"/>
        <source>Pod {name} has no containers.</source>
        <translation>Pod {name} 没有容器。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2865"/>
        <source>Select the container of {name}:</source>
        <translation>选择 {name} 的容器：</translation>
    </message>
    <message>
        <location filename="../window.py" line="2891"/>
        <source>Save to a file</source>
        <translation>保存到文件</translation>
    </message>
    <message>
        <location filename="../window.py" line="2902"/>
        <source>Could not save</source>
        <translation>无法保存</translation>
    </message>
    <message>
        <location filename="../window.py" line="2903"/>
        <source>The file could not be written: {reason}</source>
        <translation>无法写入文件：{reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2951"/>
        <source>Logs: {pod} / {container}</source>
        <translation>日志：{pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3001"/>
        <source>Automatic</source>
        <translation>自动</translation>
    </message>
    <message>
        <location filename="../window.py" line="3014"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>默认关闭。开启后，KubeScope 会将其操作记录写入 {path}，但绝不包含 Pod 日志或资源内容。分享前请先阅读：其中包含上下文名称。</translation>
    </message>
    <message>
        <location filename="../window.py" line="3045"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>在 kubeconfig 中未找到上下文。</translation>
    </message>
    <message>
        <location filename="../window.py" line="3074"/>
        <source>Choose a kubeconfig file</source>
        <translation>选择 kubeconfig 文件</translation>
    </message>
    <message>
        <location filename="../window.py" line="3120"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>第 {row} 行的登录命令无效。</translation>
    </message>
    <message>
        <location filename="../window.py" line="3133"/>
        <source>Light</source>
        <translation>浅色</translation>
    </message>
    <message>
        <location filename="../window.py" line="3133"/>
        <source>Dark</source>
        <translation>深色</translation>
    </message>
    <message>
        <location filename="../window.py" line="3152"/>
        <source>My theme</source>
        <translation>我的主题</translation>
    </message>
    <message>
        <location filename="../window.py" line="3196"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>缓存已清除。下次需要时会重新加载所有内容。</translation>
    </message>
    <message>
        <location filename="../window.py" line="3251"/>
        <source>Settings saved.</source>
        <translation>设置已保存。</translation>
    </message>
    <message>
        <location filename="../window.py" line="3290"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>您的用户无权执行此操作（{action}）。请向集群管理员申请访问权限。</translation>
    </message>
    <message>
        <location filename="../window.py" line="3295"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>您的用户无权执行此操作。请向集群管理员申请访问权限。</translation>
    </message>
    <message>
        <location filename="../window.py" line="3314"/>
        <source>Query failed</source>
        <translation>查询失败</translation>
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
        <translation>事件</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="293"/>
        <source>TYPE</source>
        <translation>类型</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="298"/>
        <source>SOURCE</source>
        <translation>来源</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>INVOLVED OBJECT</source>
        <translation>相关对象</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>MESSAGE</source>
        <translation>消息</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>COUNT</source>
        <translation>次数</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>AGE</source>
        <translation>存在时间</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>LAST SEEN</source>
        <translation>最后出现</translation>
    </message>
</context>
</TS>
