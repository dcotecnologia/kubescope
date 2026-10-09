# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'workloads_overview_page.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from kubescope.widgets import StatusBar

class Ui_WorkloadsOverviewPage(object):
    def setupUi(self, WorkloadsOverviewPage):
        if not WorkloadsOverviewPage.objectName():
            WorkloadsOverviewPage.setObjectName(u"WorkloadsOverviewPage")
        self.workloadsOverviewLayout = QVBoxLayout(WorkloadsOverviewPage)
        self.workloadsOverviewLayout.setSpacing(14)
        self.workloadsOverviewLayout.setObjectName(u"workloadsOverviewLayout")
        self.workloadsOverviewLayout.setContentsMargins(32, 24, 32, 22)
        self.workloadsHeaderRow = QHBoxLayout()
        self.workloadsHeaderRow.setSpacing(12)
        self.workloadsHeaderRow.setObjectName(u"workloadsHeaderRow")
        self.workloadsHeading = QLabel(WorkloadsOverviewPage)
        self.workloadsHeading.setObjectName(u"workloadsHeading")
        self.workloadsHeading.setProperty(u"variant", u"cardTitle")

        self.workloadsHeaderRow.addWidget(self.workloadsHeading)

        self.workloadsHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.workloadsHeaderRow.addItem(self.workloadsHeaderSpacer)

        self.workloadsRefreshButton = QPushButton(WorkloadsOverviewPage)
        self.workloadsRefreshButton.setObjectName(u"workloadsRefreshButton")
        self.workloadsRefreshButton.setProperty(u"iconOnly", u"true")
        self.workloadsRefreshButton.setProperty(u"variant", u"primary")

        self.workloadsHeaderRow.addWidget(self.workloadsRefreshButton)


        self.workloadsOverviewLayout.addLayout(self.workloadsHeaderRow)

        self.kindsCard = QFrame(WorkloadsOverviewPage)
        self.kindsCard.setObjectName(u"kindsCard")
        self.kindsCard.setProperty(u"card", u"true")
        self.kindsGrid = QGridLayout(self.kindsCard)
        self.kindsGrid.setObjectName(u"kindsGrid")
        self.kindsGrid.setHorizontalSpacing(12)
        self.kindsGrid.setVerticalSpacing(6)
        self.kindsGrid.setContentsMargins(20, 14, 20, 14)
        self.podsLink = QPushButton(self.kindsCard)
        self.podsLink.setObjectName(u"podsLink")
        self.podsLink.setMinimumSize(QSize(150, 28))
        self.podsLink.setFlat(True)
        self.podsLink.setProperty(u"variant", u"link")

        self.kindsGrid.addWidget(self.podsLink, 0, 0, 1, 1)

        self.podsBar = StatusBar(self.kindsCard)
        self.podsBar.setObjectName(u"podsBar")

        self.kindsGrid.addWidget(self.podsBar, 0, 1, 1, 1)

        self.deploymentsLink = QPushButton(self.kindsCard)
        self.deploymentsLink.setObjectName(u"deploymentsLink")
        self.deploymentsLink.setMinimumSize(QSize(150, 28))
        self.deploymentsLink.setFlat(True)
        self.deploymentsLink.setProperty(u"variant", u"link")

        self.kindsGrid.addWidget(self.deploymentsLink, 1, 0, 1, 1)

        self.deploymentsBar = StatusBar(self.kindsCard)
        self.deploymentsBar.setObjectName(u"deploymentsBar")

        self.kindsGrid.addWidget(self.deploymentsBar, 1, 1, 1, 1)

        self.daemonsetsLink = QPushButton(self.kindsCard)
        self.daemonsetsLink.setObjectName(u"daemonsetsLink")
        self.daemonsetsLink.setMinimumSize(QSize(150, 28))
        self.daemonsetsLink.setFlat(True)
        self.daemonsetsLink.setProperty(u"variant", u"link")

        self.kindsGrid.addWidget(self.daemonsetsLink, 2, 0, 1, 1)

        self.daemonsetsBar = StatusBar(self.kindsCard)
        self.daemonsetsBar.setObjectName(u"daemonsetsBar")

        self.kindsGrid.addWidget(self.daemonsetsBar, 2, 1, 1, 1)

        self.statefulsetsLink = QPushButton(self.kindsCard)
        self.statefulsetsLink.setObjectName(u"statefulsetsLink")
        self.statefulsetsLink.setMinimumSize(QSize(150, 28))
        self.statefulsetsLink.setFlat(True)
        self.statefulsetsLink.setProperty(u"variant", u"link")

        self.kindsGrid.addWidget(self.statefulsetsLink, 3, 0, 1, 1)

        self.statefulsetsBar = StatusBar(self.kindsCard)
        self.statefulsetsBar.setObjectName(u"statefulsetsBar")

        self.kindsGrid.addWidget(self.statefulsetsBar, 3, 1, 1, 1)

        self.replicasetsLink = QPushButton(self.kindsCard)
        self.replicasetsLink.setObjectName(u"replicasetsLink")
        self.replicasetsLink.setMinimumSize(QSize(150, 28))
        self.replicasetsLink.setFlat(True)
        self.replicasetsLink.setProperty(u"variant", u"link")

        self.kindsGrid.addWidget(self.replicasetsLink, 0, 3, 1, 1)

        self.replicasetsBar = StatusBar(self.kindsCard)
        self.replicasetsBar.setObjectName(u"replicasetsBar")

        self.kindsGrid.addWidget(self.replicasetsBar, 0, 4, 1, 1)

        self.jobsLink = QPushButton(self.kindsCard)
        self.jobsLink.setObjectName(u"jobsLink")
        self.jobsLink.setMinimumSize(QSize(150, 28))
        self.jobsLink.setFlat(True)
        self.jobsLink.setProperty(u"variant", u"link")

        self.kindsGrid.addWidget(self.jobsLink, 1, 3, 1, 1)

        self.jobsBar = StatusBar(self.kindsCard)
        self.jobsBar.setObjectName(u"jobsBar")

        self.kindsGrid.addWidget(self.jobsBar, 1, 4, 1, 1)

        self.cronjobsLink = QPushButton(self.kindsCard)
        self.cronjobsLink.setObjectName(u"cronjobsLink")
        self.cronjobsLink.setMinimumSize(QSize(150, 28))
        self.cronjobsLink.setFlat(True)
        self.cronjobsLink.setProperty(u"variant", u"link")

        self.kindsGrid.addWidget(self.cronjobsLink, 2, 3, 1, 1)

        self.cronjobsBar = StatusBar(self.kindsCard)
        self.cronjobsBar.setObjectName(u"cronjobsBar")

        self.kindsGrid.addWidget(self.cronjobsBar, 2, 4, 1, 1)

        self.kindsGap = QSpacerItem(32, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kindsGrid.addItem(self.kindsGap, 0, 2, 4, 1)

        self.kindsGrid.setColumnStretch(1, 1)
        self.kindsGrid.setColumnStretch(4, 1)

        self.workloadsOverviewLayout.addWidget(self.kindsCard)

        self.noticeLabel = QLabel(WorkloadsOverviewPage)
        self.noticeLabel.setObjectName(u"noticeLabel")
        self.noticeLabel.setText(u"")
        self.noticeLabel.setProperty(u"variant", u"muted")

        self.workloadsOverviewLayout.addWidget(self.noticeLabel)

        self.eventsHeading = QLabel(WorkloadsOverviewPage)
        self.eventsHeading.setObjectName(u"eventsHeading")
        self.eventsHeading.setProperty(u"variant", u"cardTitle")

        self.workloadsOverviewLayout.addWidget(self.eventsHeading)

        self.eventsTable = QTableWidget(WorkloadsOverviewPage)
        if (self.eventsTable.columnCount() < 8):
            self.eventsTable.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.eventsTable.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.eventsTable.setObjectName(u"eventsTable")
        self.eventsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.eventsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.eventsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.eventsTable.setAlternatingRowColors(False)
        self.eventsTable.setTextElideMode(Qt.ElideRight)
        self.eventsTable.setProperty(u"variant", u"data")
        self.eventsTable.horizontalHeader().setStretchLastSection(False)
        self.eventsTable.verticalHeader().setVisible(False)
        self.eventsTable.verticalHeader().setDefaultSectionSize(40)

        self.workloadsOverviewLayout.addWidget(self.eventsTable)

        self.workloadsOverviewLayout.setStretch(4, 1)

        self.retranslateUi(WorkloadsOverviewPage)

        QMetaObject.connectSlotsByName(WorkloadsOverviewPage)
    # setupUi

    def retranslateUi(self, WorkloadsOverviewPage):
        self.workloadsHeading.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"Workloads", None))
