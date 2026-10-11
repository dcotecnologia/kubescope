<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ja">
<context>
    <name>Errors</name>
    <message>
        <location filename="../errors.py" line="71"/>
        <source>Login tool not found</source>
        <translation>ログインツールが見つかりません</translation>
    </message>
    <message>
        <location filename="../errors.py" line="72"/>
        <source>Your kubeconfig runs “{tool}” to sign in, but it is not installed or not on the PATH. Install it and refresh.</source>
        <translation>kubeconfig はサインインに「{tool}」を実行しますが、インストールされていないか PATH にありません。インストールしてから更新してください。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="81"/>
        <source>Context not found</source>
        <translation>コンテキストが見つかりません</translation>
    </message>
    <message>
        <location filename="../errors.py" line="82"/>
        <source>This context is not in your kubeconfig. Check ~/.kube/config.</source>
        <translation>このコンテキストは kubeconfig にありません。~/.kube/config を確認してください。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="90"/>
        <source>Authentication failed</source>
        <translation>認証に失敗しました</translation>
    </message>
    <message>
        <location filename="../errors.py" line="91"/>
        <source>Your credentials may have expired. Sign in again (for example “aws sso login”, “gcloud auth login” or “az login”) and refresh.</source>
        <translation>認証情報の有効期限が切れた可能性があります。もう一度サインインして（例：「aws sso login」「gcloud auth login」「az login」）、更新してください。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="100"/>
        <source>Access denied</source>
        <translation>アクセスが拒否されました</translation>
    </message>
    <message>
        <location filename="../errors.py" line="101"/>
        <source>Your user is not allowed to read this resource.</source>
        <translation>このユーザーにはこのリソースを読み取る権限がありません。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="122"/>
        <source>Cluster unreachable</source>
        <translation>クラスターに接続できません</translation>
    </message>
    <message>
        <location filename="../errors.py" line="123"/>
        <source>Check your network or VPN and that the cluster is running.</source>
        <translation>ネットワークまたは VPN と、クラスターが稼働していることを確認してください。</translation>
    </message>
    <message>
        <location filename="../errors.py" line="129"/>
        <source>Something went wrong</source>
        <translation>問題が発生しました</translation>
    </message>
</context>
<context>
    <name>LogTab</name>
    <message>
        <location filename="../log_tab.py" line="42"/>
        <source>No log lines returned.</source>
        <translation>ログ行が返されませんでした。</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="47"/>
        <source>Updated at {time}</source>
        <translation>{time} に更新</translation>
    </message>
    <message>
        <location filename="../log_tab.py" line="54"/>
        <source>Could not refresh logs: {message}</source>
        <translation>ログを更新できませんでした：{message}</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="29"/>
        <source>Auto-refresh</source>
        <translation>自動更新</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="32"/>
        <source>Fetch new log lines every few seconds and follow the end of the log</source>
        <translation>数秒ごとに新しいログ行を取得し、ログの末尾を追従します</translation>
    </message>
    <message>
        <location filename="../ui/log_tab.ui" line="42"/>
        <source>Refresh now</source>
        <translation>今すぐ更新</translation>
    </message>
