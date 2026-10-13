<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="hi">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>लॉगिन टूल नहीं मिला</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>आपका kubeconfig साइन इन के लिए “{tool}” चलाता है, लेकिन वह इंस्टॉल नहीं है या PATH में नहीं है। उसे इंस्टॉल करें और रीफ़्रेश करें।</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>कॉन्टेक्स्ट नहीं मिला</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>यह कॉन्टेक्स्ट आपके kubeconfig में नहीं है। ~/.kube/config जाँचें।</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>प्रमाणीकरण विफल</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>आपके क्रेडेंशियल की अवधि समाप्त हो गई होगी। फिर से साइन इन करें (उदाहरण के लिए “aws sso login”, “gcloud auth login” या “az login”) और रीफ़्रेश करें।</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Not an Amazon EKS cluster</source>
        <translation>यह Amazon EKS क्लस्टर नहीं है</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Node Groups, Add-ons and the AWS cards of the Overview exist only on Amazon EKS contexts.</source>
        <translation>Node Groups, Add-ons और ओवरव्यू के AWS कार्ड केवल Amazon EKS कॉन्टेक्स्ट में होते हैं।</translation>
    </message>
    <message>
        <location filename="../errors.py" line="110"/>
        <source>Unexpected answer from AWS</source>
        <translation>AWS से अप्रत्याशित उत्तर</translation>
    </message>
    <message>
        <location filename="../errors.py" line="111"/>
        <source>Update the AWS CLI to its latest version and refresh.</source>
        <translation>AWS CLI को नवीनतम संस्करण में अपडेट करें और रीफ़्रेश करें।</translation>
    </message>
    <message>
        <location filename="../errors.py" line="118"/>
        <location filename="../errors.py" line="128"/>
        <source>Access denied</source>
        <translation>पहुँच अस्वीकृत</translation>
    </message>
    <message>
        <location filename="../errors.py" line="119"/>
        <source>Your AWS identity is not allowed to read this. The wiki lists the eks: permissions KubeScope needs.</source>
        <translation>आपकी AWS पहचान को इसे पढ़ने की अनुमति नहीं है। KubeScope को जिन eks: अनुमतियों की ज़रूरत है, वे विकी में सूचीबद्ध हैं।</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>आपके उपयोगकर्ता को यह संसाधन पढ़ने की अनुमति नहीं है।</translation>
    </message>
    <message>
        <location filename="../errors.py" line="143"/>
        <source>No network connection</source>
        <translation>नेटवर्क कनेक्शन नहीं है</translation>
    </message>
    <message>
        <location filename="../errors.py" line="144"/>
        <source>Check your internet connection or VPN and refresh.</source>
        <translation>अपना इंटरनेट कनेक्शन या VPN जाँचें और रीफ़्रेश करें।</translation>
    </message>
    <message>
        <location filename="../errors.py" line="165"/>
        <source>Cluster unreachable</source>
        <translation>क्लस्टर तक पहुँच नहीं हो पा रही</translation>
    </message>
    <message>
        <location filename="../errors.py" line="166"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>अपना नेटवर्क या VPN जाँचें और देखें कि क्लस्टर चल रहा है।</translation>
    </message>
    <message>
        <location filename="../errors.py" line="172"/>
        <source>Something went wrong</source>
        <translation>कुछ गड़बड़ हो गई</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="42"/>
        <source>No log lines returned.</source>
        <translation>कोई लॉग पंक्ति नहीं मिली।</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="47"/>
        <source>Updated at {time}</source>
        <translation>{time} पर अपडेट किया गया</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="54"/>
        <source>Could not refresh logs: {message}</source>
        <translation>लॉग रीफ़्रेश नहीं हो सके: {message}</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>ऑटो-रीफ़्रेश</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>हर कुछ सेकंड में नई लॉग पंक्तियाँ लाएँ और लॉग के अंत का अनुसरण करें</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>अभी रीफ़्रेश करें</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../window.py" line="1540"/>
        <location filename="../window.py" line="1569"/>
        <source>TYPE</source>
        <translation>प्रकार</translation>
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
        <translation>पोर्ट</translation>
    </message>
    <message>
        <location filename="../window.py" line="1546"/>
        <source>ADDRESS TYPE</source>
        <translation>पता प्रकार</translation>
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
        <translation>क्लास</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <source>HOSTS</source>
        <translation>होस्ट</translation>
    </message>
    <message>
        <location filename="../window.py" line="1554"/>
        <source>ADDRESS</source>
        <translation>पता</translation>
    </message>
    <message>
        <location filename="../window.py" line="1558"/>
        <source>CONTROLLER</source>
        <translation>कंट्रोलर</translation>
    </message>
    <message>
        <location filename="../window.py" line="1559"/>
        <source>PARAMETERS</source>
        <translation>पैरामीटर</translation>
    </message>
    <message>
        <location filename="../window.py" line="1562"/>
        <source>POD SELECTOR</source>
        <translation>POD सेलेक्टर</translation>
    </message>
    <message>
        <location filename="../window.py" line="1563"/>
        <source>POLICY TYPES</source>
        <translation>पॉलिसी प्रकार</translation>
    </message>
    <message>
        <location filename="../window.py" line="1566"/>
        <location filename="../window.py" line="1570"/>
        <source>DATA</source>
        <translation>डेटा</translation>
    </message>
    <message>
        <location filename="../window.py" line="1573"/>
        <source>USAGE</source>
        <translation>उपयोग</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>TYPES</source>
        <translation>प्रकार</translation>
    </message>
    <message>
        <location filename="../window.py" line="1579"/>
        <source>REFERENCE</source>
        <translation>संदर्भ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1580"/>
        <source>MIN PODS</source>
        <translation>न्यूनतम PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1581"/>
        <source>MAX PODS</source>
        <translation>अधिकतम PODS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1582"/>
        <source>REPLICAS</source>
        <translation>रेप्लिका</translation>
    </message>
    <message>
        <location filename="../window.py" line="1585"/>
        <source>MIN AVAILABLE</source>
        <translation>न्यूनतम उपलब्ध</translation>
    </message>
    <message>
        <location filename="../window.py" line="1586"/>
        <source>MAX UNAVAILABLE</source>
        <translation>अधिकतम अनुपलब्ध</translation>
    </message>
    <message>
        <location filename="../window.py" line="1587"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>अनुमत व्यवधान</translation>
    </message>
    <message>
        <location filename="../window.py" line="1590"/>
        <source>VALUE</source>
        <translation>मान</translation>
    </message>
    <message>
        <location filename="../window.py" line="1591"/>
        <source>GLOBAL DEFAULT</source>
        <translation>ग्लोबल डिफ़ॉल्ट</translation>
    </message>
    <message>
        <location filename="../window.py" line="1594"/>
        <source>HANDLER</source>
        <translation>HANDLER</translation>
    </message>
    <message>
        <location filename="../window.py" line="1597"/>
        <source>HOLDER</source>
        <translation>धारक</translation>
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
        <translation>स्थिति</translation>
    </message>
    <message>
        <location filename="../window.py" line="1607"/>
        <source>INSTANCE TYPES</source>
        <translation>इंस्टेंस प्रकार</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <source>NODES</source>
        <translation>नोड</translation>
    </message>
    <message>
        <location filename="../window.py" line="1609"/>
        <source>AMI TYPE</source>
        <translation>AMI प्रकार</translation>
    </message>
    <message>
        <location filename="../window.py" line="1610"/>
        <source>AMI VERSION</source>
        <translation>AMI संस्करण</translation>
    </message>
    <message>
        <location filename="../window.py" line="1614"/>
        <location filename="../ui/main_window.ui" line="2557"/>
        <source>VERSION</source>
        <translation>संस्करण</translation>
    </message>
    <message>
        <location filename="../window.py" line="1615"/>
        <source>SOURCE</source>
        <translation>स्रोत</translation>
    </message>
    <message>
        <location filename="../window.py" line="1625"/>
        <source>COMPLETIONS</source>
        <translation>पूर्णताएँ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1626"/>
        <source>SCHEDULE</source>
        <translation>शेड्यूल</translation>
    </message>
    <message>
        <location filename="../window.py" line="1627"/>
        <location filename="../ui/main_window.ui" line="2018"/>
        <source>READY</source>
        <translation>तैयार</translation>
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
        <translation>नाम</translation>
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
        <translation>मेमोरी</translation>
    </message>
    <message>
        <location filename="../window.py" line="1639"/>
        <source>RESTARTS</source>
        <translation>रीस्टार्ट</translation>
    </message>
    <message>
        <location filename="../window.py" line="1640"/>
        <location filename="../window.py" line="1652"/>
        <location filename="../ui/main_window.ui" line="2028"/>
        <location filename="../ui/main_window.ui" line="2577"/>
        <source>AGE</source>
        <translation>आयु</translation>
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
        <translation>Kubernetes कंसोल</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="339"/>
        <source>CONTEXT</source>
        <translation>कॉन्टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>आपके kubeconfig का Kubernetes कॉन्टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="372"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>क्लाउड CLI से साइन इन करें, फिर क्लस्टर डेटा फिर से लोड करें</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="375"/>
        <source>Sign in</source>
        <translation>साइन इन</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="397"/>
        <source>Settings</source>
        <translation>सेटिंग्स</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="437"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>आपके kubeconfig में कोई क्लस्टर कॉन्टेक्स्ट नहीं मिला। अपने kubeconfig में क्लस्टर जोड़ें (उदाहरण के लिए AWS CLI से: aws eks update-kubeconfig) और फिर से लोड करें।</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="478"/>
        <source>Dismiss</source>
        <translation>बंद करें</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="569"/>
        <source>MONITORING</source>
        <translation>मॉनिटरिंग</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1714"/>
        <source>Overview</source>
        <translation>ओवरव्यू</translation>
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
        <translation>नेटवर्क</translation>
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
        <translation>कॉन्फ़िग</translation>
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
        <translation>सुरक्षित पहुँच
