# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'overview_page.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QProgressBar, QSizePolicy, QSpacerItem,
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


        self.overviewLayout.addLayout(self.headerRow)

        self.clusterInfoCard = QFrame(OverviewPage)
        self.clusterInfoCard.setObjectName(u"clusterInfoCard")
        self.clusterInfoCard.setVisible(False)
        self.clusterInfoCard.setProperty(u"card", u"true")
        self.clusterInfoLayout = QVBoxLayout(self.clusterInfoCard)
        self.clusterInfoLayout.setSpacing(10)
        self.clusterInfoLayout.setObjectName(u"clusterInfoLayout")
        self.clusterInfoLayout.setContentsMargins(16, 14, 16, 14)
        self.clusterInfoTitle = QLabel(self.clusterInfoCard)
        self.clusterInfoTitle.setObjectName(u"clusterInfoTitle")
        self.clusterInfoTitle.setProperty(u"variant", u"cardTitle")

        self.clusterInfoLayout.addWidget(self.clusterInfoTitle)

        self.clusterInfoGrid = QGridLayout()
        self.clusterInfoGrid.setObjectName(u"clusterInfoGrid")
        self.clusterInfoGrid.setHorizontalSpacing(24)
        self.clusterInfoGrid.setVerticalSpacing(10)

        self.clusterInfoLayout.addLayout(self.clusterInfoGrid)


        self.overviewLayout.addWidget(self.clusterInfoCard)

        self.networkingCard = QFrame(OverviewPage)
        self.networkingCard.setObjectName(u"networkingCard")
        self.networkingCard.setVisible(False)
        self.networkingCard.setProperty(u"card", u"true")
        self.networkingLayout = QVBoxLayout(self.networkingCard)
        self.networkingLayout.setSpacing(10)
        self.networkingLayout.setObjectName(u"networkingLayout")
        self.networkingLayout.setContentsMargins(16, 14, 16, 14)
        self.networkingTitle = QLabel(self.networkingCard)
        self.networkingTitle.setObjectName(u"networkingTitle")
        self.networkingTitle.setProperty(u"variant", u"cardTitle")

        self.networkingLayout.addWidget(self.networkingTitle)

        self.networkingGrid = QGridLayout()
        self.networkingGrid.setObjectName(u"networkingGrid")
        self.networkingGrid.setHorizontalSpacing(24)
        self.networkingGrid.setVerticalSpacing(10)

        self.networkingLayout.addLayout(self.networkingGrid)


        self.overviewLayout.addWidget(self.networkingCard)

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

        self.overviewSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.overviewLayout.addItem(self.overviewSpacer)

        self.noticeLabel = QLabel(OverviewPage)
        self.noticeLabel.setObjectName(u"noticeLabel")
        self.noticeLabel.setText(u"")
        self.noticeLabel.setProperty(u"variant", u"muted")

        self.overviewLayout.addWidget(self.noticeLabel)

        self.overviewLayout.setStretch(5, 1)

        self.retranslateUi(OverviewPage)

        QMetaObject.connectSlotsByName(OverviewPage)
    # setupUi

    def retranslateUi(self, OverviewPage):
        self.overviewHeading.setText(QCoreApplication.translate("OverviewPage", u"Cluster resources", None))
        self.clusterInfoTitle.setText(QCoreApplication.translate("OverviewPage", u"CLUSTER INFO", None))
        self.networkingTitle.setText(QCoreApplication.translate("OverviewPage", u"NETWORKING", None))
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
        pass
    # retranslateUi

