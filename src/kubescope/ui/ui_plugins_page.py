# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugins_page.ui'
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
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_PluginsPage(object):
    def setupUi(self, PluginsPage):
        if not PluginsPage.objectName():
            PluginsPage.setObjectName(u"PluginsPage")
        self.pluginsLayout = QVBoxLayout(PluginsPage)
        self.pluginsLayout.setSpacing(14)
        self.pluginsLayout.setObjectName(u"pluginsLayout")
        self.pluginsLayout.setContentsMargins(32, 24, 32, 22)
        self.pluginsHeaderRow = QHBoxLayout()
        self.pluginsHeaderRow.setSpacing(12)
        self.pluginsHeaderRow.setObjectName(u"pluginsHeaderRow")
        self.searchInput = QLineEdit(PluginsPage)
        self.searchInput.setObjectName(u"searchInput")
        self.searchInput.setClearButtonEnabled(True)

        self.pluginsHeaderRow.addWidget(self.searchInput)

        self.searchButton = QPushButton(PluginsPage)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setProperty(u"variant", u"primary")

        self.pluginsHeaderRow.addWidget(self.searchButton)


        self.pluginsLayout.addLayout(self.pluginsHeaderRow)

        self.statusLabel = QLabel(PluginsPage)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setWordWrap(True)

        self.pluginsLayout.addWidget(self.statusLabel)

        self.cardsScroll = QScrollArea(PluginsPage)
        self.cardsScroll.setObjectName(u"cardsScroll")
        self.cardsScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.cardsScroll.setWidgetResizable(True)
        self.cardsContent = QWidget()
        self.cardsContent.setObjectName(u"cardsContent")
        self.cardsGrid = QGridLayout(self.cardsContent)
        self.cardsGrid.setSpacing(14)
        self.cardsGrid.setObjectName(u"cardsGrid")
        self.cardsGrid.setContentsMargins(0, 0, 0, 0)
        self.cardsScroll.setWidget(self.cardsContent)

        self.pluginsLayout.addWidget(self.cardsScroll)

        self.pluginsLayout.setStretch(2, 1)

        self.retranslateUi(PluginsPage)

        QMetaObject.connectSlotsByName(PluginsPage)
    # setupUi

    def retranslateUi(self, PluginsPage):
        self.searchInput.setPlaceholderText(QCoreApplication.translate("PluginsPage", u"Search the charts of Artifact Hub...", None))
        self.searchButton.setText(QCoreApplication.translate("PluginsPage", u"Search", None))
        self.statusLabel.setText("")
        pass
    # retranslateUi

