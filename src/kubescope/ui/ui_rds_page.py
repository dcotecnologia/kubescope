# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rds_page.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_RdsPage(object):
    def setupUi(self, RdsPage):
        if not RdsPage.objectName():
            RdsPage.setObjectName(u"RdsPage")
        self.rdsLayout = QVBoxLayout(RdsPage)
        self.rdsLayout.setSpacing(14)
        self.rdsLayout.setObjectName(u"rdsLayout")
        self.rdsLayout.setContentsMargins(32, 24, 32, 22)
        self.rdsHeaderRow = QHBoxLayout()
        self.rdsHeaderRow.setSpacing(12)
        self.rdsHeaderRow.setObjectName(u"rdsHeaderRow")
        self.regionCombo = QComboBox(RdsPage)
        self.regionCombo.setObjectName(u"regionCombo")
        self.regionCombo.setMinimumSize(QSize(170, 38))
        self.regionCombo.setProperty(u"variant", u"filter")

        self.rdsHeaderRow.addWidget(self.regionCombo)

        self.searchInput = QLineEdit(RdsPage)
        self.searchInput.setObjectName(u"searchInput")
        self.searchInput.setMinimumSize(QSize(240, 38))
        self.searchInput.setMaximumSize(QSize(300, 16777215))
        self.searchInput.setClearButtonEnabled(True)

        self.rdsHeaderRow.addWidget(self.searchInput)

        self.noticeLabel = QLabel(RdsPage)
        self.noticeLabel.setObjectName(u"noticeLabel")
        self.noticeLabel.setText(u"")
        self.noticeLabel.setWordWrap(True)
        self.noticeLabel.setProperty(u"variant", u"muted")

        self.rdsHeaderRow.addWidget(self.noticeLabel)

        self.rdsHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.rdsHeaderRow.addItem(self.rdsHeaderSpacer)


        self.rdsLayout.addLayout(self.rdsHeaderRow)

        self.rdsBanner = QFrame(RdsPage)
        self.rdsBanner.setObjectName(u"rdsBanner")
        self.rdsBanner.setVisible(False)
        self.rdsBannerLayout = QVBoxLayout(self.rdsBanner)
        self.rdsBannerLayout.setSpacing(6)
        self.rdsBannerLayout.setObjectName(u"rdsBannerLayout")
        self.rdsBannerLayout.setContentsMargins(14, 8, 14, 8)
        self.rdsBannerRow = QHBoxLayout()
        self.rdsBannerRow.setObjectName(u"rdsBannerRow")
        self.bannerLabel = QLabel(self.rdsBanner)
        self.bannerLabel.setObjectName(u"bannerLabel")
        self.bannerLabel.setText(u"")
        self.bannerLabel.setWordWrap(True)

        self.rdsBannerRow.addWidget(self.bannerLabel)

        self.detailsButton = QPushButton(self.rdsBanner)
        self.detailsButton.setObjectName(u"detailsButton")
        self.detailsButton.setFlat(True)
        self.detailsButton.setProperty(u"variant", u"link")

        self.rdsBannerRow.addWidget(self.detailsButton)

        self.dismissButton = QPushButton(self.rdsBanner)
        self.dismissButton.setObjectName(u"dismissButton")
        self.dismissButton.setFlat(True)
        self.dismissButton.setProperty(u"variant", u"link")

        self.rdsBannerRow.addWidget(self.dismissButton)

        self.rdsBannerRow.setStretch(0, 1)

        self.rdsBannerLayout.addLayout(self.rdsBannerRow)

        self.bannerDetails = QLabel(self.rdsBanner)
        self.bannerDetails.setObjectName(u"bannerDetails")
        self.bannerDetails.setVisible(False)
        self.bannerDetails.setText(u"")
        self.bannerDetails.setWordWrap(True)
        self.bannerDetails.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.rdsBannerLayout.addWidget(self.bannerDetails)


        self.rdsLayout.addWidget(self.rdsBanner)

        self.instancesTable = QTableWidget(RdsPage)
        if (self.instancesTable.columnCount() < 10):
            self.instancesTable.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.instancesTable.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        self.instancesTable.setObjectName(u"instancesTable")
        self.instancesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.instancesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.instancesTable.setShowGrid(False)
        self.instancesTable.setProperty(u"variant", u"data")
        self.instancesTable.horizontalHeader().setStretchLastSection(True)
        self.instancesTable.verticalHeader().setVisible(False)

        self.rdsLayout.addWidget(self.instancesTable)

        self.rdsLayout.setStretch(2, 1)

        self.retranslateUi(RdsPage)

        QMetaObject.connectSlotsByName(RdsPage)
    # setupUi

    def retranslateUi(self, RdsPage):
#if QT_CONFIG(tooltip)
        self.regionCombo.setToolTip(QCoreApplication.translate("RdsPage", u"Region", None))
#endif // QT_CONFIG(tooltip)
        self.searchInput.setPlaceholderText(QCoreApplication.translate("RdsPage", u"Search all columns...", None))
        self.detailsButton.setText(QCoreApplication.translate("RdsPage", u"Details", None))
        self.dismissButton.setText(QCoreApplication.translate("RdsPage", u"Dismiss", None))
        ___qtablewidgetitem = self.instancesTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RdsPage", u"NAME", None))
        ___qtablewidgetitem1 = self.instancesTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RdsPage", u"ENGINE", None))
        ___qtablewidgetitem2 = self.instancesTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RdsPage", u"VERSION", None))
        ___qtablewidgetitem3 = self.instancesTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RdsPage", u"CLASS", None))
        ___qtablewidgetitem4 = self.instancesTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RdsPage", u"STATUS", None))
        ___qtablewidgetitem5 = self.instancesTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RdsPage", u"STORAGE", None))
        ___qtablewidgetitem6 = self.instancesTable.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("RdsPage", u"MULTI-AZ", None))
        ___qtablewidgetitem7 = self.instancesTable.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("RdsPage", u"REGION", None))
        ___qtablewidgetitem8 = self.instancesTable.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("RdsPage", u"ACCOUNT", None))
        ___qtablewidgetitem9 = self.instancesTable.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("RdsPage", u"ENDPOINT", None))
        pass
    # retranslateUi