</context>
<context>
    <name>MainWindow</name>
    <message>
        <location filename="../window.py" line="1141"/>
        <source>TYPE</source>
        <translation>タイプ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1142"/>
        <source>CLUSTER IP</source>
        <translation>クラスター IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1143"/>
        <source>EXTERNAL IP</source>
        <translation>外部 IP</translation>
    </message>
    <message>
        <location filename="../window.py" line="1144"/>
        <location filename="../window.py" line="1148"/>
        <location filename="../window.py" line="1156"/>
        <source>PORTS</source>
        <translation>ポート</translation>
    </message>
    <message>
        <location filename="../window.py" line="1147"/>
        <source>ADDRESS TYPE</source>
        <translation>アドレスタイプ</translation>
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
        <translation>クラス</translation>
    </message>
    <message>
        <location filename="../window.py" line="1154"/>
        <source>HOSTS</source>
        <translation>ホスト</translation>
    </message>
    <message>
        <location filename="../window.py" line="1155"/>
        <source>ADDRESS</source>
        <translation>アドレス</translation>
    </message>
    <message>
        <location filename="../window.py" line="1159"/>
        <source>CONTROLLER</source>
        <translation>コントローラー</translation>
    </message>
    <message>
        <location filename="../window.py" line="1160"/>
        <source>PARAMETERS</source>
        <translation>パラメーター</translation>
    </message>
    <message>
        <location filename="../window.py" line="1163"/>
        <source>POD SELECTOR</source>
        <translation>POD セレクター</translation>
    </message>
    <message>
        <location filename="../window.py" line="1164"/>
        <source>POLICY TYPES</source>
        <translation>ポリシータイプ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1174"/>
        <source>COMPLETIONS</source>
        <translation>完了数</translation>
    </message>
    <message>
        <location filename="../window.py" line="1175"/>
        <source>SCHEDULE</source>
        <translation>スケジュール</translation>
    </message>
    <message>
        <location filename="../window.py" line="1176"/>
        <location filename="../ui/main_window.ui" line="1519"/>
        <source>READY</source>
        <translation>準備完了</translation>
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
        <translation>名前</translation>
    </message>
    <message>
        <location filename="../window.py" line="1185"/>
        <location filename="../ui/main_window.ui" line="1524"/>
        <source>STATUS</source>
        <translation>ステータス</translation>
    </message>
    <message>
        <location filename="../window.py" line="1186"/>
        <source>CPU</source>
        <translation>CPU</translation>
    </message>
    <message>
        <location filename="../window.py" line="1187"/>
        <source>MEMORY</source>
        <translation>メモリ</translation>
    </message>
    <message>
        <location filename="../window.py" line="1188"/>
        <source>RESTARTS</source>
        <translation>再起動</translation>
    </message>
    <message>
        <location filename="../window.py" line="1189"/>
        <location filename="../window.py" line="1201"/>
        <location filename="../ui/main_window.ui" line="1529"/>
        <source>AGE</source>
        <translation>経過時間</translation>
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
        <translation>Kubernetes コンソール</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="307"/>
        <source>CONTEXT</source>
        <translation>コンテキスト</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="320"/>
        <source>Kubernetes context from your kubeconfig</source>
        <translation>kubeconfig の Kubernetes コンテキスト</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="340"/>
        <source>Sign in with the cloud CLI, then reload the cluster data</source>
        <translation>クラウド CLI でサインインしてから、クラスターのデータを再読み込みします</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="343"/>
        <source>Sign in</source>
        <translation>サインイン</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="365"/>
        <source>Settings</source>
        <translation>設定</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="405"/>
        <source>No cluster contexts were found in your kubeconfig. Add a cluster to your kubeconfig (for example with the AWS CLI: aws eks update-kubeconfig) and reload.</source>
        <translation>kubeconfig にクラスターのコンテキストが見つかりません。kubeconfig にクラスターを追加して（例：AWS CLI の aws eks update-kubeconfig）、再読み込みしてください。</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="446"/>
        <source>Dismiss</source>
        <translation>閉じる</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="537"/>
        <source>MONITORING</source>
        <translation>モニタリング</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="544"/>
        <location filename="../ui/main_window.ui" line="627"/>
        <location filename="../ui/main_window.ui" line="1255"/>
        <source>Overview</source>
        <translation>概要</translation>
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
        <translation>ネットワーク</translation>
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
        <translation>詳細とログ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1206"/>
        <source>SECURE ACCESS
Resources in read-only mode</source>
        <translation>安全なアクセス
リソースは読み取り専用モードです</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1262"/>
        <source>Cluster resources and capacity</source>
        <translation>クラスターのリソースと容量</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1367"/>
        <source>Search by name or namespace...</source>
        <translation>名前または namespace で検索...</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1390"/>
        <source>Refresh</source>
        <translation>更新</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1430"/>
        <source>View Pods of the selected workload</source>
        <translation>選択した workload の Pods を表示</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1446"/>
        <source>View JSON details of the selected workload</source>
        <translation>選択した workload の JSON 詳細を表示</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1449"/>
        <source>Details</source>
        <translation>詳細</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1462"/>
        <source>View logs of a Pod of the selected workload</source>
        <translation>選択した workload の Pod のログを表示</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="1465"/>
        <source>Logs</source>
        <translation>ログ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2007"/>
        <source>Select a context to load workloads</source>
        <translation>コンテキストを選択して workloads を読み込みます</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2030"/>
        <source>Data fetched from the cluster API</source>
        <translation>クラスター API から取得したデータ</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2091"/>
        <source>Open the DCO Tecnologia website</source>
        <translation>DCO Tecnologia のウェブサイトを開く</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2111"/>
        <source>MIT License</source>
        <translation>MIT ライセンス</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2114"/>
        <source>KubeScope is open source software released under the MIT License</source>
        <translation>KubeScope は MIT ライセンスで公開されているオープンソースソフトウェアです</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2150"/>
        <source>Update available</source>
        <translation>アップデートあり</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2153"/>
        <source>Open the download page of the new version</source>
        <translation>新しいバージョンのダウンロードページを開く</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2181"/>
        <source>Check for updates</source>
        <translation>アップデートを確認</translation>
    </message>
    <message>
        <location filename="../ui/main_window.ui" line="2201"/>
        <source>Open the project on GitHub</source>
        <translation>GitHub でプロジェクトを開く</translation>
    </message>