संसाधन केवल-पढ़ने मोड में</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1721"/>
        <source>Cluster resources and capacity</source>
        <translation>क्लस्टर संसाधन और क्षमता</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1746"/>
        <location filename="../ui/main_window.ui" line="1759"/>
        <location filename="../ui/main_window.ui" line="1772"/>
        <source>Refresh</source>
        <translation>रीफ़्रेश</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1878"/>
        <source>Search by name or namespace...</source>
        <translation>नाम या namespace से खोजें...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1929"/>
        <source>View Pods of the selected workload</source>
        <translation>चुने गए workload के Pods देखें</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1945"/>
        <source>View JSON details of the selected workload</source>
        <translation>चुने गए workload का JSON विवरण देखें</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1948"/>
        <source>Details</source>
        <translation>विवरण</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1961"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>चुने गए workload के किसी Pod के लॉग देखें</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1964"/>
        <source>Logs</source>
        <translation>लॉग</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2507"/>
        <source>Nodes</source>
        <translation>नोड</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2542"/>
        <source>NODE</source>
        <translation>नोड</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2552"/>
        <source>ROLE</source>
        <translation>भूमिका</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2572"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2590"/>
        <source>Select a context to load workloads</source>
        <translation>workloads लोड करने के लिए कॉन्टेक्स्ट चुनें</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2613"/>
        <source>Data fetched from the cluster API</source>
        <translation>डेटा क्लस्टर API से लिया गया</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2674"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>DCO Tecnologia की वेबसाइट खोलें</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2694"/>
        <source>MIT License</source>
        <translation>MIT लाइसेंस</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2697"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope ओपन सोर्स सॉफ़्टवेयर है, जो MIT लाइसेंस के अंतर्गत जारी किया गया है</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2733"/>
        <source>Update available</source>
        <translation>अपडेट उपलब्ध</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2736"/>
        <source>Open the download page of the new version</source>
        <translation>नए संस्करण का डाउनलोड पेज खोलें</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Check for updates</source>
        <translation>अपडेट जाँचें</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2784"/>
        <source>Open the project on GitHub</source>
        <translation>GitHub पर प्रोजेक्ट खोलें</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="2030"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>नोड तैयार</translation>
    </message>
    <message>
        <location filename="../window.py" line="2046"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>कोर अनुरोधित / आवंटन योग्य</translation>
    </message>
    <message>
        <location filename="../window.py" line="2060"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>अनुरोधित / आवंटन योग्य</translation>
    </message>
    <message>
        <location filename="../window.py" line="2079"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>क्लस्टर में</translation>
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
        <translation>क्लस्टर संसाधन</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="78"/>
        <source>CLUSTER INFO</source>
        <translation>क्लस्टर जानकारी</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="125"/>
        <source>NETWORKING</source>
        <translation>नेटवर्किंग</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="174"/>
        <source>NODES</source>
        <translation>नोड</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="228"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="248"/>
        <source>running / capacity</source>
        <translation>चल रहे / क्षमता</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="295"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="362"/>
        <source>MEMORY</source>
        <translation>मेमोरी</translation>
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
        <translation>नाम</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>तैयार</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>चरण</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>कंटेनर</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>आयु</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>Pod विवरण</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>लॉग देखें</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>बंद करें</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="3069"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>अपने कॉन्टेक्स्ट को आसान नाम दें। मूल नाम रखने के लिए नाम खाली छोड़ें।</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>बदलाव सहेजें</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>सामान्य</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="107"/>
        <source>Language</source>
        <translation>भाषा</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="142"/>
        <source>Theme</source>
        <translation>थीम</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="177"/>
        <source>New theme...</source>
        <translation>नई थीम...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>थीम संपादित करें...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>थीम फ़ोल्डर खोलें</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>डिफ़ॉल्ट namespace</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>वह namespace जिस पर हर कॉन्टेक्स्ट खुलता है। सभी दिखाने के लिए खाली छोड़ें।</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>आख़िरी इस्तेमाल किया गया कॉन्टेक्स्ट याद रखें</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>ऐप शुरू होने पर नए संस्करण के लिए GitHub जाँचें</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>सार्वजनिक GitHub API से नवीनतम रिलीज़ पूछता है और ऐप के संस्करण के अलावा कुछ नहीं भेजता। फ़ुटर का आइकन माँगने पर जाँच करता है।</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>डीबग मोड: साझा करने योग्य लॉग फ़ाइल लिखें</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>लॉग फ़ोल्डर खोलें</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>कैश साफ़ करें</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>अब तक लोड की गई सूचियाँ और ओवरव्यू तथा हर क्लस्टर का साइन-इन भूल जाता है, इसलिए अगला अनुरोध फिर साइन इन करके सब कुछ दोबारा लोड करेगा। आपकी सेटिंग्स बनी रहती हैं।</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>KUBECONFIG फ़ाइलें</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>KubeScope KUBECONFIG वेरिएबल की फ़ाइलें, या ~/.kube/config पढ़ता है। उनकी जगह इन्हें पढ़ने के लिए यहाँ फ़ाइलें जोड़ें। लागू करने के लिए सहेजें दबाएँ।</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>फ़ाइल जोड़ें...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>हटाएँ</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>साइन-इन कमांड</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>ऐसे क्लाउड के लिए जिसे KubeScope नहीं जानता, वह प्रोग्राम बताएँ जिसे आपका kubeconfig साइन इन के लिए इस्तेमाल करता है (उदाहरण के लिए oci) और साइन इन करने वाला कमांड (उदाहरण के लिए oci session authenticate)। साइन इन बटन उसे बिना शेल के चलाता है। लागू करने के लिए सहेजें दबाएँ।</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>प्रोग्राम</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>साइन-इन कमांड</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>पंक्ति जोड़ें</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>कॉन्टेक्स्ट के नाम</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>कॉन्टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>प्रदर्शित नाम</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>पेज की पृष्ठभूमि</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>पैनल और कार्ड</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>वैकल्पिक पैनल</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>बार ट्रैक</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>किनारे</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>शीर्ष बार</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>शीर्ष बार का लोगो</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>शीर्ष बार का चयनकर्ता</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>शीर्ष बार के चयनकर्ता का किनारा</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>शीर्ष बार का चयन</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>शीर्ष बार का टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>साइडबार का शीर्षक</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>गौण टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>निष्क्रिय टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>एक्सेंट टेक्स्ट और लिंक</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>एक्सेंट बटन</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>होवर पर एक्सेंट बटन</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>निष्क्रिय होने पर एक्सेंट बटन</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>फ़ोकस और हाइलाइट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>बैज का टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>एक्सेंट टिंट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>टेक्स्ट चयन</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>एक्सेंट किनारा</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>शीर्ष बार और एक्सेंट बटनों पर टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>स्वस्थ का टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>स्वस्थ की पृष्ठभूमि</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>चेतावनी का टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>चेतावनी की पृष्ठभूमि</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>विफलता का टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>विफलता की पृष्ठभूमि</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>निष्क्रिय का टेक्स्ट</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>निष्क्रिय की पृष्ठभूमि</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>समस्या वाली पंक्ति</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>नए Pod की पंक्ति</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>उपयोग बार, भर रहा है</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>उपयोग बार, लगभग भरा</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>स्वास्थ्य बार, स्वस्थ</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>स्वास्थ्य बार, चेतावनी</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>स्वास्थ्य बार, विफल</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>नई थीम</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>थीम संपादित करें: {name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>थीम का नाम</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>हल्की</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>गहरी</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>नाम</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>आधार</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>रंग</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>इस टैब की सामग्री फ़ाइल में सहेजें</translation>
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
        <location filename="../window.py" line="3307"/>
        <source>All namespaces</source>
        <translation>सभी namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="832"/>
        <source>Loading contexts...</source>
        <translation>कॉन्टेक्स्ट लोड हो रहे हैं...</translation>
    </message>
    <message>
        <location filename="../window.py" line="841"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>kubeconfig लोड नहीं हो सका: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="863"/>
        <source>No contexts found in kubeconfig</source>
        <translation>kubeconfig में कोई कॉन्टेक्स्ट नहीं मिला</translation>
    </message>
    <message>
        <location filename="../window.py" line="892"/>
        <location filename="../window.py" line="970"/>
        <source>Unpin from the top</source>
        <translation>ऊपर से हटाएँ</translation>
    </message>
    <message>
        <location filename="../window.py" line="892"/>
        <source>Pin to the top</source>
        <translation>ऊपर पिन करें</translation>
    </message>
    <message>
        <location filename="../window.py" line="1008"/>
        <source>Close</source>
        <translation>बंद करें</translation>
    </message>
    <message>
        <location filename="../window.py" line="1055"/>
        <source>Status</source>
        <translation>स्थिति</translation>
    </message>
    <message>
        <location filename="../window.py" line="1056"/>
        <source>Kubernetes version</source>
        <translation>Kubernetes संस्करण</translation>
    </message>
    <message>
        <location filename="../window.py" line="1057"/>
        <source>Platform version</source>
        <translation>प्लेटफ़ॉर्म संस्करण</translation>
    </message>
    <message>
        <location filename="../window.py" line="1058"/>
        <source>Created</source>
        <translation>बनाया गया</translation>
    </message>
    <message>
        <location filename="../window.py" line="1059"/>
        <source>Provider</source>
        <translation>प्रदाता</translation>
    </message>
    <message>
        <location filename="../window.py" line="1062"/>
        <source>API server endpoint</source>
        <translation>API सर्वर endpoint</translation>
    </message>
    <message>
        <location filename="../window.py" line="1063"/>
        <source>Cluster ARN</source>
        <translation>क्लस्टर ARN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1064"/>
        <source>Cluster IAM role ARN</source>
        <translation>क्लस्टर IAM रोल ARN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1065"/>
        <source>OpenID Connect provider URL</source>
        <translation>OpenID Connect प्रदाता URL</translation>
    </message>
    <message>
        <location filename="../window.py" line="1073"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1074"/>
        <source>Cluster security group</source>
        <translation>क्लस्टर security group</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Additional security groups</source>
        <translation>अतिरिक्त security groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>None</source>
        <translation>कोई नहीं</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>API server endpoint access</source>
        <translation>API सर्वर endpoint पहुँच</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>Cluster IP address family</source>
        <translation>क्लस्टर IP पता परिवार</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Service IPv4 range</source>
        <translation>सर्विस IPv4 रेंज</translation>
    </message>
    <message>
        <location filename="../window.py" line="1086"/>
        <source>Public access source allowlist</source>
        <translation>सार्वजनिक पहुँच स्रोत सूची</translation>
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
        <translation>सक्रिय</translation>
    </message>
    <message>
        <location filename="../window.py" line="1100"/>
        <source>Creating</source>
        <translation>बनाया जा रहा है</translation>
    </message>
    <message>
        <location filename="../window.py" line="1101"/>
        <source>Updating</source>
        <translation>अपडेट हो रहा है</translation>
    </message>
    <message>
        <location filename="../window.py" line="1102"/>
        <source>Deleting</source>
        <translation>हटाया जा रहा है</translation>
    </message>
    <message>
        <location filename="../window.py" line="1103"/>
        <location filename="../window.py" line="2524"/>
        <source>Degraded</source>
        <translation>बिगड़ा हुआ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1104"/>
        <location filename="../window.py" line="2470"/>
        <location filename="../window.py" line="2528"/>
        <source>Failed</source>
        <translation>विफल</translation>
    </message>
    <message>
        <location filename="../window.py" line="1105"/>
        <source>Creation failed</source>
        <translation>निर्माण विफल</translation>
    </message>
    <message>
        <location filename="../window.py" line="1106"/>
        <source>Update failed</source>
        <translation>अपडेट विफल</translation>
    </message>
    <message>
        <location filename="../window.py" line="1107"/>
        <source>Deletion failed</source>
        <translation>हटाना विफल</translation>
    </message>
    <message>
        <location filename="../window.py" line="1108"/>
        <location filename="../window.py" line="2468"/>
        <location filename="../window.py" line="2529"/>
        <source>Pending</source>
        <translation>लंबित</translation>
    </message>
    <message>
        <location filename="../window.py" line="1109"/>
        <source>Deployed</source>
        <translation>तैनात</translation>
    </message>
    <message>
        <location filename="../window.py" line="1110"/>
        <source>Superseded</source>
        <translation>प्रतिस्थापित</translation>
    </message>
    <message>
        <location filename="../window.py" line="1111"/>
        <source>Uninstalled</source>
        <translation>अनइंस्टॉल किया गया</translation>
    </message>
    <message>
        <location filename="../window.py" line="1112"/>
        <source>Uninstalling</source>
        <translation>अनइंस्टॉल हो रहा है</translation>
    </message>
    <message>
        <location filename="../window.py" line="1113"/>
        <source>Pending install</source>
        <translation>इंस्टॉल लंबित</translation>
    </message>
    <message>
        <location filename="../window.py" line="1114"/>
        <source>Pending upgrade</source>
        <translation>अपग्रेड लंबित</translation>
    </message>
    <message>
        <location filename="../window.py" line="1115"/>
        <source>Pending rollback</source>
        <translation>रोलबैक लंबित</translation>
    </message>
    <message>
        <location filename="../window.py" line="1116"/>
        <source>Public</source>
        <translation>सार्वजनिक</translation>
    </message>
    <message>
        <location filename="../window.py" line="1117"/>
        <source>Private</source>
        <translation>निजी</translation>
    </message>
    <message>
        <location filename="../window.py" line="1118"/>
        <source>Public and private</source>
        <translation>सार्वजनिक और निजी</translation>
    </message>
    <message>
        <location filename="../window.py" line="1210"/>
        <source>Overview</source>
        <translation>ओवरव्यू</translation>
    </message>
    <message>
        <location filename="../window.py" line="1211"/>
        <source>Cluster resources and capacity</source>
        <translation>क्लस्टर संसाधन और क्षमता</translation>
    </message>
    <message>
        <location filename="../window.py" line="1213"/>
        <source>Details &amp; Logs</source>
        <translation>विवरण और लॉग</translation>
    </message>
    <message>
        <location filename="../window.py" line="1215"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>संसाधन विवरण और Pod लॉग, हर एक का अलग टैब</translation>
    </message>
    <message>
        <location filename="../window.py" line="1218"/>
        <source>Settings</source>
        <translation>सेटिंग्स</translation>
    </message>
    <message>
        <location filename="../window.py" line="1219"/>
        <source>Preferences and context names</source>
        <translation>प्राथमिकताएँ और कॉन्टेक्स्ट के नाम</translation>
    </message>
    <message>
        <location filename="../window.py" line="1221"/>
        <source>Workloads overview</source>
        <translation>Workloads ओवरव्यू</translation>
    </message>
    <message>
        <location filename="../window.py" line="1223"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>हर workload प्रकार का स्वास्थ्य और नवीनतम इवेंट</translation>
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
        <translation>क्लस्टर के Pods</translation>
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
        <translation>क्लस्टर के Deployments</translation>
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
        <translation>क्लस्टर के StatefulSets</translation>
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
        <translation>क्लस्टर के DaemonSets</translation>
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
        <translation>क्लस्टर के ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1245"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1246"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>क्लस्टर के ReplicationControllers</translation>
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
        <translation>क्लस्टर के Jobs</translation>
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
        <translation>क्लस्टर के CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1250"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1250"/>
        <source>Services of the cluster</source>
        <translation>क्लस्टर के Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1252"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1253"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>क्लस्टर के Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1256"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1257"/>
        <source>Endpoints of the cluster</source>
        <translation>क्लस्टर के Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1260"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1261"/>
        <source>Ingresses of the cluster</source>
        <translation>क्लस्टर के Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1264"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1265"/>
        <source>Ingress Classes of the cluster</source>
        <translation>क्लस्टर के Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1269"/>
        <source>Network Policies of the cluster</source>
        <translation>क्लस्टर के Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1273"/>
        <source>Config Maps of the cluster</source>
        <translation>क्लस्टर के Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1276"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1277"/>
        <source>Secrets of the cluster</source>
        <translation>क्लस्टर के Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1280"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1281"/>
        <source>Resource Quotas of the cluster</source>
        <translation>क्लस्टर के Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1284"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1285"/>
        <source>Limit Ranges of the cluster</source>
        <translation>क्लस्टर के Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1288"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1289"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>क्लस्टर के Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1292"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1293"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>क्लस्टर के Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1296"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1297"/>
        <source>Priority Classes of the cluster</source>
        <translation>क्लस्टर के Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1300"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1301"/>
        <source>Runtime Classes of the cluster</source>
        <translation>क्लस्टर के Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1304"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1305"/>
        <source>Leases of the cluster</source>
        <translation>क्लस्टर के Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1308"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1309"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>क्लस्टर के Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1312"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1313"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>क्लस्टर के Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1316"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1317"/>
        <source>Node Groups of the cluster</source>
        <translation>क्लस्टर के Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1320"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1321"/>
        <source>Add-ons of the cluster</source>
        <translation>क्लस्टर के Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Version {version}</source>
        <translation>संस्करण {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1333"/>
        <source>Open the project on GitHub</source>
        <translation>GitHub पर प्रोजेक्ट खोलें</translation>
    </message>
    <message>
        <location filename="../window.py" line="1367"/>
        <source>Up to date</source>
        <translation>अद्यतित</translation>
    </message>
    <message>
        <location filename="../window.py" line="1368"/>
        <source>Could not check</source>
        <translation>जाँच नहीं हो सकी</translation>
    </message>
    <message>
        <location filename="../window.py" line="1379"/>
        <source>Check for updates</source>
        <translation>अपडेट जाँचें</translation>
    </message>
    <message>
        <location filename="../window.py" line="1380"/>
        <source>Checking for updates...</source>
        <translation>अपडेट जाँचे जा रहे हैं...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1381"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope अद्यतित है। फिर जाँचने के लिए क्लिक करें।</translation>
    </message>
    <message>
        <location filename="../window.py" line="1382"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>अपडेट नहीं जाँचे जा सके। फिर कोशिश करने के लिए क्लिक करें।</translation>
    </message>
    <message>
        <location filename="../window.py" line="1388"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>अपडेट उपलब्ध: {version}। डाउनलोड पेज खोलने के लिए क्लिक करें; फिर जाँचने के लिए राइट-क्लिक करें।</translation>
    </message>
    <message>
        <location filename="../window.py" line="1396"/>
        <source>Update available</source>
        <translation>अपडेट उपलब्ध</translation>
    </message>
    <message>
        <location filename="../window.py" line="1398"/>
        <source>Download KubeScope {version}</source>
        <translation>KubeScope {version} डाउनलोड करें</translation>
    </message>
    <message>
        <location filename="../window.py" line="1434"/>
        <source>Check for updates again</source>
        <translation>अपडेट फिर से जाँचें</translation>
    </message>
    <message>
        <location filename="../window.py" line="1531"/>
        <location filename="../window.py" line="2206"/>
        <source>Loading resources...</source>
        <translation>संसाधन लोड हो रहे हैं...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1775"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>AWS क्रेडेंशियल कॉन्फ़िगर करें ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1779"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>प्रोफ़ाइल {profile} के AWS क्रेडेंशियल गायब या अमान्य हैं</translation>
    </message>
    <message>
        <location filename="../window.py" line="1784"/>
        <source>Sign in to {provider}</source>
        <translation>{provider} में साइन इन करें</translation>
    </message>
    <message>
        <location filename="../window.py" line="1787"/>
        <source>Not signed in to {provider}</source>
        <translation>{provider} में साइन इन नहीं है</translation>
    </message>
    <message>
        <location filename="../window.py" line="1791"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>{provider} में साइन इन करें ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1797"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>{provider} में साइन इन नहीं है (प्रोफ़ाइल {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1818"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>खुले टर्मिनल में पूरा करें, फिर रीफ़्रेश दबाएँ।</translation>
    </message>
    <message>
        <location filename="../window.py" line="1837"/>
        <source>Loading workloads...</source>
        <translation>workloads लोड हो रहे हैं...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1898"/>
        <source>Could not read: {names}</source>
        <translation>पढ़ा नहीं जा सका: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1958"/>
        <source>Loading cluster data...</source>
        <translation>क्लस्टर डेटा लोड हो रहा है...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2039"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>चल रहे · {pending} लंबित · {failed} विफल</translation>
    </message>
    <message>
        <location filename="../window.py" line="2048"/>
        <location filename="../window.py" line="2062"/>
        <source> · usage {value}</source>
        <translation> · उपयोग {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2086"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>वास्तविक उपयोग उपलब्ध नहीं: metrics-server नहीं मिला।</translation>
    </message>
    <message>
        <location filename="../window.py" line="2111"/>
        <source>Ready</source>
        <translation>तैयार</translation>
    </message>
    <message>
        <location filename="../window.py" line="2111"/>
        <source>Not ready</source>
        <translation>तैयार नहीं</translation>
    </message>
    <message>
        <location filename="../window.py" line="2223"/>
        <source>Refreshing...</source>
        <translation>रीफ़्रेश हो रहा है...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2414"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="2416"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="2419"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="2422"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="2424"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>क्लस्टर में {count} Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2426"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="2429"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="2431"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2433"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="2436"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="2439"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2442"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2444"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="2446"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>क्लस्टर में {count} Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2448"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>क्लस्टर में {count} Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2450"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>क्लस्टर में {count} Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2453"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>क्लस्टर में {count} Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2455"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>क्लस्टर में {count} Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="2456"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>क्लस्टर में {count} Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="2467"/>
        <location filename="../window.py" line="2533"/>
        <source>Running</source>
        <translation>चल रहा है</translation>
    </message>
    <message>
        <location filename="../window.py" line="2469"/>
        <source>Succeeded</source>
        <translation>सफल</translation>
    </message>
    <message>
        <location filename="../window.py" line="2471"/>
        <source>Unknown</source>
        <translation>अज्ञात</translation>
    </message>
    <message>
        <location filename="../window.py" line="2515"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2523"/>
        <source>Healthy</source>
        <translation>स्वस्थ</translation>
    </message>
    <message>
        <location filename="../window.py" line="2525"/>
        <source>Unavailable</source>
        <translation>अनुपलब्ध</translation>
    </message>
    <message>
        <location filename="../window.py" line="2526"/>
        <source>Scaled to zero</source>
        <translation>शून्य पर स्केल किया गया</translation>
    </message>
    <message>
        <location filename="../window.py" line="2527"/>
        <source>Complete</source>
        <translation>पूर्ण</translation>
    </message>
    <message>
        <location filename="../window.py" line="2530"/>
        <source>Suspended</source>
        <translation>निलंबित</translation>
    </message>
    <message>
        <location filename="../window.py" line="2532"/>
        <source>Scheduled</source>
        <translation>शेड्यूल किया गया</translation>
    </message>
    <message>
        <location filename="../window.py" line="2577"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2580"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2583"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2586"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2589"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2591"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2592"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{namespaces} namespaces में {count} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2616"/>
        <source>{visible} of {total} Pods</source>
        <translation>{total} में से {visible} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2617"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{total} में से {visible} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2618"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{total} में से {visible} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2619"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{total} में से {visible} DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2620"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{total} में से {visible} ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2622"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{total} में से {visible} ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2624"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{total} में से {visible} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2625"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{total} में से {visible} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2626"/>
        <source>{visible} of {total} Services</source>
        <translation>{total} में से {visible} Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="2627"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{total} में से {visible} Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="2628"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{total} में से {visible} Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="2629"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{total} में से {visible} Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="2630"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{total} में से {visible} Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2631"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{total} में से {visible} Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="2632"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>{total} में से {visible} Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="2633"/>
        <source>{visible} of {total} Secrets</source>
        <translation>{total} में से {visible} Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2634"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>{total} में से {visible} Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="2635"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>{total} में से {visible} Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="2637"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>{total} में से {visible} Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2640"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>{total} में से {visible} Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2642"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>{total} में से {visible} Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2643"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>{total} में से {visible} Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2644"/>
        <source>{visible} of {total} Leases</source>
        <translation>{total} में से {visible} Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="2646"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>{total} में से {visible} Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2649"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>{total} में से {visible} Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2651"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>{total} में से {visible} Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="2652"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>{total} में से {visible} Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="2698"/>
        <source>Loading...</source>
        <translation>लोड हो रहा है...</translation>
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
        <translation>{name} के Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2792"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{namespace} / {name} में {count} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2857"/>
        <source>No Pods are associated with this workload</source>
        <translation>इस workload से कोई Pod जुड़ा नहीं है</translation>
    </message>
    <message>
        <location filename="../window.py" line="2864"/>
        <location filename="../window.py" line="2887"/>
        <source>Logs</source>
        <translation>लॉग</translation>
    </message>
    <message>
        <location filename="../window.py" line="2864"/>
        <source>This workload has no Pods.</source>
        <translation>इस workload में कोई Pod नहीं है।</translation>
    </message>
    <message>
        <location filename="../window.py" line="2873"/>
        <location filename="../window.py" line="2896"/>
        <source>View logs</source>
        <translation>लॉग देखें</translation>
    </message>
    <message>
        <location filename="../window.py" line="2874"/>
        <source>Select the Pod:</source>
        <translation>Pod चुनें:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2888"/>
        <source>Pod {name} has no containers.</source>
        <translation>Pod {name} में कोई कंटेनर नहीं है।</translation>
    </message>
    <message>
        <location filename="../window.py" line="2897"/>
        <source>Select the container of {name}:</source>
        <translation>{name} का कंटेनर चुनें:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2923"/>
        <source>Save to a file</source>
        <translation>फ़ाइल में सहेजें</translation>
    </message>
    <message>
        <location filename="../window.py" line="2934"/>
        <source>Could not save</source>
        <translation>सहेजा नहीं जा सका</translation>
    </message>
    <message>
        <location filename="../window.py" line="2935"/>
        <source>The file could not be written: {reason}</source>
        <translation>फ़ाइल लिखी नहीं जा सकी: {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2982"/>
        <source>Logs: {pod} / {container}</source>
        <translation>लॉग: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3032"/>
        <source>Automatic</source>
        <translation>स्वचालित</translation>
    </message>
    <message>
        <location filename="../window.py" line="3045"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>डिफ़ॉल्ट रूप से बंद। चालू होने पर KubeScope जो करता है वह {path} में लिखता है, Pod लॉग या संसाधनों की सामग्री कभी नहीं। साझा करने से पहले पढ़ लें: इसमें कॉन्टेक्स्ट के नाम होते हैं।</translation>
    </message>
    <message>
        <location filename="../window.py" line="3076"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>kubeconfig में कोई कॉन्टेक्स्ट नहीं मिला।</translation>
    </message>
    <message>
        <location filename="../window.py" line="3105"/>
        <source>Choose a kubeconfig file</source>
        <translation>kubeconfig फ़ाइल चुनें</translation>
    </message>
    <message>
        <location filename="../window.py" line="3151"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>पंक्ति {row} का साइन-इन कमांड मान्य नहीं है।</translation>
    </message>
    <message>
        <location filename="../window.py" line="3164"/>
        <source>Light</source>
        <translation>हल्की</translation>
    </message>
    <message>
        <location filename="../window.py" line="3164"/>
        <source>Dark</source>
        <translation>गहरी</translation>
    </message>
    <message>
        <location filename="../window.py" line="3183"/>
        <source>My theme</source>
        <translation>मेरी थीम</translation>
    </message>
    <message>
        <location filename="../window.py" line="3227"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>कैश साफ़ किया गया। जब भी ज़रूरत होगी, सब कुछ फिर से लोड होगा।</translation>
    </message>
    <message>
        <location filename="../window.py" line="3282"/>
        <source>Settings saved.</source>
        <translation>सेटिंग्स सहेजी गईं।</translation>
    </message>
    <message>
        <location filename="../window.py" line="3321"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>आपके उपयोगकर्ता को यह करने की अनुमति नहीं है: {action}। पहुँच के लिए अपने क्लस्टर एडमिन से कहें।</translation>
    </message>
    <message>
        <location filename="../window.py" line="3326"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>आपके उपयोगकर्ता को यह करने की अनुमति नहीं है। पहुँच के लिए अपने क्लस्टर एडमिन से कहें।</translation>
    </message>
    <message>
        <location filename="../window.py" line="3345"/>
        <source>Query failed</source>
        <translation>क्वेरी विफल</translation>
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
        <translation>इवेंट</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="293"/>
        <source>TYPE</source>
        <translation>प्रकार</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="298"/>
        <source>SOURCE</source>
        <translation>स्रोत</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>INVOLVED OBJECT</source>
        <translation>संबंधित ऑब्जेक्ट</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>MESSAGE</source>
        <translation>संदेश</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>COUNT</source>
        <translation>गिनती</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>AGE</source>
        <translation>आयु</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>LAST SEEN</source>
        <translation>आख़िरी बार देखा</translation>
    </message>
</context>
</TS>
