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
        <source>Access denied</source>
        <translation>تم رفض الوصول</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>ليس لمستخدمك صلاحية قراءة هذا المورد.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="122"/>
        <source>Cluster unreachable</source>
        <translation>تعذّر الوصول إلى العنقود</translation>
    </message>
    <message>
        <location filename="../errors.py" line="123"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>تحقق من الشبكة أو VPN ومن أن العنقود قيد التشغيل.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Something went wrong</source>
        <translation>حدث خطأ ما</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="42"/>
        <source>No log lines returned.</source>
        <translation>لم يتم إرجاع أي أسطر من السجل.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="47"/>
        <source>Updated at {time}</source>
        <translation>تم التحديث في {time}</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="54"/>
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
        <location filename="../window.py" line="1141"/>
        <source>TYPE</source>
        <translation>النوع</translation>
    </message>
    <message>
        <location filename="../window.py" line="1142"/>
        <source>CLUSTER IP</source>
        <translation>عنوان IP للعنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1143"/>
        <source>EXTERNAL IP</source>
        <translation>عنوان IP الخارجي</translation>
    </message>
    <message>
        <location filename="../window.py" line="1144"/>
        <location filename="../window.py" line="1148"/>
        <location filename="../window.py" line="1156"/>
        <source>PORTS</source>
        <translation>المنافذ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1147"/>
        <source>ADDRESS TYPE</source>
        <translation>نوع العنوان</translation>
    </message>
    <message>
        <location filename="../window.py" line="1149"/>
        <location filename="../window.py" line="1151"/>
        <source>ENDPOINTS</source>
        <translation>ENDPOINTS</translation>
    </message>
    <message>
        <location filename="../window.py" line="1153"/>
        <source>CLASS</source>
        <translation>الفئة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1154"/>
        <source>HOSTS</source>
        <translation>المضيفون</translation>
    </message>
    <message>
        <location filename="../window.py" line="1155"/>
        <source>ADDRESS</source>
        <translation>العنوان</translation>
    </message>
    <message>
        <location filename="../window.py" line="1159"/>
        <source>CONTROLLER</source>
        <translation>المتحكم</translation>
    </message>
    <message>
        <location filename="../window.py" line="1160"/>
        <source>PARAMETERS</source>
        <translation>المعاملات</translation>
    </message>
    <message>
        <location filename="../window.py" line="1163"/>
        <source>POD SELECTOR</source>
        <translation>محدد POD</translation>
    </message>
    <message>
        <location filename="../window.py" line="1164"/>
        <source>POLICY TYPES</source>
        <translation>أنواع السياسة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1174"/>
        <source>COMPLETIONS</source>
        <translation>المكتملة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1175"/>
        <source>SCHEDULE</source>
        <translation>الجدولة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1176"/>
        <location filename="../ui/main_window.ui" line="1519"/>
        <source>READY</source>
        <translation>الجاهزة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1181"/>
        <location filename="../window.py" line="1197"/>
        <location filename="../ui/main_window.ui" line="1315"/>
        <location filename="../ui/main_window.ui" line="1504"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../window.py" line="1183"/>
        <location filename="../window.py" line="1199"/>
        <location filename="../ui/main_window.ui" line="1514"/>
        <source>NAME</source>
        <translation>الاسم</translation>
    </message>
    <message>
        <location filename="../window.py" line="1185"/>
        <location filename="../ui/main_window.ui" line="1524"/>
        <source>STATUS</source>
        <translation>الحالة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1186"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../window.py" line="1187"/>
        <source>MEMORY</source>
        <translation>الذاكرة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1188"/>
        <source>RESTARTS</source>
        <translation>مرات إعادة التشغيل</translation>
    </message>
    <message>
        <location filename="../window.py" line="1189"/>
        <location filename="../window.py" line="1201"/>
        <location filename="../ui/main_window.ui" line="1529"/>
        <source>AGE</source>
        <translation>العمر</translation>
    </message>
    <message>
        <location filename="../window.py" line="1198"/>
        <location filename="../ui/main_window.ui" line="1509"/>
        <source>KIND</source>
        <translation>KIND</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="20"/>
        <location filename="../ui/main_window.ui" line="275"/>
        <source>KubeScope</source>
        <translation>KubeScope</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="285"/>
        <source>Kubernetes console</source>
        <translation>وحدة تحكم Kubernetes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="307"/>
        <source>CONTEXT</source>
        <translation>السياق</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="320"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>سياق Kubernetes من ملف kubeconfig الخاص بك</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="340"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>سجّل الدخول عبر واجهة سطر أوامر السحابة، ثم أعد تحميل بيانات العنقود</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="343"/>
        <source>Sign in</source>
        <translation>تسجيل الدخول</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="365"/>
        <source>Settings</source>
        <translation>الإعدادات</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="405"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>لم يتم العثور على سياقات عناقيد في ملف kubeconfig. أضف عنقوداً إلى kubeconfig (مثلاً باستخدام AWS CLI: aws eks update-kubeconfig) ثم أعد التحميل.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="446"/>
        <source>Dismiss</source>
        <translation>إغلاق</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="537"/>
        <source>MONITORING</source>
        <translation>المراقبة</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="544"/>
        <location filename="../ui/main_window.ui" line="627"/>
        <location filename="../ui/main_window.ui" line="1255"/>
        <source>Overview</source>
        <translation>نظرة عامة</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="575"/>
        <source>Workloads</source>
        <translation>Workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="658"/>
        <location filename="../ui/main_window.ui" line="1433"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="689"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="720"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="751"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="782"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="813"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="844"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="875"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="909"/>
        <source>Network</source>
        <translation>الشبكة</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="961"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="992"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1023"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1054"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1085"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1116"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1150"/>
        <source>Details &amp;&amp; Logs</source>
        <translation>التفاصيل والسجلات</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1206"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>وصول آمن