</context>
<context>
    <name>OverviewPage</name>
    <message>
        <location filename="../window.py" line="1564"/>
        <location filename="../ui/overview_page.ui" line="113"/>
        <source>nodes ready</source>
        <translation>ノード準備完了</translation>
    </message>
    <message>
        <location filename="../window.py" line="1580"/>
        <location filename="../ui/overview_page.ui" line="234"/>
        <source>cores requested / allocatable</source>
        <translation>要求 / 割り当て可能なコア数</translation>
    </message>
    <message>
        <location filename="../window.py" line="1594"/>
        <location filename="../ui/overview_page.ui" line="301"/>
        <source>requested / allocatable</source>
        <translation>要求 / 割り当て可能</translation>
    </message>
    <message>
        <location filename="../window.py" line="1613"/>
        <location filename="../ui/overview_page.ui" line="375"/>
        <source>in the cluster</source>
        <translation>クラスター内</translation>
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
        <translation>クラスターのリソース</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="52"/>
        <source>Refresh</source>
        <translation>更新</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="93"/>
        <source>NODES</source>
        <translation>ノード</translation>
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
        <translation>実行中 / 容量</translation>
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
        <translation>メモリ</translation>
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
        <translation>ノード</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="584"/>
        <source>NODE</source>
        <translation>ノード</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="589"/>
        <source>STATUS</source>
        <translation>ステータス</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="594"/>
        <source>ROLE</source>
        <translation>ロール</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="599"/>
        <source>VERSION</source>
        <translation>バージョン</translation>
    </message>
    <message>
        <location filename="../ui/overview_page.ui" line="619"/>
        <source>AGE</source>
        <translation>経過時間</translation>
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
        <translation>名前</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="46"/>
        <source>READY</source>
        <translation>準備完了</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="51"/>
        <source>PHASE</source>
        <translation>フェーズ</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="56"/>
        <source>CONTAINERS</source>
        <translation>コンテナー</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="61"/>
        <source>AGE</source>
        <translation>経過時間</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="216"/>
        <source>Pod details</source>
        <translation>Pod の詳細</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="226"/>
        <source>View logs</source>
        <translation>ログを表示</translation>
    </message>
    <message>
        <location filename="../ui/pods_dialog.ui" line="249"/>
        <source>Close</source>
        <translation>閉じる</translation>
    </message>
</context>
<context>
    <name>SettingsPage</name>
    <message>
        <location filename="../window.py" line="2528"/>
        <location filename="../ui/settings_page.ui" line="514"/>
        <source>Give your contexts friendlier names. Leave a name empty to keep the original one.</source>
        <translation>コンテキストに分かりやすい名前を付けます。名前を空にすると元の名前のままになります。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="34"/>
        <source>Save changes</source>
        <translation>変更を保存</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="86"/>
        <source>GENERAL</source>
        <translation>一般</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="107"/>
        <source>Language</source>
        <translation>言語</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="142"/>
        <source>Theme</source>
        <translation>テーマ</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="177"/>
        <source>New theme...</source>
        <translation>新しいテーマ...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="187"/>
        <source>Edit theme...</source>
        <translation>テーマを編集...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="197"/>
        <source>Open the themes folder</source>
        <translation>テーマフォルダーを開く</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="222"/>
        <source>Default namespace</source>
        <translation>デフォルトの namespace</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="235"/>
        <source>The namespace each context opens on. Leave empty to show all of them.</source>
        <translation>各コンテキストを開く namespace。空にするとすべて表示します。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="242"/>
        <source>Remember the last used context</source>
        <translation>最後に使ったコンテキストを記憶する</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="252"/>
        <source>Check GitHub for a new version when the app starts</source>
        <translation>アプリの起動時に GitHub で新しいバージョンを確認する</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="255"/>
        <source>Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.</source>
        <translation>GitHub の公開 API に最新リリースを問い合わせ、アプリのバージョン以外は何も送信しません。フッターのアイコンでいつでも確認できます。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="265"/>
        <source>Debug mode: write a log file I can share</source>
        <translation>デバッグモード：共有できるログファイルを書き込む</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="290"/>
        <source>Open the log folder</source>
        <translation>ログフォルダーを開く</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="300"/>
        <source>Clear the cache</source>
        <translation>キャッシュを消去</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="303"/>
        <source>Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.</source>
        <translation>読み込み済みの一覧と概要、および各クラスターのサインイン情報を破棄します。次のリクエストで再度サインインし、すべてを読み込み直します。設定は保持されます。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="330"/>
        <source>KUBECONFIG FILES</source>
        <translation>KUBECONFIG ファイル</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="343"/>
        <source>KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.</source>
        <translation>KubeScope は KUBECONFIG 変数のファイル、または ~/.kube/config を読み込みます。ここにファイルを追加すると、代わりにそれらを読み込みます。「保存」を押して適用します。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="371"/>
        <source>Add file...</source>
        <translation>ファイルを追加...</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="381"/>
        <location filename="../ui/settings_page.ui" line="479"/>
        <source>Remove</source>
        <translation>削除</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="406"/>
        <source>SIGN-IN COMMANDS</source>
        <translation>サインインコマンド</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="419"/>
        <source>For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.</source>
        <translation>KubeScope が知らないクラウドの場合は、kubeconfig がサインインに使うプログラム（例：oci）と、サインインするコマンド（例：oci session authenticate）を指定します。「サインイン」ボタンがシェルを使わずに実行します。「保存」を押して適用します。</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="451"/>
        <source>PROGRAM</source>
        <translation>プログラム</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="456"/>
        <source>SIGN-IN COMMAND</source>
        <translation>サインインコマンド</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="469"/>
        <source>Add row</source>
        <translation>行を追加</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="504"/>
        <source>CONTEXT NAMES</source>
        <translation>コンテキスト名</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="549"/>
        <source>CONTEXT</source>
        <translation>コンテキスト</translation>
    </message>
    <message>
        <location filename="../ui/settings_page.ui" line="554"/>
        <source>DISPLAY NAME</source>
        <translation>表示名</translation>
    </message>
