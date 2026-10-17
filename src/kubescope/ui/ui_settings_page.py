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
    QFormLayout, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTableWidget,
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

        self.defaultNamespaceLabel = QLabel(self.generalCard)
        self.defaultNamespaceLabel.setObjectName(u"defaultNamespaceLabel")

        self.generalForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.defaultNamespaceLabel)

        self.defaultNamespaceCombo = QComboBox(self.generalCard)
        self.defaultNamespaceCombo.setObjectName(u"defaultNamespaceCombo")
        self.defaultNamespaceCombo.setMinimumSize(QSize(200, 0))
        self.defaultNamespaceCombo.setProperty(u"variant", u"filter")

        self.generalForm.setWidget(1, QFormLayout.ItemRole.FieldRole, self.defaultNamespaceCombo)

        self.rememberCheck = QCheckBox(self.generalCard)
        self.rememberCheck.setObjectName(u"rememberCheck")
        self.rememberCheck.setChecked(True)

        self.generalForm.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.rememberCheck)

        self.updatesCheck = QCheckBox(self.generalCard)
        self.updatesCheck.setObjectName(u"updatesCheck")
        self.updatesCheck.setChecked(True)

        self.generalForm.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.updatesCheck)


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
        if (self.contextsTable.columnCount() < 2):
            self.contextsTable.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.contextsTable.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.contextsTable.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        if (self.contextsTable.rowCount() < 2):
            self.contextsTable.setRowCount(2)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setText(u"prod-eks")
        self.contextsTable.setItem(0, 0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setText(u"Production")
        self.contextsTable.setItem(0, 1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setText(u"staging-eks")
        self.contextsTable.setItem(1, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setText(u"Staging")
        self.contextsTable.setItem(1, 1, __qtablewidgetitem7)
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

        self.settingsScroll.setWidget(self.settingsContent)

        self.settingsLayout.addWidget(self.settingsScroll)


        self.retranslateUi(SettingsPage)

        QMetaObject.connectSlotsByName(SettingsPage)
    # setupUi

    def retranslateUi(self, SettingsPage):
        self.saveButton.setText(QCoreApplication.translate("SettingsPage", u"Save changes", None))
        self.generalHeading.setText(QCoreApplication.translate("SettingsPage", u"GENERAL", None))
        self.languageLabel.setText(QCoreApplication.translate("SettingsPage", u"Language", None))

        self.defaultNamespaceLabel.setText(QCoreApplication.translate("SettingsPage", u"Default namespace", None))
#if QT_CONFIG(tooltip)
        self.defaultNamespaceCombo.setToolTip(QCoreApplication.translate("SettingsPage", u"The namespace each context opens on. Leave empty to show all of them.", None))
#endif // QT_CONFIG(tooltip)
        self.rememberCheck.setText(QCoreApplication.translate("SettingsPage", u"Remember the last used context", None))
        self.updatesCheck.setText(QCoreApplication.translate("SettingsPage", u"Check GitHub for a new version when the app starts", None))
#if QT_CONFIG(tooltip)
        self.updatesCheck.setToolTip(QCoreApplication.translate("SettingsPage", u"Asks the public GitHub API for the latest release and sends nothing but the app version. The icon in the footer checks on demand.", None))
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
        self.contextsHeading.setText(QCoreApplication.translate("SettingsPage", u"CONTEXT NAMES", None))
        self.contextsHint.setText(QCoreApplication.translate("SettingsPage", u"Give your contexts friendlier names. Leave a name empty to keep the original one.", None))
        ___qtablewidgetitem2 = self.contextsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("SettingsPage", u"CONTEXT", None))
        ___qtablewidgetitem3 = self.contextsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("SettingsPage", u"DISPLAY NAME", None))

        __sortingEnabled = self.contextsTable.isSortingEnabled()
        self.contextsTable.setSortingEnabled(False)
        self.contextsTable.setSortingEnabled(__sortingEnabled)

        pass
    # retranslateUi