الموارد في وضع القراءة فقط</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1262"/>
        <source>Cluster resources and capacity</source>
        <translation>موارد العنقود وسعته</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1367"/>
        <source>Search by name or namespace...</source>
        <translation>ابحث بالاسم أو namespace...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1390"/>
        <source>Refresh</source>
        <translation>تحديث</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1430"/>
        <source>View Pods of the selected workload</source>
        <translation>عرض Pods الخاصة بـ workload المحدد</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1446"/>
        <source>View JSON details of the selected workload</source>
        <translation>عرض تفاصيل JSON الخاصة بـ workload المحدد</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1449"/>
        <source>Details</source>
        <translation>التفاصيل</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1462"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>عرض سجلات أحد Pods الخاصة بـ workload المحدد</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1465"/>
        <source>Logs</source>
        <translation>السجلات</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2007"/>
        <source>Select a context to load workloads</source>
        <translation>اختر سياقاً لتحميل workloads</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2030"/>
        <source>Data fetched from the cluster API</source>
        <translation>البيانات مأخوذة من واجهة API الخاصة بالعنقود</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2091"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>افتح موقع DCO Tecnologia</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2111"/>
        <source>MIT License</source>
        <translation>رخصة MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2114"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope برنامج مفتوح المصدر صادر برخصة MIT</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2150"/>
        <source>Update available</source>
        <translation>يتوفر تحديث</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2153"/>
        <source>Open the download page of the new version</source>
        <translation>افتح صفحة تنزيل الإصدار الجديد</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2181"/>
        <source>Check for updates</source>
        <translation>التحقق من التحديثات</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2201"/>
        <source>Open the project on GitHub</source>
        <translation>افتح المشروع على GitHub</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="1564"/>
        <location filename="../ui/overview_page.ui" line="113"/>
        <source>nodes ready</source>
        <translation>عقد جاهزة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1580"/>
        <location filename="../ui/overview_page.ui" line="234"/>
        <source>cores requested / allocatable</source>
        <translation>الأنوية المطلوبة / القابلة للتخصيص</translation>
    </message>
    <message>
        <location filename="../window.py" line="1594"/>
        <location filename="../ui/overview_page.ui" line="301"/>
        <source>requested / allocatable</source>
        <translation>المطلوب / القابل للتخصيص</translation>
    </message>
    <message>
        <location filename="../window.py" line="1613"/>
        <location filename="../ui/overview_page.ui" line="375"/>
        <source>in the cluster</source>
        <translation>في العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1615"/>
        <location filename="../ui/overview_page.ui" line="429"/>
        <location filename="../ui/overview_page.ui" line="483"/>
        <location filename="../ui/overview_page.ui" line="537"/>
        <source>workloads</source>
        <translation>workloads</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="29"/>
        <source>Cluster resources</source>
        <translation>موارد العنقود</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="52"/>
        <source>Refresh</source>
        <translation>تحديث</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="93"/>
        <source>NODES</source>
        <translation>العقد</translation>
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
        <translation>قيد التشغيل / السعة</translation>
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
        <translation>الذاكرة</translation>
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
        <translation>العقد</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="584"/>
        <source>NODE</source>
        <translation>العقدة</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="589"/>
        <source>STATUS</source>
        <translation>الحالة</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="594"/>
        <source>ROLE</source>
        <translation>الدور</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="599"/>
        <source>VERSION</source>
        <translation>الإصدار</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="619"/>
        <source>AGE</source>
        <translation>العمر</translation>
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
        <location filename="../window.py" line="2528"/>
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
        <location filename="../window.py" line="650"/>
        <source>0 Deployments</source>
        <translation>0 Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="666"/>
        <location filename="../window.py" line="1814"/>
        <location filename="../window.py" line="1837"/>
        <location filename="../window.py" line="2764"/>
        <source>All namespaces</source>
        <translation>كل namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="766"/>
        <source>Loading contexts...</source>
        <translation>جارٍ تحميل السياقات...</translation>
    </message>
    <message>
        <location filename="../window.py" line="775"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>تعذّر تحميل kubeconfig: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="797"/>
        <source>No contexts found in kubeconfig</source>
        <translation>لم يتم العثور على سياقات في kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="864"/>
        <source>Overview</source>
        <translation>نظرة عامة</translation>
    </message>
    <message>
        <location filename="../window.py" line="865"/>
        <source>Cluster resources and capacity</source>
        <translation>موارد العنقود وسعته</translation>
    </message>
    <message>
        <location filename="../window.py" line="867"/>
        <source>Details &amp; Logs</source>
        <translation>التفاصيل والسجلات</translation>
    </message>
    <message>
        <location filename="../window.py" line="869"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>تفاصيل المورد وسجلات Pod، في علامة تبويب لكل منهما</translation>
    </message>
    <message>
        <location filename="../window.py" line="872"/>
        <source>Settings</source>
        <translation>الإعدادات</translation>
    </message>
    <message>
        <location filename="../window.py" line="873"/>
        <source>Preferences and context names</source>
        <translation>التفضيلات وأسماء السياقات</translation>
    </message>
    <message>
        <location filename="../window.py" line="875"/>
        <source>Workloads overview</source>
        <translation>نظرة عامة على workloads</translation>
    </message>
    <message>
        <location filename="../window.py" line="877"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>صحة كل نوع من workloads وآخر الأحداث</translation>
    </message>
    <message>
        <location filename="../window.py" line="881"/>
        <location filename="../window.py" line="1411"/>
        <source>Pods</source>
        <translation>Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="881"/>
        <source>Pods of the cluster</source>
        <translation>Pods العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="883"/>
        <location filename="../window.py" line="1412"/>
        <source>Deployments</source>
        <translation>Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="884"/>
        <source>Deployments of the cluster</source>
        <translation>Deployments العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="887"/>
        <location filename="../window.py" line="1414"/>
        <source>StatefulSets</source>
        <translation>StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="888"/>
        <source>StatefulSets of the cluster</source>
        <translation>StatefulSets العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="891"/>
        <location filename="../window.py" line="1413"/>
        <source>DaemonSets</source>
        <translation>DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="892"/>
        <source>DaemonSets of the cluster</source>
        <translation>DaemonSets العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="895"/>
        <location filename="../window.py" line="1415"/>
        <source>ReplicaSets</source>
        <translation>ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="896"/>
        <source>ReplicaSets of the cluster</source>
        <translation>ReplicaSets العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="899"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="900"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>ReplicationControllers العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="902"/>
        <location filename="../window.py" line="1416"/>
        <source>Jobs</source>
        <translation>Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="902"/>
        <source>Jobs of the cluster</source>
        <translation>Jobs العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="903"/>
        <location filename="../window.py" line="1417"/>
        <source>CronJobs</source>
        <translation>CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="903"/>
        <source>CronJobs of the cluster</source>
        <translation>CronJobs العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="904"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="904"/>
        <source>Services of the cluster</source>
        <translation>Services العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="906"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="907"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>Endpoint Slices العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="910"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="911"/>
        <source>Endpoints of the cluster</source>
        <translation>Endpoints العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="914"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="915"/>
        <source>Ingresses of the cluster</source>
        <translation>Ingresses العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="918"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="919"/>
        <source>Ingress Classes of the cluster</source>
        <translation>Ingress Classes العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="922"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="923"/>
        <source>Network Policies of the cluster</source>
        <translation>Network Policies العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="932"/>
        <source>Version {version}</source>
        <translation>الإصدار {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="935"/>
        <source>Open the project on GitHub</source>
        <translation>افتح المشروع على GitHub</translation>
    </message>
    <message>
        <location filename="../window.py" line="969"/>
        <source>Up to date</source>
        <translation>محدّث</translation>
    </message>
    <message>
        <location filename="../window.py" line="970"/>
        <source>Could not check</source>
        <translation>تعذّر التحقق</translation>
    </message>
    <message>
        <location filename="../window.py" line="981"/>
        <source>Check for updates</source>
        <translation>التحقق من التحديثات</translation>
    </message>
    <message>
        <location filename="../window.py" line="982"/>
        <source>Checking for updates...</source>
        <translation>جارٍ التحقق من التحديثات...</translation>
    </message>
    <message>
        <location filename="../window.py" line="983"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope محدّث. انقر للتحقق مرة أخرى.</translation>
    </message>
    <message>
        <location filename="../window.py" line="984"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>تعذّر التحقق من التحديثات. انقر لإعادة المحاولة.</translation>
    </message>
    <message>
        <location filename="../window.py" line="990"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>يتوفر تحديث: {version}. انقر لفتح صفحة التنزيل؛ انقر بزر الفأرة الأيمن للتحقق مرة أخرى.</translation>
    </message>
    <message>
        <location filename="../window.py" line="998"/>
        <source>Update available</source>
        <translation>يتوفر تحديث</translation>
    </message>
    <message>
        <location filename="../window.py" line="1000"/>
        <source>Download KubeScope {version}</source>
        <translation>نزّل KubeScope {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1036"/>
        <source>Check for updates again</source>
        <translation>تحقق من التحديثات مرة أخرى</translation>
    </message>
    <message>
        <location filename="../window.py" line="1132"/>
        <location filename="../window.py" line="1724"/>
        <source>Loading resources...</source>
        <translation>جارٍ تحميل الموارد...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1309"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>إعداد بيانات اعتماد AWS ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1313"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>بيانات اعتماد AWS للملف الشخصي {profile} مفقودة أو غير صالحة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1318"/>
        <source>Sign in to {provider}</source>
        <translation>تسجيل الدخول إلى {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1321"/>
        <source>Not signed in to {provider}</source>
        <translation>لم يتم تسجيل الدخول إلى {provider}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1325"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>تسجيل الدخول إلى {provider} ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1331"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>لم يتم تسجيل الدخول إلى {provider} (الملف الشخصي {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1352"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>أكمل في الطرفية التي فُتحت، ثم اضغط تحديث.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1371"/>
        <source>Loading workloads...</source>
        <translation>جارٍ تحميل workloads...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1432"/>
        <source>Could not read: {names}</source>
        <translation>تعذّرت القراءة: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1492"/>
        <source>Loading cluster data...</source>
        <translation>جارٍ تحميل بيانات العنقود...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1573"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>قيد التشغيل · {pending} معلّقة · {failed} فاشلة</translation>
    </message>
    <message>
        <location filename="../window.py" line="1582"/>
        <location filename="../window.py" line="1596"/>
        <source> · usage {value}</source>
        <translation> · الاستخدام {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1622"/>
        <source>Ready</source>
        <translation>جاهز</translation>
    </message>
    <message>
        <location filename="../window.py" line="1622"/>
        <source>Not ready</source>
        <translation>غير جاهز</translation>
    </message>
    <message>
        <location filename="../window.py" line="1647"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>الاستخدام الفعلي غير متاح: لم يتم العثور على metrics-server.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1741"/>
        <source>Refreshing...</source>
        <translation>جارٍ التحديث...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1926"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{count} Services في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1928"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{count} Endpoint Slices في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1931"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{count} Endpoints في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1934"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{count} Ingresses في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1936"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>{count} Ingress Classes في العنقود</translation>
    </message>
    <message>
        <location filename="../window.py" line="1938"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{count} Network Policies في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="1950"/>
        <location filename="../window.py" line="2016"/>
        <source>Running</source>
        <translation>قيد التشغيل</translation>
    </message>
    <message>
        <location filename="../window.py" line="1951"/>
        <location filename="../window.py" line="2012"/>
        <source>Pending</source>
        <translation>معلّق</translation>
    </message>
    <message>
        <location filename="../window.py" line="1952"/>
        <source>Succeeded</source>
        <translation>نجح</translation>
    </message>
    <message>
        <location filename="../window.py" line="1953"/>
        <location filename="../window.py" line="2011"/>
        <source>Failed</source>
        <translation>فشل</translation>
    </message>
    <message>
        <location filename="../window.py" line="1954"/>
        <source>Unknown</source>
        <translation>غير معروف</translation>
    </message>
    <message>
        <location filename="../window.py" line="1998"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{count} Pods في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2006"/>
        <source>Healthy</source>
        <translation>سليم</translation>
    </message>
    <message>
        <location filename="../window.py" line="2007"/>
        <source>Degraded</source>
        <translation>متدهور</translation>
    </message>
    <message>
        <location filename="../window.py" line="2008"/>
        <source>Unavailable</source>
        <translation>غير متاح</translation>
    </message>
    <message>
        <location filename="../window.py" line="2009"/>
        <source>Scaled to zero</source>
        <translation>مخفّض إلى صفر</translation>
    </message>
    <message>
        <location filename="../window.py" line="2010"/>
        <source>Complete</source>
        <translation>مكتمل</translation>
    </message>
    <message>
        <location filename="../window.py" line="2013"/>
        <source>Suspended</source>
        <translation>معلّق مؤقتاً</translation>
    </message>
    <message>
        <location filename="../window.py" line="2014"/>
        <source>Active</source>
        <translation>نشط</translation>
    </message>
    <message>
        <location filename="../window.py" line="2015"/>
        <source>Scheduled</source>
        <translation>مجدول</translation>
    </message>
    <message>
        <location filename="../window.py" line="2060"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{count} Deployments في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2063"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{count} StatefulSets في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2066"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{count} DaemonSets في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2069"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{count} ReplicaSets في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2072"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{count} ReplicationControllers في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2074"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{count} Jobs في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2075"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{count} CronJobs في {namespaces} namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="2095"/>
        <source>{visible} of {total} Pods</source>
        <translation>{visible} من {total} Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2096"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{visible} من {total} Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2097"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{visible} من {total} StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2098"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{visible} من {total} DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2099"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{visible} من {total} ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2101"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{visible} من {total} ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2103"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{visible} من {total} Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2104"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{visible} من {total} CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2105"/>
        <source>{visible} of {total} Services</source>
        <translation>{visible} من {total} Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="2106"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{visible} من {total} Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="2107"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{visible} من {total} Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="2108"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{visible} من {total} Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="2109"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{visible} من {total} Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2110"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{visible} من {total} Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="2156"/>
        <source>Loading...</source>
        <translation>جارٍ التحميل...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2202"/>
        <location filename="../window.py" line="2294"/>
        <source>Pod: {name}</source>
        <translation>Pod: {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2248"/>
        <source>Pods of {name}</source>
        <translation>Pods الخاصة بـ {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2250"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{count} Pods في {namespace} / {name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2315"/>
        <source>No Pods are associated with this workload</source>
        <translation>لا توجد Pods مرتبطة بهذا workload</translation>
    </message>
    <message>
        <location filename="../window.py" line="2322"/>
        <location filename="../window.py" line="2345"/>
        <source>Logs</source>
        <translation>السجلات</translation>
    </message>
    <message>
        <location filename="../window.py" line="2322"/>
        <source>This workload has no Pods.</source>
        <translation>ليس لهذا workload أي Pods.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2331"/>
        <location filename="../window.py" line="2354"/>
        <source>View logs</source>
        <translation>عرض السجلات</translation>
    </message>
    <message>
        <location filename="../window.py" line="2332"/>
        <source>Select the Pod:</source>
        <translation>اختر Pod:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2346"/>
        <source>Pod {name} has no containers.</source>
        <translation>ليس لـ Pod {name} أي حاويات.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2355"/>
        <source>Select the container of {name}:</source>
        <translation>اختر حاوية {name}:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2381"/>
        <source>Save to a file</source>
        <translation>حفظ في ملف</translation>
    </message>
    <message>
        <location filename="../window.py" line="2392"/>
        <source>Could not save</source>
        <translation>تعذّر الحفظ</translation>
    </message>
    <message>
        <location filename="../window.py" line="2393"/>
        <source>The file could not be written: {reason}</source>
        <translation>تعذّرت كتابة الملف: {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2441"/>
        <source>Logs: {pod} / {container}</source>
        <translation>السجلات: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2491"/>
        <source>Automatic</source>
        <translation>تلقائي</translation>
    </message>
    <message>
        <location filename="../window.py" line="2504"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>معطّل افتراضياً. عند تفعيله، يكتب KubeScope ما يفعله، وليس سجلات Pods ولا محتوى الموارد، في {path}. اقرأه قبل المشاركة: فهو يتضمن أسماء السياقات.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2535"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>لم يتم العثور على سياقات في kubeconfig.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2564"/>
        <source>Choose a kubeconfig file</source>
        <translation>اختر ملف kubeconfig</translation>
    </message>
    <message>
        <location filename="../window.py" line="2610"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>أمر تسجيل الدخول في الصف {row} غير صالح.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2623"/>
        <source>Light</source>
        <translation>فاتح</translation>
    </message>
    <message>
        <location filename="../window.py" line="2623"/>
        <source>Dark</source>
        <translation>داكن</translation>
    </message>
    <message>
        <location filename="../window.py" line="2642"/>
        <source>My theme</source>
        <translation>سمتي</translation>
    </message>
    <message>
        <location filename="../window.py" line="2686"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>تم مسح الذاكرة المؤقتة. يُحمَّل كل شيء من جديد عند الحاجة التالية.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2741"/>
        <source>Settings saved.</source>
        <translation>تم حفظ الإعدادات.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2778"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>ليس لمستخدمك صلاحية لتنفيذ هذا الإجراء ({action}). اطلب الوصول من مسؤول العنقود.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2783"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>ليس لمستخدمك صلاحية لتنفيذ هذا. اطلب الوصول من مسؤول العنقود.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2802"/>
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
        <location filename="../ui/workloads_overview_page.ui" line="52"/>
        <source>Refresh</source>
        <translation>تحديث</translation>
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
        <translation>الأحداث</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="306"/>
        <source>TYPE</source>
        <translation>النوع</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="311"/>
        <source>SOURCE</source>
        <translation>المصدر</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="316"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="321"/>
        <source>INVOLVED OBJECT</source>
        <translation>الكائن المعني</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="326"/>
        <source>MESSAGE</source>
        <translation>الرسالة</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="331"/>
        <source>COUNT</source>
        <translation>العدد</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="336"/>
        <source>AGE</source>
        <translation>العمر</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="341"/>
        <source>LAST SEEN</source>
        <translation>آخر ظهور</translation>
    </message>
</context>
</TS>