</context>
<context>
    <name>ThemeEditor</name>
    <message>
        <location filename="../theme_editor.py" line="25"/>
        <source>Page background</source>
        <translation>ページの背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="26"/>
        <source>Panels and cards</source>
        <translation>パネルとカード</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="27"/>
        <source>Alternate panels</source>
        <translation>交互のパネル</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="28"/>
        <source>Bar tracks</source>
        <translation>バーのトラック</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="29"/>
        <source>Borders</source>
        <translation>枠線</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="30"/>
        <source>Top bar</source>
        <translation>トップバー</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="31"/>
        <source>Top bar logo</source>
        <translation>トップバーのロゴ</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="32"/>
        <source>Top bar selector</source>
        <translation>トップバーのセレクター</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="33"/>
        <source>Top bar selector border</source>
        <translation>トップバーのセレクターの枠線</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="36"/>
        <source>Top bar selection</source>
        <translation>トップバーの選択</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="39"/>
        <source>Top bar text</source>
        <translation>トップバーの文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="40"/>
        <source>Text</source>
        <translation>文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="41"/>
        <source>Sidebar title</source>
        <translation>サイドバーのタイトル</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="42"/>
        <source>Secondary text</source>
        <translation>補助的な文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="43"/>
        <source>Disabled text</source>
        <translation>無効時の文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="44"/>
        <source>Accent text and links</source>
        <translation>アクセントの文字とリンク</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="45"/>
        <source>Accent buttons</source>
        <translation>アクセントのボタン</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="46"/>
        <source>Accent buttons on hover</source>
        <translation>ホバー時のアクセントのボタン</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="49"/>
        <source>Accent buttons when disabled</source>
        <translation>無効時のアクセントのボタン</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="52"/>
        <source>Focus and highlights</source>
        <translation>フォーカスとハイライト</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="53"/>
        <source>Badge text</source>
        <translation>バッジの文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="54"/>
        <source>Accent tint</source>
        <translation>アクセントの色合い</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="55"/>
        <source>Text selection</source>
        <translation>文字の選択</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="56"/>
        <source>Accent border</source>
        <translation>アクセントの枠線</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="57"/>
        <source>Text on the top bar and accent buttons</source>
        <translation>トップバーとアクセントのボタン上の文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="60"/>
        <source>Healthy text</source>
        <translation>正常の文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="61"/>
        <source>Healthy background</source>
        <translation>正常の背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="62"/>
        <source>Warning text</source>
        <translation>警告の文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="63"/>
        <source>Warning background</source>
        <translation>警告の背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="64"/>
        <source>Failing text</source>
        <translation>失敗の文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="65"/>
        <source>Failing background</source>
        <translation>失敗の背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="66"/>
        <source>Idle text</source>
        <translation>アイドルの文字</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="67"/>
        <source>Idle background</source>
        <translation>アイドルの背景</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="68"/>
        <source>Row with a problem</source>
        <translation>問題のある行</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="69"/>
        <source>Row of a young Pod</source>
        <translation>新しい Pod の行</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="70"/>
        <source>Usage bar, getting full</source>
        <translation>使用量バー（満杯に近づいている）</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="73"/>
        <source>Usage bar, nearly full</source>
        <translation>使用量バー（ほぼ満杯）</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="76"/>
        <source>Health bar, healthy</source>
        <translation>ヘルスバー（正常）</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="77"/>
        <source>Health bar, warning</source>
        <translation>ヘルスバー（警告）</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="78"/>
        <source>Health bar, failing</source>
        <translation>ヘルスバー（失敗）</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="100"/>
        <source>New theme</source>
        <translation>新しいテーマ</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="102"/>
        <source>Edit theme: {name}</source>
        <translation>テーマを編集：{name}</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="109"/>
        <source>Theme name</source>
        <translation>テーマ名</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="111"/>
        <source>Light</source>
        <translation>ライト</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="112"/>
        <source>Dark</source>
        <translation>ダーク</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="119"/>
        <source>Name</source>
        <translation>名前</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="120"/>
        <source>Starts from</source>
        <translation>ベース</translation>
    </message>
    <message>
        <location filename="../theme_editor.py" line="146"/>
        <source>Colors</source>
        <translation>色</translation>
    </message>
