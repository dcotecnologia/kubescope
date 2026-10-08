# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'overview_page.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_OverviewPage(object):
    def setupUi(self, OverviewPage):
        if not OverviewPage.objectName():
            OverviewPage.setObjectName(u"OverviewPage")
        self.overviewLayout = QVBoxLayout(OverviewPage)
        self.overviewLayout.setSpacing(14)
        self.overviewLayout.setObjectName(u"overviewLayout")
        self.overviewLayout.setContentsMargins(32, 24, 32, 22)
        self.headerRow = QHBoxLayout()
        self.headerRow.setSpacing(12)
        self.headerRow.setObjectName(u"headerRow")
        self.overviewHeading = QLabel(OverviewPage)
        self.overviewHeading.setObjectName(u"overviewHeading")
        self.overviewHeading.setProperty(u"variant", u"cardTitle")

        self.headerRow.addWidget(self.overviewHeading)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerRow.addItem(self.headerSpacer)

        self.overviewRefreshButton = QPushButton(OverviewPage)
        self.overviewRefreshButton.setObjectName(u"overviewRefreshButton")
        self.overviewRefreshButton.setProperty(u"variant", u"primary")

        self.headerRow.addWidget(self.overviewRefreshButton)


        self.overviewLayout.addLayout(self.headerRow)

        self.mainCards = QHBoxLayout()
        self.mainCards.setSpacing(14)
        self.mainCards.setObjectName(u"mainCards")
        self.nodesCard = QFrame(OverviewPage)
        self.nodesCard.setObjectName(u"nodesCard")
        self.nodesCard.setProperty(u"card", u"true")
        self.nodesCardLayout = QVBoxLayout(self.nodesCard)
        self.nodesCardLayout.setSpacing(4)
        self.nodesCardLayout.setObjectName(u"nodesCardLayout")
        self.nodesCardLayout.setContentsMargins(16, 14, 16, 14)
        self.nodesTitle = QLabel(self.nodesCard)
        self.nodesTitle.setObjectName(u"nodesTitle")
        self.nodesTitle.setProperty(u"variant", u"cardTitle")

        self.nodesCardLayout.addWidget(self.nodesTitle)

        self.nodesValue = QLabel(self.nodesCard)
        self.nodesValue.setObjectName(u"nodesValue")
        self.nodesValue.setText(u"3 / 3")
        self.nodesValue.setProperty(u"variant", u"cardValue")

        self.nodesCardLayout.addWidget(self.nodesValue)

        self.nodesCaption = QLabel(self.nodesCard)
        self.nodesCaption.setObjectName(u"nodesCaption")
        self.nodesCaption.setProperty(u"variant", u"cardCaption")

        self.nodesCardLayout.addWidget(self.nodesCaption)


        self.mainCards.addWidget(self.nodesCard)

        self.podsCard = QFrame(OverviewPage)
        self.podsCard.setObjectName(u"podsCard")
        self.podsCard.setProperty(u"card", u"true")
        self.podsCardLayout = QVBoxLayout(self.podsCard)
        self.podsCardLayout.setSpacing(4)
        self.podsCardLayout.setObjectName(u"podsCardLayout")
        self.podsCardLayout.setContentsMargins(16, 14, 16, 14)
        self.podsTitle = QLabel(self.podsCard)
        self.podsTitle.setObjectName(u"podsTitle")
        self.podsTitle.setProperty(u"variant", u"cardTitle")

        self.podsCardLayout.addWidget(self.podsTitle)

        self.podsValue = QLabel(self.podsCard)
        self.podsValue.setObjectName(u"podsValue")
        self.podsValue.setText(u"42 / 174")
        self.podsValue.setProperty(u"variant", u"cardValue")

        self.podsCardLayout.addWidget(self.podsValue)

        self.podsCaption = QLabel(self.podsCard)
        self.podsCaption.setObjectName(u"podsCaption")
        self.podsCaption.setProperty(u"variant", u"cardCaption")

        self.podsCardLayout.addWidget(self.podsCaption)

        self.podsBar = QProgressBar(self.podsCard)
        self.podsBar.setObjectName(u"podsBar")
        self.podsBar.setMaximum(100)
        self.podsBar.setValue(24)
        self.podsBar.setTextVisible(False)

        self.podsCardLayout.addWidget(self.podsBar)


        self.mainCards.addWidget(self.podsCard)

        self.cpuCard = QFrame(OverviewPage)
        self.cpuCard.setObjectName(u"cpuCard")
        self.cpuCard.setProperty(u"card", u"true")
        self.cpuCardLayout = QVBoxLayout(self.cpuCard)
        self.cpuCardLayout.setSpacing(4)
        self.cpuCardLayout.setObjectName(u"cpuCardLayout")
        self.cpuCardLayout.setContentsMargins(16, 14, 16, 14)
        self.cpuTitle = QLabel(self.cpuCard)
        self.cpuTitle.setObjectName(u"cpuTitle")
        self.cpuTitle.setProperty(u"variant", u"cardTitle")

        self.cpuCardLayout.addWidget(self.cpuTitle)

        self.cpuValue = QLabel(self.cpuCard)
        self.cpuValue.setObjectName(u"cpuValue")
        self.cpuValue.setText(u"2.4 / 11.8")
        self.cpuValue.setProperty(u"variant", u"cardValue")

        self.cpuCardLayout.addWidget(self.cpuValue)

        self.cpuCaption = QLabel(self.cpuCard)
        self.cpuCaption.setObjectName(u"cpuCaption")
        self.cpuCaption.setProperty(u"variant", u"cardCaption")

        self.cpuCardLayout.addWidget(self.cpuCaption)

        self.cpuBar = QProgressBar(self.cpuCard)
        self.cpuBar.setObjectName(u"cpuBar")
        self.cpuBar.setMaximum(100)
        self.cpuBar.setValue(20)
        self.cpuBar.setTextVisible(False)

        self.cpuCardLayout.addWidget(self.cpuBar)


        self.mainCards.addWidget(self.cpuCard)

        self.memCard = QFrame(OverviewPage)
        self.memCard.setObjectName(u"memCard")
        self.memCard.setProperty(u"card", u"true")
        self.memCardLayout = QVBoxLayout(self.memCard)
        self.memCardLayout.setSpacing(4)
        self.memCardLayout.setObjectName(u"memCardLayout")
        self.memCardLayout.setContentsMargins(16, 14, 16, 14)
        self.memTitle = QLabel(self.memCard)
        self.memTitle.setObjectName(u"memTitle")
        self.memTitle.setProperty(u"variant", u"cardTitle")

        self.memCardLayout.addWidget(self.memTitle)

        self.memValue = QLabel(self.memCard)
        self.memValue.setObjectName(u"memValue")
        self.memValue.setText(u"5.1 GiB / 21.0 GiB")
        self.memValue.setProperty(u"variant", u"cardValue")

        self.memCardLayout.addWidget(self.memValue)

        self.memCaption = QLabel(self.memCard)
        self.memCaption.setObjectName(u"memCaption")
        self.memCaption.setProperty(u"variant", u"cardCaption")

        self.memCardLayout.addWidget(self.memCaption)

        self.memBar = QProgressBar(self.memCard)
        self.memBar.setObjectName(u"memBar")
        self.memBar.setMaximum(100)
        self.memBar.setValue(24)
        self.memBar.setTextVisible(False)

        self.memCardLayout.addWidget(self.memBar)


        self.mainCards.addWidget(self.memCard)


        self.overviewLayout.addLayout(self.mainCards)

        self.countCards = QHBoxLayout()
        self.countCards.setSpacing(14)
        self.countCards.setObjectName(u"countCards")
        self.namespacesCard = QFrame(OverviewPage)
        self.namespacesCard.setObjectName(u"namespacesCard")
        self.namespacesCard.setProperty(u"card", u"true")
        self.namespacesCardLayout = QVBoxLayout(self.namespacesCard)
        self.namespacesCardLayout.setSpacing(4)
        self.namespacesCardLayout.setObjectName(u"namespacesCardLayout")
        self.namespacesCardLayout.setContentsMargins(16, 14, 16, 14)
        self.namespacesTitle = QLabel(self.namespacesCard)
        self.namespacesTitle.setObjectName(u"namespacesTitle")
        self.namespacesTitle.setProperty(u"variant", u"cardTitle")

        self.namespacesCardLayout.addWidget(self.namespacesTitle)

        self.namespacesValue = QLabel(self.namespacesCard)
        self.namespacesValue.setObjectName(u"namespacesValue")
        self.namespacesValue.setText(u"6")
        self.namespacesValue.setProperty(u"variant", u"cardValue")

        self.namespacesCardLayout.addWidget(self.namespacesValue)

        self.namespacesCaption = QLabel(self.namespacesCard)
        self.namespacesCaption.setObjectName(u"namespacesCaption")
        self.namespacesCaption.setProperty(u"variant", u"cardCaption")

        self.namespacesCardLayout.addWidget(self.namespacesCaption)


        self.countCards.addWidget(self.namespacesCard)

        self.deploymentsCard = QFrame(OverviewPage)
        self.deploymentsCard.setObjectName(u"deploymentsCard")
        self.deploymentsCard.setProperty(u"card", u"true")
        self.deploymentsCardLayout = QVBoxLayout(self.deploymentsCard)
        self.deploymentsCardLayout.setSpacing(4)
        self.deploymentsCardLayout.setObjectName(u"deploymentsCardLayout")
        self.deploymentsCardLayout.setContentsMargins(16, 14, 16, 14)
        self.deploymentsTitle = QLabel(self.deploymentsCard)
        self.deploymentsTitle.setObjectName(u"deploymentsTitle")
        self.deploymentsTitle.setProperty(u"variant", u"cardTitle")

        self.deploymentsCardLayout.addWidget(self.deploymentsTitle)

        self.deploymentsValue = QLabel(self.deploymentsCard)
        self.deploymentsValue.setObjectName(u"deploymentsValue")
        self.deploymentsValue.setText(u"18")
        self.deploymentsValue.setProperty(u"variant", u"cardValue")

        self.deploymentsCardLayout.addWidget(self.deploymentsValue)

        self.deploymentsCaption = QLabel(self.deploymentsCard)
        self.deploymentsCaption.setObjectName(u"deploymentsCaption")
        self.deploymentsCaption.setProperty(u"variant", u"cardCaption")

        self.deploymentsCardLayout.addWidget(self.deploymentsCaption)


        self.countCards.addWidget(self.deploymentsCard)

        self.statefulsetsCard = QFrame(OverviewPage)
        self.statefulsetsCard.setObjectName(u"statefulsetsCard")
        self.statefulsetsCard.setProperty(u"card", u"true")
        self.statefulsetsCardLayout = QVBoxLayout(self.statefulsetsCard)
        self.statefulsetsCardLayout.setSpacing(4)
        self.statefulsetsCardLayout.setObjectName(u"statefulsetsCardLayout")
        self.statefulsetsCardLayout.setContentsMargins(16, 14, 16, 14)
        self.statefulsetsTitle = QLabel(self.statefulsetsCard)
        self.statefulsetsTitle.setObjectName(u"statefulsetsTitle")
        self.statefulsetsTitle.setProperty(u"variant", u"cardTitle")

        self.statefulsetsCardLayout.addWidget(self.statefulsetsTitle)

        self.statefulsetsValue = QLabel(self.statefulsetsCard)
        self.statefulsetsValue.setObjectName(u"statefulsetsValue")
        self.statefulsetsValue.setText(u"2")
        self.statefulsetsValue.setProperty(u"variant", u"cardValue")

        self.statefulsetsCardLayout.addWidget(self.statefulsetsValue)

        self.statefulsetsCaption = QLabel(self.statefulsetsCard)
        self.statefulsetsCaption.setObjectName(u"statefulsetsCaption")
        self.statefulsetsCaption.setProperty(u"variant", u"cardCaption")

        self.statefulsetsCardLayout.addWidget(self.statefulsetsCaption)


        self.countCards.addWidget(self.statefulsetsCard)

        self.daemonsetsCard = QFrame(OverviewPage)
        self.daemonsetsCard.setObjectName(u"daemonsetsCard")
        self.daemonsetsCard.setProperty(u"card", u"true")
        self.daemonsetsCardLayout = QVBoxLayout(self.daemonsetsCard)
        self.daemonsetsCardLayout.setSpacing(4)
        self.daemonsetsCardLayout.setObjectName(u"daemonsetsCardLayout")
        self.daemonsetsCardLayout.setContentsMargins(16, 14, 16, 14)
        self.daemonsetsTitle = QLabel(self.daemonsetsCard)
        self.daemonsetsTitle.setObjectName(u"daemonsetsTitle")
        self.daemonsetsTitle.setProperty(u"variant", u"cardTitle")

        self.daemonsetsCardLayout.addWidget(self.daemonsetsTitle)

        self.daemonsetsValue = QLabel(self.daemonsetsCard)
        self.daemonsetsValue.setObjectName(u"daemonsetsValue")
        self.daemonsetsValue.setText(u"4")
        self.daemonsetsValue.setProperty(u"variant", u"cardValue")

        self.daemonsetsCardLayout.addWidget(self.daemonsetsValue)

        self.daemonsetsCaption = QLabel(self.daemonsetsCard)
        self.daemonsetsCaption.setObjectName(u"daemonsetsCaption")
        self.daemonsetsCaption.setProperty(u"variant", u"cardCaption")

        self.daemonsetsCardLayout.addWidget(self.daemonsetsCaption)


        self.countCards.addWidget(self.daemonsetsCard)


        self.overviewLayout.addLayout(self.countCards)

        self.nodesHeading = QLabel(OverviewPage)
        self.nodesHeading.setObjectName(u"nodesHeading")
        self.nodesHeading.setProperty(u"variant", u"cardTitle")

        self.overviewLayout.addWidget(self.nodesHeading)

        self.nodesTable = QTableWidget(OverviewPage)
        if (self.nodesTable.columnCount() < 8):
            self.nodesTable.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.nodesTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.nodesTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.nodesTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.nodesTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.nodesTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.nodesTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.nodesTable.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.nodesTable.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.nodesTable.setObjectName(u"nodesTable")
        self.nodesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.nodesTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.nodesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.nodesTable.setAlternatingRowColors(False)
        self.nodesTable.setProperty(u"variant", u"data")
        self.nodesTable.horizontalHeader().setStretchLastSection(False)
        self.nodesTable.verticalHeader().setVisible(False)
        self.nodesTable.verticalHeader().setDefaultSectionSize(44)

        self.overviewLayout.addWidget(self.nodesTable)

        self.noticeLabel = QLabel(OverviewPage)
        self.noticeLabel.setObjectName(u"noticeLabel")
        self.noticeLabel.setText(u"")
        self.noticeLabel.setProperty(u"variant", u"muted")

        self.overviewLayout.addWidget(self.noticeLabel)

        self.overviewLayout.setStretch(4, 1)

        self.retranslateUi(OverviewPage)

        QMetaObject.connectSlotsByName(OverviewPage)
    # setupUi

    def retranslateUi(self, OverviewPage):
        self.overviewHeading.setText(QCoreApplication.translate("OverviewPage", u"Cluster resources", None))
        self.overviewRefreshButton.setText(QCoreApplication.translate("OverviewPage", u"Refresh", None))
        self.nodesTitle.setText(QCoreApplication.translate("OverviewPage", u"NODES", None))
        self.nodesCaption.setText(QCoreApplication.translate("OverviewPage", u"nodes ready", None))
        self.podsTitle.setText(QCoreApplication.translate("OverviewPage", u"PODS", None))
        self.podsCaption.setText(QCoreApplication.translate("OverviewPage", u"running / capacity", None))
        self.cpuTitle.setText(QCoreApplication.translate("OverviewPage", u"CPU", None))
        self.cpuCaption.setText(QCoreApplication.translate("OverviewPage", u"cores requested / allocatable", None))
        self.memTitle.setText(QCoreApplication.translate("OverviewPage", u"MEMORY", None))
        self.memCaption.setText(QCoreApplication.translate("OverviewPage", u"requested / allocatable", None))
        self.namespacesTitle.setText(QCoreApplication.translate("OverviewPage", u"NAMESPACES", None))
        self.namespacesCaption.setText(QCoreApplication.translate("OverviewPage", u"in the cluster", None))
        self.deploymentsTitle.setText(QCoreApplication.translate("OverviewPage", u"DEPLOYMENTS", None))
        self.deploymentsCaption.setText(QCoreApplication.translate("OverviewPage", u"workloads", None))
        self.statefulsetsTitle.setText(QCoreApplication.translate("OverviewPage", u"STATEFULSETS", None))
        self.statefulsetsCaption.setText(QCoreApplication.translate("OverviewPage", u"workloads", None))
        self.daemonsetsTitle.setText(QCoreApplication.translate("OverviewPage", u"DAEMONSETS", None))
        self.daemonsetsCaption.setText(QCoreApplication.translate("OverviewPage", u"workloads", None))
        self.nodesHeading.setText(QCoreApplication.translate("OverviewPage", u"Nodes", None))
        ___qtablewidgetitem = self.nodesTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("OverviewPage", u"NODE", None))
        ___qtablewidgetitem1 = self.nodesTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("OverviewPage", u"STATUS", None))
        ___qtablewidgetitem2 = self.nodesTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("OverviewPage", u"ROLE", None))
        ___qtablewidgetitem3 = self.nodesTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("OverviewPage", u"VERSION", None))
        ___qtablewidgetitem4 = self.nodesTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("OverviewPage", u"CPU", None))
        ___qtablewidgetitem5 = self.nodesTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("OverviewPage", u"MEMORY", None))
        ___qtablewidgetitem6 = self.nodesTable.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("OverviewPage", u"PODS", None))
        ___qtablewidgetitem7 = self.nodesTable.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("OverviewPage", u"AGE", None))
        pass
    # retranslateUi

