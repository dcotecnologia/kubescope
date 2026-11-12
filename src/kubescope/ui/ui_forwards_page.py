# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'forwards_page.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_ForwardsPage(object):
    def setupUi(self, ForwardsPage):
        if not ForwardsPage.objectName():
            ForwardsPage.setObjectName(u"ForwardsPage")
        self.forwardsLayout = QVBoxLayout(ForwardsPage)
        self.forwardsLayout.setSpacing(14)
        self.forwardsLayout.setObjectName(u"forwardsLayout")
        self.forwardsLayout.setContentsMargins(32, 24, 32, 22)
        self.forwardsHeaderRow = QHBoxLayout()
        self.forwardsHeaderRow.setSpacing(8)
        self.forwardsHeaderRow.setObjectName(u"forwardsHeaderRow")
        self.stopButton = QPushButton(ForwardsPage)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setProperty(u"variant", u"secondary")

        self.forwardsHeaderRow.addWidget(self.stopButton)

        self.stopAllButton = QPushButton(ForwardsPage)
        self.stopAllButton.setObjectName(u"stopAllButton")
        self.stopAllButton.setProperty(u"variant", u"secondary")

        self.forwardsHeaderRow.addWidget(self.stopAllButton)

        self.clearButton = QPushButton(ForwardsPage)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setProperty(u"variant", u"secondary")

        self.forwardsHeaderRow.addWidget(self.clearButton)

        self.noticeLabel = QLabel(ForwardsPage)
        self.noticeLabel.setObjectName(u"noticeLabel")
        self.noticeLabel.setText(u"")
        self.noticeLabel.setProperty(u"variant", u"muted")

        self.forwardsHeaderRow.addWidget(self.noticeLabel)

        self.forwardsHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.forwardsHeaderRow.addItem(self.forwardsHeaderSpacer)


        self.forwardsLayout.addLayout(self.forwardsHeaderRow)

        self.forwardsTable = QTableWidget(ForwardsPage)
        if (self.forwardsTable.columnCount() < 6):
            self.forwardsTable.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.forwardsTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.forwardsTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.forwardsTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.forwardsTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.forwardsTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.forwardsTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.forwardsTable.setObjectName(u"forwardsTable")
        self.forwardsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.forwardsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.forwardsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.forwardsTable.setShowGrid(False)
        self.forwardsTable.setProperty(u"variant", u"data")
        self.forwardsTable.horizontalHeader().setStretchLastSection(True)
        self.forwardsTable.verticalHeader().setVisible(False)

        self.forwardsLayout.addWidget(self.forwardsTable)

        self.forwardsLayout.setStretch(1, 1)

        self.retranslateUi(ForwardsPage)

        QMetaObject.connectSlotsByName(ForwardsPage)
    # setupUi

    def retranslateUi(self, ForwardsPage):
        self.stopButton.setText(QCoreApplication.translate("ForwardsPage", u"Stop", None))
        self.stopAllButton.setText(QCoreApplication.translate("ForwardsPage", u"Stop all", None))
        self.clearButton.setText(QCoreApplication.translate("ForwardsPage", u"Clear finished", None))
        ___qtablewidgetitem = self.forwardsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ForwardsPage", u"NAME", None))
        ___qtablewidgetitem1 = self.forwardsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ForwardsPage", u"TYPE", None))
        ___qtablewidgetitem2 = self.forwardsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ForwardsPage", u"LOCAL", None))
        ___qtablewidgetitem3 = self.forwardsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ForwardsPage", u"TARGET", None))
        ___qtablewidgetitem4 = self.forwardsTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ForwardsPage", u"STATUS", None))
        ___qtablewidgetitem5 = self.forwardsTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ForwardsPage", u"DETAIL", None))
        pass
    # retranslateUi