</context>
<context>
    <name>ViewerPage</name>
    <message>
        <location filename="../ui/viewer_page.ui" line="94"/>
        <source>Save what this tab shows to a file</source>
        <translation>このタブの内容をファイルに保存します</translation>
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
        <translation>すべての namespaces</translation>
    </message>
    <message>
        <location filename="../window.py" line="766"/>
        <source>Loading contexts...</source>
        <translation>コンテキストを読み込み中...</translation>
    </message>
    <message>
        <location filename="../window.py" line="775"/>
        <source>Could not load kubeconfig: {error}</source>
        <translation>kubeconfig を読み込めませんでした：{error}</translation>
    </message>
    <message>
        <location filename="../window.py" line="797"/>
        <source>No contexts found in kubeconfig</source>
        <translation>kubeconfig にコンテキストが見つかりません</translation>
    </message>
    <message>
        <location filename="../window.py" line="864"/>
        <source>Overview</source>
        <translation>概要</translation>
    </message>
    <message>
        <location filename="../window.py" line="865"/>
        <source>Cluster resources and capacity</source>
        <translation>クラスターのリソースと容量</translation>
    </message>
    <message>
        <location filename="../window.py" line="867"/>
        <source>Details &amp; Logs</source>
        <translation>詳細とログ</translation>
    </message>
    <message>
        <location filename="../window.py" line="869"/>
        <source>Resource details and Pod logs, one tab each</source>
        <translation>リソースの詳細と Pod のログ（それぞれ別のタブ）</translation>
    </message>
    <message>
        <location filename="../window.py" line="872"/>
        <source>Settings</source>
        <translation>設定</translation>
    </message>
    <message>
        <location filename="../window.py" line="873"/>
        <source>Preferences and context names</source>
        <translation>設定とコンテキスト名</translation>
    </message>
    <message>
        <location filename="../window.py" line="875"/>
        <source>Workloads overview</source>
        <translation>Workloads の概要</translation>
    </message>
    <message>
        <location filename="../window.py" line="877"/>
        <source>Health of every workload kind and the latest events</source>
        <translation>各 workload の種類ごとの状態と最新のイベント</translation>
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
        <translation>クラスターの Pods</translation>
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
        <translation>クラスターの Deployments</translation>
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
        <translation>クラスターの StatefulSets</translation>
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
        <translation>クラスターの DaemonSets</translation>
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
        <translation>クラスターの ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="899"/>
        <source>ReplicationControllers</source>
        <translation>ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="900"/>
        <source>ReplicationControllers of the cluster</source>
        <translation>クラスターの ReplicationControllers</translation>
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
        <translation>クラスターの Jobs</translation>
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
        <translation>クラスターの CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="904"/>
        <source>Services</source>
        <translation>Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="904"/>
        <source>Services of the cluster</source>
        <translation>クラスターの Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="906"/>
        <source>Endpoint Slices</source>
        <translation>Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="907"/>
        <source>Endpoint Slices of the cluster</source>
        <translation>クラスターの Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="910"/>
        <source>Endpoints</source>
        <translation>Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="911"/>
        <source>Endpoints of the cluster</source>
        <translation>クラスターの Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="914"/>
        <source>Ingresses</source>
        <translation>Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="915"/>
        <source>Ingresses of the cluster</source>
        <translation>クラスターの Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="918"/>
        <source>Ingress Classes</source>
        <translation>Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="919"/>
        <source>Ingress Classes of the cluster</source>
        <translation>クラスターの Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="922"/>
        <source>Network Policies</source>
        <translation>Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="923"/>
        <source>Network Policies of the cluster</source>
        <translation>クラスターの Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="932"/>
        <source>Version {version}</source>
        <translation>バージョン {version}</translation>
    </message>
    <message>
        <location filename="../window.py" line="935"/>
        <source>Open the project on GitHub</source>
        <translation>GitHub でプロジェクトを開く</translation>
    </message>
    <message>
        <location filename="../window.py" line="969"/>
        <source>Up to date</source>
        <translation>最新です</translation>
    </message>
    <message>
        <location filename="../window.py" line="970"/>
        <source>Could not check</source>
        <translation>確認できませんでした</translation>
    </message>
    <message>
        <location filename="../window.py" line="981"/>
        <source>Check for updates</source>
        <translation>アップデートを確認</translation>
    </message>
    <message>
        <location filename="../window.py" line="982"/>
        <source>Checking for updates...</source>
        <translation>アップデートを確認中...</translation>
    </message>
    <message>
        <location filename="../window.py" line="983"/>
        <source>KubeScope is up to date. Click to check again.</source>
        <translation>KubeScope は最新です。クリックすると再確認します。</translation>
    </message>
    <message>
        <location filename="../window.py" line="984"/>
        <source>Could not check for updates. Click to try again.</source>
        <translation>アップデートを確認できませんでした。クリックして再試行します。</translation>
    </message>
    <message>
        <location filename="../window.py" line="990"/>
        <source>Update available: {version}. Click to open the download page; right-click to check again.</source>
        <translation>アップデートがあります：{version}。クリックでダウンロードページを開きます。右クリックで再確認します。</translation>
    </message>
    <message>
        <location filename="../window.py" line="998"/>
        <source>Update available</source>
        <translation>アップデートあり</translation>
    </message>
    <message>
        <location filename="../window.py" line="1000"/>
        <source>Download KubeScope {version}</source>
        <translation>KubeScope {version} をダウンロード</translation>
    </message>
    <message>
        <location filename="../window.py" line="1036"/>
        <source>Check for updates again</source>
        <translation>もう一度アップデートを確認</translation>
    </message>
    <message>
        <location filename="../window.py" line="1132"/>
        <location filename="../window.py" line="1724"/>
        <source>Loading resources...</source>
        <translation>リソースを読み込み中...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1309"/>
        <source>Configure AWS credentials ({profile})</source>
        <translation>AWS 認証情報を設定（{profile}）</translation>
    </message>
    <message>
        <location filename="../window.py" line="1313"/>
        <source>AWS credentials for profile {profile} are missing or invalid</source>
        <translation>プロファイル {profile} の AWS 認証情報がないか無効です</translation>
    </message>
    <message>
        <location filename="../window.py" line="1318"/>
        <source>Sign in to {provider}</source>
        <translation>{provider} にサインイン</translation>
    </message>
    <message>
        <location filename="../window.py" line="1321"/>
        <source>Not signed in to {provider}</source>
        <translation>{provider} にサインインしていません</translation>
    </message>
    <message>
        <location filename="../window.py" line="1325"/>
        <source>Sign in to {provider} ({profile})</source>
        <translation>{provider} にサインイン（{profile}）</translation>
    </message>
    <message>
        <location filename="../window.py" line="1331"/>
        <source>Not signed in to {provider} (profile {profile})</source>
        <translation>{provider} にサインインしていません（プロファイル {profile}）</translation>
    </message>
    <message>
        <location filename="../window.py" line="1352"/>
        <source>Finish in the terminal that opened, then press Refresh.</source>
        <translation>開いたターミナルで完了してから、「更新」を押してください。</translation>
    </message>
    <message>
        <location filename="../window.py" line="1371"/>
        <source>Loading workloads...</source>
        <translation>workloads を読み込み中...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1432"/>
        <source>Could not read: {names}</source>
        <translation>読み取れませんでした：{names}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1492"/>
        <source>Loading cluster data...</source>
        <translation>クラスターのデータを読み込み中...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1573"/>
        <source>running · {pending} pending · {failed} failed</source>
        <translation>実行中 · 保留 {pending} · 失敗 {failed}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1582"/>
        <location filename="../window.py" line="1596"/>
        <source> · usage {value}</source>
        <translation> · 使用量 {value}</translation>
    </message>
    <message>
        <location filename="../window.py" line="1622"/>
        <source>Ready</source>
        <translation>準備完了</translation>
    </message>
    <message>
        <location filename="../window.py" line="1622"/>
        <source>Not ready</source>
        <translation>準備未完了</translation>
    </message>
    <message>
        <location filename="../window.py" line="1647"/>
        <source>Real usage unavailable: metrics-server not found.</source>
        <translation>実際の使用量を取得できません：metrics-server が見つかりません。</translation>
    </message>
    <message>
        <location filename="../window.py" line="1741"/>
        <source>Refreshing...</source>
        <translation>更新中...</translation>
    </message>
    <message>
        <location filename="../window.py" line="1926"/>
        <source>{count} Services in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="1928"/>
        <source>{count} Endpoint Slices in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="1931"/>
        <source>{count} Endpoints in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="1934"/>
        <source>{count} Ingresses in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="1936"/>
        <source>{count} Ingress Classes in the cluster</source>
        <translation>クラスターに {count} 個の Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="1938"/>
        <source>{count} Network Policies in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="1950"/>
        <location filename="../window.py" line="2016"/>
        <source>Running</source>
        <translation>実行中</translation>
    </message>
    <message>
        <location filename="../window.py" line="1951"/>
        <location filename="../window.py" line="2012"/>
        <source>Pending</source>
        <translation>保留中</translation>
    </message>
    <message>
        <location filename="../window.py" line="1952"/>
        <source>Succeeded</source>
        <translation>成功</translation>
    </message>
    <message>
        <location filename="../window.py" line="1953"/>
        <location filename="../window.py" line="2011"/>
        <source>Failed</source>
        <translation>失敗</translation>
    </message>
    <message>
        <location filename="../window.py" line="1954"/>
        <source>Unknown</source>
        <translation>不明</translation>
    </message>
    <message>
        <location filename="../window.py" line="1998"/>
        <source>{count} Pods in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2006"/>
        <source>Healthy</source>
        <translation>正常</translation>
    </message>
    <message>
        <location filename="../window.py" line="2007"/>
        <source>Degraded</source>
        <translation>低下</translation>
    </message>
    <message>
        <location filename="../window.py" line="2008"/>
        <source>Unavailable</source>
        <translation>利用不可</translation>
    </message>
    <message>
        <location filename="../window.py" line="2009"/>
        <source>Scaled to zero</source>
        <translation>ゼロにスケール済み</translation>
    </message>
    <message>
        <location filename="../window.py" line="2010"/>
        <source>Complete</source>
        <translation>完了</translation>
    </message>
    <message>
        <location filename="../window.py" line="2013"/>
        <source>Suspended</source>
        <translation>一時停止中</translation>
    </message>
    <message>
        <location filename="../window.py" line="2014"/>
        <source>Active</source>
        <translation>アクティブ</translation>
    </message>
    <message>
        <location filename="../window.py" line="2015"/>
        <source>Scheduled</source>
        <translation>スケジュール済み</translation>
    </message>
    <message>
        <location filename="../window.py" line="2060"/>
        <source>{count} Deployments in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2063"/>
        <source>{count} StatefulSets in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2066"/>
        <source>{count} DaemonSets in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2069"/>
        <source>{count} ReplicaSets in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2072"/>
        <source>{count} ReplicationControllers in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2074"/>
        <source>{count} Jobs in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2075"/>
        <source>{count} CronJobs in {namespaces} namespaces</source>
        <translation>{namespaces} 個の namespaces に {count} 個の CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2095"/>
        <source>{visible} of {total} Pods</source>
        <translation>{total} 個中 {visible} 個の Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2096"/>
        <source>{visible} of {total} Deployments</source>
        <translation>{total} 個中 {visible} 個の Deployments</translation>
    </message>
    <message>
        <location filename="../window.py" line="2097"/>
        <source>{visible} of {total} StatefulSets</source>
        <translation>{total} 個中 {visible} 個の StatefulSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2098"/>
        <source>{visible} of {total} DaemonSets</source>
        <translation>{total} 個中 {visible} 個の DaemonSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2099"/>
        <source>{visible} of {total} ReplicaSets</source>
        <translation>{total} 個中 {visible} 個の ReplicaSets</translation>
    </message>
    <message>
        <location filename="../window.py" line="2101"/>
        <source>{visible} of {total} ReplicationControllers</source>
        <translation>{total} 個中 {visible} 個の ReplicationControllers</translation>
    </message>
    <message>
        <location filename="../window.py" line="2103"/>
        <source>{visible} of {total} Jobs</source>
        <translation>{total} 個中 {visible} 個の Jobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2104"/>
        <source>{visible} of {total} CronJobs</source>
        <translation>{total} 個中 {visible} 個の CronJobs</translation>
    </message>
    <message>
        <location filename="../window.py" line="2105"/>
        <source>{visible} of {total} Services</source>
        <translation>{total} 個中 {visible} 個の Services</translation>
    </message>
    <message>
        <location filename="../window.py" line="2106"/>
        <source>{visible} of {total} Endpoint Slices</source>
        <translation>{total} 個中 {visible} 個の Endpoint Slices</translation>
    </message>
    <message>
        <location filename="../window.py" line="2107"/>
        <source>{visible} of {total} Endpoints</source>
        <translation>{total} 個中 {visible} 個の Endpoints</translation>
    </message>
    <message>
        <location filename="../window.py" line="2108"/>
        <source>{visible} of {total} Ingresses</source>
        <translation>{total} 個中 {visible} 個の Ingresses</translation>
    </message>
    <message>
        <location filename="../window.py" line="2109"/>
        <source>{visible} of {total} Ingress Classes</source>
        <translation>{total} 個中 {visible} 個の Ingress Classes</translation>
    </message>
    <message>
        <location filename="../window.py" line="2110"/>
        <source>{visible} of {total} Network Policies</source>
        <translation>{total} 個中 {visible} 個の Network Policies</translation>
    </message>
    <message>
        <location filename="../window.py" line="2156"/>
        <source>Loading...</source>
        <translation>読み込み中...</translation>
    </message>
    <message>
        <location filename="../window.py" line="2202"/>
        <location filename="../window.py" line="2294"/>
        <source>Pod: {name}</source>
        <translation>Pod：{name}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2248"/>
        <source>Pods of {name}</source>
        <translation>{name} の Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2250"/>
        <source>{count} Pods in {namespace} / {name}</source>
        <translation>{namespace} / {name} に {count} 個の Pods</translation>
    </message>
    <message>
        <location filename="../window.py" line="2315"/>
        <source>No Pods are associated with this workload</source>
        <translation>この workload に関連付けられた Pod はありません</translation>
    </message>
    <message>
        <location filename="../window.py" line="2322"/>
        <location filename="../window.py" line="2345"/>
        <source>Logs</source>
        <translation>ログ</translation>
    </message>
    <message>
        <location filename="../window.py" line="2322"/>
        <source>This workload has no Pods.</source>
        <translation>この workload には Pod がありません。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2331"/>
        <location filename="../window.py" line="2354"/>
        <source>View logs</source>
        <translation>ログを表示</translation>
    </message>
    <message>
        <location filename="../window.py" line="2332"/>
        <source>Select the Pod:</source>
        <translation>Pod を選択：</translation>
    </message>
    <message>
        <location filename="../window.py" line="2346"/>
        <source>Pod {name} has no containers.</source>
        <translation>Pod {name} にはコンテナーがありません。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2355"/>
        <source>Select the container of {name}:</source>
        <translation>{name} のコンテナーを選択：</translation>
    </message>
    <message>
        <location filename="../window.py" line="2381"/>
        <source>Save to a file</source>
        <translation>ファイルに保存</translation>
    </message>
    <message>
        <location filename="../window.py" line="2392"/>
        <source>Could not save</source>
        <translation>保存できませんでした</translation>
    </message>
    <message>
        <location filename="../window.py" line="2393"/>
        <source>The file could not be written: {reason}</source>
        <translation>ファイルを書き込めませんでした：{reason}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2441"/>
        <source>Logs: {pod} / {container}</source>
        <translation>ログ：{pod} / {container}</translation>
    </message>
    <message>
        <location filename="../window.py" line="2491"/>
        <source>Automatic</source>
        <translation>自動</translation>
    </message>
    <message>
        <location filename="../window.py" line="2504"/>
        <source>Off by default. When on, KubeScope writes what it does, never Pod logs or resource contents, to {path}. Read it before sharing: it includes context names.</source>
        <translation>デフォルトではオフです。オンにすると、KubeScope は動作の記録を {path} に書き込みます。Pod のログやリソースの内容は書き込みません。共有する前に内容を確認してください。コンテキスト名が含まれます。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2535"/>
        <source>No contexts were found in kubeconfig.</source>
        <translation>kubeconfig にコンテキストが見つかりません。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2564"/>
        <source>Choose a kubeconfig file</source>
        <translation>kubeconfig ファイルを選択</translation>
    </message>
    <message>
        <location filename="../window.py" line="2610"/>
        <source>The sign-in command in row {row} is not valid.</source>
        <translation>{row} 行目のサインインコマンドが正しくありません。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2623"/>
        <source>Light</source>
        <translation>ライト</translation>
    </message>
    <message>
        <location filename="../window.py" line="2623"/>
        <source>Dark</source>
        <translation>ダーク</translation>
    </message>
    <message>
        <location filename="../window.py" line="2642"/>
        <source>My theme</source>
        <translation>マイテーマ</translation>
    </message>
    <message>
        <location filename="../window.py" line="2686"/>
        <source>Cache cleared. Everything loads again the next time it is needed.</source>
        <translation>キャッシュを消去しました。必要になったときに、すべて読み込み直します。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2741"/>
        <source>Settings saved.</source>
        <translation>設定を保存しました。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2778"/>
        <source>Your user is not allowed to {action}. Ask your cluster admin for access.</source>
        <translation>このユーザーには次の操作を行う権限がありません（{action}）。クラスター管理者にアクセスを依頼してください。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2783"/>
        <source>Your user is not allowed to do this. Ask your cluster admin for access.</source>
        <translation>このユーザーにはこの操作を行う権限がありません。クラスター管理者にアクセスを依頼してください。</translation>
    </message>
    <message>
        <location filename="../window.py" line="2802"/>
        <source>Query failed</source>
        <translation>クエリに失敗しました</translation>
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
        <translation>更新</translation>
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
        <translation>イベント</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="306"/>
        <source>TYPE</source>
        <translation>タイプ</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="311"/>
        <source>SOURCE</source>
        <translation>ソース</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="316"/>
        <source>NAMESPACE</source>
        <translation>NAMESPACE</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="321"/>
        <source>INVOLVED OBJECT</source>
        <translation>関連オブジェクト</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="326"/>
        <source>MESSAGE</source>
        <translation>メッセージ</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="331"/>
        <source>COUNT</source>
        <translation>回数</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="336"/>
        <source>AGE</source>
        <translation>経過時間</translation>
    </message>
    <message>
        <location filename="../ui/workloads_overview_page.ui" line="341"/>
        <source>LAST SEEN</source>
        <translation>最終確認</translation>
    </message>
</context>
</TS>