#if QT_CONFIG(tooltip)
        self.workloadsRefreshButton.setToolTip(QCoreApplication.translate("WorkloadsOverviewPage", u"Refresh", None))
#endif // QT_CONFIG(tooltip)
        self.podsLink.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"Pods", None))
        self.deploymentsLink.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"Deployments", None))
        self.daemonsetsLink.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"DaemonSets", None))
        self.statefulsetsLink.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"StatefulSets", None))
        self.replicasetsLink.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"ReplicaSets", None))
        self.jobsLink.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"Jobs", None))
        self.cronjobsLink.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"CronJobs", None))
        self.eventsHeading.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"Events", None))
        ___qtablewidgetitem = self.eventsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"TYPE", None))
        ___qtablewidgetitem1 = self.eventsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"SOURCE", None))
        ___qtablewidgetitem2 = self.eventsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"NAMESPACE", None))
        ___qtablewidgetitem3 = self.eventsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"INVOLVED OBJECT", None))
        ___qtablewidgetitem4 = self.eventsTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"MESSAGE", None))
        ___qtablewidgetitem5 = self.eventsTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"COUNT", None))
        ___qtablewidgetitem6 = self.eventsTable.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"AGE", None))
        ___qtablewidgetitem7 = self.eventsTable.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("WorkloadsOverviewPage", u"LAST SEEN", None))
        pass
    # retranslateUi

