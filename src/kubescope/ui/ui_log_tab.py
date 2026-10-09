# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_tab.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_LogTab(object):
    def setupUi(self, LogTab):
        if not LogTab.objectName():
            LogTab.setObjectName(u"LogTab")
        self.logLayout = QVBoxLayout(LogTab)
        self.logLayout.setSpacing(8)
        self.logLayout.setObjectName(u"logLayout")
        self.logLayout.setContentsMargins(0, 10, 0, 0)
        self.logToolbar = QHBoxLayout()
        self.logToolbar.setSpacing(12)
        self.logToolbar.setObjectName(u"logToolbar")
        self.autoCheck = QCheckBox(LogTab)
        self.autoCheck.setObjectName(u"autoCheck")
        self.autoCheck.setChecked(True)

        self.logToolbar.addWidget(self.autoCheck)

        self.refreshButton = QPushButton(LogTab)
        self.refreshButton.setObjectName(u"refreshButton")
        self.refreshButton.setProperty(u"variant", u"secondary")

        self.logToolbar.addWidget(self.refreshButton)

        self.logToolbarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.logToolbar.addItem(self.logToolbarSpacer)

        self.logStatus = QLabel(LogTab)
        self.logStatus.setObjectName(u"logStatus")
        self.logStatus.setText(u"")
        self.logStatus.setProperty(u"variant", u"muted")

        self.logToolbar.addWidget(self.logStatus)


        self.logLayout.addLayout(self.logToolbar)

        self.logText = QPlainTextEdit(LogTab)
        self.logText.setObjectName(u"logText")
        self.logText.setReadOnly(True)
        self.logText.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.logText.setPlainText(u"2026-10-08T05:00:01Z INFO server started\n"
"2026-10-08T05:00:02Z WARN slow query took 1.8s")

        self.logLayout.addWidget(self.logText)


        self.retranslateUi(LogTab)

        QMetaObject.connectSlotsByName(LogTab)
    # setupUi

    def retranslateUi(self, LogTab):
        self.autoCheck.setText(QCoreApplication.translate("LogTab", u"Auto-refresh", None))
#if QT_CONFIG(tooltip)
        self.autoCheck.setToolTip(QCoreApplication.translate("LogTab", u"Fetch new log lines every few seconds and follow the end of the log", None))
#endif // QT_CONFIG(tooltip)
        self.refreshButton.setText(QCoreApplication.translate("LogTab", u"Refresh now", None))
        pass
    # retranslateUi

