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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QMainWindow,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QWidget)

from qfluentwidgets import (BodyLabel, CheckBox, ComboBox, LineEdit,
    PushButton)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(934, 706)
        MainWindow.setMinimumSize(QSize(934, 706))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_21 = QGridLayout(self.centralwidget)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_19 = QGridLayout(self.tab_3)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_9 = BodyLabel(self.tab_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)

        self.label_8 = BodyLabel(self.tab_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)

        self.mAB = LineEdit(self.tab_3)
        self.mAB.setObjectName(u"mAB")

        self.gridLayout_3.addWidget(self.mAB, 0, 1, 1, 1)

        self.peierls = LineEdit(self.tab_3)
        self.peierls.setObjectName(u"peierls")

        self.gridLayout_3.addWidget(self.peierls, 2, 1, 1, 1)

        self.fermi = LineEdit(self.tab_3)
        self.fermi.setObjectName(u"fermi")

        self.gridLayout_3.addWidget(self.fermi, 1, 1, 1, 1)

        self.label_10 = BodyLabel(self.tab_3)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 2, 0, 1, 1)

        self.label_36 = BodyLabel(self.tab_3)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_3.addWidget(self.label_36, 3, 0, 1, 1)

        self.haldane = LineEdit(self.tab_3)
        self.haldane.setObjectName(u"haldane")

        self.gridLayout_3.addWidget(self.haldane, 3, 1, 1, 1)

        self.crystalfield = LineEdit(self.tab_3)
        self.crystalfield.setObjectName(u"crystalfield")

        self.gridLayout_3.addWidget(self.crystalfield, 4, 1, 1, 1)

        self.label_38 = BodyLabel(self.tab_3)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_3.addWidget(self.label_38, 4, 0, 1, 1)


        self.gridLayout_19.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.gridLayout_20 = QGridLayout(self.tab_11)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.edge_potential = LineEdit(self.tab_11)
        self.edge_potential.setObjectName(u"edge_potential")

        self.gridLayout_14.addWidget(self.edge_potential, 0, 1, 1, 1)

        self.label_35 = BodyLabel(self.tab_11)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_14.addWidget(self.label_35, 0, 0, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_14, 0, 0, 1, 1)

        self.show_potential = PushButton(self.tab_11)
        self.show_potential.setObjectName(u"show_potential")

        self.gridLayout_20.addWidget(self.show_potential, 1, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_11, "")

        self.gridLayout_21.addWidget(self.tabWidget_2, 0, 0, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.show_lattice = PushButton(self.centralwidget)
        self.show_lattice.setObjectName(u"show_lattice")

        self.gridLayout_6.addWidget(self.show_lattice, 0, 0, 1, 1)

        self.initialize = PushButton(self.centralwidget)
        self.initialize.setObjectName(u"initialize")

        self.gridLayout_6.addWidget(self.initialize, 1, 0, 1, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_6.addWidget(self.save_results, 2, 0, 1, 1)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_6.addWidget(self.load_results, 3, 0, 1, 1)


        self.gridLayout_21.addLayout(self.gridLayout_6, 0, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")

        self.gridLayout_21.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_24 = QGridLayout(self.groupBox)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.geometry_mode = ComboBox(self.groupBox)
        self.geometry_mode.addItem("")
        self.geometry_mode.setObjectName(u"geometry_mode")

        self.gridLayout_4.addWidget(self.geometry_mode, 0, 1, 1, 1)

        self.label_11 = BodyLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)


        self.gridLayout_24.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(self.groupBox)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_22 = QGridLayout(self.tab)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lattice = ComboBox(self.tab)
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.setObjectName(u"lattice")

        self.gridLayout.addWidget(self.lattice, 0, 1, 1, 1)

        self.label_2 = BodyLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_5 = BodyLabel(self.tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(False)

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_3 = BodyLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.rotation = LineEdit(self.tab)
        self.rotation.setObjectName(u"rotation")

        self.gridLayout.addWidget(self.rotation, 1, 1, 1, 1)

        self.target_diameter = CheckBox(self.tab)
        self.target_diameter.setObjectName(u"target_diameter")
        self.target_diameter.setEnabled(False)

        self.gridLayout.addWidget(self.target_diameter, 4, 1, 1, 1)

        self.clean_island = CheckBox(self.tab)
        self.clean_island.setObjectName(u"clean_island")

        self.gridLayout.addWidget(self.clean_island, 3, 1, 1, 1)

        self.label = BodyLabel(self.tab)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_4 = BodyLabel(self.tab)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_6 = BodyLabel(self.tab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setEnabled(False)

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.desired_dameter = LineEdit(self.tab)
        self.desired_dameter.setObjectName(u"desired_dameter")
        self.desired_dameter.setEnabled(False)

        self.gridLayout.addWidget(self.desired_dameter, 5, 1, 1, 1)

        self.size = LineEdit(self.tab)
        self.size.setObjectName(u"size")

        self.gridLayout.addWidget(self.size, 2, 1, 1, 1)


        self.gridLayout_22.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_23 = QGridLayout(self.tab_2)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.nedges = LineEdit(self.tab_2)
        self.nedges.setObjectName(u"nedges")

        self.gridLayout_2.addWidget(self.nedges, 0, 1, 1, 1)

        self.label_7 = BodyLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)


        self.gridLayout_23.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_24.addWidget(self.tabWidget, 1, 0, 1, 1)


        self.gridLayout_21.addWidget(self.groupBox, 2, 0, 1, 1)

        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_16 = QGridLayout(self.tab_4)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.show_ldos = PushButton(self.tab_4)
        self.show_ldos.setObjectName(u"show_ldos")

        self.gridLayout_16.addWidget(self.show_ldos, 0, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_15 = BodyLabel(self.tab_4)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_5.addWidget(self.label_15, 4, 0, 1, 1)

        self.label_14 = BodyLabel(self.tab_4)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_5.addWidget(self.label_14, 3, 0, 1, 1)

        self.label_13 = BodyLabel(self.tab_4)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_5.addWidget(self.label_13, 2, 0, 1, 1)

        self.select_atoms_dos = PushButton(self.tab_4)
        self.select_atoms_dos.setObjectName(u"select_atoms_dos")

        self.gridLayout_5.addWidget(self.select_atoms_dos, 0, 0, 1, 1)

        self.label_12 = BodyLabel(self.tab_4)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_5.addWidget(self.label_12, 1, 0, 1, 1)

        self.LDOS_num_atom = LineEdit(self.tab_4)
        self.LDOS_num_atom.setObjectName(u"LDOS_num_atom")

        self.gridLayout_5.addWidget(self.LDOS_num_atom, 0, 1, 1, 1)

        self.LDOS_polynomials = LineEdit(self.tab_4)
        self.LDOS_polynomials.setObjectName(u"LDOS_polynomials")

        self.gridLayout_5.addWidget(self.LDOS_polynomials, 1, 1, 1, 1)

        self.smearing_local_dos = LineEdit(self.tab_4)
        self.smearing_local_dos.setObjectName(u"smearing_local_dos")

        self.gridLayout_5.addWidget(self.smearing_local_dos, 2, 1, 1, 1)

        self.num_ene_ldos = LineEdit(self.tab_4)
        self.num_ene_ldos.setObjectName(u"num_ene_ldos")

        self.gridLayout_5.addWidget(self.num_ene_ldos, 3, 1, 1, 1)

        self.energy_cutoff_local_dos = LineEdit(self.tab_4)
        self.energy_cutoff_local_dos.setObjectName(u"energy_cutoff_local_dos")

        self.gridLayout_5.addWidget(self.energy_cutoff_local_dos, 4, 1, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_5, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_15 = QGridLayout(self.tab_5)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.show_dos = PushButton(self.tab_5)
        self.show_dos.setObjectName(u"show_dos")

        self.gridLayout_15.addWidget(self.show_dos, 0, 0, 1, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_16 = BodyLabel(self.tab_5)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_7.addWidget(self.label_16, 3, 0, 1, 1)

        self.label_17 = BodyLabel(self.tab_5)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_7.addWidget(self.label_17, 2, 0, 1, 1)

        self.label_19 = BodyLabel(self.tab_5)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_7.addWidget(self.label_19, 0, 0, 1, 1)

        self.DOS_polynomials = LineEdit(self.tab_5)
        self.DOS_polynomials.setObjectName(u"DOS_polynomials")

        self.gridLayout_7.addWidget(self.DOS_polynomials, 0, 1, 1, 1)

        self.DOS_iterations = LineEdit(self.tab_5)
        self.DOS_iterations.setObjectName(u"DOS_iterations")

        self.gridLayout_7.addWidget(self.DOS_iterations, 1, 1, 1, 1)

        self.smearing_dos = LineEdit(self.tab_5)
        self.smearing_dos.setObjectName(u"smearing_dos")

        self.gridLayout_7.addWidget(self.smearing_dos, 2, 1, 1, 1)

        self.num_ene_dos = LineEdit(self.tab_5)
        self.num_ene_dos.setObjectName(u"num_ene_dos")

        self.gridLayout_7.addWidget(self.num_ene_dos, 3, 1, 1, 1)

        self.label_18 = BodyLabel(self.tab_5)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_7.addWidget(self.label_18, 1, 0, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_7, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_17 = QGridLayout(self.tab_6)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.show_spatial_dos = PushButton(self.tab_6)
        self.show_spatial_dos.setObjectName(u"show_spatial_dos")

        self.gridLayout_17.addWidget(self.show_spatial_dos, 0, 0, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.mode_dosmap = ComboBox(self.tab_6)
        self.mode_dosmap.addItem("")
        self.mode_dosmap.addItem("")
        self.mode_dosmap.setObjectName(u"mode_dosmap")

        self.gridLayout_11.addWidget(self.mode_dosmap, 0, 1, 1, 1)

        self.label_27 = BodyLabel(self.tab_6)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_11.addWidget(self.label_27, 0, 0, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_11, 1, 0, 1, 1)

        self.tabWidget_4 = QTabWidget(self.tab_6)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.gridLayoutWidget_8 = QWidget(self.tab_7)
        self.gridLayoutWidget_8.setObjectName(u"gridLayoutWidget_8")
        self.gridLayoutWidget_8.setGeometry(QRect(40, 10, 241, 141))
        self.gridLayout_8 = QGridLayout(self.gridLayoutWidget_8)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_20 = BodyLabel(self.gridLayoutWidget_8)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_8.addWidget(self.label_20, 0, 0, 1, 1)

        self.label_21 = BodyLabel(self.gridLayoutWidget_8)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_8.addWidget(self.label_21, 1, 0, 1, 1)

        self.label_22 = BodyLabel(self.gridLayoutWidget_8)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_8.addWidget(self.label_22, 2, 0, 1, 1)

        self.mode_stm = ComboBox(self.gridLayoutWidget_8)
        self.mode_stm.addItem("")
        self.mode_stm.addItem("")
        self.mode_stm.setObjectName(u"mode_stm")

        self.gridLayout_8.addWidget(self.mode_stm, 0, 1, 1, 1)

        self.smearing_spatial_DOS = LineEdit(self.gridLayoutWidget_8)
        self.smearing_spatial_DOS.setObjectName(u"smearing_spatial_DOS")

        self.gridLayout_8.addWidget(self.smearing_spatial_DOS, 1, 1, 1, 1)

        self.nwaves_dos = LineEdit(self.gridLayoutWidget_8)
        self.nwaves_dos.setObjectName(u"nwaves_dos")

        self.gridLayout_8.addWidget(self.nwaves_dos, 2, 1, 1, 1)

        self.tabWidget_4.addTab(self.tab_7, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.gridLayoutWidget_9 = QWidget(self.tab_8)
        self.gridLayoutWidget_9.setObjectName(u"gridLayoutWidget_9")
        self.gridLayoutWidget_9.setGeometry(QRect(80, 40, 160, 80))
        self.gridLayout_9 = QGridLayout(self.gridLayoutWidget_9)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.energy_spatial_DOS = LineEdit(self.gridLayoutWidget_9)
        self.energy_spatial_DOS.setObjectName(u"energy_spatial_DOS")

        self.gridLayout_9.addWidget(self.energy_spatial_DOS, 0, 1, 1, 1)

        self.label_23 = BodyLabel(self.gridLayoutWidget_9)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_9.addWidget(self.label_23, 0, 0, 1, 1)

        self.tabWidget_4.addTab(self.tab_8, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.gridLayoutWidget_10 = QWidget(self.tab_9)
        self.gridLayoutWidget_10.setObjectName(u"gridLayoutWidget_10")
        self.gridLayoutWidget_10.setGeometry(QRect(70, 40, 201, 113))
        self.gridLayout_10 = QGridLayout(self.gridLayoutWidget_10)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_24 = BodyLabel(self.gridLayoutWidget_10)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_10.addWidget(self.label_24, 0, 0, 1, 1)

        self.label_25 = BodyLabel(self.gridLayoutWidget_10)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_10.addWidget(self.label_25, 1, 0, 1, 1)

        self.label_26 = BodyLabel(self.gridLayoutWidget_10)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_10.addWidget(self.label_26, 2, 0, 1, 1)

        self.mine_movie = LineEdit(self.gridLayoutWidget_10)
        self.mine_movie.setObjectName(u"mine_movie")

        self.gridLayout_10.addWidget(self.mine_movie, 0, 1, 1, 1)

        self.maxe_movie = LineEdit(self.gridLayoutWidget_10)
        self.maxe_movie.setObjectName(u"maxe_movie")

        self.gridLayout_10.addWidget(self.maxe_movie, 1, 1, 1, 1)

        self.stepse_movie = LineEdit(self.gridLayoutWidget_10)
        self.stepse_movie.setObjectName(u"stepse_movie")

        self.gridLayout_10.addWidget(self.stepse_movie, 2, 1, 1, 1)

        self.tabWidget_4.addTab(self.tab_9, "")

        self.gridLayout_17.addWidget(self.tabWidget_4, 2, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_6, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.gridLayout_18 = QGridLayout(self.tab_10)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.show_path_dos = PushButton(self.tab_10)
        self.show_path_dos.setObjectName(u"show_path_dos")

        self.gridLayout_18.addWidget(self.show_path_dos, 0, 0, 1, 2)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_33 = BodyLabel(self.tab_10)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_13.addWidget(self.label_33, 2, 0, 1, 1)

        self.label_32 = BodyLabel(self.tab_10)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_13.addWidget(self.label_32, 1, 0, 1, 1)

        self.label_31 = BodyLabel(self.tab_10)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_13.addWidget(self.label_31, 0, 0, 1, 1)

        self.label_34 = BodyLabel(self.tab_10)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_13.addWidget(self.label_34, 3, 0, 1, 1)

        self.pols_path = LineEdit(self.tab_10)
        self.pols_path.setObjectName(u"pols_path")

        self.gridLayout_13.addWidget(self.pols_path, 0, 1, 1, 1)

        self.ecut_path = LineEdit(self.tab_10)
        self.ecut_path.setObjectName(u"ecut_path")

        self.gridLayout_13.addWidget(self.ecut_path, 1, 1, 1, 1)

        self.num_ene_path = LineEdit(self.tab_10)
        self.num_ene_path.setObjectName(u"num_ene_path")

        self.gridLayout_13.addWidget(self.num_ene_path, 2, 1, 1, 1)

        self.smearing_path_dos = LineEdit(self.tab_10)
        self.smearing_path_dos.setObjectName(u"smearing_path_dos")

        self.gridLayout_13.addWidget(self.smearing_path_dos, 3, 1, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_13, 1, 0, 2, 2)

        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_29 = BodyLabel(self.tab_10)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_12.addWidget(self.label_29, 1, 0, 1, 1)

        self.label_30 = BodyLabel(self.tab_10)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_12.addWidget(self.label_30, 2, 0, 1, 1)

        self.label_28 = BodyLabel(self.tab_10)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_12.addWidget(self.label_28, 0, 0, 1, 1)

        self.initial_atom = LineEdit(self.tab_10)
        self.initial_atom.setObjectName(u"initial_atom")

        self.gridLayout_12.addWidget(self.initial_atom, 0, 1, 1, 1)

        self.final_atom = LineEdit(self.tab_10)
        self.final_atom.setObjectName(u"final_atom")

        self.gridLayout_12.addWidget(self.final_atom, 1, 1, 1, 1)

        self.width_path = LineEdit(self.tab_10)
        self.width_path.setObjectName(u"width_path")

        self.gridLayout_12.addWidget(self.width_path, 2, 1, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_12, 4, 0, 1, 2)

        self.show_path = PushButton(self.tab_10)
        self.show_path.setObjectName(u"show_path")

        self.gridLayout_18.addWidget(self.show_path, 3, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_10, "")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.gridLayout_26 = QGridLayout(self.tab_12)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_25 = QGridLayout()
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.label_37 = BodyLabel(self.tab_12)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_25.addWidget(self.label_37, 0, 0, 1, 1)

        self.num_eigenvalues = LineEdit(self.tab_12)
        self.num_eigenvalues.setObjectName(u"num_eigenvalues")

        self.gridLayout_25.addWidget(self.num_eigenvalues, 0, 1, 1, 1)


        self.gridLayout_26.addLayout(self.gridLayout_25, 0, 0, 1, 1)

        self.show_eigenvalues = PushButton(self.tab_12)
        self.show_eigenvalues.setObjectName(u"show_eigenvalues")

        self.gridLayout_26.addWidget(self.show_eigenvalues, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_12, "")

        self.gridLayout_21.addWidget(self.tabWidget_3, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 934, 25))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Huge islands", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Fermi shift", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"AB imbalance", None))
#if QT_CONFIG(tooltip)
        self.mAB.setToolTip(QCoreApplication.translate("MainWindow", u"Sublattice imbalance in a bipartite lattice", None))
#endif // QT_CONFIG(tooltip)
        self.mAB.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
#if QT_CONFIG(tooltip)
        self.peierls.setToolTip(QCoreApplication.translate("MainWindow", u"Orbital magnetic field, creates Landau levels", None))
#endif // QT_CONFIG(tooltip)
        self.peierls.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
#if QT_CONFIG(tooltip)
        self.fermi.setToolTip(QCoreApplication.translate("MainWindow", u"Global shift of the onsite energies", None))
#endif // QT_CONFIG(tooltip)
        self.fermi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Magnetic field", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Haldane", None))
#if QT_CONFIG(tooltip)
        self.haldane.setToolTip(QCoreApplication.translate("MainWindow", u"Haldane coupling, creates a quantum anomalous Hall state", None))
#endif // QT_CONFIG(tooltip)
        self.haldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
#if QT_CONFIG(tooltip)
        self.crystalfield.setToolTip(QCoreApplication.translate("MainWindow", u"Crystal field that makes the edge atoms inequivalent", None))
#endif // QT_CONFIG(tooltip)
        self.crystalfield.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Crystal field", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Global parameters", None))
#if QT_CONFIG(tooltip)
        self.edge_potential.setToolTip(QCoreApplication.translate("MainWindow", u"This term will introduce an onsite term in the edge atoms", None))
#endif // QT_CONFIG(tooltip)
        self.edge_potential.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Potential", None))
#if QT_CONFIG(tooltip)
        self.show_potential.setToolTip(QCoreApplication.translate("MainWindow", u"This shows in which atoms the edge potential is added", None))
#endif // QT_CONFIG(tooltip)
        self.show_potential.setText(QCoreApplication.translate("MainWindow", u"Show edge atoms", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_11), QCoreApplication.translate("MainWindow", u"Edge perturbation", None))
#if QT_CONFIG(tooltip)
        self.show_lattice.setToolTip(QCoreApplication.translate("MainWindow", u"Show the geometry created", None))
#endif // QT_CONFIG(tooltip)
        self.show_lattice.setText(QCoreApplication.translate("MainWindow", u"Show island", None))
#if QT_CONFIG(tooltip)
        self.initialize.setToolTip(QCoreApplication.translate("MainWindow", u"Write the Hamiltonian to a file, to allow quick access for the rest of the computations", None))
#endif // QT_CONFIG(tooltip)
        self.initialize.setText(QCoreApplication.translate("MainWindow", u"Initialize Hamiltonian", None))
#if QT_CONFIG(tooltip)
        self.save_results.setToolTip(QCoreApplication.translate("MainWindow", u"Copy the results to a local folder", None))
#endif // QT_CONFIG(tooltip)
        self.save_results.setText(QCoreApplication.translate("MainWindow", u"Save results", None))
#if QT_CONFIG(tooltip)
        self.load_results.setToolTip(QCoreApplication.translate("MainWindow", u"Restore the parameters and results from the last saved state", None))
#endif // QT_CONFIG(tooltip)
        self.load_results.setText(QCoreApplication.translate("MainWindow", u"Load results", None))
        self.groupBox_3.setTitle("")
        self.groupBox.setTitle("")
        self.geometry_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"Recipe", None))

        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Geometry generation mode", None))
        self.lattice.setItemText(0, QCoreApplication.translate("MainWindow", u"Honeycomb", None))
        self.lattice.setItemText(1, QCoreApplication.translate("MainWindow", u"Square", None))
        self.lattice.setItemText(2, QCoreApplication.translate("MainWindow", u"Triangular", None))
        self.lattice.setItemText(3, QCoreApplication.translate("MainWindow", u"Lieb", None))
        self.lattice.setItemText(4, QCoreApplication.translate("MainWindow", u"Kagome", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Target diameter", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Size", None))
#if QT_CONFIG(tooltip)
        self.rotation.setToolTip(QCoreApplication.translate("MainWindow", u"Global rotation of the unit cell used to build the island", None))
#endif // QT_CONFIG(tooltip)
        self.rotation.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.target_diameter.setText("")
        self.clean_island.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Lattice", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Remove single bonded", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Desired diameter", None))
        self.desired_dameter.setText(QCoreApplication.translate("MainWindow", u"40", None))
#if QT_CONFIG(tooltip)
        self.size.setToolTip(QCoreApplication.translate("MainWindow", u"Size of the supercell used to build the island, controls the overal size of hte island", None))
#endif // QT_CONFIG(tooltip)
        self.size.setText(QCoreApplication.translate("MainWindow", u"11", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Common options", None))
        self.nedges.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Number of edges", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Recipe", None))
#if QT_CONFIG(tooltip)
        self.tabWidget_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.show_ldos.setToolTip(QCoreApplication.translate("MainWindow", u"Shows the local density of states in specific atoms", None))
#endif // QT_CONFIG(tooltip)
        self.show_ldos.setText(QCoreApplication.translate("MainWindow", u"Compute DOS in certain atoms", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Energy cutoff", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Number of energies", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.select_atoms_dos.setText(QCoreApplication.translate("MainWindow", u"Select atoms", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"# of polynomials", None))
        self.LDOS_num_atom.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.LDOS_polynomials.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.smearing_local_dos.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.num_ene_ldos.setText(QCoreApplication.translate("MainWindow", u"2000", None))
        self.energy_cutoff_local_dos.setText(QCoreApplication.translate("MainWindow", u"0.8", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Local DOS", None))
#if QT_CONFIG(tooltip)
        self.show_dos.setToolTip(QCoreApplication.translate("MainWindow", u"Show the density of states avergaed over the whole sample", None))
#endif // QT_CONFIG(tooltip)
        self.show_dos.setText(QCoreApplication.translate("MainWindow", u"Compute total DOS ", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"# of polynomials", None))
        self.DOS_polynomials.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.DOS_iterations.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.smearing_dos.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.num_ene_dos.setText(QCoreApplication.translate("MainWindow", u"6000", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Iterations", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Total DOS", None))
#if QT_CONFIG(tooltip)
        self.show_spatial_dos.setToolTip(QCoreApplication.translate("MainWindow", u"Show a spatial profile of the density of states at a specific energy", None))
#endif // QT_CONFIG(tooltip)
        self.show_spatial_dos.setText(QCoreApplication.translate("MainWindow", u"Compute spatially resolved DOS", None))
        self.mode_dosmap.setItemText(0, QCoreApplication.translate("MainWindow", u"Single shot", None))
        self.mode_dosmap.setItemText(1, QCoreApplication.translate("MainWindow", u"Movie", None))

        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Mode ofr spatial DOS", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"# of waves", None))
        self.mode_stm.setItemText(0, QCoreApplication.translate("MainWindow", u"Eigen", None))
        self.mode_stm.setItemText(1, QCoreApplication.translate("MainWindow", u"Full", None))

        self.smearing_spatial_DOS.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.nwaves_dos.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"Common options", None))
        self.energy_spatial_DOS.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Energy", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"Single shot", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Initial energy", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Final energy", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.mine_movie.setText(QCoreApplication.translate("MainWindow", u"-0.5", None))
        self.maxe_movie.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.stepse_movie.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"Movie", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"DOS map", None))
#if QT_CONFIG(tooltip)
        self.show_path_dos.setToolTip(QCoreApplication.translate("MainWindow", u"Shows the density of states in a sequence of atoms that intersect a certain line", None))
#endif // QT_CONFIG(tooltip)
        self.show_path_dos.setText(QCoreApplication.translate("MainWindow", u"Compute DOS in a line of atoms", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Energy cutoff", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"# of polynomials", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.pols_path.setText(QCoreApplication.translate("MainWindow", u"200", None))
        self.ecut_path.setText(QCoreApplication.translate("MainWindow", u"0.8", None))
        self.num_ene_path.setText(QCoreApplication.translate("MainWindow", u"2000", None))
        self.smearing_path_dos.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Final atom", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Width accepted", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Initial atom", None))
        self.initial_atom.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.final_atom.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.width_path.setText(QCoreApplication.translate("MainWindow", u"1.5", None))
        self.show_path.setText(QCoreApplication.translate("MainWindow", u"Show path", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_10), QCoreApplication.translate("MainWindow", u"DOS in a line", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"# of eigenvalues", None))
#if QT_CONFIG(tooltip)
        self.num_eigenvalues.setToolTip(QCoreApplication.translate("MainWindow", u"Minimum number of eigenvalues to compute (for small systems all of them will be computed)", None))
#endif // QT_CONFIG(tooltip)
        self.num_eigenvalues.setText(QCoreApplication.translate("MainWindow", u"40", None))
        self.show_eigenvalues.setText(QCoreApplication.translate("MainWindow", u"Show eigenvalues", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_12), QCoreApplication.translate("MainWindow", u"Eigenvalues", None))
    # retranslateUi

