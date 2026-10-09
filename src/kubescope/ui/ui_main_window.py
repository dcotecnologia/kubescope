# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(980, 640)
        MainWindow.setMinimumSize(QSize(980, 640))
        MainWindow.setStyleSheet(u"QMainWindow, QWidget#page { background: #f7f7fa; color: #20232a; }\n"
"QWidget#topBar { background: #06234a; }\n"
"QLabel#topBrand {\n"
"    color: #ffffff; font-size: 13px; font-weight: 700;\n"
"    padding: 0 12px; background: #123764; min-height: 46px;\n"
"}\n"
"QLabel#topCaption { color: #b8c7dc; font-size: 9px; font-weight: 700; }\n"
"QLabel#topAccess { color: #d2deec; font-size: 9px; font-weight: 700; }\n"
"QComboBox#contextCombo {\n"
"    background: #0d315d; color: #ffffff; border: 1px solid #2d5077;\n"
"    border-radius: 4px; min-height: 30px; padding: 0 9px; font-size: 11px;\n"
"}\n"
"QWidget#sidebar { background: #ffffff; border-right: 1px solid #e1e3e9; }\n"
"QLabel#sidebarBrand { color: #16375f; font-size: 19px; font-weight: 700; }\n"
"QLabel#sidebarSubtitle { color: #4f5966; font-size: 11px; }\n"
"QLabel#navSection, QLabel#filterLabel {\n"
"    color: #535d69; font-size: 9px; font-weight: 700;\n"
"}\n"
"QFrame#sidebarRule { color: #e6e7ed; }\n"
"QLabel#sidebarNote { color: #4d5866; font-size: 10"
                        "px; line-height: 1.4; }\n"
"QWidget#pageHeader { background: #ffffff; border-bottom: 1px solid #e4e5eb; }\n"
"QLabel#pageTitle { color: #17191e; font-size: 22px; font-weight: 700; }\n"
"QLabel[variant=\"muted\"] { color: #4f5966; font-size: 11px; }\n"
"QLabel#profileBadge {\n"
"    color: #4d35a8; background: #eee9f7; border-radius: 5px;\n"
"    font-size: 12px; font-weight: 700;\n"
"}\n"
"QComboBox[variant=\"filter\"], QLineEdit#searchInput, QPushButton[variant=\"primary\"] {\n"
"    background: #ffffff; border: 1px solid #d9dce4; border-radius: 5px;\n"
"    min-height: 36px; padding: 0 10px; font-size: 11px;\n"
"}\n"
"QComboBox[variant=\"filter\"], QLineEdit#searchInput {\n"
"    color: #20232a; selection-background-color: #d9d3f2;\n"
"    selection-color: #20232a;\n"
"}\n"
"QComboBox[variant=\"filter\"] { padding-right: 28px; }\n"
"QComboBox[variant=\"filter\"]:hover { border-color: #b9b3dc; }\n"
"QComboBox[variant=\"filter\"]:focus, QComboBox[variant=\"filter\"]:on,\n"
"QLineEdit#searchInput:focus { border"
                        ": 1px solid #6252b5; }\n"
"QComboBox[variant=\"filter\"]::drop-down {\n"
"    subcontrol-origin: padding; subcontrol-position: center right;\n"
"    width: 26px; border: 0; background: transparent;\n"
"}\n"
"QComboBox[variant=\"filter\"]::down-arrow {\n"
"    image: url(CHEVRON); width: 10px; height: 6px; margin-right: 8px;\n"
"}\n"
"QComboBox[variant=\"filter\"] QAbstractItemView {\n"
"    background: #ffffff; color: #20232a; border: 1px solid #d9dce4;\n"
"    selection-background-color: #eee9f7; selection-color: #3220a0;\n"
"    outline: 0; padding: 2px;\n"
"}\n"
"QComboBox[variant=\"filter\"]:disabled {\n"
"    color: #6b7380; background: #f3f4f7; border-color: #e4e5eb;\n"
"}\n"
"QComboBox#contextCombo:disabled { color: #ffffff; }\n"
"QComboBox#contextCombo { padding-right: 28px; }\n"
"QComboBox#contextCombo::drop-down {\n"
"    subcontrol-origin: padding; subcontrol-position: center right;\n"
"    width: 26px; border: 0; background: transparent;\n"
"}\n"
"QComboBox#contextCombo::down-arrow {\n"
"    image:"
                        " url(CHEVRON_LIGHT); width: 10px; height: 6px; margin-right: 8px;\n"
"}\n"
"QComboBox#contextCombo QAbstractItemView {\n"
"    background: #0d315d; color: #ffffff; border: 1px solid #2d5077;\n"
"    selection-background-color: #1f4f87; selection-color: #ffffff;\n"
"    outline: 0; padding: 2px;\n"
"}\n"
"QPushButton[variant=\"primary\"] {\n"
"    background: #3020a5; color: #ffffff; border: 0;\n"
"    font-weight: 700; padding: 0 16px;\n"
"}\n"
"QPushButton[variant=\"primary\"]:hover { background: #4030b8; }\n"
"QPushButton[variant=\"primary\"]:disabled { background: #6c5fc4; color: #ffffff; }\n"
"QPushButton[variant=\"link\"] {\n"
"  border: none; background: transparent; padding: 2px 0; text-align: left;\n"
"  color: #3220a0; font-weight: 600; text-decoration: underline;\n"
"}\n"
"QPushButton[variant=\"link\"]:hover { color: #4030b8; }\n"
"QPushButton[variant=\"link\"]:disabled { color: #4f5966; text-decoration: none; }\n"
"QPushButton[variant=\"secondary\"] {\n"
"    background: #ffffff; color: #3220a0; bor"
                        "der: 1px solid #d9dce4;\n"
"    border-radius: 5px; min-height: 32px; padding: 0 10px;\n"
"    font-size: 11px; font-weight: 600;\n"
"}\n"
"QPushButton[variant=\"secondary\"]:hover:enabled {\n"
"    background: #f3f1f9; border-color: #a9a0d6;\n"
"}\n"
"QPushButton[variant=\"secondary\"]:disabled { color: #7b8089; }\n"
"QLabel#summaryLabel { color: #4f5966; font-size: 11px; font-weight: 600; }\n"
"QTableWidget[variant=\"data\"] {\n"
"    background: #ffffff; color: #242a33;\n"
"    border: 1px solid #dfe2e9; border-radius: 5px;\n"
"    gridline-color: #e8e9ee; selection-background-color: #f0edfa;\n"
"    selection-color: #28213f;\n"
"}\n"
"QHeaderView { background: #fbfbfc; }\n"
"QHeaderView::up-arrow { image: url(SORT_UP); width: 9px; height: 6px; }\n"
"QHeaderView::down-arrow { image: url(SORT_DOWN); width: 9px; height: 6px; }\n"
"QHeaderView::section {\n"
"    background: #fbfbfc; color: #3c4149; border: 0;\n"
"    border-bottom: 1px solid #dfe2e9; padding: 10px 8px;\n"
"    font-size: 9px; font-weight: 700;"
                        "\n"
"}\n"
"QTableWidget[variant=\"data\"]::item {\n"
"    padding: 6px 8px; border-bottom: 1px solid #e8e9ee;\n"
"}\n"
"QPushButton[nav=\"true\"] {\n"
"    text-align: left; color: #4f5966; background: transparent;\n"
"    border: 0; border-right: 3px solid transparent; border-radius: 0;\n"
"    padding: 0 12px; font-size: 12px; font-weight: 600;\n"
"}\n"
"QPushButton[nav=\"true\"]:hover { background: #f6f6fa; }\n"
"QPushButton[nav=\"true\"]:checked {\n"
"    color: #3220a0; background: #f3f1f9; border-right: 3px solid #3220a0;\n"
"    font-weight: 700;\n"
"}\n"
"QFrame[card=\"true\"] {\n"
"    background: #ffffff; border: 1px solid #dfe2e9; border-radius: 8px;\n"
"}\n"
"QFrame[card=\"true\"] QLabel { background: transparent; border: 0; }\n"
"QLabel[variant=\"cardTitle\"] { color: #535d69; font-size: 9px; font-weight: 700; }\n"
"QLabel[variant=\"cardValue\"] { color: #17191e; font-size: 20px; font-weight: 700; }\n"
"QLabel[variant=\"cardCaption\"] { color: #4f5966; font-size: 10px; }\n"
"QProgressBar {\n"
"   "
                        " background: #eceef3; border: 0; border-radius: 3px;\n"
"    min-height: 6px; max-height: 6px;\n"
"}\n"
"QProgressBar::chunk { background: #6252b5; border-radius: 3px; }\n"
"QProgressBar[level=\"warn\"]::chunk { background: #d58a2b; }\n"
"QProgressBar[level=\"high\"]::chunk { background: #c9484f; }\n"
"QCheckBox { color: #20232a; spacing: 8px; font-size: 11px; }\n"
"QLabel { color: #20232a; }\n"
"QTabWidget::pane { border: 0; border-top: 1px solid #dfe2e9; top: -1px; }\n"
"QTabBar::tab {\n"
"    background: transparent; color: #4f5966; padding: 9px 14px;\n"
"    border: 0; border-bottom: 2px solid transparent; font-size: 11px;\n"
"    font-weight: 600; max-width: 260px;\n"
"}\n"
"QTabBar::tab:hover { color: #3220a0; }\n"
"QTabBar::tab:selected { color: #3220a0; border-bottom: 2px solid #3220a0; }\n"
"QTabBar::close-button {\n"
"    image: url(CLOSE_ICON); subcontrol-position: right; margin-left: 6px;\n"
"    width: 10px; height: 10px; padding: 3px; border-radius: 4px;\n"
"}\n"
"QTabBar::close-button:hover { im"
                        "age: url(CLOSE_ICON_HOVER); background: #eee9f7; }\n"
"QPlainTextEdit {\n"
"    background: #ffffff; color: #242a33; border: 1px solid #dfe2e9;\n"
"    border-radius: 5px; padding: 8px; selection-background-color: #d9d3f2;\n"
"    selection-color: #20232a;\n"
"}\n"
"QFrame#appFooter { background: #ffffff; border-top: 1px solid #e4e5eb; }\n"
"QLabel#footerLicense { color: #6b7380; font-size: 10px; }\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.topBar = QFrame(self.centralwidget)
        self.topBar.setObjectName(u"topBar")
        self.topBar.setMinimumSize(QSize(0, 46))
        self.topBar.setMaximumSize(QSize(16777215, 46))
        self.topLayout = QHBoxLayout(self.topBar)
        self.topLayout.setSpacing(12)
        self.topLayout.setObjectName(u"topLayout")
        self.topLayout.setContentsMargins(18, 0, 22, 0)
        self.topSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topLayout.addItem(self.topSpacer)

        self.topCaption = QLabel(self.topBar)
        self.topCaption.setObjectName(u"topCaption")

        self.topLayout.addWidget(self.topCaption)

        self.contextCombo = QComboBox(self.topBar)
        self.contextCombo.addItem(u"prod-eks")
        self.contextCombo.addItem(u"staging-eks")
        self.contextCombo.setObjectName(u"contextCombo")
        self.contextCombo.setMinimumSize(QSize(220, 32))

        self.topLayout.addWidget(self.contextCombo)

        self.loginButton = QPushButton(self.topBar)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setVisible(False)
        self.loginButton.setProperty(u"variant", u"primary")

        self.topLayout.addWidget(self.loginButton)

        self.topAccess = QLabel(self.topBar)
        self.topAccess.setObjectName(u"topAccess")

        self.topLayout.addWidget(self.topAccess)


        self.rootLayout.addWidget(self.topBar)

        self.shell = QHBoxLayout()
        self.shell.setSpacing(0)
        self.shell.setObjectName(u"shell")
        self.shell.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(252, 0))
        self.sidebar.setMaximumSize(QSize(252, 16777215))
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(8)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(24, 22, 18, 18)
        self.sidebarBrand = QLabel(self.sidebar)
        self.sidebarBrand.setObjectName(u"sidebarBrand")

        self.sidebarLayout.addWidget(self.sidebarBrand)

        self.sidebarSubtitle = QLabel(self.sidebar)
        self.sidebarSubtitle.setObjectName(u"sidebarSubtitle")

        self.sidebarLayout.addWidget(self.sidebarSubtitle)

        self.sidebarGap = QSpacerItem(20, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.sidebarGap)

        self.navSection = QLabel(self.sidebar)
        self.navSection.setObjectName(u"navSection")

        self.sidebarLayout.addWidget(self.navSection)

        self.navOverview = QPushButton(self.sidebar)
        self.navOverview.setObjectName(u"navOverview")
        self.navOverview.setMinimumSize(QSize(0, 42))
        self.navOverview.setIconSize(QSize(16, 16))
        self.navOverview.setCheckable(True)
        self.navOverview.setChecked(True)
        self.navOverview.setAutoExclusive(True)
        self.navOverview.setProperty(u"nav", u"true")

        self.sidebarLayout.addWidget(self.navOverview)

        self.navWorkloads = QPushButton(self.sidebar)
        self.navWorkloads.setObjectName(u"navWorkloads")
        self.navWorkloads.setMinimumSize(QSize(0, 42))
        self.navWorkloads.setIconSize(QSize(16, 16))
        self.navWorkloads.setCheckable(True)
        self.navWorkloads.setChecked(False)
        self.navWorkloads.setProperty(u"nav", u"true")

        self.sidebarLayout.addWidget(self.navWorkloads)

        self.workloadsSubmenu = QFrame(self.sidebar)
        self.workloadsSubmenu.setObjectName(u"workloadsSubmenu")
        self.workloadsSubmenu.setMaximumSize(QSize(16777215, 0))
        self.workloadsSubmenuLayout = QVBoxLayout(self.workloadsSubmenu)
        self.workloadsSubmenuLayout.setSpacing(0)
        self.workloadsSubmenuLayout.setObjectName(u"workloadsSubmenuLayout")
        self.workloadsSubmenuLayout.setContentsMargins(16, 0, 0, 0)
        self.navWorkloadsOverview = QPushButton(self.workloadsSubmenu)
        self.navWorkloadsOverview.setObjectName(u"navWorkloadsOverview")
        self.navWorkloadsOverview.setMinimumSize(QSize(0, 42))
        self.navWorkloadsOverview.setIconSize(QSize(16, 16))
        self.navWorkloadsOverview.setCheckable(True)
        self.navWorkloadsOverview.setChecked(False)
        self.navWorkloadsOverview.setAutoExclusive(True)
        self.navWorkloadsOverview.setProperty(u"nav", u"true")

        self.workloadsSubmenuLayout.addWidget(self.navWorkloadsOverview)

        self.navPods = QPushButton(self.workloadsSubmenu)
        self.navPods.setObjectName(u"navPods")
        self.navPods.setMinimumSize(QSize(0, 42))
        self.navPods.setIconSize(QSize(16, 16))
        self.navPods.setCheckable(True)
        self.navPods.setChecked(False)
        self.navPods.setAutoExclusive(True)
        self.navPods.setProperty(u"nav", u"true")

        self.workloadsSubmenuLayout.addWidget(self.navPods)

        self.navDeployments = QPushButton(self.workloadsSubmenu)
        self.navDeployments.setObjectName(u"navDeployments")
        self.navDeployments.setMinimumSize(QSize(0, 42))
        self.navDeployments.setIconSize(QSize(16, 16))
        self.navDeployments.setCheckable(True)
        self.navDeployments.setChecked(False)
        self.navDeployments.setAutoExclusive(True)
        self.navDeployments.setProperty(u"nav", u"true")

        self.workloadsSubmenuLayout.addWidget(self.navDeployments)

        self.navStatefulSets = QPushButton(self.workloadsSubmenu)
        self.navStatefulSets.setObjectName(u"navStatefulSets")
        self.navStatefulSets.setMinimumSize(QSize(0, 42))
        self.navStatefulSets.setIconSize(QSize(16, 16))
        self.navStatefulSets.setCheckable(True)
        self.navStatefulSets.setChecked(False)
        self.navStatefulSets.setAutoExclusive(True)
        self.navStatefulSets.setProperty(u"nav", u"true")

        self.workloadsSubmenuLayout.addWidget(self.navStatefulSets)

        self.navJobs = QPushButton(self.workloadsSubmenu)
        self.navJobs.setObjectName(u"navJobs")
        self.navJobs.setMinimumSize(QSize(0, 42))
        self.navJobs.setIconSize(QSize(16, 16))
        self.navJobs.setCheckable(True)
        self.navJobs.setChecked(False)
        self.navJobs.setAutoExclusive(True)
        self.navJobs.setProperty(u"nav", u"true")

        self.workloadsSubmenuLayout.addWidget(self.navJobs)

        self.navCronJobs = QPushButton(self.workloadsSubmenu)
        self.navCronJobs.setObjectName(u"navCronJobs")
        self.navCronJobs.setMinimumSize(QSize(0, 42))
        self.navCronJobs.setIconSize(QSize(16, 16))
        self.navCronJobs.setCheckable(True)
        self.navCronJobs.setChecked(False)
        self.navCronJobs.setAutoExclusive(True)
        self.navCronJobs.setProperty(u"nav", u"true")

        self.workloadsSubmenuLayout.addWidget(self.navCronJobs)


        self.sidebarLayout.addWidget(self.workloadsSubmenu)

        self.navViewer = QPushButton(self.sidebar)
        self.navViewer.setObjectName(u"navViewer")
        self.navViewer.setVisible(False)
        self.navViewer.setMinimumSize(QSize(0, 42))
        self.navViewer.setIconSize(QSize(16, 16))
        self.navViewer.setCheckable(True)
        self.navViewer.setAutoExclusive(True)
        self.navViewer.setProperty(u"nav", u"true")

        self.sidebarLayout.addWidget(self.navViewer)

        self.sidebarSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarSpacer)

        self.settingsButton = QPushButton(self.sidebar)
        self.settingsButton.setObjectName(u"settingsButton")
        self.settingsButton.setCheckable(True)
        self.settingsButton.setAutoExclusive(True)
        self.settingsButton.setMinimumSize(QSize(0, 42))
        self.settingsButton.setIconSize(QSize(16, 16))
        self.settingsButton.setProperty(u"nav", u"true")

        self.sidebarLayout.addWidget(self.settingsButton)

        self.sidebarRule = QFrame(self.sidebar)
        self.sidebarRule.setObjectName(u"sidebarRule")
        self.sidebarRule.setFrameShape(QFrame.Shape.HLine)

        self.sidebarLayout.addWidget(self.sidebarRule)

        self.sidebarNote = QLabel(self.sidebar)
        self.sidebarNote.setObjectName(u"sidebarNote")

        self.sidebarLayout.addWidget(self.sidebarNote)


        self.shell.addWidget(self.sidebar)

        self.page = QFrame(self.centralwidget)
        self.page.setObjectName(u"page")
        self.pageLayout = QVBoxLayout(self.page)
        self.pageLayout.setSpacing(0)
        self.pageLayout.setObjectName(u"pageLayout")
        self.pageLayout.setContentsMargins(0, 0, 0, 0)
        self.pageHeader = QFrame(self.page)
        self.pageHeader.setObjectName(u"pageHeader")
        self.pageHeaderLayout = QHBoxLayout(self.pageHeader)
        self.pageHeaderLayout.setObjectName(u"pageHeaderLayout")
        self.pageHeaderLayout.setContentsMargins(32, 12, 32, 12)
        self.titleBlock = QVBoxLayout()
        self.titleBlock.setSpacing(3)
        self.titleBlock.setObjectName(u"titleBlock")
        self.pageTitle = QLabel(self.pageHeader)
        self.pageTitle.setObjectName(u"pageTitle")

        self.titleBlock.addWidget(self.pageTitle)

        self.pageSubtitle = QLabel(self.pageHeader)
        self.pageSubtitle.setObjectName(u"pageSubtitle")
        self.pageSubtitle.setProperty(u"variant", u"muted")

        self.titleBlock.addWidget(self.pageSubtitle)


        self.pageHeaderLayout.addLayout(self.titleBlock)

        self.pageHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pageHeaderLayout.addItem(self.pageHeaderSpacer)

        self.profileBadge = QLabel(self.pageHeader)
        self.profileBadge.setObjectName(u"profileBadge")
        self.profileBadge.setMinimumSize(QSize(36, 36))
        self.profileBadge.setMaximumSize(QSize(36, 36))
        self.profileBadge.setText(u"RO")
        self.profileBadge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pageHeaderLayout.addWidget(self.profileBadge)


        self.pageLayout.addWidget(self.pageHeader)

        self.pages = QStackedWidget(self.page)
        self.pages.setObjectName(u"pages")
        self.overviewHost = QWidget()
        self.overviewHost.setObjectName(u"overviewHost")
        self.pages.addWidget(self.overviewHost)
        self.workArea = QFrame()
        self.workArea.setObjectName(u"workArea")
        self.workLayout = QVBoxLayout(self.workArea)
        self.workLayout.setSpacing(14)
        self.workLayout.setObjectName(u"workLayout")
        self.workLayout.setContentsMargins(32, 24, 32, 22)
        self.filtersLayout = QHBoxLayout()
        self.filtersLayout.setSpacing(12)
        self.filtersLayout.setObjectName(u"filtersLayout")
        self.filterLabel = QLabel(self.workArea)
        self.filterLabel.setObjectName(u"filterLabel")

        self.filtersLayout.addWidget(self.filterLabel)

        self.namespaceCombo = QComboBox(self.workArea)
        self.namespaceCombo.addItem(u"All namespaces")
        self.namespaceCombo.addItem(u"default")
        self.namespaceCombo.addItem(u"monitoring")
        self.namespaceCombo.addItem(u"kube-system")
        self.namespaceCombo.setObjectName(u"namespaceCombo")
        self.namespaceCombo.setMinimumSize(QSize(170, 38))
        self.namespaceCombo.setProperty(u"variant", u"filter")

        self.filtersLayout.addWidget(self.namespaceCombo)

        self.searchInput = QLineEdit(self.workArea)
        self.searchInput.setObjectName(u"searchInput")
        self.searchInput.setMinimumSize(QSize(240, 38))
        self.searchInput.setMaximumSize(QSize(300, 16777215))
        self.searchInput.setClearButtonEnabled(True)

        self.filtersLayout.addWidget(self.searchInput)

        self.filtersSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filtersLayout.addItem(self.filtersSpacer)

        self.refreshButton = QPushButton(self.workArea)
        self.refreshButton.setObjectName(u"refreshButton")
        self.refreshButton.setProperty(u"variant", u"primary")

        self.filtersLayout.addWidget(self.refreshButton)


        self.workLayout.addLayout(self.filtersLayout)

        self.summaryRow = QHBoxLayout()
        self.summaryRow.setObjectName(u"summaryRow")
        self.summaryLabel = QLabel(self.workArea)
        self.summaryLabel.setObjectName(u"summaryLabel")
        self.summaryLabel.setText(u"5 of 5 workloads")

        self.summaryRow.addWidget(self.summaryLabel)

        self.summarySpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.summaryRow.addItem(self.summarySpacer)

        self.podsButton = QPushButton(self.workArea)
        self.podsButton.setObjectName(u"podsButton")
        self.podsButton.setEnabled(False)
        self.podsButton.setProperty(u"variant", u"secondary")

        self.summaryRow.addWidget(self.podsButton)

        self.detailsButton = QPushButton(self.workArea)
        self.detailsButton.setObjectName(u"detailsButton")
        self.detailsButton.setEnabled(False)
        self.detailsButton.setProperty(u"variant", u"secondary")

        self.summaryRow.addWidget(self.detailsButton)

        self.logsButton = QPushButton(self.workArea)
        self.logsButton.setObjectName(u"logsButton")
        self.logsButton.setEnabled(False)
        self.logsButton.setProperty(u"variant", u"secondary")

        self.summaryRow.addWidget(self.logsButton)


        self.workLayout.addLayout(self.summaryRow)

        self.workloadTable = QTableWidget(self.workArea)
        if (self.workloadTable.columnCount() < 6):
            self.workloadTable.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.workloadTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.workloadTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.workloadTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.workloadTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.workloadTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.workloadTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        if (self.workloadTable.rowCount() < 5):
            self.workloadTable.setRowCount(5)
        brush = QBrush(QColor(36, 42, 51, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setText(u"default")
        __qtablewidgetitem6.setForeground(brush)
        self.workloadTable.setItem(0, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setText(u"Deployment")
        __qtablewidgetitem7.setForeground(brush)
        self.workloadTable.setItem(0, 1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setText(u"api")
        __qtablewidgetitem8.setForeground(brush)
        self.workloadTable.setItem(0, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setText(u"3/3")
        __qtablewidgetitem9.setForeground(brush)
        self.workloadTable.setItem(0, 3, __qtablewidgetitem9)
        brush1 = QBrush(QColor(23, 107, 88, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        brush2 = QBrush(QColor(229, 244, 235, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setText(u"Healthy")
        __qtablewidgetitem10.setBackground(brush2)
        __qtablewidgetitem10.setForeground(brush1)
        self.workloadTable.setItem(0, 4, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setText(u"12d")
        __qtablewidgetitem11.setForeground(brush)
        self.workloadTable.setItem(0, 5, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setText(u"default")
        __qtablewidgetitem12.setForeground(brush)
        self.workloadTable.setItem(1, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setText(u"Deployment")
        __qtablewidgetitem13.setForeground(brush)
        self.workloadTable.setItem(1, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setText(u"worker")
        __qtablewidgetitem14.setForeground(brush)
        self.workloadTable.setItem(1, 2, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setText(u"1/2")
        __qtablewidgetitem15.setForeground(brush)
        self.workloadTable.setItem(1, 3, __qtablewidgetitem15)
        brush3 = QBrush(QColor(152, 84, 21, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        brush4 = QBrush(QColor(255, 242, 222, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setText(u"Degraded")
        __qtablewidgetitem16.setBackground(brush4)
        __qtablewidgetitem16.setForeground(brush3)
        self.workloadTable.setItem(1, 4, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setText(u"12d")
        __qtablewidgetitem17.setForeground(brush)
        self.workloadTable.setItem(1, 5, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setText(u"default")
        __qtablewidgetitem18.setForeground(brush)
        self.workloadTable.setItem(2, 0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        __qtablewidgetitem19.setText(u"StatefulSet")
        __qtablewidgetitem19.setForeground(brush)
        self.workloadTable.setItem(2, 1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setText(u"postgres")
        __qtablewidgetitem20.setForeground(brush)
        self.workloadTable.setItem(2, 2, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setText(u"0/1")
        __qtablewidgetitem21.setForeground(brush)
        self.workloadTable.setItem(2, 3, __qtablewidgetitem21)
        brush5 = QBrush(QColor(163, 61, 69, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        brush6 = QBrush(QColor(252, 233, 234, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setText(u"Unavailable")
        __qtablewidgetitem22.setBackground(brush6)
        __qtablewidgetitem22.setForeground(brush5)
        self.workloadTable.setItem(2, 4, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setText(u"40d")
        __qtablewidgetitem23.setForeground(brush)
        self.workloadTable.setItem(2, 5, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setText(u"monitoring")
        __qtablewidgetitem24.setForeground(brush)
        self.workloadTable.setItem(3, 0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setText(u"DaemonSet")
        __qtablewidgetitem25.setForeground(brush)
        self.workloadTable.setItem(3, 1, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setText(u"node-exporter")
        __qtablewidgetitem26.setForeground(brush)
        self.workloadTable.setItem(3, 2, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        __qtablewidgetitem27.setText(u"4/4")
        __qtablewidgetitem27.setForeground(brush)
        self.workloadTable.setItem(3, 3, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        __qtablewidgetitem28.setText(u"Healthy")
        __qtablewidgetitem28.setBackground(brush2)
        __qtablewidgetitem28.setForeground(brush1)
        self.workloadTable.setItem(3, 4, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        __qtablewidgetitem29.setText(u"90d")
        __qtablewidgetitem29.setForeground(brush)
        self.workloadTable.setItem(3, 5, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        __qtablewidgetitem30.setText(u"monitoring")
        __qtablewidgetitem30.setForeground(brush)
        self.workloadTable.setItem(4, 0, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        __qtablewidgetitem31.setText(u"Deployment")
        __qtablewidgetitem31.setForeground(brush)
        self.workloadTable.setItem(4, 1, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        __qtablewidgetitem32.setText(u"grafana")
        __qtablewidgetitem32.setForeground(brush)
        self.workloadTable.setItem(4, 2, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        __qtablewidgetitem33.setText(u"0/0")
        __qtablewidgetitem33.setForeground(brush)
        self.workloadTable.setItem(4, 3, __qtablewidgetitem33)
        brush7 = QBrush(QColor(80, 89, 99, 255))
        brush7.setStyle(Qt.BrushStyle.SolidPattern)
        brush8 = QBrush(QColor(239, 241, 243, 255))
        brush8.setStyle(Qt.BrushStyle.SolidPattern)
        __qtablewidgetitem34 = QTableWidgetItem()
        __qtablewidgetitem34.setText(u"Scaled to zero")
        __qtablewidgetitem34.setBackground(brush8)
        __qtablewidgetitem34.setForeground(brush7)
        self.workloadTable.setItem(4, 4, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        __qtablewidgetitem35.setText(u"90d")
        __qtablewidgetitem35.setForeground(brush)
        self.workloadTable.setItem(4, 5, __qtablewidgetitem35)
        self.workloadTable.setObjectName(u"workloadTable")
        self.workloadTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.workloadTable.setAlternatingRowColors(False)
        self.workloadTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.workloadTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.workloadTable.setProperty(u"variant", u"data")
        self.workloadTable.horizontalHeader().setStretchLastSection(False)
        self.workloadTable.verticalHeader().setVisible(False)
        self.workloadTable.verticalHeader().setDefaultSectionSize(58)

        self.workLayout.addWidget(self.workloadTable)

        self.footerRow = QHBoxLayout()
        self.footerRow.setObjectName(u"footerRow")
        self.statusLabel = QLabel(self.workArea)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setProperty(u"variant", u"muted")

        self.footerRow.addWidget(self.statusLabel)

        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footerRow.addItem(self.footerSpacer)

        self.footerNote = QLabel(self.workArea)
        self.footerNote.setObjectName(u"footerNote")
        self.footerNote.setProperty(u"variant", u"muted")

        self.footerRow.addWidget(self.footerNote)


        self.workLayout.addLayout(self.footerRow)

        self.pages.addWidget(self.workArea)
        self.settingsHost = QWidget()
        self.settingsHost.setObjectName(u"settingsHost")
        self.pages.addWidget(self.settingsHost)
        self.viewerHost = QWidget()
        self.viewerHost.setObjectName(u"viewerHost")
        self.pages.addWidget(self.viewerHost)
        self.workloadsOverviewHost = QWidget()
        self.workloadsOverviewHost.setObjectName(u"workloadsOverviewHost")
        self.pages.addWidget(self.workloadsOverviewHost)

        self.pageLayout.addWidget(self.pages)

        self.pageLayout.setStretch(1, 1)

        self.shell.addWidget(self.page)

        self.shell.setStretch(1, 1)

        self.rootLayout.addLayout(self.shell)

        self.appFooter = QFrame(self.centralwidget)
        self.appFooter.setObjectName(u"appFooter")
        self.appFooter.setMinimumSize(QSize(0, 30))
        self.appFooter.setMaximumSize(QSize(16777215, 30))
        self.appFooterLayout = QHBoxLayout(self.appFooter)
        self.appFooterLayout.setObjectName(u"appFooterLayout")
        self.appFooterLayout.setContentsMargins(18, 0, 22, 0)
        self.footerLicense = QLabel(self.appFooter)
        self.footerLicense.setObjectName(u"footerLicense")

        self.appFooterLayout.addWidget(self.footerLicense)

        self.appFooterSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.appFooterLayout.addItem(self.appFooterSpacer)


        self.rootLayout.addWidget(self.appFooter)

        self.rootLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"KubeScope", None))
        self.topCaption.setText(QCoreApplication.translate("MainWindow", u"CONTEXT", None))

#if QT_CONFIG(tooltip)
        self.contextCombo.setToolTip(QCoreApplication.translate("MainWindow", u"Kubernetes context from your kubeconfig", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.loginButton.setToolTip(QCoreApplication.translate("MainWindow", u"Sign in with the AWS CLI, then reload the cluster data", None))
#endif // QT_CONFIG(tooltip)
        self.loginButton.setText(QCoreApplication.translate("MainWindow", u"Sign in to AWS", None))
        self.topAccess.setText(QCoreApplication.translate("MainWindow", u"READ ONLY", None))
        self.sidebarBrand.setText(QCoreApplication.translate("MainWindow", u"KubeScope", None))
        self.sidebarSubtitle.setText(QCoreApplication.translate("MainWindow", u"Kubernetes console", None))
        self.navSection.setText(QCoreApplication.translate("MainWindow", u"MONITORING", None))
        self.navOverview.setText(QCoreApplication.translate("MainWindow", u"Overview", None))
        self.navWorkloads.setText(QCoreApplication.translate("MainWindow", u"Workloads", None))
        self.navWorkloadsOverview.setText(QCoreApplication.translate("MainWindow", u"Overview", None))
        self.navPods.setText(QCoreApplication.translate("MainWindow", u"Pods", None))
        self.navDeployments.setText(QCoreApplication.translate("MainWindow", u"Deployments", None))
        self.navStatefulSets.setText(QCoreApplication.translate("MainWindow", u"StatefulSets", None))
        self.navJobs.setText(QCoreApplication.translate("MainWindow", u"Jobs", None))
        self.navCronJobs.setText(QCoreApplication.translate("MainWindow", u"CronJobs", None))
        self.navViewer.setText(QCoreApplication.translate("MainWindow", u"Details && Logs", None))
        self.settingsButton.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.sidebarNote.setText(QCoreApplication.translate("MainWindow", u"SECURE ACCESS\n"
"Resources in read-only mode", None))
        self.pageTitle.setText(QCoreApplication.translate("MainWindow", u"Overview", None))
        self.pageSubtitle.setText(QCoreApplication.translate("MainWindow", u"Cluster resources and capacity", None))
        self.filterLabel.setText(QCoreApplication.translate("MainWindow", u"NAMESPACE", None))

        self.searchInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search by name or namespace...", None))
        self.refreshButton.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
#if QT_CONFIG(tooltip)
        self.podsButton.setToolTip(QCoreApplication.translate("MainWindow", u"View Pods of the selected workload", None))
#endif // QT_CONFIG(tooltip)
        self.podsButton.setText(QCoreApplication.translate("MainWindow", u"Pods", None))
#if QT_CONFIG(tooltip)
        self.detailsButton.setToolTip(QCoreApplication.translate("MainWindow", u"View JSON details of the selected workload", None))
#endif // QT_CONFIG(tooltip)
        self.detailsButton.setText(QCoreApplication.translate("MainWindow", u"Details", None))
#if QT_CONFIG(tooltip)
        self.logsButton.setToolTip(QCoreApplication.translate("MainWindow", u"View logs of a Pod of the selected workload", None))
#endif // QT_CONFIG(tooltip)
        self.logsButton.setText(QCoreApplication.translate("MainWindow", u"Logs", None))
        ___qtablewidgetitem = self.workloadTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"NAMESPACE", None))
        ___qtablewidgetitem1 = self.workloadTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"KIND", None))
        ___qtablewidgetitem2 = self.workloadTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"NAME", None))
        ___qtablewidgetitem3 = self.workloadTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"READY", None))
        ___qtablewidgetitem4 = self.workloadTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"STATUS", None))
        ___qtablewidgetitem5 = self.workloadTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"AGE", None))

        __sortingEnabled = self.workloadTable.isSortingEnabled()
        self.workloadTable.setSortingEnabled(False)
        self.workloadTable.setSortingEnabled(__sortingEnabled)

        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Select a context to load workloads", None))
        self.footerNote.setText(QCoreApplication.translate("MainWindow", u"Data fetched via kubectl", None))
        self.footerLicense.setText(QCoreApplication.translate("MainWindow", u"\u00a9 2026 DCO Tecnologia \u00b7 MIT License", None))
#if QT_CONFIG(tooltip)
        self.footerLicense.setToolTip(QCoreApplication.translate("MainWindow", u"KubeScope is open source software released under the MIT License", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

