# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'viewer_page.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_ViewerPage(object):
    def setupUi(self, ViewerPage):
        if not ViewerPage.objectName():
            ViewerPage.setObjectName(u"ViewerPage")
        self.viewerLayout = QVBoxLayout(ViewerPage)
        self.viewerLayout.setObjectName(u"viewerLayout")
        self.viewerLayout.setContentsMargins(32, 20, 32, 22)
        self.viewerTabs = QTabWidget(ViewerPage)
        self.viewerTabs.setObjectName(u"viewerTabs")
        self.viewerTabs.setTabsClosable(True)
        self.viewerTabs.setMovable(True)
        self.viewerTabs.setDocumentMode(True)
        self.sampleTab = QWidget()
        self.sampleTab.setObjectName(u"sampleTab")
        self.sampleLayout = QVBoxLayout(self.sampleTab)
        self.sampleLayout.setObjectName(u"sampleLayout")
        self.sampleLayout.setContentsMargins(0, 0, 0, 0)
        self.sampleText = QPlainTextEdit(self.sampleTab)
        self.sampleText.setObjectName(u"sampleText")
        self.sampleText.setReadOnly(True)
        self.sampleText.setPlainText(u"{\n"
"  \"kind\": \"Deployment\",\n"
"  \"metadata\": {\"name\": \"api\", \"namespace\": \"default\"},\n"
"  \"spec\": {\"replicas\": 3}\n"
"}")

        self.sampleLayout.addWidget(self.sampleText)

        self.viewerTabs.addTab(self.sampleTab, "")
        self.viewerTabs.setTabText(self.viewerTabs.indexOf(self.sampleTab), u"Deployment: api")

        self.viewerLayout.addWidget(self.viewerTabs)

        self.viewerFooter = QHBoxLayout()
        self.viewerFooter.setObjectName(u"viewerFooter")
        self.viewerFooterSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.viewerFooter.addItem(self.viewerFooterSpacer)

        self.saveButton = QPushButton(ViewerPage)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMinimumSize(QSize(36, 36))
        self.saveButton.setMaximumSize(QSize(36, 36))
        self.saveButton.setIconSize(QSize(18, 18))
        self.saveButton.setProperty(u"variant", u"secondary")

        self.viewerFooter.addWidget(self.saveButton)


        self.viewerLayout.addLayout(self.viewerFooter)


        self.retranslateUi(ViewerPage)

        QMetaObject.connectSlotsByName(ViewerPage)
    # setupUi

    def retranslateUi(self, ViewerPage):
#if QT_CONFIG(tooltip)
        self.saveButton.setToolTip(QCoreApplication.translate("ViewerPage", u"Save what this tab shows to a file", None))
#endif // QT_CONFIG(tooltip)
        pass
    # retranslateUi

