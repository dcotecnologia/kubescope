# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_page.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFormLayout, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_SettingsPage(object):
    def setupUi(self, SettingsPage):
        if not SettingsPage.objectName():
            SettingsPage.setObjectName(u"SettingsPage")
        self.settingsLayout = QVBoxLayout(SettingsPage)
        self.settingsLayout.setSpacing(14)
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.settingsLayout.setContentsMargins(32, 24, 32, 22)
        self.settingsHeader = QHBoxLayout()
        self.settingsHeader.setObjectName(u"settingsHeader")
        self.noticeLabel = QLabel(SettingsPage)
        self.noticeLabel.setObjectName(u"noticeLabel")
        self.noticeLabel.setText(u"")
        self.noticeLabel.setProperty(u"variant", u"muted")

        self.settingsHeader.addWidget(self.noticeLabel)

        self.settingsHeaderSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.settingsHeader.addItem(self.settingsHeaderSpacer)

        self.saveButton = QPushButton(SettingsPage)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setProperty(u"variant", u"primary")

        self.settingsHeader.addWidget(self.saveButton)


        self.settingsLayout.addLayout(self.settingsHeader)

        self.generalHeading = QLabel(SettingsPage)
        self.generalHeading.setObjectName(u"generalHeading")
        self.generalHeading.setProperty(u"variant", u"cardTitle")

        self.settingsLayout.addWidget(self.generalHeading)

        self.generalForm = QFormLayout()
        self.generalForm.setObjectName(u"generalForm")
        self.generalForm.setHorizontalSpacing(16)
        self.generalForm.setVerticalSpacing(10)
        self.languageLabel = QLabel(SettingsPage)
        self.languageLabel.setObjectName(u"languageLabel")

        self.generalForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.languageLabel)

        self.languageCombo = QComboBox(SettingsPage)
        self.languageCombo.addItem(u"Automatic")
        self.languageCombo.addItem(u"English")
        self.languageCombo.addItem(u"Portugu\u00eas")
        self.languageCombo.setObjectName(u"languageCombo")
        self.languageCombo.setMinimumSize(QSize(200, 0))
        self.languageCombo.setProperty(u"variant", u"filter")

        self.generalForm.setWidget(0, QFormLayout.ItemRole.FieldRole, self.languageCombo)

        self.rememberCheck = QCheckBox(SettingsPage)
        self.rememberCheck.setObjectName(u"rememberCheck")
        self.rememberCheck.setChecked(True)

        self.generalForm.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.rememberCheck)


        self.settingsLayout.addLayout(self.generalForm)

        self.contextsHeading = QLabel(SettingsPage)
        self.contextsHeading.setObjectName(u"contextsHeading")
        self.contextsHeading.setProperty(u"variant", u"cardTitle")

        self.settingsLayout.addWidget(self.contextsHeading)

        self.contextsHint = QLabel(SettingsPage)
        self.contextsHint.setObjectName(u"contextsHint")
        self.contextsHint.setWordWrap(True)
        self.contextsHint.setProperty(u"variant", u"muted")

        self.settingsLayout.addWidget(self.contextsHint)

        self.contextsTable = QTableWidget(SettingsPage)
        if (self.contextsTable.columnCount() < 2):
            self.contextsTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.contextsTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.contextsTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.contextsTable.rowCount() < 2):
            self.contextsTable.setRowCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setText(u"prod-eks")
        self.contextsTable.setItem(0, 0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setText(u"Production")
        self.contextsTable.setItem(0, 1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setText(u"staging-eks")
        self.contextsTable.setItem(1, 0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setText(u"Staging")
        self.contextsTable.setItem(1, 1, __qtablewidgetitem5)
        self.contextsTable.setObjectName(u"contextsTable")
        self.contextsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.contextsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contextsTable.setProperty(u"variant", u"data")
        self.contextsTable.horizontalHeader().setStretchLastSection(True)
        self.contextsTable.verticalHeader().setVisible(False)
        self.contextsTable.verticalHeader().setDefaultSectionSize(40)

        self.settingsLayout.addWidget(self.contextsTable)


        self.retranslateUi(SettingsPage)

        QMetaObject.connectSlotsByName(SettingsPage)
    # setupUi

    def retranslateUi(self, SettingsPage):
        self.saveButton.setText(QCoreApplication.translate("SettingsPage", u"Save changes", None))
        self.generalHeading.setText(QCoreApplication.translate("SettingsPage", u"GENERAL", None))
        self.languageLabel.setText(QCoreApplication.translate("SettingsPage", u"Language", None))

        self.rememberCheck.setText(QCoreApplication.translate("SettingsPage", u"Remember the last used context", None))
        self.contextsHeading.setText(QCoreApplication.translate("SettingsPage", u"CONTEXT NAMES", None))
        self.contextsHint.setText(QCoreApplication.translate("SettingsPage", u"Give your contexts friendlier names. Leave a name empty to keep the original one.", None))
        ___qtablewidgetitem = self.contextsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SettingsPage", u"CONTEXT", None))
        ___qtablewidgetitem1 = self.contextsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SettingsPage", u"DISPLAY NAME", None))

        __sortingEnabled = self.contextsTable.isSortingEnabled()
        self.contextsTable.setSortingEnabled(False)
        self.contextsTable.setSortingEnabled(__sortingEnabled)

        pass
    # retranslateUi

