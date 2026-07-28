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
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QTabWidget, QVBoxLayout,
    QWidget)

from qfluentwidgets import (BodyLabel, ComboBox, LineEdit, PushButton)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(878, 626)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_9 = QGridLayout(self.centralwidget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_12 = QGridLayout(self.tab_3)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.mAF = LineEdit(self.tab_3)
        self.mAF.setObjectName(u"mAF")
        self.mAF.setEnabled(True)

        self.gridLayout.addWidget(self.mAF, 11, 1, 1, 1)

        self.label_rashba = BodyLabel(self.tab_3)
        self.label_rashba.setObjectName(u"label_rashba")

        self.gridLayout.addWidget(self.label_rashba, 6, 0, 1, 1)

        self.label_kanemele = BodyLabel(self.tab_3)
        self.label_kanemele.setObjectName(u"label_kanemele")

        self.gridLayout.addWidget(self.label_kanemele, 7, 0, 1, 1)

        self.fermi = LineEdit(self.tab_3)
        self.fermi.setObjectName(u"fermi")
        self.fermi.setEnabled(True)

        self.gridLayout.addWidget(self.fermi, 1, 1, 1, 1)

        self.rashba = LineEdit(self.tab_3)
        self.rashba.setObjectName(u"rashba")
        self.rashba.setEnabled(True)

        self.gridLayout.addWidget(self.rashba, 6, 1, 1, 1)

        self.haldane = LineEdit(self.tab_3)
        self.haldane.setObjectName(u"haldane")

        self.gridLayout.addWidget(self.haldane, 8, 1, 1, 1)

        self.mAB = LineEdit(self.tab_3)
        self.mAB.setObjectName(u"mAB")

        self.gridLayout.addWidget(self.mAB, 10, 1, 1, 1)

        self.Bx = LineEdit(self.tab_3)
        self.Bx.setObjectName(u"Bx")
        self.Bx.setEnabled(True)

        self.gridLayout.addWidget(self.Bx, 3, 1, 1, 1)

        self.label_5 = BodyLabel(self.tab_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.label_14 = BodyLabel(self.tab_3)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 2, 0, 1, 1)

        self.Bz = LineEdit(self.tab_3)
        self.Bz.setObjectName(u"Bz")
        self.Bz.setEnabled(True)

        self.gridLayout.addWidget(self.Bz, 5, 1, 1, 1)

        self.label_haldane = BodyLabel(self.tab_3)
        self.label_haldane.setObjectName(u"label_haldane")

        self.gridLayout.addWidget(self.label_haldane, 8, 0, 1, 1)

        self.antihaldane = LineEdit(self.tab_3)
        self.antihaldane.setObjectName(u"antihaldane")

        self.gridLayout.addWidget(self.antihaldane, 9, 1, 1, 1)

        self.label_swave = BodyLabel(self.tab_3)
        self.label_swave.setObjectName(u"label_swave")

        self.gridLayout.addWidget(self.label_swave, 12, 0, 1, 1)

        self.swave = LineEdit(self.tab_3)
        self.swave.setObjectName(u"swave")
        self.swave.setEnabled(False)

        self.gridLayout.addWidget(self.swave, 12, 1, 1, 1)

        self.By = LineEdit(self.tab_3)
        self.By.setObjectName(u"By")
        self.By.setEnabled(True)

        self.gridLayout.addWidget(self.By, 4, 1, 1, 1)

        self.label_fermi = BodyLabel(self.tab_3)
        self.label_fermi.setObjectName(u"label_fermi")

        self.gridLayout.addWidget(self.label_fermi, 1, 0, 1, 1)

        self.peierls = LineEdit(self.tab_3)
        self.peierls.setObjectName(u"peierls")
        self.peierls.setEnabled(True)

        self.gridLayout.addWidget(self.peierls, 2, 1, 1, 1)

        self.kanemele = LineEdit(self.tab_3)
        self.kanemele.setObjectName(u"kanemele")
        self.kanemele.setEnabled(True)

        self.gridLayout.addWidget(self.kanemele, 7, 1, 1, 1)

        self.label_mAF = BodyLabel(self.tab_3)
        self.label_mAF.setObjectName(u"label_mAF")

        self.gridLayout.addWidget(self.label_mAF, 11, 0, 1, 1)

        self.label_antihaldane = BodyLabel(self.tab_3)
        self.label_antihaldane.setObjectName(u"label_antihaldane")

        self.gridLayout.addWidget(self.label_antihaldane, 9, 0, 1, 1)

        self.label_3 = BodyLabel(self.tab_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_4 = BodyLabel(self.tab_3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_mAB = BodyLabel(self.tab_3)
        self.label_mAB.setObjectName(u"label_mAB")

        self.gridLayout.addWidget(self.label_mAB, 10, 0, 1, 1)

        self.ti = LineEdit(self.tab_3)
        self.ti.setObjectName(u"ti")

        self.gridLayout.addWidget(self.ti, 0, 1, 1, 1)

        self.label_22 = BodyLabel(self.tab_3)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout.addWidget(self.label_22, 0, 0, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")

        self.gridLayout_9.addWidget(self.tabWidget_2, 0, 0, 2, 1)

        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_18 = QGridLayout(self.tab_4)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.nsuper_struct = LineEdit(self.tab_4)
        self.nsuper_struct.setObjectName(u"nsuper_struct")

        self.gridLayout_3.addWidget(self.nsuper_struct, 0, 1, 1, 1)

        self.label_7 = BodyLabel(self.tab_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.show_structure = PushButton(self.tab_4)
        self.show_structure.setObjectName(u"show_structure")

        self.gridLayout_18.addWidget(self.show_structure, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_17 = QGridLayout(self.tab_5)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.show_bands = PushButton(self.tab_5)
        self.show_bands.setObjectName(u"show_bands")

        self.gridLayout_17.addWidget(self.show_bands, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
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
        self.bands_color.setObjectName(u"bands_color")

        self.gridLayout_2.addWidget(self.bands_color, 0, 1, 1, 1)

        self.label_9 = BodyLabel(self.tab_5)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)

        self.nk_bands = LineEdit(self.tab_5)
        self.nk_bands.setObjectName(u"nk_bands")

        self.gridLayout_2.addWidget(self.nk_bands, 1, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.gridLayout_14 = QGridLayout(self.tab_9)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
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


        self.gridLayout_14.addLayout(self.gridLayout_11, 0, 0, 1, 1)

        self.show_dosbands = PushButton(self.tab_9)
        self.show_dosbands.setObjectName(u"show_dosbands")

        self.gridLayout_14.addWidget(self.show_dosbands, 0, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab_9, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_15 = QGridLayout(self.tab_6)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.show_dos = PushButton(self.tab_6)
        self.show_dos.setObjectName(u"show_dos")

        self.gridLayout_15.addWidget(self.show_dos, 0, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_16 = BodyLabel(self.tab_6)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_5.addWidget(self.label_16, 0, 0, 1, 1)

        self.DOS_smearing = LineEdit(self.tab_6)
        self.DOS_smearing.setObjectName(u"DOS_smearing")

        self.gridLayout_5.addWidget(self.DOS_smearing, 0, 1, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_5, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.gridLayout_16 = QGridLayout(self.tab_7)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.ne_ldos = LineEdit(self.tab_7)
        self.ne_ldos.setObjectName(u"ne_ldos")

        self.gridLayout_6.addWidget(self.ne_ldos, 0, 1, 1, 1)

        self.delta_ldos = LineEdit(self.tab_7)
        self.delta_ldos.setObjectName(u"delta_ldos")

        self.gridLayout_6.addWidget(self.delta_ldos, 3, 1, 1, 1)

        self.label_20 = BodyLabel(self.tab_7)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_6.addWidget(self.label_20, 3, 0, 1, 1)

        self.nk_ldos = LineEdit(self.tab_7)
        self.nk_ldos.setObjectName(u"nk_ldos")

        self.gridLayout_6.addWidget(self.nk_ldos, 1, 1, 1, 1)

        self.label_17 = BodyLabel(self.tab_7)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_6.addWidget(self.label_17, 0, 0, 1, 1)

        self.label_18 = BodyLabel(self.tab_7)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_6.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_19 = BodyLabel(self.tab_7)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 2, 0, 1, 1)

        self.window_ldos = LineEdit(self.tab_7)
        self.window_ldos.setObjectName(u"window_ldos")

        self.gridLayout_6.addWidget(self.window_ldos, 2, 1, 1, 1)

        self.nsuper_ldos = LineEdit(self.tab_7)
        self.nsuper_ldos.setObjectName(u"nsuper_ldos")

        self.gridLayout_6.addWidget(self.nsuper_ldos, 4, 1, 1, 1)

        self.label_21 = BodyLabel(self.tab_7)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_6.addWidget(self.label_21, 4, 0, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.show_interactive_ldos = PushButton(self.tab_7)
        self.show_interactive_ldos.setObjectName(u"show_interactive_ldos")

        self.gridLayout_16.addWidget(self.show_interactive_ldos, 0, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab_7, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_13 = QGridLayout(self.tab)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_33 = BodyLabel(self.tab)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_7.addWidget(self.label_33, 1, 0, 1, 1)

        self.nume_hofs = LineEdit(self.tab)
        self.nume_hofs.setObjectName(u"nume_hofs")

        self.gridLayout_7.addWidget(self.nume_hofs, 4, 1, 1, 1)

        self.label_35 = BodyLabel(self.tab)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_7.addWidget(self.label_35, 3, 0, 1, 1)

        self.numb_hofs = LineEdit(self.tab)
        self.numb_hofs.setObjectName(u"numb_hofs")

        self.gridLayout_7.addWidget(self.numb_hofs, 2, 1, 1, 1)

        self.label_36 = BodyLabel(self.tab)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_7.addWidget(self.label_36, 4, 0, 1, 1)

        self.ewindow_hofs = LineEdit(self.tab)
        self.ewindow_hofs.setObjectName(u"ewindow_hofs")

        self.gridLayout_7.addWidget(self.ewindow_hofs, 3, 1, 1, 1)

        self.maxb_hofs = LineEdit(self.tab)
        self.maxb_hofs.setObjectName(u"maxb_hofs")

        self.gridLayout_7.addWidget(self.maxb_hofs, 1, 1, 1, 1)

        self.label_38 = BodyLabel(self.tab)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_7.addWidget(self.label_38, 5, 0, 1, 1)

        self.minb_hofs = LineEdit(self.tab)
        self.minb_hofs.setObjectName(u"minb_hofs")

        self.gridLayout_7.addWidget(self.minb_hofs, 0, 1, 1, 1)

        self.label_32 = BodyLabel(self.tab)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_7.addWidget(self.label_32, 0, 0, 1, 1)

        self.label_34 = BodyLabel(self.tab)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_7.addWidget(self.label_34, 2, 0, 1, 1)

        self.nite_hofs = LineEdit(self.tab)
        self.nite_hofs.setObjectName(u"nite_hofs")

        self.gridLayout_7.addWidget(self.nite_hofs, 5, 1, 1, 1)

        self.nk_hofs = LineEdit(self.tab)
        self.nk_hofs.setObjectName(u"nk_hofs")

        self.gridLayout_7.addWidget(self.nk_hofs, 6, 1, 1, 1)

        self.label_39 = BodyLabel(self.tab)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout_7.addWidget(self.label_39, 6, 0, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_7, 0, 0, 2, 1)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.hofstader_mode = ComboBox(self.tab)
        self.hofstader_mode.addItem("")
        self.hofstader_mode.addItem("")
        self.hofstader_mode.addItem("")
        self.hofstader_mode.setObjectName(u"hofstader_mode")

        self.gridLayout_8.addWidget(self.hofstader_mode, 0, 1, 1, 1)

        self.label_37 = BodyLabel(self.tab)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_8.addWidget(self.label_37, 0, 0, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_8, 0, 1, 1, 1)

        self.show_hofstader = PushButton(self.tab)
        self.show_hofstader.setObjectName(u"show_hofstader")

        self.gridLayout_13.addWidget(self.show_hofstader, 1, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab, "")
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

        self.gridLayout_9.addWidget(self.tabWidget_3, 0, 1, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_10 = QGridLayout(self.tab_2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
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

        self.width = LineEdit(self.tab_2)
        self.width.setObjectName(u"width")

        self.gridLayout_4.addWidget(self.width, 2, 1, 1, 1)

        self.label_2 = BodyLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_9.addWidget(self.tabWidget, 1, 1, 1, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_9.addWidget(self.save_results, 2, 0, 1, 2)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_9.addWidget(self.load_results, 3, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 878, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.bands_color.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hofstadter spectra", None))
        self.mAF.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_rashba.setText(QCoreApplication.translate("MainWindow", u"Rashba", None))
        self.label_kanemele.setText(QCoreApplication.translate("MainWindow", u"Kane-Mele", None))
        self.fermi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.rashba.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.haldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mAB.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.Bx.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jz", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Magnetic field", None))
        self.Bz.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_haldane.setText(QCoreApplication.translate("MainWindow", u"Haldane", None))
        self.antihaldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_swave.setText(QCoreApplication.translate("MainWindow", u"swave pairing", None))
        self.swave.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.By.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_fermi.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
        self.peierls.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.kanemele.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_mAF.setText(QCoreApplication.translate("MainWindow", u"Antiferromagnetism", None))
        self.label_antihaldane.setText(QCoreApplication.translate("MainWindow", u"Anti-Haldane", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jx", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jy", None))
        self.label_mAB.setText(QCoreApplication.translate("MainWindow", u"Sublattice imbalance", None))
        self.ti.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Interlayer hopping", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Terms in the Hamiltonian", None))
        self.nsuper_struct.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Structure", None))
        self.show_bands.setText(QCoreApplication.translate("MainWindow", u"Band structure", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.bands_color.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.bands_color.setItemText(1, QCoreApplication.translate("MainWindow", u"y-position", None))
        self.bands_color.setItemText(2, QCoreApplication.translate("MainWindow", u"Sx", None))
        self.bands_color.setItemText(3, QCoreApplication.translate("MainWindow", u"Sy", None))
        self.bands_color.setItemText(4, QCoreApplication.translate("MainWindow", u"Sz", None))
        self.bands_color.setItemText(5, QCoreApplication.translate("MainWindow", u"Valley", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.nk_bands.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Bands", None))
        self.delta_kbands.setText(QCoreApplication.translate("MainWindow", u"0.02", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.ne_kbands.setText(QCoreApplication.translate("MainWindow", u"400", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.window_kbands.setText(QCoreApplication.translate("MainWindow", u"3.0", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"KPM scale", None))
        self.scale_kbands.setText(QCoreApplication.translate("MainWindow", u"10.0", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"# vectors", None))
        self.nv_kbands.setText(QCoreApplication.translate("MainWindow", u"3", None))
#if QT_CONFIG(tooltip)
        self.show_dosbands.setToolTip(QCoreApplication.translate("MainWindow", u"This is equivalent to band structure calculation, but it can be applied for very large systems", None))
#endif // QT_CONFIG(tooltip)
        self.show_dosbands.setText(QCoreApplication.translate("MainWindow", u"Show DOS Bands", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"DOS Bands", None))
        self.show_dos.setText(QCoreApplication.translate("MainWindow", u"Density of states", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.DOS_smearing.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"DOS", None))
        self.ne_ldos.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.delta_ldos.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.nk_ldos.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"# of kpoints", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.window_ldos.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.nsuper_ldos.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.show_interactive_ldos.setText(QCoreApplication.translate("MainWindow", u"Show LDOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"LDOS", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Final B", None))
        self.nume_hofs.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.numb_hofs.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.ewindow_hofs.setText(QCoreApplication.translate("MainWindow", u"1.0", None))
        self.maxb_hofs.setText(QCoreApplication.translate("MainWindow", u"0.05", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"# of iterations", None))
        self.minb_hofs.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Initial B", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"# of B", None))
#if QT_CONFIG(tooltip)
        self.nite_hofs.setToolTip(QCoreApplication.translate("MainWindow", u"Number of random vectors used in the KPM. INcrease this number to remove noise", None))
#endif // QT_CONFIG(tooltip)
        self.nite_hofs.setText(QCoreApplication.translate("MainWindow", u"5", None))
#if QT_CONFIG(tooltip)
        self.nk_hofs.setToolTip(QCoreApplication.translate("MainWindow", u"NUmber of kpoints in KPM. It should not very critical for the hofstader spectra", None))
#endif // QT_CONFIG(tooltip)
        self.nk_hofs.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"# of kpoints", None))
        self.hofstader_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"Bulk", None))
        self.hofstader_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"All", None))
        self.hofstader_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"Edge", None))

        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.show_hofstader.setText(QCoreApplication.translate("MainWindow", u"Hofstader spectra", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Hofstader spectra", None))
        self.label_site_dos_info.setText(QCoreApplication.translate("MainWindow", u"Click a site in the structure plot to compute the DOS there", None))
        self.label_site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.label_site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.show_site_dos.setText(QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_site_dos), QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Type of lattice", None))
        self.lattice.setItemText(0, QCoreApplication.translate("MainWindow", u"Graphene", None))
        self.lattice.setItemText(1, QCoreApplication.translate("MainWindow", u"Bilayer graphene AB", None))
        self.lattice.setItemText(2, QCoreApplication.translate("MainWindow", u"Bilayer graphene AA", None))
        self.lattice.setItemText(3, QCoreApplication.translate("MainWindow", u"Square", None))
        self.lattice.setItemText(4, QCoreApplication.translate("MainWindow", u"Honeycomb zigzag", None))
        self.lattice.setItemText(5, QCoreApplication.translate("MainWindow", u"Honeycomb armchair", None))
        self.lattice.setItemText(6, QCoreApplication.translate("MainWindow", u"Triangular", None))
        self.lattice.setItemText(7, QCoreApplication.translate("MainWindow", u"Kagome", None))
        self.lattice.setItemText(8, QCoreApplication.translate("MainWindow", u"Lieb", None))

        self.nsuper.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.width.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Width", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Geometry", None))
        self.save_results.setText(QCoreApplication.translate("MainWindow", u"Save results", None))
        self.load_results.setText(QCoreApplication.translate("MainWindow", u"Load results", None))
    # retranslateUi

