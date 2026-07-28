# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CheckBox, ComboBox, LineEdit,
    PushButton)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(950, 659)
        MainWindow.setMinimumSize(QSize(950, 659))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_7 = QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_15 = QGridLayout(self.tab_3)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.horizontalLayout_nparts = QHBoxLayout()
        self.horizontalLayout_nparts.setObjectName(u"horizontalLayout_nparts")
        self.label_nparts = BodyLabel(self.tab_3)
        self.label_nparts.setObjectName(u"label_nparts")

        self.horizontalLayout_nparts.addWidget(self.label_nparts)

        self.nparts = ComboBox(self.tab_3)
        self.nparts.addItem("")
        self.nparts.addItem("")
        self.nparts.addItem("")
        self.nparts.addItem("")
        self.nparts.addItem("")
        self.nparts.setObjectName(u"nparts")

        self.horizontalLayout_nparts.addWidget(self.nparts)


        self.gridLayout_15.addLayout(self.horizontalLayout_nparts, 0, 0, 1, 1)

        self.tabWidget_4 = QTabWidget(self.tab_3)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.gridLayout_17 = QGridLayout(self.tab_11)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.mAF_2 = LineEdit(self.tab_11)
        self.mAF_2.setObjectName(u"mAF_2")

        self.gridLayout_10.addWidget(self.mAF_2, 10, 1, 1, 1)

        self.label_42 = BodyLabel(self.tab_11)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_10.addWidget(self.label_42, 11, 0, 1, 1)

        self.label_36 = BodyLabel(self.tab_11)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_10.addWidget(self.label_36, 2, 0, 1, 1)

        self.exchange_2 = LineEdit(self.tab_11)
        self.exchange_2.setObjectName(u"exchange_2")

        self.gridLayout_10.addWidget(self.exchange_2, 2, 1, 1, 1)

        self.label_22 = BodyLabel(self.tab_11)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_10.addWidget(self.label_22, 9, 0, 1, 1)

        self.fermi_2 = LineEdit(self.tab_11)
        self.fermi_2.setObjectName(u"fermi_2")
        self.fermi_2.setEnabled(True)

        self.gridLayout_10.addWidget(self.fermi_2, 0, 1, 1, 1)

        self.mAB_2 = LineEdit(self.tab_11)
        self.mAB_2.setObjectName(u"mAB_2")

        self.gridLayout_10.addWidget(self.mAB_2, 9, 1, 1, 1)

        self.label_41 = BodyLabel(self.tab_11)
        self.label_41.setObjectName(u"label_41")

        self.gridLayout_10.addWidget(self.label_41, 7, 0, 1, 1)

        self.haldane_2 = LineEdit(self.tab_11)
        self.haldane_2.setObjectName(u"haldane_2")

        self.gridLayout_10.addWidget(self.haldane_2, 7, 1, 1, 1)

        self.antihaldane_2 = LineEdit(self.tab_11)
        self.antihaldane_2.setObjectName(u"antihaldane_2")

        self.gridLayout_10.addWidget(self.antihaldane_2, 8, 1, 1, 1)

        self.label_32 = BodyLabel(self.tab_11)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_10.addWidget(self.label_32, 5, 0, 1, 1)

        self.kanemele_2 = LineEdit(self.tab_11)
        self.kanemele_2.setObjectName(u"kanemele_2")

        self.gridLayout_10.addWidget(self.kanemele_2, 6, 1, 1, 1)

        self.label_39 = BodyLabel(self.tab_11)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout_10.addWidget(self.label_39, 10, 0, 1, 1)

        self.label_33 = BodyLabel(self.tab_11)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_10.addWidget(self.label_33, 6, 0, 1, 1)

        self.label_37 = BodyLabel(self.tab_11)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_10.addWidget(self.label_37, 0, 0, 1, 1)

        self.rashba_2 = LineEdit(self.tab_11)
        self.rashba_2.setObjectName(u"rashba_2")

        self.gridLayout_10.addWidget(self.rashba_2, 5, 1, 1, 1)

        self.swave_2 = LineEdit(self.tab_11)
        self.swave_2.setObjectName(u"swave_2")

        self.gridLayout_10.addWidget(self.swave_2, 11, 1, 1, 1)

        self.label_40 = BodyLabel(self.tab_11)
        self.label_40.setObjectName(u"label_40")

        self.gridLayout_10.addWidget(self.label_40, 8, 0, 1, 1)

        self.peierls_2 = LineEdit(self.tab_11)
        self.peierls_2.setObjectName(u"peierls_2")

        self.gridLayout_10.addWidget(self.peierls_2, 1, 1, 1, 1)

        self.label_19 = BodyLabel(self.tab_11)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_10.addWidget(self.label_19, 1, 0, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_10, 0, 0, 1, 1)

        self.tabWidget_4.addTab(self.tab_11, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.gridLayout_16 = QGridLayout(self.tab_8)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.mAF = LineEdit(self.tab_8)
        self.mAF.setObjectName(u"mAF")

        self.gridLayout.addWidget(self.mAF, 10, 1, 1, 1)

        self.label_rashba = BodyLabel(self.tab_8)
        self.label_rashba.setObjectName(u"label_rashba")

        self.gridLayout.addWidget(self.label_rashba, 5, 0, 1, 1)

        self.label_mAF = BodyLabel(self.tab_8)
        self.label_mAF.setObjectName(u"label_mAF")

        self.gridLayout.addWidget(self.label_mAF, 10, 0, 1, 1)

        self.label_antihaldane = BodyLabel(self.tab_8)
        self.label_antihaldane.setObjectName(u"label_antihaldane")

        self.gridLayout.addWidget(self.label_antihaldane, 8, 0, 1, 1)

        self.kanemele = LineEdit(self.tab_8)
        self.kanemele.setObjectName(u"kanemele")

        self.gridLayout.addWidget(self.kanemele, 6, 1, 1, 1)

        self.haldane = LineEdit(self.tab_8)
        self.haldane.setObjectName(u"haldane")

        self.gridLayout.addWidget(self.haldane, 7, 1, 1, 1)

        self.label_fermi = BodyLabel(self.tab_8)
        self.label_fermi.setObjectName(u"label_fermi")

        self.gridLayout.addWidget(self.label_fermi, 0, 0, 1, 1)

        self.label_kanemele = BodyLabel(self.tab_8)
        self.label_kanemele.setObjectName(u"label_kanemele")

        self.gridLayout.addWidget(self.label_kanemele, 6, 0, 1, 1)

        self.fermi = LineEdit(self.tab_8)
        self.fermi.setObjectName(u"fermi")
        self.fermi.setEnabled(True)

        self.gridLayout.addWidget(self.fermi, 0, 1, 1, 1)

        self.mAB = LineEdit(self.tab_8)
        self.mAB.setObjectName(u"mAB")

        self.gridLayout.addWidget(self.mAB, 9, 1, 1, 1)

        self.rashba = LineEdit(self.tab_8)
        self.rashba.setObjectName(u"rashba")

        self.gridLayout.addWidget(self.rashba, 5, 1, 1, 1)

        self.exchange = LineEdit(self.tab_8)
        self.exchange.setObjectName(u"exchange")

        self.gridLayout.addWidget(self.exchange, 2, 1, 1, 1)

        self.antihaldane = LineEdit(self.tab_8)
        self.antihaldane.setObjectName(u"antihaldane")

        self.gridLayout.addWidget(self.antihaldane, 8, 1, 1, 1)

        self.label_mAB = BodyLabel(self.tab_8)
        self.label_mAB.setObjectName(u"label_mAB")

        self.gridLayout.addWidget(self.label_mAB, 9, 0, 1, 1)

        self.label_haldane = BodyLabel(self.tab_8)
        self.label_haldane.setObjectName(u"label_haldane")

        self.gridLayout.addWidget(self.label_haldane, 7, 0, 1, 1)

        self.label_swave = BodyLabel(self.tab_8)
        self.label_swave.setObjectName(u"label_swave")

        self.gridLayout.addWidget(self.label_swave, 11, 0, 1, 1)

        self.swave = LineEdit(self.tab_8)
        self.swave.setObjectName(u"swave")

        self.gridLayout.addWidget(self.swave, 11, 1, 1, 1)

        self.label_3 = BodyLabel(self.tab_8)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_14 = BodyLabel(self.tab_8)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 1, 0, 1, 1)

        self.peierls = LineEdit(self.tab_8)
        self.peierls.setObjectName(u"peierls")

        self.gridLayout.addWidget(self.peierls, 1, 1, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget_4.addTab(self.tab_8, "")

        self.gridLayout_15.addWidget(self.tabWidget_4, 1, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")

        self.gridLayout_7.addWidget(self.tabWidget_2, 0, 0, 3, 1)

        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_8 = QGridLayout(self.tab_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_7 = BodyLabel(self.tab_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.nsuper_struct = LineEdit(self.tab_4)
        self.nsuper_struct.setObjectName(u"nsuper_struct")

        self.gridLayout_3.addWidget(self.nsuper_struct, 0, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.show_structure = PushButton(self.tab_4)
        self.show_structure.setObjectName(u"show_structure")

        self.gridLayout_8.addWidget(self.show_structure, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_9 = QGridLayout(self.tab_5)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_9 = BodyLabel(self.tab_5)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)

        self.label_15 = BodyLabel(self.tab_5)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 0, 0, 1, 1)

        self.bands_color = ComboBox(self.tab_5)
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.setObjectName(u"bands_color")

        self.gridLayout_2.addWidget(self.bands_color, 0, 1, 1, 1)

        self.nk_bands = LineEdit(self.tab_5)
        self.nk_bands.setObjectName(u"nk_bands")

        self.gridLayout_2.addWidget(self.nk_bands, 1, 1, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.show_bands = PushButton(self.tab_5)
        self.show_bands.setObjectName(u"show_bands")

        self.gridLayout_9.addWidget(self.show_bands, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.gridLayout_12 = QGridLayout(self.tab_9)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.delta_kbands = LineEdit(self.tab_9)
        self.delta_kbands.setObjectName(u"delta_kbands")

        self.gridLayout_11.addWidget(self.delta_kbands, 0, 1, 1, 1)

        self.label_27 = BodyLabel(self.tab_9)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_11.addWidget(self.label_27, 0, 0, 1, 1)

        self.ne_kbands = LineEdit(self.tab_9)
        self.ne_kbands.setObjectName(u"ne_kbands")

        self.gridLayout_11.addWidget(self.ne_kbands, 1, 1, 1, 1)

        self.label_28 = BodyLabel(self.tab_9)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_11.addWidget(self.label_28, 1, 0, 1, 1)

        self.label_29 = BodyLabel(self.tab_9)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_11.addWidget(self.label_29, 2, 0, 1, 1)

        self.window_kbands = LineEdit(self.tab_9)
        self.window_kbands.setObjectName(u"window_kbands")

        self.gridLayout_11.addWidget(self.window_kbands, 2, 1, 1, 1)

        self.label_30 = BodyLabel(self.tab_9)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_11.addWidget(self.label_30, 3, 0, 1, 1)

        self.scale_kbands = LineEdit(self.tab_9)
        self.scale_kbands.setObjectName(u"scale_kbands")

        self.gridLayout_11.addWidget(self.scale_kbands, 3, 1, 1, 1)

        self.label_31 = BodyLabel(self.tab_9)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_11.addWidget(self.label_31, 4, 0, 1, 1)

        self.nv_kbands = LineEdit(self.tab_9)
        self.nv_kbands.setObjectName(u"nv_kbands")

        self.gridLayout_11.addWidget(self.nv_kbands, 4, 1, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_11, 0, 0, 1, 1)

        self.show_dosbands = PushButton(self.tab_9)
        self.show_dosbands.setObjectName(u"show_dosbands")

        self.gridLayout_12.addWidget(self.show_dosbands, 0, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab_9, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_13 = QGridLayout(self.tab_6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_16 = BodyLabel(self.tab_6)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_5.addWidget(self.label_16, 0, 0, 1, 1)

        self.dos_delta = LineEdit(self.tab_6)
        self.dos_delta.setObjectName(u"dos_delta")

        self.gridLayout_5.addWidget(self.dos_delta, 0, 1, 1, 1)

        self.label_43 = BodyLabel(self.tab_6)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_5.addWidget(self.label_43, 1, 0, 1, 1)

        self.dos_nk = LineEdit(self.tab_6)
        self.dos_nk.setObjectName(u"dos_nk")

        self.gridLayout_5.addWidget(self.dos_nk, 1, 1, 1, 1)

        self.dos_ewindow = LineEdit(self.tab_6)
        self.dos_ewindow.setObjectName(u"dos_ewindow")

        self.gridLayout_5.addWidget(self.dos_ewindow, 2, 1, 1, 1)

        self.label_44 = BodyLabel(self.tab_6)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_5.addWidget(self.label_44, 2, 0, 1, 1)

        self.label_dos_mode = BodyLabel(self.tab_6)
        self.label_dos_mode.setObjectName(u"label_dos_mode")

        self.gridLayout_5.addWidget(self.label_dos_mode, 3, 0, 1, 1)

        self.dos_mode = ComboBox(self.tab_6)
        self.dos_mode.addItem("")
        self.dos_mode.addItem("")
        self.dos_mode.addItem("")
        self.dos_mode.setObjectName(u"dos_mode")

        self.gridLayout_5.addWidget(self.dos_mode, 3, 1, 1, 1)

        self.label_dos_operator = BodyLabel(self.tab_6)
        self.label_dos_operator.setObjectName(u"label_dos_operator")

        self.gridLayout_5.addWidget(self.label_dos_operator, 4, 0, 1, 1)

        self.dos_operator = ComboBox(self.tab_6)
        self.dos_operator.setObjectName(u"dos_operator")

        self.gridLayout_5.addWidget(self.dos_operator, 4, 1, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.show_dos = PushButton(self.tab_6)
        self.show_dos.setObjectName(u"show_dos")

        self.gridLayout_13.addWidget(self.show_dos, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.gridLayout_14 = QGridLayout(self.tab_7)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.ne_ldos = LineEdit(self.tab_7)
        self.ne_ldos.setObjectName(u"ne_ldos")

        self.gridLayout_6.addWidget(self.ne_ldos, 0, 1, 1, 1)

        self.delta_ldos = LineEdit(self.tab_7)
        self.delta_ldos.setObjectName(u"delta_ldos")

        self.gridLayout_6.addWidget(self.delta_ldos, 3, 1, 1, 1)

        self.label_35 = BodyLabel(self.tab_7)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_6.addWidget(self.label_35, 3, 0, 1, 1)

        self.nk_ldos = LineEdit(self.tab_7)
        self.nk_ldos.setObjectName(u"nk_ldos")

        self.gridLayout_6.addWidget(self.nk_ldos, 1, 1, 1, 1)

        self.label_17 = BodyLabel(self.tab_7)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_6.addWidget(self.label_17, 0, 0, 1, 1)

        self.label_18 = BodyLabel(self.tab_7)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_6.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_55 = BodyLabel(self.tab_7)
        self.label_55.setObjectName(u"label_55")

        self.gridLayout_6.addWidget(self.label_55, 2, 0, 1, 1)

        self.window_ldos = LineEdit(self.tab_7)
        self.window_ldos.setObjectName(u"window_ldos")

        self.gridLayout_6.addWidget(self.window_ldos, 2, 1, 1, 1)

        self.label_56 = BodyLabel(self.tab_7)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_6.addWidget(self.label_56, 4, 0, 1, 1)

        self.nsuper_ldos = LineEdit(self.tab_7)
        self.nsuper_ldos.setObjectName(u"nsuper_ldos")

        self.gridLayout_6.addWidget(self.nsuper_ldos, 4, 1, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.show_interactive_ldos = PushButton(self.tab_7)
        self.show_interactive_ldos.setObjectName(u"show_interactive_ldos")

        self.gridLayout_14.addWidget(self.show_interactive_ldos, 0, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab_7, "")
        self.tab_site_dos = QWidget()
        self.tab_site_dos.setObjectName(u"tab_site_dos")
        self.verticalLayout_site_dos = QVBoxLayout(self.tab_site_dos)
        self.verticalLayout_site_dos.setObjectName(u"verticalLayout_site_dos")
        self.label_site_dos_info = BodyLabel(self.tab_site_dos)
        self.label_site_dos_info.setObjectName(u"label_site_dos_info")
        self.label_site_dos_info.setWordWrap(True)

        self.verticalLayout_site_dos.addWidget(self.label_site_dos_info)

        self.gridLayout_site_dos = QGridLayout()
        self.gridLayout_site_dos.setObjectName(u"gridLayout_site_dos")
        self.label_site_dos_ewindow = BodyLabel(self.tab_site_dos)
        self.label_site_dos_ewindow.setObjectName(u"label_site_dos_ewindow")

        self.gridLayout_site_dos.addWidget(self.label_site_dos_ewindow, 0, 0, 1, 1)

        self.site_dos_ewindow = LineEdit(self.tab_site_dos)
        self.site_dos_ewindow.setObjectName(u"site_dos_ewindow")

        self.gridLayout_site_dos.addWidget(self.site_dos_ewindow, 0, 1, 1, 1)

        self.label_site_dos_delta = BodyLabel(self.tab_site_dos)
        self.label_site_dos_delta.setObjectName(u"label_site_dos_delta")

        self.gridLayout_site_dos.addWidget(self.label_site_dos_delta, 1, 0, 1, 1)

        self.site_dos_delta = LineEdit(self.tab_site_dos)
        self.site_dos_delta.setObjectName(u"site_dos_delta")

        self.gridLayout_site_dos.addWidget(self.site_dos_delta, 1, 1, 1, 1)

        self.label_site_dos_nk = BodyLabel(self.tab_site_dos)
        self.label_site_dos_nk.setObjectName(u"label_site_dos_nk")

        self.gridLayout_site_dos.addWidget(self.label_site_dos_nk, 2, 0, 1, 1)

        self.site_dos_nk = LineEdit(self.tab_site_dos)
        self.site_dos_nk.setObjectName(u"site_dos_nk")

        self.gridLayout_site_dos.addWidget(self.site_dos_nk, 2, 1, 1, 1)


        self.verticalLayout_site_dos.addLayout(self.gridLayout_site_dos)

        self.show_site_dos = PushButton(self.tab_site_dos)
        self.show_site_dos.setObjectName(u"show_site_dos")

        self.verticalLayout_site_dos.addWidget(self.show_site_dos)

        self.tabWidget_3.addTab(self.tab_site_dos, "")
        self.tab_scf = QWidget()
        self.tab_scf.setObjectName(u"tab_scf")
        self.gridLayout_scf_16 = QGridLayout(self.tab_scf)
        self.gridLayout_scf_16.setObjectName(u"gridLayout_scf_16")
        self.tabWidget_scf_bc = QTabWidget(self.tab_scf)
        self.tabWidget_scf_bc.setObjectName(u"tabWidget_scf_bc")
        self.tab_scf_basic = QWidget()
        self.tab_scf_basic.setObjectName(u"tab_scf_basic")
        self.gridLayout_scf_18 = QGridLayout(self.tab_scf_basic)
        self.gridLayout_scf_18.setObjectName(u"gridLayout_scf_18")
        self.gridLayout_scf_10 = QGridLayout()
        self.gridLayout_scf_10.setObjectName(u"gridLayout_scf_10")
        self.scf_terms_container = QWidget(self.tab_scf_basic)
        self.scf_terms_container.setObjectName(u"scf_terms_container")

        self.gridLayout_scf_10.addWidget(self.scf_terms_container, 1, 0, 1, 2)

        self.scf_initialization = ComboBox(self.tab_scf_basic)
        self.scf_initialization.addItem("")
        self.scf_initialization.addItem("")
        self.scf_initialization.addItem("")
        self.scf_initialization.setObjectName(u"scf_initialization")

        self.gridLayout_scf_10.addWidget(self.scf_initialization, 0, 1, 1, 1)

        self.label_scf_22 = BodyLabel(self.tab_scf_basic)
        self.label_scf_22.setObjectName(u"label_scf_22")

        self.gridLayout_scf_10.addWidget(self.label_scf_22, 0, 0, 1, 1)

        self.label_scf_34 = BodyLabel(self.tab_scf_basic)
        self.label_scf_34.setObjectName(u"label_scf_34")

        self.gridLayout_scf_10.addWidget(self.label_scf_34, 2, 0, 1, 1)

        self.filling_scf = LineEdit(self.tab_scf_basic)
        self.filling_scf.setObjectName(u"filling_scf")

        self.gridLayout_scf_10.addWidget(self.filling_scf, 2, 1, 1, 1)


        self.gridLayout_scf_18.addLayout(self.gridLayout_scf_10, 0, 0, 1, 2)

        self.do_scf = CheckBox(self.tab_scf_basic)
        self.do_scf.setObjectName(u"do_scf")

        self.gridLayout_scf_18.addWidget(self.do_scf, 1, 0, 1, 1)

        self.solve_scf = PushButton(self.tab_scf_basic)
        self.solve_scf.setObjectName(u"solve_scf")

        self.gridLayout_scf_18.addWidget(self.solve_scf, 1, 1, 1, 1)

        self.tabWidget_scf_bc.addTab(self.tab_scf_basic, "")
        self.tab_scf_convergence = QWidget()
        self.tab_scf_convergence.setObjectName(u"tab_scf_convergence")
        self.gridLayoutWidget_scf_12 = QWidget(self.tab_scf_convergence)
        self.gridLayoutWidget_scf_12.setObjectName(u"gridLayoutWidget_scf_12")
        self.gridLayoutWidget_scf_12.setGeometry(QRect(30, 30, 215, 161))
        self.gridLayout_scf_12 = QGridLayout(self.gridLayoutWidget_scf_12)
        self.gridLayout_scf_12.setObjectName(u"gridLayout_scf_12")
        self.gridLayout_scf_12.setContentsMargins(0, 0, 0, 0)
        self.label_scf_32 = BodyLabel(self.gridLayoutWidget_scf_12)
        self.label_scf_32.setObjectName(u"label_scf_32")

        self.gridLayout_scf_12.addWidget(self.label_scf_32, 0, 0, 1, 1)

        self.label_scf_33 = BodyLabel(self.gridLayoutWidget_scf_12)
        self.label_scf_33.setObjectName(u"label_scf_33")

        self.gridLayout_scf_12.addWidget(self.label_scf_33, 1, 0, 1, 1)

        self.nk_scf = LineEdit(self.gridLayoutWidget_scf_12)
        self.nk_scf.setObjectName(u"nk_scf")

        self.gridLayout_scf_12.addWidget(self.nk_scf, 1, 1, 1, 1)

        self.mix_scf = LineEdit(self.gridLayoutWidget_scf_12)
        self.mix_scf.setObjectName(u"mix_scf")

        self.gridLayout_scf_12.addWidget(self.mix_scf, 0, 1, 1, 1)

        self.label_scf_35 = BodyLabel(self.gridLayoutWidget_scf_12)
        self.label_scf_35.setObjectName(u"label_scf_35")

        self.gridLayout_scf_12.addWidget(self.label_scf_35, 2, 0, 1, 1)

        self.smearing_scf = LineEdit(self.gridLayoutWidget_scf_12)
        self.smearing_scf.setObjectName(u"smearing_scf")

        self.gridLayout_scf_12.addWidget(self.smearing_scf, 2, 1, 1, 1)

        self.tabWidget_scf_bc.addTab(self.tab_scf_convergence, "")

        self.gridLayout_scf_16.addWidget(self.tabWidget_scf_bc, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_scf, "")

        self.gridLayout_7.addWidget(self.tabWidget_3, 0, 1, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_18 = QGridLayout(self.tab_2)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_8 = BodyLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)

        self.lattice = ComboBox(self.tab_2)
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.setObjectName(u"lattice")

        self.gridLayout_4.addWidget(self.lattice, 0, 1, 1, 1)

        self.nsuper = LineEdit(self.tab_2)
        self.nsuper.setObjectName(u"nsuper")

        self.gridLayout_4.addWidget(self.nsuper, 1, 1, 1, 1)

        self.label_6 = BodyLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_2 = BodyLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 1)

        self.width = LineEdit(self.tab_2)
        self.width.setObjectName(u"width")

        self.gridLayout_4.addWidget(self.width, 2, 1, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_7.addWidget(self.tabWidget, 1, 1, 1, 1)

        self.label_46 = BodyLabel(self.centralwidget)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_7.addWidget(self.label_46, 2, 1, 1, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_7.addWidget(self.save_results, 3, 0, 1, 2)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_7.addWidget(self.load_results, 4, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 950, 25))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.bands_color.setCurrentIndex(0)
        self.tabWidget_scf_bc.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hybrid ribbon", None))
        self.label_nparts.setText(QCoreApplication.translate("MainWindow", u"Number of parts", None))
        self.nparts.setItemText(0, QCoreApplication.translate("MainWindow", u"2", None))
        self.nparts.setItemText(1, QCoreApplication.translate("MainWindow", u"3", None))
        self.nparts.setItemText(2, QCoreApplication.translate("MainWindow", u"4", None))
        self.nparts.setItemText(3, QCoreApplication.translate("MainWindow", u"5", None))
        self.nparts.setItemText(4, QCoreApplication.translate("MainWindow", u"6", None))

        self.mAF_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"swave pairing", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Exchange field", None))
#if QT_CONFIG(tooltip)
        self.exchange_2.setToolTip(QCoreApplication.translate("MainWindow", u"Exchange field in the system, taken as a vector with component Jx, Jy and Jz", None))
#endif // QT_CONFIG(tooltip)
        self.exchange_2.setText(QCoreApplication.translate("MainWindow", u"0.0, 0.0, 0.0", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Sublattice imbalance", None))
        self.fermi_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mAB_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Haldane", None))
        self.haldane_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.antihaldane_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Rashba", None))
        self.kanemele_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Antiferromagnetism", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Kane-Mele", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
        self.rashba_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.swave_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Anti-Haldane", None))
        self.peierls_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Magnetic field", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_11), QCoreApplication.translate("MainWindow", u"Lower", None))
        self.mAF.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_rashba.setText(QCoreApplication.translate("MainWindow", u"Rashba", None))
        self.label_mAF.setText(QCoreApplication.translate("MainWindow", u"Antiferromagnetism", None))
        self.label_antihaldane.setText(QCoreApplication.translate("MainWindow", u"Anti-Haldane", None))
        self.kanemele.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.haldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_fermi.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
        self.label_kanemele.setText(QCoreApplication.translate("MainWindow", u"Kane-Mele", None))
        self.fermi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mAB.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.rashba.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
#if QT_CONFIG(tooltip)
        self.exchange.setToolTip(QCoreApplication.translate("MainWindow", u"Exchange field in the system, taken as a vector with component Jx, Jy and Jz", None))
#endif // QT_CONFIG(tooltip)
        self.exchange.setText(QCoreApplication.translate("MainWindow", u"0.0, 0.0, 0.0", None))
        self.antihaldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_mAB.setText(QCoreApplication.translate("MainWindow", u"Sublattice imbalance", None))
        self.label_haldane.setText(QCoreApplication.translate("MainWindow", u"Haldane", None))
        self.label_swave.setText(QCoreApplication.translate("MainWindow", u"swave pairing", None))
        self.swave.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Exchange field", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Magnetic field", None))
        self.peierls.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"Upper", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Terms in the Hamiltonian", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.nsuper_struct.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Structure", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.bands_color.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.bands_color.setItemText(1, QCoreApplication.translate("MainWindow", u"y-position", None))
        self.bands_color.setItemText(2, QCoreApplication.translate("MainWindow", u"Sx", None))
        self.bands_color.setItemText(3, QCoreApplication.translate("MainWindow", u"Sy", None))
        self.bands_color.setItemText(4, QCoreApplication.translate("MainWindow", u"Sz", None))
        self.bands_color.setItemText(5, QCoreApplication.translate("MainWindow", u"Valley", None))
        self.bands_color.setItemText(6, QCoreApplication.translate("MainWindow", u"IPR", None))

        self.nk_bands.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.show_bands.setText(QCoreApplication.translate("MainWindow", u"Band structure", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Bands", None))
        self.delta_kbands.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.ne_kbands.setText(QCoreApplication.translate("MainWindow", u"400", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.window_kbands.setText(QCoreApplication.translate("MainWindow", u"3.0", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"KPM scale", None))
        self.scale_kbands.setText(QCoreApplication.translate("MainWindow", u"10.0", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"# vectors", None))
        self.nv_kbands.setText(QCoreApplication.translate("MainWindow", u"10", None))
#if QT_CONFIG(tooltip)
        self.show_dosbands.setToolTip(QCoreApplication.translate("MainWindow", u"This is equivalent to band structure calculation, but it can be applied for very large systems", None))
#endif // QT_CONFIG(tooltip)
        self.show_dosbands.setText(QCoreApplication.translate("MainWindow", u"Show DOS Bands", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"DOS Bands", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Number of k-points", None))
        self.dos_nk.setText(QCoreApplication.translate("MainWindow", u"400", None))
        self.dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.label_dos_mode.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.dos_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"ED", None))
        self.dos_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"Green", None))
        self.dos_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"KPM", None))

        self.label_dos_operator.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.show_dos.setText(QCoreApplication.translate("MainWindow", u"Density of states", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"DOS", None))
        self.ne_ldos.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.delta_ldos.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.nk_ldos.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"# of kpoints", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.window_ldos.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.nsuper_ldos.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.show_interactive_ldos.setText(QCoreApplication.translate("MainWindow", u"Show LDOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"LDOS", None))
        self.label_site_dos_info.setText(QCoreApplication.translate("MainWindow", u"Click a site in the structure plot to compute the DOS there", None))
        self.label_site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.label_site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.show_site_dos.setText(QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_site_dos), QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.scf_initialization.setItemText(0, QCoreApplication.translate("MainWindow", u"antiferro", None))
        self.scf_initialization.setItemText(1, QCoreApplication.translate("MainWindow", u"ferro", None))
        self.scf_initialization.setItemText(2, QCoreApplication.translate("MainWindow", u"random", None))

        self.label_scf_22.setText(QCoreApplication.translate("MainWindow", u"Initialization", None))
        self.label_scf_34.setText(QCoreApplication.translate("MainWindow", u"Filling", None))
        self.filling_scf.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.do_scf.setText(QCoreApplication.translate("MainWindow", u"Include mean field", None))
        self.solve_scf.setText(QCoreApplication.translate("MainWindow", u"Solve SCF", None))
        self.tabWidget_scf_bc.setTabText(self.tabWidget_scf_bc.indexOf(self.tab_scf_basic), QCoreApplication.translate("MainWindow", u"Basic", None))
        self.label_scf_32.setText(QCoreApplication.translate("MainWindow", u"Mixing", None))
        self.label_scf_33.setText(QCoreApplication.translate("MainWindow", u"# of kpoints", None))
        self.nk_scf.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.mix_scf.setText(QCoreApplication.translate("MainWindow", u"0.9", None))
        self.label_scf_35.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.smearing_scf.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.tabWidget_scf_bc.setTabText(self.tabWidget_scf_bc.indexOf(self.tab_scf_convergence), QCoreApplication.translate("MainWindow", u"Convergence", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_scf), QCoreApplication.translate("MainWindow", u"SCF", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Type of lattice", None))
        self.lattice.setItemText(0, QCoreApplication.translate("MainWindow", u"Honeycomb zigzag", None))
        self.lattice.setItemText(1, QCoreApplication.translate("MainWindow", u"Honeycomb armchair", None))
        self.lattice.setItemText(2, QCoreApplication.translate("MainWindow", u"Square", None))
        self.lattice.setItemText(3, QCoreApplication.translate("MainWindow", u"Triangular", None))
        self.lattice.setItemText(4, QCoreApplication.translate("MainWindow", u"Kagome", None))
        self.lattice.setItemText(5, QCoreApplication.translate("MainWindow", u"Lieb", None))
        self.lattice.setItemText(6, QCoreApplication.translate("MainWindow", u"Chain", None))

        self.nsuper.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Width", None))
        self.width.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Geometry", None))
#if QT_CONFIG(tooltip)
        self.label_46.setToolTip(QCoreApplication.translate("MainWindow", u"This module allows to compute heterostructures consisting of two different films. You have to specify the parameters of the two films", None))
#endif // QT_CONFIG(tooltip)
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.save_results.setText(QCoreApplication.translate("MainWindow", u"Save results", None))
        self.load_results.setText(QCoreApplication.translate("MainWindow", u"Load results", None))
    # retranslateUi

