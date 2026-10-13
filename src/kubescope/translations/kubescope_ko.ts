<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ko">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>로그인 도구를 찾을 수 없습니다</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>kubeconfig가 로그인에 “{tool}”을(를) 실행하지만 설치되어 있지 않거나 PATH에 없습니다. 설치한 뒤 새로 고치세요.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>컨텍스트를 찾을 수 없습니다</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>이 컨텍스트는 kubeconfig에 없습니다. ~/.kube/config를 확인하세요.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>인증에 실패했습니다</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>자격 증명이 만료되었을 수 있습니다. 다시 로그인(예: “aws sso login”, “gcloud auth login”, “az login”)한 뒤 새로 고치세요.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Not an Amazon EKS cluster</source>
        <translation>Amazon EKS 클러스터가 아닙니다</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Node Groups, Add-ons and the AWS cards of the Overview exist only on Amazon EKS contexts.</source>
        <translation>Node Groups, Add-ons 및 개요의 AWS 카드는 Amazon EKS 컨텍스트에만 있습니다.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="110"/>
        <source>Unexpected answer from AWS</source>
        <translation>AWS의 예상치 못한 응답</translation>
    </message>
    <message>
        <location filename="../errors.py" line="111"/>
        <source>Update the AWS CLI to its latest version and refresh.</source>
        <translation>AWS CLI를 최신 버전으로 업데이트한 뒤 새로 고치세요.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="118"/>
        <location filename="../errors.py" line="128"/>
        <source>Access denied</source>
        <translation>접근이 거부되었습니다</translation>
    </message>
    <message>
        <location filename="../errors.py" line="119"/>
        <source>Your AWS identity is not allowed to read this. The wiki lists the eks: permissions KubeScope needs.</source>
        <translation>AWS ID에 이 항목을 읽을 권한이 없습니다. KubeScope에 필요한 eks: 권한은 위키에 나와 있습니다.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>사용자에게 이 리소스를 읽을 권한이 없습니다.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="143"/>
        <source>No network connection</source>
        <translation>네트워크 연결 없음</translation>
    </message>
    <message>
        <location filename="../errors.py" line="144"/>
        <source>Check your internet connection or VPN and refresh.</source>
        <translation>인터넷 연결이나 VPN을 확인한 뒤 새로 고치세요.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="165"/>
        <source>Cluster unreachable</source>
        <translation>클러스터에 연결할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../errors.py" line="166"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>네트워크나 VPN을 확인하고 클러스터가 실행 중인지 확인하세요.</translation>
    </message>
    <message>
        <location filename="../errors.py" line="172"/>
        <source>Something went wrong</source>
        <translation>문제가 발생했습니다</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="46"/>
        <source>No log lines returned.</source>
        <translation>반환된 로그 줄이 없습니다.</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="51"/>
        <source>Updated at {time}</source>
        <translation>{time}에 업데이트됨</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="58"/>
        <source>Could not refresh logs: {message}</source>
        <translation>로그를 새로 고칠 수 없습니다: {message}</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>자동 새로 고침</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>몇 초마다 새 로그 줄을 가져오고 로그의 끝을 따라갑니다</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>지금 새로 고침</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../window.py" line="1562"/>
        <location filename="../window.py" line="1591"/>
        <source>TYPE</source>
        <translation>유형</translation>
    </message>
    <message>
        <location filename="../window.py" line="1563"/>
        <source>CLUSTER IP</source>
        <translation>클러스터 IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1564"/>
        <source>EXTERNAL IP</source>
        <translation>외부 IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1565"/>
        <location filename="../window.py" line="1569"/>
        <location filename="../window.py" line="1577"/>
        <source>PORTS</source>
        <translation>포트</translation>
    </message>
    <message>
        <location filename="../window.py" line="1568"/>
        <source>ADDRESS TYPE</source>
        <translation>주소 유형</translation>
    </message>
    <message>
        <location filename="../window.py" line="1570"/>
        <location filename="../window.py" line="1572"/>
        <source>ENDPOINTS</source>
        <translation>엔드포인트</translation>
    </message>
    <message>
        <location filename="../window.py" line="1574"/>
        <source>CLASS</source>
        <translation>클래스</translation>
    </message>
    <message>
        <location filename="../window.py" line="1575"/>
        <source>HOSTS</source>
        <translation>호스트</translation>
    </message>
    <message>
        <location filename="../window.py" line="1576"/>
        <source>ADDRESS</source>
        <translation>주소</translation>
    </message>
    <message>
        <location filename="../window.py" line="1580"/>
        <source>CONTROLLER</source>
        <translation>컨트롤러</translation>
    </message>
    <message>
        <location filename="../window.py" line="1581"/>
        <source>PARAMETERS</source>
        <translation>매개변수</translation>
    </message>
    <message>
        <location filename="../window.py" line="1584"/>
        <source>POD SELECTOR</source>
        <translation>POD 선택기</translation>
    </message>
    <message>
        <location filename="../window.py" line="1585"/>
        <source>POLICY TYPES</source>
        <translation>정책 유형</translation>
    </message>
    <message>
        <location filename="../window.py" line="1588"/>
        <location filename="../window.py" line="1592"/>
        <source>DATA</source>
        <translation>데이터</translation>
    </message>
    <message>
        <location filename="../window.py" line="1595"/>
        <source>USAGE</source>
        <translation>사용량</translation>
    </message>
    <message>
        <location filename="../window.py" line="1598"/>
        <source>TYPES</source>
        <translation>유형</translation>
    </message>
    <message>
        <location filename="../window.py" line="1601"/>
        <source>REFERENCE</source>
        <translation>참조</translation>
    </message>
    <message>
        <location filename="../window.py" line="1602"/>
        <source>MIN PODS</source>
        <translation>최소 POD</translation>
    </message>
    <message>
        <location filename="../window.py" line="1603"/>
        <source>MAX PODS</source>
        <translation>최대 POD</translation>
    </message>
    <message>
        <location filename="../window.py" line="1604"/>
        <source>REPLICAS</source>
        <translation>레플리카</translation>
    </message>
    <message>
        <location filename="../window.py" line="1607"/>
        <source>MIN AVAILABLE</source>
        <translation>최소 가용</translation>
    </message>
    <message>
        <location filename="../window.py" line="1608"/>
        <source>MAX UNAVAILABLE</source>
        <translation>최대 불가용</translation>
    </message>
    <message>
        <location filename="../window.py" line="1609"/>
        <source>ALLOWED DISRUPTIONS</source>
        <translation>허용된 중단</translation>
    </message>
    <message>
        <location filename="../window.py" line="1612"/>
        <source>VALUE</source>
        <translation>값</translation>
    </message>
    <message>
        <location filename="../window.py" line="1613"/>
        <source>GLOBAL DEFAULT</source>
        <translation>전역 기본값</translation>
    </message>
    <message>
        <location filename="../window.py" line="1616"/>
        <source>HANDLER</source>
        <translation>핸들러</translation>
    </message>
    <message>
        <location filename="../window.py" line="1619"/>
        <source>HOLDER</source>
        <translation>보유자</translation>
    </message>
    <message>
        <location filename="../window.py" line="1622"/>
        <location filename="../window.py" line="1625"/>
        <source>WEBHOOKS</source>
        <translation>웹훅</translation>
    </message>
    <message>
        <location filename="../window.py" line="1628"/>
        <location filename="../window.py" line="1635"/>
        <location filename="../window.py" line="1658"/>
        <location filename="../ui/main_window.ui" line="2023"/>
        <location filename="../ui/main_window.ui" line="2547"/>
        <source>STATUS</source>
        <translation>상태</translation>
    </message>
    <message>
        <location filename="../window.py" line="1629"/>
        <source>INSTANCE TYPES</source>
        <translation>인스턴스 유형</translation>
    </message>
    <message>
        <location filename="../window.py" line="1630"/>
        <source>NODES</source>
        <translation>노드</translation>
    </message>
    <message>
        <location filename="../window.py" line="1631"/>
        <source>AMI TYPE</source>
        <translation>AMI 유형</translation>
    </message>
    <message>
        <location filename="../window.py" line="1632"/>
        <source>AMI VERSION</source>
        <translation>AMI 버전</translation>
    </message>
    <message>
        <location filename="../window.py" line="1636"/>
        <location filename="../ui/main_window.ui" line="2557"/>
        <source>VERSION</source>
        <translation>버전</translation>
    </message>
    <message>
        <location filename="../window.py" line="1637"/>
        <source>SOURCE</source>
        <translation>출처</translation>
    </message>
    <message>
        <location filename="../window.py" line="1647"/>
        <source>COMPLETIONS</source>
        <translation>완료</translation>
    </message>
    <message>
        <location filename="../window.py" line="1648"/>
        <source>SCHEDULE</source>
        <translation>일정</translation>
    </message>
    <message>
        <location filename="../window.py" line="1649"/>
        <location filename="../ui/main_window.ui" line="2018"/>
        <source>READY</source>
        <translation>준비됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="1654"/>
        <location filename="../window.py" line="1670"/>
        <location filename="../ui/main_window.ui" line="1826"/>
        <location filename="../ui/main_window.ui" line="2003"/>
        <source>NAMESPACE</source>
        <translation>네임스페이스</translation>
    </message>
    <message>
        <location filename="../window.py" line="1656"/>
        <location filename="../window.py" line="1672"/>
        <location filename="../ui/main_window.ui" line="2013"/>
        <source>NAME</source>
        <translation>이름</translation>
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
        <translation>메모리</translation>
    </message>
    <message>
        <location filename="../window.py" line="1661"/>
        <source>RESTARTS</source>
        <translation>재시작</translation>
    </message>
    <message>
        <location filename="../window.py" line="1662"/>
        <location filename="../window.py" line="1674"/>
        <location filename="../ui/main_window.ui" line="2028"/>
        <location filename="../ui/main_window.ui" line="2577"/>
        <source>AGE</source>
        <translation>경과</translation>
    </message>
    <message>
        <location filename="../window.py" line="1671"/>
        <location filename="../ui/main_window.ui" line="2008"/>
        <source>KIND</source>
        <translation>종류</translation>
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
        <translation>Kubernetes 콘솔</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="339"/>
        <source>CONTEXT</source>
        <translation>컨텍스트</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="352"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>kubeconfig의 Kubernetes 컨텍스트</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="372"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>클라우드 CLI로 로그인한 뒤 클러스터 데이터를 다시 불러옵니다</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="375"/>
        <source>Sign in</source>
        <translation>로그인</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="397"/>
        <source>Settings</source>
        <translation>설정</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="437"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>kubeconfig에서 클러스터 컨텍스트를 찾을 수 없습니다. kubeconfig에 클러스터를 추가(예: AWS CLI의 aws eks update-kubeconfig)한 뒤 다시 불러오세요.</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="478"/>
        <source>Dismiss</source>
        <translation>닫기</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="569"/>
        <source>MONITORING</source>
        <translation>모니터링</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="576"/>
        <source>Cluster</source>
        <translation>클러스터</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="607"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="638"/>
        <source>Workloads</source>
        <translation>워크로드</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="690"/>
        <location filename="../ui/main_window.ui" line="1714"/>
        <source>Overview</source>
        <translation>개요</translation>
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
        <translation>네트워크</translation>
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
        <translation>구성</translation>
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
        <translation>보안 접근
