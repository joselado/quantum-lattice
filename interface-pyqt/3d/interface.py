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

from qfluentwidgets import (BodyLabel, CheckBox, ComboBox, LineEdit,
    PushButton)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(950, 659)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_6 = QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_7 = QGridLayout(self.tab_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.fermi = LineEdit(self.tab_3)
        self.fermi.setObjectName(u"fermi")
        self.fermi.setEnabled(True)

        self.gridLayout.addWidget(self.fermi, 1, 1, 1, 1)

        self.rashba = LineEdit(self.tab_3)
        self.rashba.setObjectName(u"rashba")

        self.gridLayout.addWidget(self.rashba, 5, 1, 1, 1)

        self.mAB = LineEdit(self.tab_3)
        self.mAB.setObjectName(u"mAB")

        self.gridLayout.addWidget(self.mAB, 9, 1, 1, 1)

        self.label_kanemele = BodyLabel(self.tab_3)
        self.label_kanemele.setObjectName(u"label_kanemele")

        self.gridLayout.addWidget(self.label_kanemele, 6, 0, 1, 1)

        self.label_3 = BodyLabel(self.tab_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_antihaldane = BodyLabel(self.tab_3)
        self.label_antihaldane.setObjectName(u"label_antihaldane")

        self.gridLayout.addWidget(self.label_antihaldane, 8, 0, 1, 1)

        self.kanemele = LineEdit(self.tab_3)
        self.kanemele.setObjectName(u"kanemele")

        self.gridLayout.addWidget(self.kanemele, 6, 1, 1, 1)

        self.mAF = LineEdit(self.tab_3)
        self.mAF.setObjectName(u"mAF")

        self.gridLayout.addWidget(self.mAF, 10, 1, 1, 1)

        self.label_rashba = BodyLabel(self.tab_3)
        self.label_rashba.setObjectName(u"label_rashba")

        self.gridLayout.addWidget(self.label_rashba, 5, 0, 1, 1)

        self.label_mAF = BodyLabel(self.tab_3)
        self.label_mAF.setObjectName(u"label_mAF")

        self.gridLayout.addWidget(self.label_mAF, 10, 0, 1, 1)

        self.label_mAB = BodyLabel(self.tab_3)
        self.label_mAB.setObjectName(u"label_mAB")

        self.gridLayout.addWidget(self.label_mAB, 9, 0, 1, 1)

        self.label_haldane = BodyLabel(self.tab_3)
        self.label_haldane.setObjectName(u"label_haldane")

        self.gridLayout.addWidget(self.label_haldane, 7, 0, 1, 1)

        self.label_swave = BodyLabel(self.tab_3)
        self.label_swave.setObjectName(u"label_swave")

        self.gridLayout.addWidget(self.label_swave, 11, 0, 1, 1)

        self.haldane = LineEdit(self.tab_3)
        self.haldane.setObjectName(u"haldane")

        self.gridLayout.addWidget(self.haldane, 7, 1, 1, 1)

        self.label_fermi = BodyLabel(self.tab_3)
        self.label_fermi.setObjectName(u"label_fermi")

        self.gridLayout.addWidget(self.label_fermi, 1, 0, 1, 1)

        self.exchange = LineEdit(self.tab_3)
        self.exchange.setObjectName(u"exchange")

        self.gridLayout.addWidget(self.exchange, 2, 1, 1, 1)

        self.antihaldane = LineEdit(self.tab_3)
        self.antihaldane.setObjectName(u"antihaldane")

        self.gridLayout.addWidget(self.antihaldane, 8, 1, 1, 1)

        self.swave = LineEdit(self.tab_3)
        self.swave.setObjectName(u"swave")

        self.gridLayout.addWidget(self.swave, 11, 1, 1, 1)

        self.label_44 = BodyLabel(self.tab_3)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setEnabled(False)

        self.gridLayout.addWidget(self.label_44, 0, 0, 1, 1)

        self.strain = LineEdit(self.tab_3)
        self.strain.setObjectName(u"strain")
        self.strain.setEnabled(False)

        self.gridLayout.addWidget(self.strain, 0, 1, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")

        self.gridLayout_6.addWidget(self.tabWidget_2, 0, 0, 2, 1)

        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_11 = QGridLayout(self.tab_4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.show_structure = PushButton(self.tab_4)
        self.show_structure.setObjectName(u"show_structure")

        self.gridLayout_11.addWidget(self.show_structure, 1, 0, 1, 1)

        self.show_structure_3d = PushButton(self.tab_4)
        self.show_structure_3d.setObjectName(u"show_structure_3d")

        self.gridLayout_11.addWidget(self.show_structure_3d, 1, 1, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_7 = BodyLabel(self.tab_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.nsuper_struct = LineEdit(self.tab_4)
        self.nsuper_struct.setObjectName(u"nsuper_struct")

        self.gridLayout_3.addWidget(self.nsuper_struct, 0, 1, 1, 1)


        self.gridLayout_11.addLayout(self.gridLayout_3, 0, 0, 1, 2)

        self.tabWidget_3.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_8 = QGridLayout(self.tab_5)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
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

        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_15 = BodyLabel(self.tab_5)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 0, 0, 1, 1)

        self.nk_bands = LineEdit(self.tab_5)
        self.nk_bands.setObjectName(u"nk_bands")

        self.gridLayout_2.addWidget(self.nk_bands, 2, 1, 1, 1)

        self.label_16 = BodyLabel(self.tab_5)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_2.addWidget(self.label_16, 1, 0, 1, 1)

        self.bands_colormap = ComboBox(self.tab_5)
        self.bands_colormap.setObjectName(u"bands_colormap")

        self.gridLayout_2.addWidget(self.bands_colormap, 1, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.show_bands = PushButton(self.tab_5)
        self.show_bands.setObjectName(u"show_bands")

        self.gridLayout_8.addWidget(self.show_bands, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_5 = QGridLayout(self.tab_6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_36 = QGridLayout()
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.label_50 = BodyLabel(self.tab_6)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_36.addWidget(self.label_50, 0, 0, 1, 1)

        self.dos_delta = LineEdit(self.tab_6)
        self.dos_delta.setObjectName(u"dos_delta")

        self.gridLayout_36.addWidget(self.dos_delta, 2, 1, 1, 1)

        self.dos_ewindow = LineEdit(self.tab_6)
        self.dos_ewindow.setObjectName(u"dos_ewindow")

        self.gridLayout_36.addWidget(self.dos_ewindow, 1, 1, 1, 1)

        self.label_51 = BodyLabel(self.tab_6)
        self.label_51.setObjectName(u"label_51")

        self.gridLayout_36.addWidget(self.label_51, 1, 0, 1, 1)

        self.label_48 = BodyLabel(self.tab_6)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_36.addWidget(self.label_48, 2, 0, 1, 1)

        self.dos_nk = LineEdit(self.tab_6)
        self.dos_nk.setObjectName(u"dos_nk")

        self.gridLayout_36.addWidget(self.dos_nk, 0, 1, 1, 1)

        self.label_dos_mode = BodyLabel(self.tab_6)
        self.label_dos_mode.setObjectName(u"label_dos_mode")

        self.gridLayout_36.addWidget(self.label_dos_mode, 3, 0, 1, 1)

        self.dos_mode = ComboBox(self.tab_6)
        self.dos_mode.addItem("")
        self.dos_mode.addItem("")
        self.dos_mode.addItem("")
        self.dos_mode.setObjectName(u"dos_mode")

        self.gridLayout_36.addWidget(self.dos_mode, 3, 1, 1, 1)

        self.label_dos_operator = BodyLabel(self.tab_6)
        self.label_dos_operator.setObjectName(u"label_dos_operator")

        self.gridLayout_36.addWidget(self.label_dos_operator, 4, 0, 1, 1)

        self.dos_operator = ComboBox(self.tab_6)
        self.dos_operator.setObjectName(u"dos_operator")

        self.gridLayout_36.addWidget(self.dos_operator, 4, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_36, 0, 0, 1, 1)

        self.show_dos = PushButton(self.tab_6)
        self.show_dos.setObjectName(u"show_dos")

        self.gridLayout_5.addWidget(self.show_dos, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_6, "")
        self.tab_iets_qdos = QWidget()
        self.tab_iets_qdos.setObjectName(u"tab_iets_qdos")
        self.gridLayout_iets_qdos_outer = QGridLayout(self.tab_iets_qdos)
        self.gridLayout_iets_qdos_outer.setObjectName(u"gridLayout_iets_qdos_outer")
        self.gridLayout_iets_qdos = QGridLayout()
        self.gridLayout_iets_qdos.setObjectName(u"gridLayout_iets_qdos")
        self.label_iets_1 = BodyLabel(self.tab_iets_qdos)
        self.label_iets_1.setObjectName(u"label_iets_1")

        self.gridLayout_iets_qdos.addWidget(self.label_iets_1, 0, 0, 1, 1)

        self.delta_iets = LineEdit(self.tab_iets_qdos)
        self.delta_iets.setObjectName(u"delta_iets")

        self.gridLayout_iets_qdos.addWidget(self.delta_iets, 0, 1, 1, 1)

        self.label_iets_2 = BodyLabel(self.tab_iets_qdos)
        self.label_iets_2.setObjectName(u"label_iets_2")

        self.gridLayout_iets_qdos.addWidget(self.label_iets_2, 1, 0, 1, 1)

        self.ne_iets = LineEdit(self.tab_iets_qdos)
        self.ne_iets.setObjectName(u"ne_iets")

        self.gridLayout_iets_qdos.addWidget(self.ne_iets, 1, 1, 1, 1)

        self.label_iets_3 = BodyLabel(self.tab_iets_qdos)
        self.label_iets_3.setObjectName(u"label_iets_3")

        self.gridLayout_iets_qdos.addWidget(self.label_iets_3, 2, 0, 1, 1)

        self.window_iets = LineEdit(self.tab_iets_qdos)
        self.window_iets.setObjectName(u"window_iets")

        self.gridLayout_iets_qdos.addWidget(self.window_iets, 2, 1, 1, 1)

        self.label_iets_4 = BodyLabel(self.tab_iets_qdos)
        self.label_iets_4.setObjectName(u"label_iets_4")

        self.gridLayout_iets_qdos.addWidget(self.label_iets_4, 3, 0, 1, 1)

        self.nq_iets = LineEdit(self.tab_iets_qdos)
        self.nq_iets.setObjectName(u"nq_iets")

        self.gridLayout_iets_qdos.addWidget(self.nq_iets, 3, 1, 1, 1)

        self.label_iets_5 = BodyLabel(self.tab_iets_qdos)
        self.label_iets_5.setObjectName(u"label_iets_5")

        self.gridLayout_iets_qdos.addWidget(self.label_iets_5, 4, 0, 1, 1)

        self.nk_iets = LineEdit(self.tab_iets_qdos)
        self.nk_iets.setObjectName(u"nk_iets")

        self.gridLayout_iets_qdos.addWidget(self.nk_iets, 4, 1, 1, 1)

        self.show_iets_qdos = PushButton(self.tab_iets_qdos)
        self.show_iets_qdos.setObjectName(u"show_iets_qdos")

        self.gridLayout_iets_qdos.addWidget(self.show_iets_qdos, 5, 0, 1, 2)


        self.gridLayout_iets_qdos_outer.addLayout(self.gridLayout_iets_qdos, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_iets_qdos, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_13 = QGridLayout(self.tab)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.kdos_ewindow = LineEdit(self.tab)
        self.kdos_ewindow.setObjectName(u"kdos_ewindow")

        self.gridLayout_9.addWidget(self.kdos_ewindow, 0, 1, 1, 1)

        self.label_20 = BodyLabel(self.tab)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_9.addWidget(self.label_20, 0, 0, 1, 1)

        self.kdos_mesh = LineEdit(self.tab)
        self.kdos_mesh.setObjectName(u"kdos_mesh")

        self.gridLayout_9.addWidget(self.kdos_mesh, 1, 1, 1, 1)

        self.label_21 = BodyLabel(self.tab)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_9.addWidget(self.label_21, 1, 0, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_9, 0, 0, 1, 1)

        self.show_kdos = PushButton(self.tab)
        self.show_kdos.setObjectName(u"show_kdos")

        self.gridLayout_13.addWidget(self.show_kdos, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.gridLayout_15 = QGridLayout(self.tab_8)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.tabWidget_4 = QTabWidget(self.tab_8)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.gridLayout_18 = QGridLayout(self.tab_12)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.scf_terms_container = QWidget(self.tab_12)
        self.scf_terms_container.setObjectName(u"scf_terms_container")

        self.gridLayout_10.addWidget(self.scf_terms_container, 1, 0, 1, 2)

        self.scf_initialization = ComboBox(self.tab_12)
        self.scf_initialization.addItem("")
        self.scf_initialization.addItem("")
        self.scf_initialization.addItem("")
        self.scf_initialization.setObjectName(u"scf_initialization")

        self.gridLayout_10.addWidget(self.scf_initialization, 0, 1, 1, 1)

        self.label_22 = BodyLabel(self.tab_12)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_10.addWidget(self.label_22, 0, 0, 1, 1)

        self.label_34 = BodyLabel(self.tab_12)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_10.addWidget(self.label_34, 2, 0, 1, 1)

        self.filling_scf = LineEdit(self.tab_12)
        self.filling_scf.setObjectName(u"filling_scf")

        self.gridLayout_10.addWidget(self.filling_scf, 2, 1, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_10, 0, 0, 1, 2)

        self.do_scf = CheckBox(self.tab_12)
        self.do_scf.setObjectName(u"do_scf")

        self.gridLayout_18.addWidget(self.do_scf, 1, 0, 1, 1)

        self.solve_scf = PushButton(self.tab_12)
        self.solve_scf.setObjectName(u"solve_scf")

        self.gridLayout_18.addWidget(self.solve_scf, 1, 1, 1, 1)

        self.tabWidget_4.addTab(self.tab_12, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.gridLayout_19 = QGridLayout(self.tab_11)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_32 = BodyLabel(self.tab_11)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_12.addWidget(self.label_32, 0, 0, 1, 1)

        self.label_14 = BodyLabel(self.tab_11)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_12.addWidget(self.label_14, 1, 0, 1, 1)

        self.nk_scf = LineEdit(self.tab_11)
        self.nk_scf.setObjectName(u"nk_scf")

        self.gridLayout_12.addWidget(self.nk_scf, 1, 1, 1, 1)

        self.mix_scf = LineEdit(self.tab_11)
        self.mix_scf.setObjectName(u"mix_scf")

        self.gridLayout_12.addWidget(self.mix_scf, 0, 1, 1, 1)

        self.label_33 = BodyLabel(self.tab_11)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_12.addWidget(self.label_33, 2, 0, 1, 1)

        self.smearing_scf = LineEdit(self.tab_11)
        self.smearing_scf.setObjectName(u"smearing_scf")

        self.gridLayout_12.addWidget(self.smearing_scf, 2, 1, 1, 1)

        self.label_scf_solver = BodyLabel(self.tab_11)
        self.label_scf_solver.setObjectName(u"label_scf_solver")

        self.gridLayout_12.addWidget(self.label_scf_solver, 3, 0, 1, 1)

        self.scf_solver = ComboBox(self.tab_11)
        self.scf_solver.addItem("")
        self.scf_solver.addItem("")
        self.scf_solver.addItem("")
        self.scf_solver.setObjectName(u"scf_solver")

        self.gridLayout_12.addWidget(self.scf_solver, 3, 1, 1, 1)

        self.label_scf_maxite = BodyLabel(self.tab_11)
        self.label_scf_maxite.setObjectName(u"label_scf_maxite")

        self.gridLayout_12.addWidget(self.label_scf_maxite, 4, 0, 1, 1)

        self.scf_maxite = LineEdit(self.tab_11)
        self.scf_maxite.setObjectName(u"scf_maxite")

        self.gridLayout_12.addWidget(self.scf_maxite, 4, 1, 1, 1)


        self.gridLayout_19.addLayout(self.gridLayout_12, 0, 0, 1, 1)

        self.tabWidget_4.addTab(self.tab_11, "")

        self.gridLayout_15.addWidget(self.tabWidget_4, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_8, "")
        self.tab_13 = QWidget()
        self.tab_13.setObjectName(u"tab_13")
        self.gridLayout_16 = QGridLayout(self.tab_13)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.magnetization_nrep = LineEdit(self.tab_13)
        self.magnetization_nrep.setObjectName(u"magnetization_nrep")

        self.gridLayout_16.addWidget(self.magnetization_nrep, 1, 1, 1, 1)

        self.label_2 = BodyLabel(self.tab_13)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_16.addWidget(self.label_2, 1, 0, 1, 1)

        self.show_magnetism = PushButton(self.tab_13)
        self.show_magnetism.setObjectName(u"show_magnetism")

        self.gridLayout_16.addWidget(self.show_magnetism, 0, 0, 1, 2)

        self.tabWidget_3.addTab(self.tab_13, "")
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

        self.gridLayout_6.addWidget(self.tabWidget_3, 0, 1, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_17 = QGridLayout(self.tab_2)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.nsuper = LineEdit(self.tab_2)
        self.nsuper.setObjectName(u"nsuper")

        self.gridLayout_4.addWidget(self.nsuper, 1, 1, 1, 1)

        self.label_6 = BodyLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_8 = BodyLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)

        self.lattice = ComboBox(self.tab_2)
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.setObjectName(u"lattice")

        self.gridLayout_4.addWidget(self.lattice, 0, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.verticalLayout = QVBoxLayout(self.tab_10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.remove_single_bonded = CheckBox(self.tab_10)
        self.remove_single_bonded.setObjectName(u"remove_single_bonded")
        self.remove_single_bonded.setChecked(True)

        self.gridLayout_21.addWidget(self.remove_single_bonded, 0, 0, 1, 1)

        self.remove_selected = CheckBox(self.tab_10)
        self.remove_selected.setObjectName(u"remove_selected")

        self.gridLayout_21.addWidget(self.remove_selected, 1, 0, 1, 1)

        self.select_atoms_removal = PushButton(self.tab_10)
        self.select_atoms_removal.setObjectName(u"select_atoms_removal")

        self.gridLayout_21.addWidget(self.select_atoms_removal, 2, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_21)

        self.tabWidget.addTab(self.tab_10, "")

        self.gridLayout_6.addWidget(self.tabWidget, 1, 1, 1, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_6.addWidget(self.save_results, 2, 0, 1, 2)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_6.addWidget(self.load_results, 3, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 950, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.bands_color.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"3D crystals", None))
        self.fermi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.rashba.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mAB.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_kanemele.setText(QCoreApplication.translate("MainWindow", u"Kane-Mele", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Exchange field", None))
        self.label_antihaldane.setText(QCoreApplication.translate("MainWindow", u"Anti-Haldane", None))
        self.kanemele.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mAF.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_rashba.setText(QCoreApplication.translate("MainWindow", u"Rashba", None))
        self.label_mAF.setText(QCoreApplication.translate("MainWindow", u"Antiferromagnetism", None))
        self.label_mAB.setText(QCoreApplication.translate("MainWindow", u"Sublattice imbalance", None))
        self.label_haldane.setText(QCoreApplication.translate("MainWindow", u"Haldane", None))
        self.label_swave.setText(QCoreApplication.translate("MainWindow", u"swave pairing", None))
        self.haldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_fermi.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
#if QT_CONFIG(tooltip)
        self.exchange.setToolTip(QCoreApplication.translate("MainWindow", u"Exchange field in the system, taken as a vector with component Jx, Jy and Jz", None))
#endif // QT_CONFIG(tooltip)
        self.exchange.setText(QCoreApplication.translate("MainWindow", u"0.0, 0.0, 0.0", None))
        self.antihaldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.swave.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Strain", None))
        self.strain.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Terms in the Hamiltonian", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.show_structure_3d.setText(QCoreApplication.translate("MainWindow", u"Show 3D structure", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.nsuper_struct.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Structure", None))
        self.bands_color.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.bands_color.setItemText(1, QCoreApplication.translate("MainWindow", u"Sx", None))
        self.bands_color.setItemText(2, QCoreApplication.translate("MainWindow", u"Sy", None))
        self.bands_color.setItemText(3, QCoreApplication.translate("MainWindow", u"Sz", None))
        self.bands_color.setItemText(4, QCoreApplication.translate("MainWindow", u"Valley", None))
        self.bands_color.setItemText(5, QCoreApplication.translate("MainWindow", u"IPR", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.nk_bands.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Colormap", None))
        self.show_bands.setText(QCoreApplication.translate("MainWindow", u"Band structure", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Bands", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.dos_nk.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.label_dos_mode.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.dos_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"ED", None))
        self.dos_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"Green", None))
        self.dos_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"KPM", None))

        self.label_dos_operator.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.show_dos.setText(QCoreApplication.translate("MainWindow", u"Density of states", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"DOS", None))
        self.label_iets_1.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.delta_iets.setText(QCoreApplication.translate("MainWindow", u"0.05", None))
        self.label_iets_2.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.ne_iets.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_iets_3.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.window_iets.setText(QCoreApplication.translate("MainWindow", u"5.0", None))
        self.label_iets_4.setText(QCoreApplication.translate("MainWindow", u"# q-points", None))
        self.nq_iets.setText(QCoreApplication.translate("MainWindow", u"80", None))
        self.label_iets_5.setText(QCoreApplication.translate("MainWindow", u"# k-points (BZ mesh)", None))
        self.nk_iets.setText(QCoreApplication.translate("MainWindow", u"80", None))
        self.show_iets_qdos.setText(QCoreApplication.translate("MainWindow", u"Show IETS QDOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_iets_qdos), QCoreApplication.translate("MainWindow", u"IETS QDOS", None))
        self.kdos_ewindow.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.kdos_mesh.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"# of points", None))
        self.show_kdos.setText(QCoreApplication.translate("MainWindow", u"Show Surface DOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"SDOS", None))
        self.scf_initialization.setItemText(0, QCoreApplication.translate("MainWindow", u"antiferro", None))
        self.scf_initialization.setItemText(1, QCoreApplication.translate("MainWindow", u"ferro", None))
        self.scf_initialization.setItemText(2, QCoreApplication.translate("MainWindow", u"random", None))

        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Initialization", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Filling", None))
        self.filling_scf.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.do_scf.setText(QCoreApplication.translate("MainWindow", u"Include mean field", None))
        self.solve_scf.setText(QCoreApplication.translate("MainWindow", u"Solve SCF", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_12), QCoreApplication.translate("MainWindow", u"Basic", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Mixing", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"# of kpoints", None))
        self.nk_scf.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.mix_scf.setText(QCoreApplication.translate("MainWindow", u"0.9", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.smearing_scf.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.label_scf_solver.setText(QCoreApplication.translate("MainWindow", u"Solver", None))
        self.scf_solver.setItemText(0, QCoreApplication.translate("MainWindow", u"linear_mixing", None))
        self.scf_solver.setItemText(1, QCoreApplication.translate("MainWindow", u"error_gradient", None))
        self.scf_solver.setItemText(2, QCoreApplication.translate("MainWindow", u"krylov", None))

#if QT_CONFIG(tooltip)
        self.scf_solver.setToolTip(QCoreApplication.translate("MainWindow", u"Iterative algorithm used to converge the self-consistent mean field (requires the optional jax extra; falls back to the default plain-mixing solver for a Hamiltonian with superconducting pairing)", None))
#endif // QT_CONFIG(tooltip)
        self.label_scf_maxite.setText(QCoreApplication.translate("MainWindow", u"Max iterations", None))
        self.scf_maxite.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_11), QCoreApplication.translate("MainWindow", u"Convergence", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"SCF", None))
        self.magnetization_nrep.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Unit cells", None))
        self.show_magnetism.setText(QCoreApplication.translate("MainWindow", u"Show magnetism", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_13), QCoreApplication.translate("MainWindow", u"Magnetism", None))
        self.label_site_dos_info.setText(QCoreApplication.translate("MainWindow", u"Click a site in the structure plot to compute the DOS there", None))
        self.label_site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.label_site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.show_site_dos.setText(QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_site_dos), QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.nsuper.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Type of lattice", None))
        self.lattice.setItemText(0, QCoreApplication.translate("MainWindow", u"Diamond", None))
        self.lattice.setItemText(1, QCoreApplication.translate("MainWindow", u"Cubic", None))
        self.lattice.setItemText(2, QCoreApplication.translate("MainWindow", u"Pyrochlore", None))
        self.lattice.setItemText(3, QCoreApplication.translate("MainWindow", u"Hyperhoneycomb", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Geometry", None))
#if QT_CONFIG(tooltip)
        self.remove_single_bonded.setToolTip(QCoreApplication.translate("MainWindow", u"Remove atoms that have a single bond in the structure", None))
#endif // QT_CONFIG(tooltip)
        self.remove_single_bonded.setText(QCoreApplication.translate("MainWindow", u"Remove single bonds", None))
        self.remove_selected.setText(QCoreApplication.translate("MainWindow", u"Remove selected atoms", None))
        self.select_atoms_removal.setText(QCoreApplication.translate("MainWindow", u"Select atoms to remove", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_10), QCoreApplication.translate("MainWindow", u"Modify geometry", None))
        self.save_results.setText(QCoreApplication.translate("MainWindow", u"Save results", None))
        self.load_results.setText(QCoreApplication.translate("MainWindow", u"Load results", None))
    # retranslateUi

