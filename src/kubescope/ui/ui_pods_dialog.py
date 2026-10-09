# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pods_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_PodsDialog(object):
    def setupUi(self, PodsDialog):
        if not PodsDialog.objectName():
            PodsDialog.setObjectName(u"PodsDialog")
        PodsDialog.setMinimumSize(QSize(760, 420))
        self.podsLayout = QVBoxLayout(PodsDialog)
        self.podsLayout.setObjectName(u"podsLayout")
        self.summaryLabel = QLabel(PodsDialog)
        self.summaryLabel.setObjectName(u"summaryLabel")
        self.summaryLabel.setText(u"2 Pods in default / worker")

        self.podsLayout.addWidget(self.summaryLabel)

        self.podsTable = QTableWidget(PodsDialog)
        if (self.podsTable.columnCount() < 5):
            self.podsTable.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.podsTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.podsTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.podsTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.podsTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.podsTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        if (self.podsTable.rowCount() < 2):
            self.podsTable.setRowCount(2)
        brush = QBrush(QColor(36, 42, 51, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setText(u"worker-5f7d9c-abcde")
        __qtablewidgetitem5.setForeground(brush)
        self.podsTable.setItem(0, 0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setText(u"1/2")
        __qtablewidgetitem6.setForeground(brush)
        self.podsTable.setItem(0, 1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setText(u"Running")
        __qtablewidgetitem7.setForeground(brush)
        self.podsTable.setItem(0, 2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setText(u"2")
        __qtablewidgetitem8.setForeground(brush)
        self.podsTable.setItem(0, 3, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setText(u"3d")
        __qtablewidgetitem9.setForeground(brush)
        self.podsTable.setItem(0, 4, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setText(u"worker-5f7d9c-fghij")
        __qtablewidgetitem10.setForeground(brush)
        self.podsTable.setItem(1, 0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setText(u"0/2")
        __qtablewidgetitem11.setForeground(brush)
        self.podsTable.setItem(1, 1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setText(u"Pending")
        __qtablewidgetitem12.setForeground(brush)
        self.podsTable.setItem(1, 2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setText(u"2")
        __qtablewidgetitem13.setForeground(brush)
        self.podsTable.setItem(1, 3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setText(u"3d")
        __qtablewidgetitem14.setForeground(brush)
        self.podsTable.setItem(1, 4, __qtablewidgetitem14)
        self.podsTable.setObjectName(u"podsTable")
        self.podsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.podsTable.setAlternatingRowColors(False)
        self.podsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.podsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.podsTable.setProperty(u"variant", u"data")
        self.podsTable.verticalHeader().setVisible(False)

        self.podsLayout.addWidget(self.podsTable)

        self.podsActions = QHBoxLayout()
        self.podsActions.setObjectName(u"podsActions")
        self.detailsButton = QPushButton(PodsDialog)
        self.detailsButton.setObjectName(u"detailsButton")
        self.detailsButton.setEnabled(False)

        self.podsActions.addWidget(self.detailsButton)

        self.logsButton = QPushButton(PodsDialog)
        self.logsButton.setObjectName(u"logsButton")
        self.logsButton.setEnabled(False)

        self.podsActions.addWidget(self.logsButton)

        self.podsActionsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.podsActions.addItem(self.podsActionsSpacer)

        self.closeButton = QPushButton(PodsDialog)
        self.closeButton.setObjectName(u"closeButton")

        self.podsActions.addWidget(self.closeButton)


        self.podsLayout.addLayout(self.podsActions)

        self.podsLayout.setStretch(1, 1)

        self.retranslateUi(PodsDialog)

        QMetaObject.connectSlotsByName(PodsDialog)
    # setupUi

    def retranslateUi(self, PodsDialog):
        PodsDialog.setWindowTitle(QCoreApplication.translate("PodsDialog", u"Pods", None))
        ___qtablewidgetitem = self.podsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PodsDialog", u"NAME", None))
        ___qtablewidgetitem1 = self.podsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PodsDialog", u"READY", None))
        ___qtablewidgetitem2 = self.podsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PodsDialog", u"PHASE", None))
        ___qtablewidgetitem3 = self.podsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PodsDialog", u"CONTAINERS", None))
        ___qtablewidgetitem4 = self.podsTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PodsDialog", u"AGE", None))

        __sortingEnabled = self.podsTable.isSortingEnabled()
        self.podsTable.setSortingEnabled(False)
        self.podsTable.setSortingEnabled(__sortingEnabled)

        self.detailsButton.setText(QCoreApplication.translate("PodsDialog", u"Pod details", None))
        self.logsButton.setText(QCoreApplication.translate("PodsDialog", u"View logs", None))
        self.closeButton.setText(QCoreApplication.translate("PodsDialog", u"Close", None))
    # retranslateUi