리소스 읽기 전용 모드</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1721"/>
        <source>Cluster resources and capacity</source>
        <translation>클러스터 리소스와 용량</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1746"/>
        <location filename="../ui/main_window.ui" line="1759"/>
        <location filename="../ui/main_window.ui" line="1772"/>
        <source>Refresh</source>
        <translation>새로 고침</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1878"/>
        <source>Search by name or namespace...</source>
        <translation>이름 또는 네임스페이스로 검색...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1929"/>
        <source>View Pods of the selected workload</source>
        <translation>선택한 워크로드의 Pod 보기</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1945"/>
        <source>View JSON details of the selected workload</source>
        <translation>선택한 워크로드의 JSON 세부 정보 보기</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1948"/>
        <source>Details</source>
        <translation>세부 정보</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1961"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>선택한 워크로드의 Pod 로그 보기</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1964"/>
        <source>Logs</source>
        <translation>로그</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2507"/>
        <source>Nodes</source>
        <translation>노드</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2542"/>
        <source>NODE</source>
        <translation>노드</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2552"/>
        <source>ROLE</source>
        <translation>역할</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2572"/>
        <source>PODS</source>
        <translation>POD</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2590"/>
        <source>Select a context to load workloads</source>
        <translation>워크로드를 불러올 컨텍스트를 선택하세요</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2613"/>
        <source>Data fetched from the cluster API</source>
        <translation>클러스터 API에서 가져온 데이터</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2674"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>DCO Tecnologia 웹사이트 열기</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2694"/>
        <source>MIT License</source>
        <translation>MIT 라이선스</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2697"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope는 MIT 라이선스로 배포되는 오픈 소스 소프트웨어입니다</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2733"/>
        <source>Update available</source>
        <translation>업데이트 가능</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2736"/>
        <source>Open the download page of the new version</source>
        <translation>새 버전의 다운로드 페이지 열기</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2764"/>
        <source>Check for updates</source>
        <translation>업데이트 확인</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2784"/>
        <source>Open the project on GitHub</source>
        <translation>GitHub에서 프로젝트 열기</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="2052"/>
        <location filename="../ui/overview_page.ui" line="194"/>
        <source>nodes ready</source>
        <translation>노드 준비됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="2068"/>
        <location filename="../ui/overview_page.ui" line="315"/>
        <source>cores requested / allocatable</source>
        <translation>코어 요청됨 / 할당 가능</translation>
    </message>
    <message>
        <location filename="../window.py" line="2082"/>
        <location filename="../ui/overview_page.ui" line="382"/>
        <source>requested / allocatable</source>
        <translation>요청됨 / 할당 가능</translation>
    </message>
    <message>
        <location filename="../window.py" line="2101"/>
        <location filename="../ui/overview_page.ui" line="456"/>
        <source>in the cluster</source>
        <translation>클러스터 내</translation>
    </message>
    <message>
        <location filename="../window.py" line="2103"/>
        <location filename="../ui/overview_page.ui" line="510"/>
        <location filename="../ui/overview_page.ui" line="564"/>
        <location filename="../ui/overview_page.ui" line="618"/>
        <source>workloads</source>
        <translation>워크로드</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="29"/>
        <source>Cluster resources</source>
        <translation>클러스터 리소스</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="78"/>
        <source>CLUSTER INFO</source>
        <translation>클러스터 정보</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="125"/>
        <source>NETWORKING</source>
        <translation>네트워킹</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="174"/>
        <source>NODES</source>
        <translation>노드</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="228"/>
        <source>PODS</source>
        <translation>POD</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="248"/>
        <source>running / capacity</source>
        <translation>실행 중 / 용량</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="295"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="362"/>
        <source>MEMORY</source>
        <translation>메모리</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="436"/>
        <source>NAMESPACES</source>
        <translation>네임스페이스</translation>
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
        <translation>이름</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>준비됨</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>단계</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>컨테이너</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>경과</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>Pod 세부 정보</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>로그 보기</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>닫기</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="3090"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>컨텍스트에 알기 쉬운 이름을 지정하세요. 이름을 비워 두면 원래 이름이 유지됩니다.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>변경 사항 저장</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>일반</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="107"/>
        <source>Language</source>
        <translation>언어</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="142"/>
        <source>Theme</source>
        <translation>테마</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="177"/>
        <source>New theme...</source>
        <translation>새 테마...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>테마 편집...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>테마 폴더 열기</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>기본 네임스페이스</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>각 컨텍스트가 처음 열리는 네임스페이스입니다. 비워 두면 모두 표시합니다.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>마지막으로 사용한 컨텍스트 기억</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>앱을 시작할 때 GitHub에서 새 버전 확인</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>공개 GitHub API에 최신 릴리스를 요청하며 앱 버전 외에는 아무것도 보내지 않습니다. 하단의 아이콘으로 직접 확인할 수 있습니다.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>디버그 모드: 공유할 수 있는 로그 파일 작성</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>로그 폴더 열기</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>캐시 지우기</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>이미 불러온 목록과 개요, 모든 클러스터의 로그인 정보를 지워서 다음 요청 때 다시 로그인하고 모두 새로 불러옵니다. 설정은 유지됩니다.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>KUBECONFIG 파일</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>KubeScope는 KUBECONFIG 변수의 파일 또는 ~/.kube/config를 읽습니다. 대신 읽을 파일을 여기에 추가하세요. 적용하려면 저장을 누르세요.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>파일 추가...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>제거</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>로그인 명령</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>KubeScope가 모르는 클라우드의 경우 kubeconfig가 로그인에 사용하는 프로그램(예: oci)과 로그인하는 명령(예: oci session authenticate)을 입력하세요. 그러면 로그인 버튼이 셸 없이 그 명령을 실행합니다. 적용하려면 저장을 누르세요.</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>프로그램</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>로그인 명령</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>행 추가</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>컨텍스트 이름</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>컨텍스트</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>표시 이름</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>페이지 배경</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>패널과 카드</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>보조 패널</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>막대 트랙</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>테두리</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>상단 바</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>상단 바 로고</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>상단 바 선택기</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>상단 바 선택기 테두리</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>상단 바 선택 항목</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>상단 바 텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>사이드바 제목</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>보조 텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>비활성 텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>강조 텍스트와 링크</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>강조 버튼</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>마우스를 올린 강조 버튼</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>비활성 강조 버튼</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>포커스와 하이라이트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>배지 텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>강조 색조</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>텍스트 선택</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>강조 테두리</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>상단 바와 강조 버튼의 텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>정상 텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>정상 배경</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>경고 텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>경고 배경</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>실패 텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>실패 배경</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>대기 텍스트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>대기 배경</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>문제가 있는 행</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>새로 생성된 Pod의 행</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>사용량 막대, 거의 찬 상태</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>사용량 막대, 가득 찬 상태</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>상태 막대, 정상</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>상태 막대, 경고</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>상태 막대, 실패</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>새 테마</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>테마 편집: {name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>테마 이름</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>라이트</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>다크</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>이름</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>기반 테마</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>색상</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>이 탭의 내용을 파일로 저장</translation>
    </message>
</context>
<context>
    <name>WorkloadWindow</name>
    <message>
        <location filename="../window.py" line="706"/>
        <source>0 Deployments</source>
        <translation>Deployments 0개</translation>
    </message>
    <message>
        <location filename="../window.py" line="722"/>
        <location filename="../window.py" line="2321"/>
        <location filename="../window.py" line="2344"/>
        <location filename="../window.py" line="3328"/>
        <source>All namespaces</source>
        <translation>모든 네임스페이스</translation>
    </message>
    <message>
        <location filename="../window.py" line="832"/>
        <source>Loading contexts...</source>
        <translation>컨텍스트를 불러오는 중...</translation>
    </message>
    <message>
        <location filename="../window.py" line="841"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>kubeconfig를 불러올 수 없습니다: {error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="863"/>
        <source>No contexts found in kubeconfig</source>
        <translation>kubeconfig에서 컨텍스트를 찾을 수 없습니다</translation>
    </message>
    <message>
        <location filename="../window.py" line="913"/>
        <location filename="../window.py" line="991"/>
        <source>Unpin from the top</source>
        <translation>상단에서 고정 해제</translation>
    </message>
    <message>
        <location filename="../window.py" line="913"/>
        <source>Pin to the top</source>
        <translation>상단에 고정</translation>
    </message>
    <message>
        <location filename="../window.py" line="1029"/>
        <source>Close</source>
        <translation>닫기</translation>
    </message>
    <message>
        <location filename="../window.py" line="1076"/>
        <source>Status</source>
        <translation>상태</translation>
    </message>
    <message>
        <location filename="../window.py" line="1077"/>
        <source>Kubernetes version</source>
        <translation>Kubernetes 버전</translation>
    </message>
    <message>
        <location filename="../window.py" line="1078"/>
        <source>Platform version</source>
        <translation>플랫폼 버전</translation>
    </message>
    <message>
        <location filename="../window.py" line="1079"/>
        <source>Created</source>
        <translation>생성됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="1080"/>
        <source>Provider</source>
        <translation>공급자</translation>
    </message>
    <message>
        <location filename="../window.py" line="1083"/>
        <source>API server endpoint</source>
        <translation>API 서버 엔드포인트</translation>
    </message>
    <message>
        <location filename="../window.py" line="1084"/>
        <source>Cluster ARN</source>
        <translation>클러스터 ARN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1085"/>
        <source>Cluster IAM role ARN</source>
        <translation>클러스터 IAM 역할 ARN</translation>
    </message>
    <message>
        <location filename="../window.py" line="1086"/>
        <source>OpenID Connect provider URL</source>
        <translation>OpenID Connect 공급자 URL</translation>
    </message>
    <message>
        <location filename="../window.py" line="1094"/>
        <source>VPC</source>
        <translation>VPC</translation>
    </message>
    <message>
        <location filename="../window.py" line="1095"/>
        <source>Cluster security group</source>
        <translation>클러스터 보안 그룹</translation>
    </message>
    <message>
        <location filename="../window.py" line="1097"/>
        <source>Additional security groups</source>
        <translation>추가 보안 그룹</translation>
    </message>
    <message>
        <location filename="../window.py" line="1098"/>
        <source>None</source>
        <translation>없음</translation>
    </message>
    <message>
        <location filename="../window.py" line="1101"/>
        <source>API server endpoint access</source>
        <translation>API 서버 엔드포인트 접근</translation>
    </message>
    <message>
        <location filename="../window.py" line="1104"/>
        <source>Cluster IP address family</source>
        <translation>클러스터 IP 주소 체계</translation>
    </message>
    <message>
        <location filename="../window.py" line="1105"/>
        <source>Service IPv4 range</source>
        <translation>서비스 IPv4 범위</translation>
    </message>
    <message>
        <location filename="../window.py" line="1107"/>
        <source>Public access source allowlist</source>
        <translation>공개 접근 허용 소스 목록</translation>
    </message>
    <message>
        <location filename="../window.py" line="1110"/>
        <source>Subnets</source>
        <translation>서브넷</translation>
    </message>
    <message>
        <location filename="../window.py" line="1120"/>
        <location filename="../window.py" line="2553"/>
        <source>Active</source>
        <translation>활성</translation>
    </message>
    <message>
        <location filename="../window.py" line="1121"/>
        <source>Creating</source>
        <translation>생성 중</translation>
    </message>
    <message>
        <location filename="../window.py" line="1122"/>
        <source>Updating</source>
        <translation>업데이트 중</translation>
    </message>
    <message>
        <location filename="../window.py" line="1123"/>
        <source>Deleting</source>
        <translation>삭제 중</translation>
    </message>
    <message>
        <location filename="../window.py" line="1124"/>
        <location filename="../window.py" line="2546"/>
        <source>Degraded</source>
        <translation>성능 저하</translation>
    </message>
    <message>
        <location filename="../window.py" line="1125"/>
        <location filename="../window.py" line="2492"/>
        <location filename="../window.py" line="2550"/>
        <source>Failed</source>
        <translation>실패</translation>
    </message>
    <message>
        <location filename="../window.py" line="1126"/>
        <source>Creation failed</source>
        <translation>생성 실패</translation>
    </message>
    <message>
        <location filename="../window.py" line="1127"/>
        <source>Update failed</source>
        <translation>업데이트 실패</translation>
    </message>
    <message>
        <location filename="../window.py" line="1128"/>
        <source>Deletion failed</source>
        <translation>삭제 실패</translation>
    </message>
    <message>
        <location filename="../window.py" line="1129"/>
        <location filename="../window.py" line="2490"/>
        <location filename="../window.py" line="2551"/>
        <source>Pending</source>
        <translation>대기 중</translation>
    </message>
    <message>
        <location filename="../window.py" line="1130"/>
        <source>Deployed</source>
        <translation>배포됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="1131"/>
        <source>Superseded</source>
        <translation>대체됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="1132"/>
        <source>Uninstalled</source>
        <translation>제거됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="1133"/>
        <source>Uninstalling</source>
        <translation>제거 중</translation>
    </message>
    <message>
        <location filename="../window.py" line="1134"/>
        <source>Pending install</source>
        <translation>설치 대기 중</translation>
    </message>
    <message>
        <location filename="../window.py" line="1135"/>
        <source>Pending upgrade</source>
        <translation>업그레이드 대기 중</translation>
    </message>
    <message>
        <location filename="../window.py" line="1136"/>
        <source>Pending rollback</source>
        <translation>롤백 대기 중</translation>
    </message>
    <message>
        <location filename="../window.py" line="1137"/>
        <source>Public</source>
        <translation>공개</translation>
    </message>
    <message>
        <location filename="../window.py" line="1138"/>
        <source>Private</source>
        <translation>비공개</translation>
    </message>
    <message>
        <location filename="../window.py" line="1139"/>
        <source>Public and private</source>
        <translation>공개 및 비공개</translation>
    </message>
    <message>
        <location filename="../window.py" line="1232"/>
        <source>Overview</source>
        <translation>개요</translation>
    </message>
    <message>
        <location filename="../window.py" line="1233"/>
        <source>Cluster resources and capacity</source>
        <translation>클러스터 리소스와 용량</translation>
    </message>
    <message>
        <location filename="../window.py" line="1235"/>
        <source>Details &amp; Logs</source>
        <translation>세부 정보 및 로그</translation>
    </message>
    <message>
        <location filename="../window.py" line="1237"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>리소스 세부 정보와 Pod 로그, 각각 별도의 탭</translation>
    </message>
    <message>
        <location filename="../window.py" line="1240"/>
        <source>Settings</source>
        <translation>설정</translation>
    </message>
    <message>
        <location filename="../window.py" line="1241"/>
        <source>Preferences and context names</source>
        <translation>환경설정과 컨텍스트 이름</translation>
    </message>
    <message>
        <location filename="../window.py" line="1243"/>
        <source>Workloads overview</source>
        <translation>워크로드 개요</translation>
    </message>
    <message>
        <location filename="../window.py" line="1245"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>모든 워크로드 종류의 상태와 최신 이벤트</translation>
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
        <translation>클러스터의 Pods</translation>
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
        <translation>클러스터의 Deployments</translation>
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
        <translation>클러스터의 StatefulSets</translation>
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
        <translation>클러스터의 DaemonSets</translation>
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
        <translation>클러스터의 ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1267"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1268"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>클러스터의 ReplicationControllers</translation>
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
        <translation>클러스터의 Jobs</translation>
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
        <translation>클러스터의 CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1272"/>
        <source>Services of the cluster</source>
        <translation>클러스터의 Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1274"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1275"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>클러스터의 Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1278"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1279"/>
        <source>Endpoints of the cluster</source>
        <translation>클러스터의 Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1282"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1283"/>
        <source>Ingresses of the cluster</source>
        <translation>클러스터의 Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1286"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1287"/>
        <source>Ingress Classes of the cluster</source>
        <translation>클러스터의 Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1290"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1291"/>
        <source>Network Policies of the cluster</source>
        <translation>클러스터의 Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1294"/>
        <source>Config Maps</source>
        <translation>Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1295"/>
        <source>Config Maps of the cluster</source>
        <translation>클러스터의 Config Maps</translation>
    </message>
    <message>
        <location filename="../window.py" line="1298"/>
        <source>Secrets</source>
        <translation>Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1299"/>
        <source>Secrets of the cluster</source>
        <translation>클러스터의 Secrets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1302"/>
        <source>Resource Quotas</source>
        <translation>Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1303"/>
        <source>Resource Quotas of the cluster</source>
        <translation>클러스터의 Resource Quotas</translation>
    </message>
    <message>
        <location filename="../window.py" line="1306"/>
        <source>Limit Ranges</source>
        <translation>Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1307"/>
        <source>Limit Ranges of the cluster</source>
        <translation>클러스터의 Limit Ranges</translation>
    </message>
    <message>
        <location filename="../window.py" line="1310"/>
        <source>Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1311"/>
        <source>Horizontal Pod Autoscalers of the cluster</source>
        <translation>클러스터의 Horizontal Pod Autoscalers</translation>
    </message>
    <message>
        <location filename="../window.py" line="1314"/>
        <source>Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1315"/>
        <source>Pod Disruption Budgets of the cluster</source>
        <translation>클러스터의 Pod Disruption Budgets</translation>
    </message>
    <message>
        <location filename="../window.py" line="1318"/>
        <source>Priority Classes</source>
        <translation>Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1319"/>
        <source>Priority Classes of the cluster</source>
        <translation>클러스터의 Priority Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1322"/>
        <source>Runtime Classes</source>
        <translation>Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1323"/>
        <source>Runtime Classes of the cluster</source>
        <translation>클러스터의 Runtime Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1326"/>
        <source>Leases</source>
        <translation>Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1327"/>
        <source>Leases of the cluster</source>
        <translation>클러스터의 Leases</translation>
    </message>
    <message>
        <location filename="../window.py" line="1330"/>
        <source>Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1331"/>
        <source>Mutating Webhook Configurations of the cluster</source>
        <translation>클러스터의 Mutating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1334"/>
        <source>Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1335"/>
        <source>Validating Webhook Configurations of the cluster</source>
        <translation>클러스터의 Validating Webhook Configurations</translation>
    </message>
    <message>
        <location filename="../window.py" line="1338"/>
        <source>Node Groups</source>
        <translation>Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1339"/>
        <source>Node Groups of the cluster</source>
        <translation>클러스터의 Node Groups</translation>
    </message>
    <message>
        <location filename="../window.py" line="1342"/>
        <source>Add-ons</source>
        <translation>Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1343"/>
        <source>Add-ons of the cluster</source>
        <translation>클러스터의 Add-ons</translation>
    </message>
    <message>
        <location filename="../window.py" line="1352"/>
        <source>Version {version}</source>
        <translation>버전 {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1355"/>
        <source>Open the project on GitHub</source>
        <translation>GitHub에서 프로젝트 열기</translation>
    </message>
    <message>
        <location filename="../window.py" line="1389"/>
        <source>Up to date</source>
        <translation>최신 버전</translation>
    </message>
    <message>
        <location filename="../window.py" line="1390"/>
        <source>Could not check</source>
        <translation>확인할 수 없음</translation>
    </message>
    <message>
        <location filename="../window.py" line="1401"/>
        <source>Check for updates</source>
        <translation>업데이트 확인</translation>
    </message>
    <message>
        <location filename="../window.py" line="1402"/>
        <source>Checking for updates...</source>
        <translation>업데이트 확인 중...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1403"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope가 최신 버전입니다. 클릭하여 다시 확인하세요.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1404"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>업데이트를 확인할 수 없습니다. 클릭하여 다시 시도하세요.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1410"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>업데이트 가능: {version}. 클릭하면 다운로드 페이지가 열리고, 오른쪽 클릭하면 다시 확인합니다.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1418"/>
        <source>Update available</source>
        <translation>업데이트 가능</translation>
    </message>
    <message>
        <location filename="../window.py" line="1420"/>
        <source>Download KubeScope {version}</source>
        <translation>KubeScope {version} 다운로드</translation>
    </message>
    <message>
        <location filename="../window.py" line="1456"/>
        <source>Check for updates again</source>
        <translation>업데이트 다시 확인</translation>
    </message>
    <message>
        <location filename="../window.py" line="1553"/>
        <location filename="../window.py" line="2228"/>
        <source>Loading resources...</source>
        <translation>리소스를 불러오는 중...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1797"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>AWS 자격 증명 구성 ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1801"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>프로필 {profile}의 AWS 자격 증명이 없거나 올바르지 않습니다</translation>
    </message>
    <message>
        <location filename="../window.py" line="1806"/>
        <source>Sign in to {provider}</source>
        <translation>{provider}에 로그인</translation>
    </message>
    <message>
        <location filename="../window.py" line="1809"/>
        <source>Not signed in to {provider}</source>
        <translation>{provider}에 로그인되어 있지 않습니다</translation>
    </message>
    <message>
        <location filename="../window.py" line="1813"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>{provider}에 로그인 ({profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1819"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>{provider}에 로그인되어 있지 않습니다 (프로필 {profile})</translation>
    </message>
    <message>
        <location filename="../window.py" line="1840"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>열린 터미널에서 완료한 뒤 새로 고침을 누르세요.</translation>
    </message>
    <message>
        <location filename="../window.py" line="1859"/>
        <source>Loading workloads...</source>
        <translation>워크로드를 불러오는 중...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1920"/>
        <source>Could not read: {names}</source>
        <translation>읽을 수 없음: {names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1980"/>
        <source>Loading cluster data...</source>
        <translation>클러스터 데이터를 불러오는 중...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2061"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>실행 중 · 대기 {pending} · 실패 {failed}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2070"/>
        <location filename="../window.py" line="2084"/>
        <source> · usage {value}</source>
        <translation> · 사용량 {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2108"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>실제 사용량을 확인할 수 없습니다: metrics-server를 찾을 수 없습니다.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2133"/>
        <source>Ready</source>
        <translation>준비됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="2133"/>
        <source>Not ready</source>
        <translation>준비 안 됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="2245"/>
        <source>Refreshing...</source>
        <translation>새로 고치는 중...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2436"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Services {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2438"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Endpoint Slices {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2441"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Endpoints {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2444"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Ingresses {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2446"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>클러스터의 Ingress Classes {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2448"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Network Policies {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2451"/>
        <source>{count} Config Maps in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Config Maps {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2453"/>
        <source>{count} Secrets in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Secrets {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2455"/>
        <source>{count} Resource Quotas in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Resource Quotas {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2458"/>
        <source>{count} Limit Ranges in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Limit Ranges {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2461"/>
        <source>{count} Horizontal Pod Autoscalers in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Horizontal Pod Autoscalers {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2464"/>
        <source>{count} Pod Disruption Budgets in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Pod Disruption Budgets {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2466"/>
        <source>{count} Leases in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Leases {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2468"/>
        <source>{count} Priority Classes in the cluster</source>
        <translation>클러스터의 Priority Classes {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2470"/>
        <source>{count} Runtime Classes in the cluster</source>
        <translation>클러스터의 Runtime Classes {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2472"/>
        <source>{count} Mutating Webhook Configurations in the cluster</source>
        <translation>클러스터의 Mutating Webhook Configurations {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2475"/>
        <source>{count} Validating Webhook Configurations in the cluster</source>
        <translation>클러스터의 Validating Webhook Configurations {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2477"/>
        <source>{count} Node Groups in the cluster</source>
        <translation>클러스터의 Node Groups {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2478"/>
        <source>{count} Add-ons in the cluster</source>
        <translation>클러스터의 Add-ons {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2489"/>
        <location filename="../window.py" line="2555"/>
        <source>Running</source>
        <translation>실행 중</translation>
    </message>
    <message>
        <location filename="../window.py" line="2491"/>
        <source>Succeeded</source>
        <translation>성공</translation>
    </message>
    <message>
        <location filename="../window.py" line="2493"/>
        <source>Unknown</source>
        <translation>알 수 없음</translation>
    </message>
    <message>
        <location filename="../window.py" line="2537"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Pods {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2545"/>
        <source>Healthy</source>
        <translation>정상</translation>
    </message>
    <message>
        <location filename="../window.py" line="2547"/>
        <source>Unavailable</source>
        <translation>사용 불가</translation>
    </message>
    <message>
        <location filename="../window.py" line="2548"/>
        <source>Scaled to zero</source>
        <translation>0으로 축소됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="2549"/>
        <source>Complete</source>
        <translation>완료</translation>
    </message>
    <message>
        <location filename="../window.py" line="2552"/>
        <source>Suspended</source>
        <translation>일시 중지됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="2554"/>
        <source>Scheduled</source>
        <translation>예약됨</translation>
    </message>
    <message>
        <location filename="../window.py" line="2599"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Deployments {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2602"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 StatefulSets {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2605"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 DaemonSets {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2608"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 ReplicaSets {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2611"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 ReplicationControllers {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2613"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 Jobs {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2614"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{namespaces}개 네임스페이스의 CronJobs {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2638"/>
        <source>{visible} of {total} Pods</source>
        <translation>Pods {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2639"/>
        <source>{visible} of {total} Deployments</source>
        <translation>Deployments {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2640"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>StatefulSets {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2641"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>DaemonSets {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2642"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>ReplicaSets {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2644"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>ReplicationControllers {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2646"/>
        <source>{visible} of {total} Jobs</source>
        <translation>Jobs {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2647"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>CronJobs {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2648"/>
        <source>{visible} of {total} Services</source>
        <translation>Services {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2649"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>Endpoint Slices {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2650"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>Endpoints {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2651"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>Ingresses {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2652"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>Ingress Classes {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2653"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>Network Policies {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2654"/>
        <source>{visible} of {total} Config Maps</source>
        <translation>Config Maps {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2655"/>
        <source>{visible} of {total} Secrets</source>
        <translation>Secrets {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2656"/>
        <source>{visible} of {total} Resource Quotas</source>
        <translation>Resource Quotas {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2657"/>
        <source>{visible} of {total} Limit Ranges</source>
        <translation>Limit Ranges {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2659"/>
        <source>{visible} of {total} Horizontal Pod Autoscalers</source>
        <translation>Horizontal Pod Autoscalers {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2662"/>
        <source>{visible} of {total} Pod Disruption Budgets</source>
        <translation>Pod Disruption Budgets {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2664"/>
        <source>{visible} of {total} Priority Classes</source>
        <translation>Priority Classes {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2665"/>
        <source>{visible} of {total} Runtime Classes</source>
        <translation>Runtime Classes {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2666"/>
        <source>{visible} of {total} Leases</source>
        <translation>Leases {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2668"/>
        <source>{visible} of {total} Mutating Webhook Configurations</source>
        <translation>Mutating Webhook Configurations {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2671"/>
        <source>{visible} of {total} Validating Webhook Configurations</source>
        <translation>Validating Webhook Configurations {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2673"/>
        <source>{visible} of {total} Node Groups</source>
        <translation>Node Groups {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2674"/>
        <source>{visible} of {total} Add-ons</source>
        <translation>Add-ons {total}개 중 {visible}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2720"/>
        <source>Loading...</source>
        <translation>불러오는 중...</translation>
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
        <translation>{name}의 Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2814"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{namespace} / {name}의 Pods {count}개</translation>
    </message>
    <message>
        <location filename="../window.py" line="2879"/>
        <source>No Pods are associated with this workload</source>
        <translation>이 워크로드와 연결된 Pod가 없습니다</translation>
    </message>
    <message>
        <location filename="../window.py" line="2886"/>
        <location filename="../window.py" line="2909"/>
        <source>Logs</source>
        <translation>로그</translation>
    </message>
    <message>
        <location filename="../window.py" line="2886"/>
        <source>This workload has no Pods.</source>
        <translation>이 워크로드에는 Pod가 없습니다.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2895"/>
        <location filename="../window.py" line="2918"/>
        <source>View logs</source>
        <translation>로그 보기</translation>
    </message>
    <message>
        <location filename="../window.py" line="2896"/>
        <source>Select the Pod:</source>
        <translation>Pod 선택:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2910"/>
        <source>Pod {name} has no containers.</source>
        <translation>Pod {name}에는 컨테이너가 없습니다.</translation>
    </message>
    <message>
        <location filename="../window.py" line="2919"/>
        <source>Select the container of {name}:</source>
        <translation>{name}의 컨테이너 선택:</translation>
    </message>
    <message>
        <location filename="../window.py" line="2945"/>
        <source>Save to a file</source>
        <translation>파일로 저장</translation>
    </message>
    <message>
        <location filename="../window.py" line="2956"/>
        <source>Could not save</source>
        <translation>저장할 수 없습니다</translation>
    </message>
    <message>
        <location filename="../window.py" line="2957"/>
        <source>The file could not be written: {reason}</source>
        <translation>파일을 쓸 수 없습니다: {reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3003"/>
        <source>Logs: {pod} / {container}</source>
        <translation>로그: {pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="3053"/>
        <source>Automatic</source>
        <translation>자동</translation>
    </message>
    <message>
        <location filename="../window.py" line="3066"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>기본적으로 꺼져 있습니다. 켜면 KubeScope가 수행한 작업을 {path}에 기록하며 Pod 로그나 리소스 내용은 기록하지 않습니다. 공유하기 전에 읽어 보세요. 컨텍스트 이름이 포함되어 있습니다.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3097"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>kubeconfig에서 컨텍스트를 찾을 수 없습니다.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3126"/>
        <source>Choose a kubeconfig file</source>
        <translation>kubeconfig 파일 선택</translation>
    </message>
    <message>
        <location filename="../window.py" line="3172"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>{row}행의 로그인 명령이 올바르지 않습니다.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3185"/>
        <source>Light</source>
        <translation>라이트</translation>
    </message>
    <message>
        <location filename="../window.py" line="3185"/>
        <source>Dark</source>
        <translation>다크</translation>
    </message>
    <message>
        <location filename="../window.py" line="3204"/>
        <source>My theme</source>
        <translation>내 테마</translation>
    </message>
    <message>
        <location filename="../window.py" line="3248"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>캐시를 지웠습니다. 다음에 필요할 때 모두 다시 불러옵니다.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3303"/>
        <source>Settings saved.</source>
        <translation>설정을 저장했습니다.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3342"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>사용자에게 {action} 권한이 없습니다. 클러스터 관리자에게 접근 권한을 요청하세요.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3347"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>사용자에게 이 작업을 수행할 권한이 없습니다. 클러스터 관리자에게 접근 권한을 요청하세요.</translation>
    </message>
    <message>
        <location filename="../window.py" line="3366"/>
        <source>Query failed</source>
        <translation>쿼리에 실패했습니다</translation>
    </message>
</context>
<context>
    <name>WorkloadsOverviewPage</name>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="29"/>
        <source>Workloads</source>
        <translation>워크로드</translation>
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
        <translation>이벤트</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="293"/>
        <source>TYPE</source>
        <translation>유형</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="298"/>
        <source>SOURCE</source>
        <translation>출처</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="303"/>
        <source>NAMESPACE</source>
        <translation>네임스페이스</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="308"/>
        <source>INVOLVED OBJECT</source>
        <translation>관련 객체</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="313"/>
        <source>MESSAGE</source>
        <translation>메시지</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="318"/>
        <source>COUNT</source>
        <translation>횟수</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="323"/>
        <source>AGE</source>
        <translation>경과</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="328"/>
        <source>LAST SEEN</source>
        <translation>마지막 발생</translation>
    </message>
</context>
</TS>
