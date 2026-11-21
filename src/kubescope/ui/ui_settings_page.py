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
    QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_SettingsPage(object):
    def setupUi(self, SettingsPage):
        if not SettingsPage.objectName():
            SettingsPage.setObjectName(u"SettingsPage")
        self.settingsLayout = QVBoxLayout(SettingsPage)
        self.settingsLayout.setSpacing(14)
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.settingsLayout.setContentsMargins(32, 24, 32, 22)
        self.settingsSections = QHBoxLayout()
        self.settingsSections.setObjectName(u"settingsSections")
        self.settingsSections.setContentsMargins(-1, -1, 16, -1)
        self.generalSectionButton = QPushButton(SettingsPage)
        self.generalSectionButton.setObjectName(u"generalSectionButton")
        self.generalSectionButton.setCheckable(True)
        self.generalSectionButton.setChecked(True)
        self.generalSectionButton.setProperty(u"variant", u"secondary")

        self.settingsSections.addWidget(self.generalSectionButton)

        self.kubeSectionButton = QPushButton(SettingsPage)
        self.kubeSectionButton.setObjectName(u"kubeSectionButton")
        self.kubeSectionButton.setCheckable(True)
        self.kubeSectionButton.setChecked(False)
        self.kubeSectionButton.setProperty(u"variant", u"secondary")

        self.settingsSections.addWidget(self.kubeSectionButton)

        self.shortcutsSectionButton = QPushButton(SettingsPage)
        self.shortcutsSectionButton.setObjectName(u"shortcutsSectionButton")
        self.shortcutsSectionButton.setCheckable(True)
        self.shortcutsSectionButton.setChecked(False)
        self.shortcutsSectionButton.setProperty(u"variant", u"secondary")

        self.settingsSections.addWidget(self.shortcutsSectionButton)

        self.integrationsSectionButton = QPushButton(SettingsPage)
        self.integrationsSectionButton.setObjectName(u"integrationsSectionButton")
        self.integrationsSectionButton.setCheckable(True)
        self.integrationsSectionButton.setChecked(False)
        self.integrationsSectionButton.setProperty(u"variant", u"secondary")

        self.settingsSections.addWidget(self.integrationsSectionButton)

        self.extensionsSectionButton = QPushButton(SettingsPage)
        self.extensionsSectionButton.setObjectName(u"extensionsSectionButton")
        self.extensionsSectionButton.setCheckable(True)
        self.extensionsSectionButton.setChecked(False)
        self.extensionsSectionButton.setProperty(u"variant", u"secondary")

        self.settingsSections.addWidget(self.extensionsSectionButton)

        self.settingsSectionsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.settingsSections.addItem(self.settingsSectionsSpacer)

        self.noticeLabel = QLabel(SettingsPage)
        self.noticeLabel.setObjectName(u"noticeLabel")
        self.noticeLabel.setText(u"")
        self.noticeLabel.setProperty(u"variant", u"muted")

        self.settingsSections.addWidget(self.noticeLabel)

        self.saveButton = QPushButton(SettingsPage)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setProperty(u"variant", u"primary")

        self.settingsSections.addWidget(self.saveButton)


        self.settingsLayout.addLayout(self.settingsSections)

        self.settingsScroll = QScrollArea(SettingsPage)
        self.settingsScroll.setObjectName(u"settingsScroll")
        self.settingsScroll.setFrameShape(QFrame.NoFrame)
        self.settingsScroll.setWidgetResizable(True)
        self.settingsContent = QWidget()
        self.settingsContent.setObjectName(u"settingsContent")
        self.settingsContentLayout = QVBoxLayout(self.settingsContent)
        self.settingsContentLayout.setSpacing(12)
        self.settingsContentLayout.setObjectName(u"settingsContentLayout")
        self.settingsContentLayout.setContentsMargins(0, 0, 16, 8)
        self.generalCard = QFrame(self.settingsContent)
        self.generalCard.setObjectName(u"generalCard")
        self.generalCard.setProperty(u"card", u"true")
        self.generalCardLayout = QVBoxLayout(self.generalCard)
        self.generalCardLayout.setSpacing(10)
        self.generalCardLayout.setObjectName(u"generalCardLayout")
        self.generalCardLayout.setContentsMargins(16, 14, 16, 14)
        self.generalHeading = QLabel(self.generalCard)
        self.generalHeading.setObjectName(u"generalHeading")
        self.generalHeading.setProperty(u"variant", u"cardTitle")

        self.generalCardLayout.addWidget(self.generalHeading)

        self.generalForm = QFormLayout()
        self.generalForm.setObjectName(u"generalForm")
        self.generalForm.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.generalForm.setHorizontalSpacing(16)
        self.generalForm.setVerticalSpacing(10)
        self.languageLabel = QLabel(self.generalCard)
        self.languageLabel.setObjectName(u"languageLabel")

        self.generalForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.languageLabel)

        self.languageCombo = QComboBox(self.generalCard)
        self.languageCombo.addItem(u"Automatic")
        self.languageCombo.addItem(u"English")
        self.languageCombo.addItem(u"Portugu\u00eas")
        self.languageCombo.setObjectName(u"languageCombo")
        self.languageCombo.setMinimumSize(QSize(200, 0))
        self.languageCombo.setProperty(u"variant", u"filter")

        self.generalForm.setWidget(0, QFormLayout.ItemRole.FieldRole, self.languageCombo)

        self.timezoneLabel = QLabel(self.generalCard)
        self.timezoneLabel.setObjectName(u"timezoneLabel")

        self.generalForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.timezoneLabel)

        self.timezoneCombo = QComboBox(self.generalCard)
        self.timezoneCombo.setObjectName(u"timezoneCombo")
        self.timezoneCombo.setMinimumSize(QSize(200, 0))
        self.timezoneCombo.setProperty(u"variant", u"filter")

        self.generalForm.setWidget(1, QFormLayout.ItemRole.FieldRole, self.timezoneCombo)

        self.defaultNamespaceLabel = QLabel(self.generalCard)
        self.defaultNamespaceLabel.setObjectName(u"defaultNamespaceLabel")

        self.generalForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.defaultNamespaceLabel)

        self.defaultNamespaceEdit = QLineEdit(self.generalCard)
        self.defaultNamespaceEdit.setObjectName(u"defaultNamespaceEdit")
        self.defaultNamespaceEdit.setMinimumSize(QSize(200, 0))
        self.defaultNamespaceEdit.setProperty(u"variant", u"filter")

        self.generalForm.setWidget(2, QFormLayout.ItemRole.FieldRole, self.defaultNamespaceEdit)

        self.terminalLabel = QLabel(self.generalCard)
        self.terminalLabel.setObjectName(u"terminalLabel")

        self.generalForm.setWidget(3, QFormLayout.ItemRole.LabelRole, self.terminalLabel)

        self.terminalCombo = QComboBox(self.generalCard)
        self.terminalCombo.setObjectName(u"terminalCombo")
        self.terminalCombo.setMinimumSize(QSize(200, 0))
        self.terminalCombo.setProperty(u"variant", u"filter")

        self.generalForm.setWidget(3, QFormLayout.ItemRole.FieldRole, self.terminalCombo)

        self.terminalCommandEdit = QLineEdit(self.generalCard)
        self.terminalCommandEdit.setObjectName(u"terminalCommandEdit")
        self.terminalCommandEdit.setMinimumSize(QSize(200, 0))
        self.terminalCommandEdit.setPlaceholderText(u"alacritty -e")
        self.terminalCommandEdit.setProperty(u"variant", u"filter")

        self.generalForm.setWidget(4, QFormLayout.ItemRole.FieldRole, self.terminalCommandEdit)

        self.rememberCheck = QCheckBox(self.generalCard)
        self.rememberCheck.setObjectName(u"rememberCheck")
        self.rememberCheck.setChecked(True)

        self.generalForm.setWidget(5, QFormLayout.ItemRole.SpanningRole, self.rememberCheck)

        self.updatesCheck = QCheckBox(self.generalCard)
        self.updatesCheck.setObjectName(u"updatesCheck")
        self.updatesCheck.setChecked(True)

        self.generalForm.setWidget(6, QFormLayout.ItemRole.SpanningRole, self.updatesCheck)

        self.backgroundCheck = QCheckBox(self.generalCard)
        self.backgroundCheck.setObjectName(u"backgroundCheck")
        self.backgroundCheck.setChecked(True)

        self.generalForm.setWidget(7, QFormLayout.ItemRole.SpanningRole, self.backgroundCheck)

        self.titleBarCheck = QCheckBox(self.generalCard)
        self.titleBarCheck.setObjectName(u"titleBarCheck")

        self.generalForm.setWidget(8, QFormLayout.ItemRole.SpanningRole, self.titleBarCheck)

        self.animationsCheck = QCheckBox(self.generalCard)
        self.animationsCheck.setObjectName(u"animationsCheck")

        self.generalForm.setWidget(9, QFormLayout.ItemRole.SpanningRole, self.animationsCheck)


        self.generalCardLayout.addLayout(self.generalForm)


        self.settingsContentLayout.addWidget(self.generalCard)

        self.appearanceCard = QFrame(self.settingsContent)
        self.appearanceCard.setObjectName(u"appearanceCard")
        self.appearanceCard.setProperty(u"card", u"true")
        self.appearanceCardLayout = QVBoxLayout(self.appearanceCard)
        self.appearanceCardLayout.setSpacing(10)
        self.appearanceCardLayout.setObjectName(u"appearanceCardLayout")
        self.appearanceCardLayout.setContentsMargins(16, 14, 16, 14)
        self.appearanceHeading = QLabel(self.appearanceCard)
        self.appearanceHeading.setObjectName(u"appearanceHeading")
        self.appearanceHeading.setProperty(u"variant", u"cardTitle")

        self.appearanceCardLayout.addWidget(self.appearanceHeading)

        self.appearanceForm = QFormLayout()
        self.appearanceForm.setObjectName(u"appearanceForm")
        self.appearanceForm.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.appearanceForm.setHorizontalSpacing(16)
        self.appearanceForm.setVerticalSpacing(10)
        self.themeLabel = QLabel(self.appearanceCard)
        self.themeLabel.setObjectName(u"themeLabel")

        self.appearanceForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.themeLabel)

        self.themeCombo = QComboBox(self.appearanceCard)
        self.themeCombo.addItem(u"Light")
        self.themeCombo.addItem(u"Dark")
        self.themeCombo.setObjectName(u"themeCombo")
        self.themeCombo.setMinimumSize(QSize(200, 0))
        self.themeCombo.setProperty(u"variant", u"filter")

        self.appearanceForm.setWidget(0, QFormLayout.ItemRole.FieldRole, self.themeCombo)

        self.themeButtonsRow = QHBoxLayout()
        self.themeButtonsRow.setSpacing(8)
        self.themeButtonsRow.setObjectName(u"themeButtonsRow")
        self.newThemeButton = QPushButton(self.appearanceCard)
        self.newThemeButton.setObjectName(u"newThemeButton")
        self.newThemeButton.setProperty(u"variant", u"secondary")

        self.themeButtonsRow.addWidget(self.newThemeButton)

        self.editThemeButton = QPushButton(self.appearanceCard)
        self.editThemeButton.setObjectName(u"editThemeButton")
        self.editThemeButton.setProperty(u"variant", u"secondary")

        self.themeButtonsRow.addWidget(self.editThemeButton)

        self.deleteThemeButton = QPushButton(self.appearanceCard)
        self.deleteThemeButton.setObjectName(u"deleteThemeButton")
        self.deleteThemeButton.setProperty(u"variant", u"secondary")

        self.themeButtonsRow.addWidget(self.deleteThemeButton)

        self.openThemesButton = QPushButton(self.appearanceCard)
        self.openThemesButton.setObjectName(u"openThemesButton")
        self.openThemesButton.setProperty(u"variant", u"secondary")

        self.themeButtonsRow.addWidget(self.openThemesButton)

        self.themeButtonsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.themeButtonsRow.addItem(self.themeButtonsSpacer)


        self.appearanceForm.setLayout(1, QFormLayout.ItemRole.SpanningRole, self.themeButtonsRow)


        self.appearanceCardLayout.addLayout(self.appearanceForm)


        self.settingsContentLayout.addWidget(self.appearanceCard)

        self.accessCard = QFrame(self.settingsContent)
        self.accessCard.setObjectName(u"accessCard")
        self.accessCard.setProperty(u"card", u"true")
        self.accessCardLayout = QVBoxLayout(self.accessCard)
        self.accessCardLayout.setSpacing(10)
        self.accessCardLayout.setObjectName(u"accessCardLayout")
        self.accessCardLayout.setContentsMargins(16, 14, 16, 14)
        self.accessHeading = QLabel(self.accessCard)
        self.accessHeading.setObjectName(u"accessHeading")
        self.accessHeading.setProperty(u"variant", u"cardTitle")

        self.accessCardLayout.addWidget(self.accessHeading)

        self.writeModeCheck = QCheckBox(self.accessCard)
        self.writeModeCheck.setObjectName(u"writeModeCheck")

        self.accessCardLayout.addWidget(self.writeModeCheck)


        self.settingsContentLayout.addWidget(self.accessCard)

        self.debugCard = QFrame(self.settingsContent)
        self.debugCard.setObjectName(u"debugCard")
        self.debugCard.setProperty(u"card", u"true")
        self.debugCardLayout = QVBoxLayout(self.debugCard)
        self.debugCardLayout.setSpacing(10)
        self.debugCardLayout.setObjectName(u"debugCardLayout")
        self.debugCardLayout.setContentsMargins(16, 14, 16, 14)
        self.debugHeading = QLabel(self.debugCard)
        self.debugHeading.setObjectName(u"debugHeading")
        self.debugHeading.setProperty(u"variant", u"cardTitle")

        self.debugCardLayout.addWidget(self.debugHeading)

        self.debugCheck = QCheckBox(self.debugCard)
        self.debugCheck.setObjectName(u"debugCheck")

        self.debugCardLayout.addWidget(self.debugCheck)

        self.debugHint = QLabel(self.debugCard)
        self.debugHint.setObjectName(u"debugHint")
        self.debugHint.setText(u"")
        self.debugHint.setWordWrap(True)
        self.debugHint.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.debugHint.setProperty(u"variant", u"muted")

        self.debugCardLayout.addWidget(self.debugHint)

        self.logButtonsRow = QHBoxLayout()
        self.logButtonsRow.setObjectName(u"logButtonsRow")
        self.openLogsButton = QPushButton(self.debugCard)
        self.openLogsButton.setObjectName(u"openLogsButton")
        self.openLogsButton.setProperty(u"variant", u"secondary")

        self.logButtonsRow.addWidget(self.openLogsButton)

        self.clearCacheButton = QPushButton(self.debugCard)
        self.clearCacheButton.setObjectName(u"clearCacheButton")
        self.clearCacheButton.setProperty(u"variant", u"secondary")

        self.logButtonsRow.addWidget(self.clearCacheButton)

        self.logButtonsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.logButtonsRow.addItem(self.logButtonsSpacer)


        self.debugCardLayout.addLayout(self.logButtonsRow)


        self.settingsContentLayout.addWidget(self.debugCard)

        self.kubeconfigCard = QFrame(self.settingsContent)
        self.kubeconfigCard.setObjectName(u"kubeconfigCard")
        self.kubeconfigCard.setProperty(u"card", u"true")
        self.kubeconfigCardLayout = QVBoxLayout(self.kubeconfigCard)
        self.kubeconfigCardLayout.setSpacing(10)
        self.kubeconfigCardLayout.setObjectName(u"kubeconfigCardLayout")
        self.kubeconfigCardLayout.setContentsMargins(16, 14, 16, 14)
        self.kubeconfigHeading = QLabel(self.kubeconfigCard)
        self.kubeconfigHeading.setObjectName(u"kubeconfigHeading")
        self.kubeconfigHeading.setWordWrap(True)
        self.kubeconfigHeading.setProperty(u"variant", u"cardTitle")

        self.kubeconfigCardLayout.addWidget(self.kubeconfigHeading)

        self.kubeconfigHint = QLabel(self.kubeconfigCard)
        self.kubeconfigHint.setObjectName(u"kubeconfigHint")
        self.kubeconfigHint.setWordWrap(True)
        self.kubeconfigHint.setProperty(u"variant", u"muted")

        self.kubeconfigCardLayout.addWidget(self.kubeconfigHint)

        self.kubeconfigList = QListWidget(self.kubeconfigCard)
        self.kubeconfigList.setObjectName(u"kubeconfigList")
        self.kubeconfigList.setMinimumSize(QSize(0, 90))
        self.kubeconfigList.setProperty(u"variant", u"data")

        self.kubeconfigCardLayout.addWidget(self.kubeconfigList)

        self.kubeconfigButtonsRow = QHBoxLayout()
        self.kubeconfigButtonsRow.setObjectName(u"kubeconfigButtonsRow")
        self.kubeconfigAddButton = QPushButton(self.kubeconfigCard)
        self.kubeconfigAddButton.setObjectName(u"kubeconfigAddButton")
        self.kubeconfigAddButton.setProperty(u"variant", u"secondary")

        self.kubeconfigButtonsRow.addWidget(self.kubeconfigAddButton)

        self.kubeconfigRemoveButton = QPushButton(self.kubeconfigCard)
        self.kubeconfigRemoveButton.setObjectName(u"kubeconfigRemoveButton")
        self.kubeconfigRemoveButton.setProperty(u"variant", u"secondary")

        self.kubeconfigButtonsRow.addWidget(self.kubeconfigRemoveButton)

        self.kubeconfigButtonsRowSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kubeconfigButtonsRow.addItem(self.kubeconfigButtonsRowSpacer)


        self.kubeconfigCardLayout.addLayout(self.kubeconfigButtonsRow)


        self.settingsContentLayout.addWidget(self.kubeconfigCard)

        self.loginCard = QFrame(self.settingsContent)
        self.loginCard.setObjectName(u"loginCard")
        self.loginCard.setProperty(u"card", u"true")
        self.loginCardLayout = QVBoxLayout(self.loginCard)
        self.loginCardLayout.setSpacing(10)
        self.loginCardLayout.setObjectName(u"loginCardLayout")
        self.loginCardLayout.setContentsMargins(16, 14, 16, 14)
        self.loginHeading = QLabel(self.loginCard)
        self.loginHeading.setObjectName(u"loginHeading")
        self.loginHeading.setWordWrap(True)
        self.loginHeading.setProperty(u"variant", u"cardTitle")

        self.loginCardLayout.addWidget(self.loginHeading)

        self.loginHint = QLabel(self.loginCard)
        self.loginHint.setObjectName(u"loginHint")
        self.loginHint.setWordWrap(True)
        self.loginHint.setProperty(u"variant", u"muted")

        self.loginCardLayout.addWidget(self.loginHint)

        self.loginTable = QTableWidget(self.loginCard)
        if (self.loginTable.columnCount() < 2):
            self.loginTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.loginTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.loginTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.loginTable.setObjectName(u"loginTable")
        self.loginTable.setMinimumSize(QSize(0, 120))
        self.loginTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.loginTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.loginTable.setProperty(u"variant", u"data")
        self.loginTable.horizontalHeader().setStretchLastSection(True)
        self.loginTable.verticalHeader().setVisible(False)

        self.loginCardLayout.addWidget(self.loginTable)

        self.loginButtonsRow = QHBoxLayout()
        self.loginButtonsRow.setObjectName(u"loginButtonsRow")
        self.loginAddButton = QPushButton(self.loginCard)
        self.loginAddButton.setObjectName(u"loginAddButton")
        self.loginAddButton.setProperty(u"variant", u"secondary")

        self.loginButtonsRow.addWidget(self.loginAddButton)

        self.loginRemoveButton = QPushButton(self.loginCard)
        self.loginRemoveButton.setObjectName(u"loginRemoveButton")
        self.loginRemoveButton.setProperty(u"variant", u"secondary")

        self.loginButtonsRow.addWidget(self.loginRemoveButton)

        self.loginButtonsRowSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.loginButtonsRow.addItem(self.loginButtonsRowSpacer)


        self.loginCardLayout.addLayout(self.loginButtonsRow)


        self.settingsContentLayout.addWidget(self.loginCard)

        self.integrationsCard = QFrame(self.settingsContent)
        self.integrationsCard.setObjectName(u"integrationsCard")
        self.integrationsCard.setProperty(u"card", u"true")
        self.integrationsLayout = QVBoxLayout(self.integrationsCard)
        self.integrationsLayout.setSpacing(14)
        self.integrationsLayout.setObjectName(u"integrationsLayout")
        self.integrationsLayout.setContentsMargins(16, 14, 16, 14)

        self.settingsContentLayout.addWidget(self.integrationsCard)

        self.extensionsCard = QFrame(self.settingsContent)
        self.extensionsCard.setObjectName(u"extensionsCard")
        self.extensionsCard.setProperty(u"card", u"true")
        self.extensionsCardLayout = QVBoxLayout(self.extensionsCard)
        self.extensionsCardLayout.setSpacing(10)
        self.extensionsCardLayout.setObjectName(u"extensionsCardLayout")
        self.extensionsCardLayout.setContentsMargins(16, 14, 16, 14)
        self.extensionsHeading = QLabel(self.extensionsCard)
        self.extensionsHeading.setObjectName(u"extensionsHeading")
        self.extensionsHeading.setProperty(u"variant", u"cardTitle")

        self.extensionsCardLayout.addWidget(self.extensionsHeading)

        self.extensionsHint = QLabel(self.extensionsCard)
        self.extensionsHint.setObjectName(u"extensionsHint")
        self.extensionsHint.setWordWrap(True)
        self.extensionsHint.setProperty(u"variant", u"muted")

        self.extensionsCardLayout.addWidget(self.extensionsHint)

        self.extensionsButtonsRow = QHBoxLayout()
        self.extensionsButtonsRow.setObjectName(u"extensionsButtonsRow")
        self.extensionsInstallFolderButton = QPushButton(self.extensionsCard)
        self.extensionsInstallFolderButton.setObjectName(u"extensionsInstallFolderButton")
        self.extensionsInstallFolderButton.setProperty(u"variant", u"secondary")

        self.extensionsButtonsRow.addWidget(self.extensionsInstallFolderButton)

        self.extensionsInstallRepoButton = QPushButton(self.extensionsCard)
        self.extensionsInstallRepoButton.setObjectName(u"extensionsInstallRepoButton")
        self.extensionsInstallRepoButton.setProperty(u"variant", u"secondary")

        self.extensionsButtonsRow.addWidget(self.extensionsInstallRepoButton)

        self.extensionsDevCheck = QCheckBox(self.extensionsCard)
        self.extensionsDevCheck.setObjectName(u"extensionsDevCheck")

        self.extensionsButtonsRow.addWidget(self.extensionsDevCheck)

        self.extensionsButtonsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.extensionsButtonsRow.addItem(self.extensionsButtonsSpacer)


        self.extensionsCardLayout.addLayout(self.extensionsButtonsRow)

        self.extensionsCardsHost = QWidget(self.extensionsCard)
        self.extensionsCardsHost.setObjectName(u"extensionsCardsHost")
        self.extensionsCardsGrid = QGridLayout(self.extensionsCardsHost)
        self.extensionsCardsGrid.setSpacing(14)
        self.extensionsCardsGrid.setObjectName(u"extensionsCardsGrid")
        self.extensionsCardsGrid.setContentsMargins(0, 4, 0, 0)

        self.extensionsCardLayout.addWidget(self.extensionsCardsHost)


        self.settingsContentLayout.addWidget(self.extensionsCard)

        self.shortcutsCard = QFrame(self.settingsContent)
        self.shortcutsCard.setObjectName(u"shortcutsCard")
        self.shortcutsCard.setProperty(u"card", u"true")
        self.shortcutsCardLayout = QVBoxLayout(self.shortcutsCard)
        self.shortcutsCardLayout.setSpacing(10)
        self.shortcutsCardLayout.setObjectName(u"shortcutsCardLayout")
        self.shortcutsCardLayout.setContentsMargins(16, 14, 16, 14)
        self.shortcutsHeading = QLabel(self.shortcutsCard)
        self.shortcutsHeading.setObjectName(u"shortcutsHeading")
        self.shortcutsHeading.setProperty(u"variant", u"cardTitle")

        self.shortcutsCardLayout.addWidget(self.shortcutsHeading)

        self.shortcutsHint = QLabel(self.shortcutsCard)
        self.shortcutsHint.setObjectName(u"shortcutsHint")
        self.shortcutsHint.setWordWrap(True)
        self.shortcutsHint.setProperty(u"variant", u"muted")

        self.shortcutsCardLayout.addWidget(self.shortcutsHint)

        self.shortcutsTable = QTableWidget(self.shortcutsCard)
        if (self.shortcutsTable.columnCount() < 2):
            self.shortcutsTable.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.shortcutsTable.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.shortcutsTable.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        self.shortcutsTable.setObjectName(u"shortcutsTable")
        self.shortcutsTable.setMinimumSize(QSize(0, 300))
        self.shortcutsTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.shortcutsTable.setProperty(u"variant", u"data")
        self.shortcutsTable.horizontalHeader().setStretchLastSection(True)
        self.shortcutsTable.verticalHeader().setVisible(False)

        self.shortcutsCardLayout.addWidget(self.shortcutsTable)

        self.shortcutsButtonsRow = QHBoxLayout()
        self.shortcutsButtonsRow.setObjectName(u"shortcutsButtonsRow")
        self.shortcutsResetButton = QPushButton(self.shortcutsCard)
        self.shortcutsResetButton.setObjectName(u"shortcutsResetButton")
        self.shortcutsResetButton.setProperty(u"variant", u"secondary")

        self.shortcutsButtonsRow.addWidget(self.shortcutsResetButton)

        self.shortcutsButtonsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.shortcutsButtonsRow.addItem(self.shortcutsButtonsSpacer)


        self.shortcutsCardLayout.addLayout(self.shortcutsButtonsRow)


        self.settingsContentLayout.addWidget(self.shortcutsCard)

        self.contextsCard = QFrame(self.settingsContent)
        self.contextsCard.setObjectName(u"contextsCard")
        self.contextsCard.setProperty(u"card", u"true")
        self.contextsCardLayout = QVBoxLayout(self.contextsCard)
        self.contextsCardLayout.setSpacing(10)
        self.contextsCardLayout.setObjectName(u"contextsCardLayout")
        self.contextsCardLayout.setContentsMargins(16, 14, 16, 14)
        self.contextsHeading = QLabel(self.contextsCard)
        self.contextsHeading.setObjectName(u"contextsHeading")
        self.contextsHeading.setProperty(u"variant", u"cardTitle")

        self.contextsCardLayout.addWidget(self.contextsHeading)

        self.contextsHint = QLabel(self.contextsCard)
        self.contextsHint.setObjectName(u"contextsHint")
        self.contextsHint.setWordWrap(True)
        self.contextsHint.setProperty(u"variant", u"muted")

        self.contextsCardLayout.addWidget(self.contextsHint)

        self.contextsTable = QTableWidget(self.contextsCard)
        if (self.contextsTable.columnCount() < 3):
            self.contextsTable.setColumnCount(3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.contextsTable.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.contextsTable.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.contextsTable.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        if (self.contextsTable.rowCount() < 2):
            self.contextsTable.setRowCount(2)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setText(u"prod-eks")
        self.contextsTable.setItem(0, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setText(u"Production")
        self.contextsTable.setItem(0, 1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setText(u"staging-eks")
        self.contextsTable.setItem(1, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setText(u"Staging")
        self.contextsTable.setItem(1, 1, __qtablewidgetitem10)
        self.contextsTable.setObjectName(u"contextsTable")
        self.contextsTable.setMinimumSize(QSize(0, 260))
        self.contextsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.contextsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.contextsTable.setProperty(u"variant", u"data")
        self.contextsTable.horizontalHeader().setStretchLastSection(True)
        self.contextsTable.verticalHeader().setVisible(False)
        self.contextsTable.verticalHeader().setDefaultSectionSize(40)

        self.contextsCardLayout.addWidget(self.contextsTable)


        self.settingsContentLayout.addWidget(self.contextsCard)

        self.settingsContentSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settingsContentLayout.addItem(self.settingsContentSpacer)

        self.settingsScroll.setWidget(self.settingsContent)

        self.settingsLayout.addWidget(self.settingsScroll)


        self.retranslateUi(SettingsPage)

        QMetaObject.connectSlotsByName(SettingsPage)
    # setupUi

    def retranslateUi(self, SettingsPage):
        self.generalSectionButton.setText(QCoreApplication.translate("SettingsPage", u"General", None))
        self.kubeSectionButton.setText(QCoreApplication.translate("SettingsPage", u"Kube", None))
        self.shortcutsSectionButton.setText(QCoreApplication.translate("SettingsPage", u"Shortcuts", None))
        self.integrationsSectionButton.setText(QCoreApplication.translate("SettingsPage", u"Integrations", None))
        self.extensionsSectionButton.setText(QCoreApplication.translate("SettingsPage", u"Extensions", None))
#if QT_CONFIG(tooltip)
        self.saveButton.setToolTip(QCoreApplication.translate("SettingsPage", u"Save changes", None))
#endif // QT_CONFIG(tooltip)
        self.generalHeading.setText(QCoreApplication.translate("SettingsPage", u"GENERAL", None))
        self.languageLabel.setText(QCoreApplication.translate("SettingsPage", u"Language", None))

        self.timezoneLabel.setText(QCoreApplication.translate("SettingsPage", u"Time zone", None))
        self.defaultNamespaceLabel.setText(QCoreApplication.translate("SettingsPage", u"Default namespace", None))
#if QT_CONFIG(tooltip)
        self.defaultNamespaceEdit.setToolTip(QCoreApplication.translate("SettingsPage", u"The namespace each context opens on. Leave empty to show all of them.", None))
#endif // QT_CONFIG(tooltip)
        self.defaultNamespaceEdit.setPlaceholderText(QCoreApplication.translate("SettingsPage", u"All namespaces", None))
        self.terminalLabel.setText(QCoreApplication.translate("SettingsPage", u"Terminal", None))
#if QT_CONFIG(tooltip)
        self.terminalCombo.setToolTip(QCoreApplication.translate("SettingsPage", u"The terminal that opens for a shell in a Pod, a port-forward or a sign-in that asks for keys. Automatic uses the first one the computer has.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.terminalCommandEdit.setToolTip(QCoreApplication.translate("SettingsPage", u"The program and what it needs before the command it runs, for example: alacritty -e", None))
#endif // QT_CONFIG(tooltip)
        self.rememberCheck.setText(QCoreApplication.translate("SettingsPage", u"Remember the last used context", None))
        self.updatesCheck.setText(QCoreApplication.translate("SettingsPage", u"Check GitHub for a new version when the app starts and every hour", None))
#if QT_CONFIG(tooltip)
        self.updatesCheck.setToolTip(QCoreApplication.translate("SettingsPage", u"Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.", None))
#endif // QT_CONFIG(tooltip)
        self.backgroundCheck.setText(QCoreApplication.translate("SettingsPage", u"Keep running in the background, with an icon in the system tray", None))
#if QT_CONFIG(tooltip)
        self.backgroundCheck.setToolTip(QCoreApplication.translate("SettingsPage", u"Closing the window hides it instead of quitting; click the tray icon to bring it back, or choose Quit in its menu. It has no effect where the desktop shows no system tray.", None))
#endif // QT_CONFIG(tooltip)
        self.titleBarCheck.setText(QCoreApplication.translate("SettingsPage", u"Use the title bar of the system", None))
#if QT_CONFIG(tooltip)
        self.titleBarCheck.setToolTip(QCoreApplication.translate("SettingsPage", u"Off by default: the window draws its own title bar in the top bar, which saves a row of space. Turn it on if moving or resizing the window misbehaves on your desktop.", None))
#endif // QT_CONFIG(tooltip)
        self.animationsCheck.setText(QCoreApplication.translate("SettingsPage", u"Animate windows and lists as they open", None))
#if QT_CONFIG(tooltip)
        self.animationsCheck.setToolTip(QCoreApplication.translate("SettingsPage", u"On by default: a window or a list rises into place as it first shows. Turn it off to show everything at once.", None))
#endif // QT_CONFIG(tooltip)
        self.appearanceHeading.setText(QCoreApplication.translate("SettingsPage", u"APPEARANCE", None))
        self.themeLabel.setText(QCoreApplication.translate("SettingsPage", u"Theme", None))

        self.newThemeButton.setText(QCoreApplication.translate("SettingsPage", u"New theme...", None))
        self.editThemeButton.setText(QCoreApplication.translate("SettingsPage", u"Edit theme...", None))
        self.deleteThemeButton.setText(QCoreApplication.translate("SettingsPage", u"Delete theme...", None))
        self.openThemesButton.setText(QCoreApplication.translate("SettingsPage", u"Open the themes folder", None))
        self.accessHeading.setText(QCoreApplication.translate("SettingsPage", u"CLUSTER ACCESS", None))
        self.writeModeCheck.setText(QCoreApplication.translate("SettingsPage", u"Write mode: allow actions that change the cluster", None))
#if QT_CONFIG(tooltip)
        self.writeModeCheck.setToolTip(QCoreApplication.translate("SettingsPage", u"Shows, in the right-click menu, the actions that change a cluster: delete or evict a Pod, scale or restart a Deployment. Each one asks for confirmation. It also shows the kubectl command to open a shell in a Pod. Off keeps the app read-only.", None))
#endif // QT_CONFIG(tooltip)
        self.debugHeading.setText(QCoreApplication.translate("SettingsPage", u"DEBUGGING", None))
        self.debugCheck.setText(QCoreApplication.translate("SettingsPage", u"Debug mode: write a log file I can share", None))
        self.openLogsButton.setText(QCoreApplication.translate("SettingsPage", u"Open the log folder", None))
        self.clearCacheButton.setText(QCoreApplication.translate("SettingsPage", u"Clear the cache", None))
#if QT_CONFIG(tooltip)
        self.clearCacheButton.setToolTip(QCoreApplication.translate("SettingsPage", u"Forgets the lists and overviews already loaded and the sign-in of every cluster, so the next request signs in and loads everything again. Your settings are kept.", None))
#endif // QT_CONFIG(tooltip)
        self.kubeconfigHeading.setText(QCoreApplication.translate("SettingsPage", u"KUBECONFIG FILES", None))
        self.kubeconfigHint.setText(QCoreApplication.translate("SettingsPage", u"KubeScope reads the files in the KUBECONFIG variable, or ~/.kube/config. Add files here to read those instead. Press Save to apply.", None))
        self.kubeconfigAddButton.setText(QCoreApplication.translate("SettingsPage", u"Add file...", None))
        self.kubeconfigRemoveButton.setText(QCoreApplication.translate("SettingsPage", u"Remove", None))
        self.loginHeading.setText(QCoreApplication.translate("SettingsPage", u"SIGN-IN COMMANDS", None))
        self.loginHint.setText(QCoreApplication.translate("SettingsPage", u"For a cloud KubeScope does not know, give the program your kubeconfig uses to sign in (for example oci) and the command that signs you in (for example oci session authenticate). The Sign in button then runs it, without a shell. Press Save to apply.", None))
        ___qtablewidgetitem = self.loginTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SettingsPage", u"PROGRAM", None))
        ___qtablewidgetitem1 = self.loginTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SettingsPage", u"SIGN-IN COMMAND", None))
        self.loginAddButton.setText(QCoreApplication.translate("SettingsPage", u"Add row", None))
        self.loginRemoveButton.setText(QCoreApplication.translate("SettingsPage", u"Remove", None))
        self.extensionsHeading.setText(QCoreApplication.translate("SettingsPage", u"EXTENSIONS", None))
        self.extensionsHint.setText(QCoreApplication.translate("SettingsPage", u"An extension adds a feature to KubeScope. It is code that runs with your permissions, so install only the ones you trust. KubeScope looks for the kubescope-extension.toml in the folder or the repository you give it. Changes apply the next time KubeScope starts.", None))
        self.extensionsInstallFolderButton.setText(QCoreApplication.translate("SettingsPage", u"Install from a folder...", None))
        self.extensionsInstallRepoButton.setText(QCoreApplication.translate("SettingsPage", u"Install from GitHub...", None))
        self.extensionsDevCheck.setText(QCoreApplication.translate("SettingsPage", u"Development mode", None))
#if QT_CONFIG(tooltip)
        self.extensionsDevCheck.setToolTip(QCoreApplication.translate("SettingsPage", u"Run the extension from its own folder, without a copy, and reload it when its files change. Only for a folder.", None))
#endif // QT_CONFIG(tooltip)
        self.shortcutsHeading.setText(QCoreApplication.translate("SettingsPage", u"KEYBOARD SHORTCUTS", None))
        self.shortcutsHint.setText(QCoreApplication.translate("SettingsPage", u"Click a shortcut and press the keys you want (two keys one after the other, like G then P, work too); Backspace clears it, and a shortcut left empty is off. Press Save to apply.", None))
        ___qtablewidgetitem2 = self.shortcutsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("SettingsPage", u"ACTION", None))
        ___qtablewidgetitem3 = self.shortcutsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("SettingsPage", u"SHORTCUT", None))
        self.shortcutsResetButton.setText(QCoreApplication.translate("SettingsPage", u"Restore defaults", None))
        self.contextsHeading.setText(QCoreApplication.translate("SettingsPage", u"CONTEXTS", None))
        self.contextsHint.setText(QCoreApplication.translate("SettingsPage", u"Give your contexts friendlier names. Leave a name empty to keep the original one.", None))
        ___qtablewidgetitem4 = self.contextsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("SettingsPage", u"CONTEXT", None))
        ___qtablewidgetitem5 = self.contextsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("SettingsPage", u"DISPLAY NAME", None))
        ___qtablewidgetitem6 = self.contextsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("SettingsPage", u"CONNECTED", None))

        __sortingEnabled = self.contextsTable.isSortingEnabled()
        self.contextsTable.setSortingEnabled(False)
        self.contextsTable.setSortingEnabled(__sortingEnabled)

        pass
    # retranslateUi

