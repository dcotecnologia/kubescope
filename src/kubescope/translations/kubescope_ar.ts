<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ar">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>لم يتم العثور على أداة تسجيل الدخول</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>يشغّل ملف kubeconfig الخاص بك «{tool}» لتسجيل الدخول، لكنه غير مثبّت أو ليس في PATH. ثبّته ثم حدّث.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>لم يتم العثور على السياق</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>هذا السياق غير موجود في ملف kubeconfig. تحقق من ~/.kube/config.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>فشلت المصادقة</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>ربما انتهت صلاحية بيانات اعتمادك. سجّل الدخول مرة أخرى (مثلاً باستخدام «aws sso login» أو «gcloud auth login» أو «az login») ثم حدّث.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Not an Amazon EKS cluster</source>
        <translation>هذا ليس عنقود Amazon EKS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Node Groups, Add-ons and the AWS cards of the Overview exist only on Amazon EKS contexts.</source>
        <translation>توجد Node Groups وAdd-ons وبطاقات AWS في نظرة عامة فقط في سياقات Amazon EKS.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="110"/>
        <source>Unexpected answer from AWS</source>
        <translation>استجابة غير متوقعة من AWS</translation>
    </message>
    <message>
        <location filename="../errors.py" line="111"/>
        <source>Update the AWS CLI to its latest version and refresh.</source>
        <translation>حدّث AWS CLI إلى أحدث إصدار ثم أعد التحميل.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="118"/>
        <location filename="../errors.py" line="128"/>
        <source>Access denied</source>
        <translation>تم رفض الوصول</translation>
    </message>
    <message>
        <location filename="../errors.py" line="119"/>
        <source>Your AWS identity is not allowed to read this. The wiki lists the eks: permissions KubeScope needs.</source>
        <translation>هوية AWS الخاصة بك غير مسموح لها بقراءة هذا. تسرد الـ wiki أذونات eks: التي يحتاجها KubeScope.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>ليس لمستخدمك صلاحية قراءة هذا المورد.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="143"/>
        <source>No network connection</source>
        <translation>لا يوجد اتصال بالشبكة</translation>
    </message>
    <message>
        <location filename="../errors.py" line="144"/>
        <source>Check your internet connection or VPN and refresh.</source>
        <translation>تحقق من اتصالك بالإنترنت أو VPN ثم قم بالتحديث.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="165"/>
        <source>Cluster unreachable</source>
        <translation>تعذّر الوصول إلى العنقود</translation>
    </message>
    <message>
        <location filename="../errors.py" line="166"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>تحقق من الشبكة أو VPN ومن أن العنقود قيد التشغيل.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="172"/>
        <source>Something went wrong</source>
        <translation>حدث خطأ ما</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="46"/>
        <source>No log lines returned.</source>
        <translation>لم يتم إرجاع أي أسطر من السجل.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="51"/>
        <source>Updated at {time}</source>
        <translation>تم التحديث في {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="58"/>
        <source>Could not refresh logs: {message}</source>
        <translation>تعذّر تحديث السجلات: {message}</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>تحديث تلقائي</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>يجلب أسطر سجل جديدة كل بضع ثوانٍ ويتابع نهاية السجل</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>حدّث الآن</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../window.py" line="1562"/>
        <location filename="../window.py" line="1591"/>
        <source>TYPE</source>
        <translation>النوع</translation>
    </message>
    <message>
        <location filename="../window.py" line="1563"/>
        <source>CLUSTER IP</source>
        <translation>عنوان IP للعنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1564"/>
        <source>EXTERNAL IP</source>
        <translation>عنوان IP الخارجي</translation>
    </message>
    <message>
        <location filename="../window.py" line="1565"/>
        <location filename="../window.py" line="1569"/>
        <location filename="../window.py" line="1577"/>
        <source>PORTS</source>
        <translation>المنافذ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1568"/>
        <source>ADDRESS TYPE</source>
        <translation>نوع العنوان</translation>
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
        <translation>الفئة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1575"/>
        <source>HOSTS</source>
        <translation>المضيفون</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>ADDRESS</source>
        <translation>العنوان</translation>
    </message>
    <message>
        <location filename="../window.py" line="1580"/>
        <source>CONTROLLER</source>
        <translation>المتحكم</translation>
    </message>
    <message>
        <location filename="../window.py" line="1581"/>
        <source>PARAMETERS</source>
        <translation>المعاملات</translation>
    </message>
    <message>
        <location filename="../window.py" line="1584"/>
        <source>POD SELECTOR</source>
        <translation>محدد POD</translation>
    </message>
    <message>
        <location filename="../window.py" line="1585"/>
        <source>POLICY TYPES</source>
        <translation>أنواع السياسة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1588"/>
        <location filename="../window.py" line="1592"/>
        <source>DATA</source>
        <translation>البيانات</translation>
    </message>
    <message>
        <location filename="../window.py" line="1595"/>
        <source>USAGE</source>
        <translation>الاستخدام</translation>
    </message>
    <message>
        <location filename="../window.py" line="1598"/>
        <source>TYPES</source>
        <translation>الأنواع</translation>
    </message>
    <message>
        <location filename="../window.py" line="1601"/>
        <source>REFERENCE</source>
        <translation>المرجع</translation>
    </message>
    <message>
        <location filename="../window.py" line="1602"/>
        <source>MIN PODS</source>
        <translation>الحد الأدنى للـ Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="1603"/>
        <source>MAX PODS</source>
        <translation>الحد الأقصى للـ Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="1604"/>
        <source>REPLICAS</source>
        <translation>النسخ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1607"/>
        <source>MIN AVAILABLE</source>
        <translation>الحد الأدنى المتاح</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <source>MAX UNAVAILABLE</source>
        <translation>الحد الأقصى غير المتاح</translation>
    </message>
    <message>
        <location filename="../window.py" line="1609"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>الانقطاعات المسموح بها</translation>
    </message>
    <message>
        <location filename="../window.py" line="1612"/>
        <source>VALUE</source>
        <translation>القيمة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1613"/>
        <source>GLOBAL DEFAULT</source>
        <translation>الافتراضي العام</translation>
    </message>
    <message>
        <location filename="../window.py" line="1616"/>
        <source>HANDLER</source>
        <translation>المعالج</translation>
    </message>
    <message>
        <location filename="../window.py" line="1619"/>
        <source>HOLDER</source>
        <translation>الحائز</translation>
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
        <translation>أنواع المثيلات</translation>
    </message>
    <message>
        <location filename="../window.py" line="1630"/>
        <source>NODES</source>
        <translation>العقد</translation>
    </message>
    <message>
        <location filename="../window.py" line="1631"/>
        <source>AMI TYPE</source>
        <translation>نوع AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1632"/>
        <source>AMI VERSION</source>
        <translation>إصدار AMI</translation>
    </message>
    <message>
        <location filename="../window.py" line="1636"/>
        <location filename="../ui/main_window.ui" line="2557"/>
        <source>VERSION</source>
        <translation>الإصدار</translation>
    </message>
    <message>
        <location filename="../window.py" line="1637"/>
        <source>SOURCE</source>
        <translation>المصدر</translation>
    </message>
    <message>
        <location filename="../window.py" line="1647"/>
        <source>COMPLETIONS</source>
        <translation>المكتملة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1648"/>
        <source>SCHEDULE</source>
        <translation>الجدولة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1649"/>
        <location filename="../ui/main_window.ui" line="2018"/>
        <source>READY</source>
        <translation>الجاهزة</translation>
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
        <translation>الاسم</translation>
    </message>
    <message>
        <location filename="../window.py" line="1628"/>
        <location filename="../window.py" line="1635"/>
        <location filename="../window.py" line="1658"/>
        <location filename="../ui/main_window.ui" line="2023"/>
        <location filename="../ui/main_window.ui" line="2547"/>
        <source>STATUS</source>
        <translation>الحالة</translation>
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
        <translation>الذاكرة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1661"/>
        <source>RESTARTS</source>
        <translation>مرات إعادة التشغيل</translation>
    </message>
    <message>
        <location filename="../window.py" line="1662"/>
        <location filename="../window.py" line="1674"/>
        <location filename="../ui/main_window.ui" line="2028"/>
        <location filename="../ui/main_window.ui" line="2577"/>
        <source>AGE</source>
        <translation>العمر</translation>
    </message>
    <message>
        <location filename="../window.py" line="1671"/>
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
        <translation>وحدة تحكم Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="339"/>
        <source>CONTEXT</source>
        <translation>السياق</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>سياق Kubernetes من ملف kubeconfig الخاص بك</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="372"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>سجّل الدخول عبر واجهة سطر أوامر السحابة، ثم أعد تحميل بيانات العنقود</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="375"/>
        <source>Sign in</source>
        <translation>تسجيل الدخول</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="397"/>
        <source>Settings</source>
        <translation>الإعدادات</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="437"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>لم يتم العثور على سياقات عناقيد في ملف kubeconfig. أضف عنقوداً إلى kubeconfig (مثلاً باستخدام AWS CLI: aws eks update-kubeconfig) ثم أعد التحميل.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="478"/>
        <source>Dismiss</source>
        <translation>إغلاق</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="569"/>
        <source>MONITORING</source>
        <translation>المراقبة</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1714"/>
        <source>Overview</source>
        <translation>نظرة عامة</translation>
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
        <translation>الشبكة</translation>
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
        <translation>الإعدادات</translation>
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
        <translation>وصول آمن
الموارد في وضع القراءة فقط</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1721"/>
        <source>Cluster resources and capacity</source>
        <translation>موارد العنقود وسعته</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1878"/>
        <source>Search by name or namespace...</source>
        <translation>ابحث بالاسم أو namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1746"/>
        <location filename="../ui/main_window.ui" line="1759"/>
        <location filename="../ui/main_window.ui" line="1772"/>
        <source>Refresh</source>
        <translation>تحديث</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <source>Cluster</source>
        <translation>العنقود</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1929"/>
        <source>View Pods of the selected workload</source>
        <translation>عرض Pods الخاصة بـ workload المحدد</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1945"/>
        <source>View JSON details of the selected workload</source>
        <translation>عرض تفاصيل JSON الخاصة بـ workload المحدد</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1948"/>
        <source>Details</source>
        <translation>التفاصيل</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1961"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>عرض سجلات أحد Pods الخاصة بـ workload المحدد</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1964"/>
        <source>Logs</source>
        <translation>السجلات</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2507"/>
        <source>Nodes</source>
        <translation>العقد</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2542"/>
        <source>NODE</source>
        <translation>العقدة</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2552"/>
        <source>ROLE</source>
        <translation>الدور</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2572"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2590"/>
        <source>Select a context to load workloads</source>
        <translation>اختر سياقاً لتحميل workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2613"/>
        <source>Data fetched from the cluster API</source>
        <translation>البيانات مأخوذة من واجهة API الخاصة بالعنقود</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2674"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>افتح موقع DCO Tecnologia</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2694"/>
        <source>MIT License</source>
        <translation>رخصة MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2697"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope برنامج مفتوح المصدر صادر برخصة MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2733"/>
        <source>Update available</source>
        <translation>يتوفر تحديث</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2736"/>
        <source>Open the download page of the new version</source>
        <translation>افتح صفحة تنزيل الإصدار الجديد</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Check for updates</source>
        <translation>التحقق من التحديثات</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2784"/>
        <source>Open the project on GitHub</source>
        <translation>افتح المشروع على GitHub</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="2052"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>عقد جاهزة</translation>
    </message>
    <message>
        <location filename="../window.py" line="2068"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>الأنوية المطلوبة / القابلة للتخصيص</translation>
    </message>
    <message>
        <location filename="../window.py" line="2082"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>المطلوب / القابل للتخصيص</translation>
    </message>
    <message>
        <location filename="../window.py" line="2101"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>في العنقود</translation>
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
        <translation>موارد العنقود</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="78"/>
        <source>CLUSTER INFO</source>
        <translation>معلومات العنقود</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="125"/>
        <source>NETWORKING</source>
        <translation>الشبكة</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="174"/>
        <source>NODES</source>
        <translation>العقد</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="228"/>
        <source>PODS</source>
        <translation>PODS</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="248"/>
        <source>running / capacity</source>
        <translation>قيد التشغيل / السعة</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="295"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="362"/>
        <source>MEMORY</source>
        <translation>الذاكرة</translation>
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
        <translation>الاسم</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>الجاهزة</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>المرحلة</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>الحاويات</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>العمر</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>تفاصيل Pod</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>عرض السجلات</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>إغلاق</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="3090"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>أعطِ سياقاتك أسماء أسهل. اترك الاسم فارغاً للاحتفاظ بالاسم الأصلي.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>حفظ التغييرات</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>عام</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="107"/>
        <source>Language</source>
        <translation>اللغة</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="142"/>
        <source>Theme</source>
        <translation>السمة</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="177"/>
        <source>New theme...</source>
        <translation>سمة جديدة...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>تعديل السمة...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>افتح مجلد السمات</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>namespace الافتراضي</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>الـ namespace الذي يُفتح عليه كل سياق. اتركه فارغاً لعرضها كلها.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>تذكّر آخر سياق مستخدم</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>ابحث في GitHub عن إصدار جديد عند بدء التطبيق</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>يستعلم عن آخر إصدار من واجهة GitHub API العامة ولا يرسل سوى إصدار التطبيق. أيقونة التذييل تتحقق عند الطلب.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>وضع التصحيح: اكتب ملف سجل يمكنني مشاركته</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>افتح مجلد السجلات</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>مسح الذاكرة المؤقتة</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>ينسى القوائم والنظرات العامة التي تم تحميلها وتسجيل الدخول إلى كل عنقود، فيسجّل الطلب التالي الدخول ويحمّل كل شيء من جديد. تبقى إعداداتك كما هي.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>ملفات KUBECONFIG</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>يقرأ KubeScope الملفات الموجودة في المتغير KUBECONFIG أو ~/.kube/config. أضف ملفات هنا لقراءتها بدلاً من ذلك. اضغط حفظ للتطبيق.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>إضافة ملف...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>إزالة</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>أوامر تسجيل الدخول</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>بالنسبة لسحابة لا يعرفها KubeScope، حدّد البرنامج الذي يستخدمه kubeconfig لتسجيل الدخول (مثل oci) والأمر الذي يسجّل دخولك (مثل oci session authenticate). يشغّله زر تسجيل الدخول دون shell. اضغط حفظ للتطبيق.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>البرنامج</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>أمر تسجيل الدخول</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>إضافة صف</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>أسماء السياقات</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>السياق</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>الاسم المعروض</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>خلفية الصفحة</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>اللوحات والبطاقات</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>اللوحات المتناوبة</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>مسارات الأشرطة</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>الحدود</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>الشريط العلوي</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>شعار الشريط العلوي</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>محدد الشريط العلوي</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>حد محدد الشريط العلوي</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>تحديد الشريط العلوي</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>نص الشريط العلوي</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>النص</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>عنوان الشريط الجانبي</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>النص الثانوي</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>النص المعطّل</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>نص التمييز والروابط</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>أزرار التمييز</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>أزرار التمييز عند التمرير</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>أزرار التمييز عند التعطيل</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>التركيز والتظليل</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>نص الشارة</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>درجة التمييز</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>تحديد النص</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>حد التمييز</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>النص على الشريط العلوي وأزرار التمييز</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>نص الحالة السليمة</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>خلفية الحالة السليمة</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>نص التحذير</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>خلفية التحذير</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>نص الفشل</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>خلفية الفشل</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>نص الخمول</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>خلفية الخمول</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>صف به مشكلة</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>صف Pod حديث</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>شريط الاستخدام، يمتلئ</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>شريط الاستخدام، شبه ممتلئ</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>شريط الصحة، سليم</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>شريط الصحة، تحذير</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>شريط الصحة، فشل</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>سمة جديدة</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>تعديل السمة: {name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>اسم السمة</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>فاتح</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>داكن</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>الاسم</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>يبدأ من</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>الألوان</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>احفظ في ملف ما تعرضه علامة التبويب هذه</translation>
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
        <translation>كل namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="832"/>
        <source>Loading contexts...</source>
        <translation>جارٍ تحميل السياقات...</translation>
    </message>
    <message>
        <location filename="../window.py" line="841"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>تعذّر تحميل kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="863"/>
        <source>No contexts found in kubeconfig</source>
        <translation>لم يتم العثور على سياقات في kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="913"/>
        <location filename="../window.py" line="991"/>
        <source>Unpin from the top</source>
        <translation>إلغاء التثبيت من الأعلى</translation>
    </message>
    <message>
        <location filename="../window.py" line="913"/>
        <source>Pin to the top</source>
        <translation>تثبيت في الأعلى</translation>
    </message>
    <message>
        <location filename="../window.py" line="1029"/>
        <source>Close</source>
        <translation>إغلاق</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Status</source>
        <translation>الحالة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>Kubernetes version</source>
        <translation>إصدار Kubernetes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1078"/>
        <source>Platform version</source>
        <translation>إصدار المنصة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1079"/>
        <source>Created</source>
        <translation>تاريخ الإنشاء</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>Provider</source>
        <translation>المزوّد</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>API server endpoint</source>
        <translation>نقطة نهاية خادم API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Cluster ARN</source>
        <translation>ARN العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1085"/>
        <source>Cluster IAM role ARN</source>
        <translation>ARN دور IAM للعنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1086"/>
        <source>OpenID Connect provider URL</source>
        <translation>عنوان URL لمزوّد OpenID Connect</translation>
    </message>
    <message>
        <location filename="../window.py" line="1094"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1095"/>
        <source>Cluster security group</source>
        <translation>مجموعة أمان العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1097"/>
        <source>Additional security groups</source>
        <translation>مجموعات الأمان الإضافية</translation>
    </message>
    <message>
        <location filename="../window.py" line="1098"/>
        <source>None</source>
        <translation>لا شيء</translation>
    </message>
    <message>
        <location filename="../window.py" line="1101"/>
        <source>API server endpoint access</source>
        <translation>الوصول إلى نقطة نهاية خادم API</translation>
    </message>
    <message>
        <location filename="../window.py" line="1104"/>
        <source>Cluster IP address family</source>
        <translation>عائلة عناوين IP للعنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1105"/>
        <source>Service IPv4 range</source>
        <translation>نطاق IPv4 للخدمات</translation>
    </message>
    <message>
        <location filename="../window.py" line="1107"/>
        <source>Public access source allowlist</source>
        <translation>قائمة المصادر المسموح لها بالوصول العام</translation>
    </message>
    <message>
        <location filename="../window.py" line="1110"/>
        <source>Subnets</source>
        <translation>الشبكات الفرعية</translation>
    </message>
    <message>
        <location filename="../window.py" line="1121"/>
        <source>Creating</source>
        <translation>قيد الإنشاء</translation>
    </message>
    <message>
        <location filename="../window.py" line="1122"/>
        <source>Updating</source>
        <translation>قيد التحديث</translation>
    </message>
    <message>
        <location filename="../window.py" line="1123"/>
        <source>Deleting</source>
        <translation>قيد الحذف</translation>
    </message>
    <message>
        <location filename="../window.py" line="1126"/>
        <source>Creation failed</source>
        <translation>فشل الإنشاء</translation>
    </message>
    <message>
        <location filename="../window.py" line="1127"/>
        <source>Update failed</source>
        <translation>فشل التحديث</translation>
    </message>
    <message>
        <location filename="../window.py" line="1128"/>
        <source>Deletion failed</source>
        <translation>فشل الحذف</translation>
    </message>
    <message>
        <location filename="../window.py" line="1130"/>
        <source>Deployed</source>
        <translation>تم النشر</translation>
    </message>
    <message>
        <location filename="../window.py" line="1131"/>
        <source>Superseded</source>
        <translation>تم استبداله</translation>
    </message>
    <message>
        <location filename="../window.py" line="1132"/>
        <source>Uninstalled</source>
        <translation>تم إلغاء التثبيت</translation>
    </message>
    <message>
        <location filename="../window.py" line="1133"/>
        <source>Uninstalling</source>
        <translation>جارٍ إلغاء التثبيت</translation>
    </message>
    <message>
        <location filename="../window.py" line="1134"/>
        <source>Pending install</source>
        <translation>التثبيت معلّق</translation>
    </message>
    <message>
        <location filename="../window.py" line="1135"/>
        <source>Pending upgrade</source>
        <translation>الترقية معلّقة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1136"/>
        <source>Pending rollback</source>
        <translation>التراجع معلّق</translation>
    </message>
    <message>
        <location filename="../window.py" line="1137"/>
        <source>Public</source>
        <translation>عام</translation>
    </message>
    <message>
        <location filename="../window.py" line="1138"/>
        <source>Private</source>
        <translation>خاص</translation>
    </message>
    <message>
        <location filename="../window.py" line="1139"/>
        <source>Public and private</source>
        <translation>عام وخاص</translation>
    </message>
    <message>
        <location filename="../window.py" line="1232"/>
        <source>Overview</source>
        <translation>نظرة عامة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1233"/>
        <source>Cluster resources and capacity</source>
        <translation>موارد العنقود وسعته</translation>
    </message>
    <message>
        <location filename="../window.py" line="1235"/>
        <source>Details &amp; Logs</source>
        <translation>التفاصيل والسجلات</translation>
    </message>
    <message>
        <location filename="../window.py" line="1237"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>تفاصيل المورد وسجلات Pod، في علامة تبويب لكل منهما</translation>
    </message>
    <message>
        <location filename="../window.py" line="1240"/>
        <source>Settings</source>
        <translation>الإعدادات</translation>
    </message>
    <message>
        <location filename="../window.py" line="1241"/>
        <source>Preferences and context names</source>
        <translation>التفضيلات وأسماء السياقات</translation>
    </message>
    <message>
        <location filename="../window.py" line="1243"/>
        <source>Workloads overview</source>
        <translation>نظرة عامة على workloads</translation>
    </message>
    <message>
        <location filename="../window.py" line="1245"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>صحة كل نوع من workloads وآخر الأحداث</translation>
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
        <translation>Pods العنقود</translation>
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
        <translation>Deployments العنقود</translation>
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
        <translation>StatefulSets العنقود</translation>
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
        <translation>DaemonSets العنقود</translation>
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
        <translation>ReplicaSets العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1267"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>ReplicationControllers العنقود</translation>
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
        <translation>Jobs العنقود</translation>
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
        <translation>CronJobs العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Services of the cluster</source>
        <translation>Services العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1274"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1275"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>Endpoint Slices العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1278"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1279"/>
        <source>Endpoints of the cluster</source>
        <translation>Endpoints العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1282"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1283"/>
        <source>Ingresses of the cluster</source>
        <translation>Ingresses العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1286"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1287"/>
        <source>Ingress Classes of the cluster</source>
        <translation>Ingress Classes العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1290"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1291"/>
        <source>Network Policies of the cluster</source>
        <translation>Network Policies العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1294"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1295"/>
        <source>Config Maps of the cluster</source>
        <translation>Config Maps العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1298"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1299"/>
        <source>Secrets of the cluster</source>
        <translation>Secrets العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1302"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1303"/>
        <source>Resource Quotas of the cluster</source>
        <translation>Resource Quotas العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1306"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1307"/>
        <source>Limit Ranges of the cluster</source>
        <translation>Limit Ranges العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1310"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1311"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>Horizontal Pod Autoscalers العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1314"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1315"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>Pod Disruption Budgets العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1318"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1319"/>
        <source>Priority Classes of the cluster</source>
        <translation>Priority Classes العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1322"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1323"/>
        <source>Runtime Classes of the cluster</source>
        <translation>Runtime Classes العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1326"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1327"/>
        <source>Leases of the cluster</source>
        <translation>Leases العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1331"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>Mutating Webhook Configurations العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1334"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1335"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>Validating Webhook Configurations العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1338"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1339"/>
        <source>Node Groups of the cluster</source>
        <translation>Node Groups العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1342"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1343"/>
        <source>Add-ons of the cluster</source>
        <translation>Add-ons العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1352"/>
        <source>Version {version}</source>
        <translation>الإصدار {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1355"/>
        <source>Open the project on GitHub</source>
        <translation>افتح المشروع على GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="1389"/>
        <source>Up to date</source>
        <translation>محدّث</translation>
    </message>
    <message>
        <location filename="../window.py" line="1390"/>
        <source>Could not check</source>
        <translation>تعذّر التحقق</translation>
    </message>
    <message>
        <location filename="../window.py" line="1401"/>
        <source>Check for updates</source>
        <translation>التحقق من التحديثات</translation>
    </message>
    <message>
        <location filename="../window.py" line="1402"/>
        <source>Checking for updates...</source>
        <translation>جارٍ التحقق من التحديثات...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1403"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope محدّث. انقر للتحقق مرة أخرى.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1404"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>تعذّر التحقق من التحديثات. انقر لإعادة المحاولة.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1410"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>يتوفر تحديث: {version}. انقر لفتح صفحة التنزيل؛ انقر بزر الفأرة الأيمن للتحقق مرة أخرى.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1418"/>
        <source>Update available</source>
        <translation>يتوفر تحديث</translation>
    </message>
    <message>
        <location filename="../window.py" line="1420"/>
        <source>Download KubeScope {version}</source>
        <translation>نزّل KubeScope {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1456"/>
        <source>Check for updates again</source>
        <translation>تحقق من التحديثات مرة أخرى</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <location filename="../window.py" line="2228"/>
        <source>Loading resources...</source>
        <translation>جارٍ تحميل الموارد...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1797"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>إعداد بيانات اعتماد AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1801"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>بيانات اعتماد AWS للملف الشخصي {profile} مفقودة أو غير صالحة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1806"/>
        <source>Sign in to {provider}</source>
        <translation>تسجيل الدخول إلى {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1809"/>
        <source>Not signed in to {provider}</source>
        <translation>لم يتم تسجيل الدخول إلى {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1813"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>تسجيل الدخول إلى {provider} ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1819"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>لم يتم تسجيل الدخول إلى {provider} (الملف الشخصي {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1840"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>أكمل في الطرفية التي فُتحت، ثم اضغط تحديث.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1859"/>
        <source>Loading workloads...</source>
        <translation>جارٍ تحميل workloads...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1920"/>
        <source>Could not read: {names}</source>
        <translation>تعذّرت القراءة: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1980"/>
        <source>Loading cluster data...</source>
        <translation>جارٍ تحميل بيانات العنقود...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2061"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>قيد التشغيل · {pending} معلّقة · {failed} فاشلة</translation>
    </message>
    <message>
        <location filename="../window.py" line="2070"/>
        <location filename="../window.py" line="2084"/>
        <source> · usage {value}</source>
        <translation> · الاستخدام {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2133"/>
        <source>Ready</source>
        <translation>جاهز</translation>
    </message>
    <message>
        <location filename="../window.py" line="2133"/>
        <source>Not ready</source>
        <translation>غير جاهز</translation>
    </message>
    <message>
        <location filename="../window.py" line="2108"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>الاستخدام الفعلي غير متاح: لم يتم العثور على metrics-server.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2245"/>
        <source>Refreshing...</source>
        <translation>جارٍ التحديث...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2436"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{count} Services في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2438"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{count} Endpoint Slices في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2441"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{count} Endpoints في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2444"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{count} Ingresses في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2446"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>{count} Ingress Classes في العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="2448"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{count} Network Policies في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2451"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>{count} Config Maps في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2453"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>{count} Secrets في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2455"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>{count} Resource Quotas في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2458"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>{count} Limit Ranges في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2461"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>{count} Horizontal Pod Autoscalers في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2464"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>{count} Pod Disruption Budgets في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2466"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>{count} Leases في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2468"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>{count} Priority Classes في العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="2470"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>{count} Runtime Classes في العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="2472"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>{count} Mutating Webhook Configurations في العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="2475"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>{count} Validating Webhook Configurations في العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="2477"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>{count} Node Groups في العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="2478"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>{count} Add-ons في العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="2489"/>
        <location filename="../window.py" line="2555"/>
        <source>Running</source>
        <translation>قيد التشغيل</translation>
    </message>
    <message>
        <location filename="../window.py" line="1129"/>
        <location filename="../window.py" line="2490"/>
        <location filename="../window.py" line="2551"/>
        <source>Pending</source>
        <translation>معلّق</translation>
    </message>
    <message>
        <location filename="../window.py" line="2491"/>
        <source>Succeeded</source>
        <translation>نجح</translation>
    </message>
    <message>
        <location filename="../window.py" line="1125"/>
        <location filename="../window.py" line="2492"/>
        <location filename="../window.py" line="2550"/>
        <source>Failed</source>
        <translation>فشل</translation>
    </message>
    <message>
        <location filename="../window.py" line="2493"/>
        <source>Unknown</source>
        <translation>غير معروف</translation>
    </message>
    <message>
        <location filename="../window.py" line="2537"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pods في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2545"/>
        <source>Healthy</source>
        <translation>سليم</translation>
    </message>
    <message>
        <location filename="../window.py" line="1124"/>
        <location filename="../window.py" line="2546"/>
        <source>Degraded</source>
        <translation>متدهور</translation>
    </message>
    <message>
        <location filename="../window.py" line="2547"/>
        <source>Unavailable</source>
        <translation>غير متاح</translation>
    </message>
    <message>
        <location filename="../window.py" line="2548"/>
        <source>Scaled to zero</source>
        <translation>مخفّض إلى صفر</translation>
    </message>
    <message>
        <location filename="../window.py" line="2549"/>
        <source>Complete</source>
        <translation>مكتمل</translation>
    </message>
    <message>
        <location filename="../window.py" line="2552"/>
        <source>Suspended</source>
        <translation>معلّق مؤقتاً</translation>
    </message>
    <message>
        <location filename="../window.py" line="1120"/>
        <location filename="../window.py" line="2553"/>
        <source>Active</source>
        <translation>نشط</translation>
    </message>
    <message>
        <location filename="../window.py" line="2554"/>
        <source>Scheduled</source>
        <translation>مجدول</translation>
    </message>
    <message>
        <location filename="../window.py" line="2599"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployments في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2602"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{count} StatefulSets في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2605"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{count} DaemonSets في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2608"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{count} ReplicaSets في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2611"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{count} ReplicationControllers في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2613"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{count} Jobs في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2614"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{count} CronJobs في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2638"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} من {total} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2639"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} من {total} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2640"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{visible} من {total} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2641"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{visible} من {total} DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2642"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{visible} من {total} ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2644"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{visible} من {total} ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2646"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{visible} من {total} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2647"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{visible} من {total} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2648"/>
        <source>{visible} of {total} Services</source>
        <translation>{visible} من {total} Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="2649"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{visible} من {total} Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="2650"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{visible} من {total} Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="2651"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{visible} من {total} Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="2652"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{visible} من {total} Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2653"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{visible} من {total} Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="2654"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>{visible} من {total} Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="2655"/>
        <source>{visible} of {total} Secrets</source>
        <translation>{visible} من {total} Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2656"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>{visible} من {total} Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="2657"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>{visible} من {total} Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="2659"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>{visible} من {total} Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2662"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>{visible} من {total} Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2664"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>{visible} من {total} Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2665"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>{visible} من {total} Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2666"/>
        <source>{visible} of {total} Leases</source>
        <translation>{visible} من {total} Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="2668"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>{visible} من {total} Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2671"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>{visible} من {total} Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="2673"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>{visible} من {total} Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="2674"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>{visible} من {total} Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="2720"/>
        <source>Loading...</source>
        <translation>جارٍ التحميل...</translation>
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
        <translation>Pods الخاصة بـ {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2814"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods في {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2879"/>
        <source>No Pods are associated with this workload</source>
        <translation>لا توجد Pods مرتبطة بهذا workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="2886"/>
        <location filename="../window.py" line="2909"/>
        <source>Logs</source>
        <translation>السجلات</translation>
    </message>
    <message>
        <location filename="../window.py" line="2886"/>
        <source>This workload has no Pods.</source>
        <translation>ليس لهذا workload أي Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2895"/>
        <location filename="../window.py" line="2918"/>
        <source>View logs</source>
        <translation>عرض السجلات</translation>
    </message>
    <message>
        <location filename="../window.py" line="2896"/>
        <source>Select the Pod:</source>
        <translation>اختر Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2910"/>
        <source>Pod {name} has no containers.</source>
        <translation>ليس لـ Pod {name} أي حاويات.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2919"/>
        <source>Select the container of {name}:</source>
        <translation>اختر حاوية {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2945"/>
        <source>Save to a file</source>
        <translation>حفظ في ملف</translation>
    </message>
    <message>
        <location filename="../window.py" line="2956"/>
        <source>Could not save</source>
        <translation>تعذّر الحفظ</translation>
    </message>
    <message>
        <location filename="../window.py" line="2957"/>
        <source>The file could not be written: {reason}</source>
        <translation>تعذّرت كتابة الملف: {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3003"/>
        <source>Logs: {pod} / {container}</source>
        <translation>السجلات: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3053"/>
        <source>Automatic</source>
        <translation>تلقائي</translation>
    </message>
    <message>
        <location filename="../window.py" line="3066"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>معطّل افتراضياً. عند تفعيله، يكتب KubeScope ما يفعله، وليس سجلات Pods ولا محتوى الموارد، في {path}. اقرأه قبل المشاركة: فهو يتضمن أسماء السياقات.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3097"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>لم يتم العثور على سياقات في kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3126"/>
        <source>Choose a kubeconfig file</source>
        <translation>اختر ملف kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="3172"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>أمر تسجيل الدخول في الصف {row} غير صالح.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3185"/>
        <source>Light</source>
        <translation>فاتح</translation>
    </message>
    <message>
        <location filename="../window.py" line="3185"/>
        <source>Dark</source>
        <translation>داكن</translation>
    </message>
    <message>
        <location filename="../window.py" line="3204"/>
        <source>My theme</source>
        <translation>سمتي</translation>
    </message>
    <message>
        <location filename="../window.py" line="3248"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>تم مسح الذاكرة المؤقتة. يُحمَّل كل شيء من جديد عند الحاجة التالية.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3303"/>
        <source>Settings saved.</source>
        <translation>تم حفظ الإعدادات.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3342"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>ليس لمستخدمك صلاحية لتنفيذ هذا الإجراء ({action}). اطلب الوصول من مسؤول العنقود.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3347"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>ليس لمستخدمك صلاحية لتنفيذ هذا. اطلب الوصول من مسؤول العنقود.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3366"/>
        <source>Query failed</source>
        <translation>فشل الاستعلام</translation>
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
        <translation>الأحداث</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="293"/>
        <source>TYPE</source>
        <translation>النوع</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="298"/>
        <source>SOURCE</source>
        <translation>المصدر</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>INVOLVED OBJECT</source>
        <translation>الكائن المعني</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>MESSAGE</source>
        <translation>الرسالة</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>COUNT</source>
        <translation>العدد</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>AGE</source>
        <translation>العمر</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>LAST SEEN</source>
        <translation>آخر ظهور</translation>
    </message>
</context>
</TS>
