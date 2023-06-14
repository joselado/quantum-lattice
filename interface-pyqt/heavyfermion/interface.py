# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1308, 653)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_24 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.exchange = QtWidgets.QLineEdit(self.tab_3)
        self.exchange.setObjectName("exchange")
        self.gridLayout.addWidget(self.exchange, 4, 1, 1, 1)
        self.label_60 = QtWidgets.QLabel(self.tab_3)
        self.label_60.setObjectName("label_60")
        self.gridLayout.addWidget(self.label_60, 1, 0, 1, 1)
        self.label_39 = QtWidgets.QLabel(self.tab_3)
        self.label_39.setObjectName("label_39")
        self.gridLayout.addWidget(self.label_39, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.fermi = QtWidgets.QLineEdit(self.tab_3)
        self.fermi.setEnabled(True)
        self.fermi.setObjectName("fermi")
        self.gridLayout.addWidget(self.fermi, 2, 1, 1, 1)
        self.hoppings = QtWidgets.QLineEdit(self.tab_3)
        self.hoppings.setObjectName("hoppings")
        self.gridLayout.addWidget(self.hoppings, 1, 1, 1, 1)
        self.kondo = QtWidgets.QLineEdit(self.tab_3)
        self.kondo.setObjectName("kondo")
        self.gridLayout.addWidget(self.kondo, 3, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.tab_3)
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 3, 0, 1, 1)
        self.gridLayout_24.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_3, "")
        self.gridLayout_6.addWidget(self.tabWidget_2, 0, 0, 2, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)
        self.lattice = QtWidgets.QComboBox(self.tab_2)
        self.lattice.setObjectName("lattice")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.gridLayout_4.addWidget(self.lattice, 0, 1, 1, 1)
        self.nsuper = QtWidgets.QLineEdit(self.tab_2)
        self.nsuper.setObjectName("nsuper")
        self.gridLayout_4.addWidget(self.nsuper, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 1, 0, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_25 = QtWidgets.QGridLayout()
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.remove_single_bonded = QtWidgets.QCheckBox(self.tab_7)
        self.remove_single_bonded.setChecked(True)
        self.remove_single_bonded.setObjectName("remove_single_bonded")
        self.gridLayout_25.addWidget(self.remove_single_bonded, 0, 0, 1, 1)
        self.remove_selected = QtWidgets.QCheckBox(self.tab_7)
        self.remove_selected.setObjectName("remove_selected")
        self.gridLayout_25.addWidget(self.remove_selected, 1, 0, 1, 1)
        self.select_atoms_removal = QtWidgets.QPushButton(self.tab_7)
        self.select_atoms_removal.setObjectName("select_atoms_removal")
        self.gridLayout_25.addWidget(self.select_atoms_removal, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_25)
        self.tabWidget.addTab(self.tab_7, "")
        self.gridLayout_6.addWidget(self.tabWidget, 1, 1, 1, 1)
        self.tabWidget_3 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.show_structure = QtWidgets.QPushButton(self.tab_4)
        self.show_structure.setObjectName("show_structure")
        self.gridLayout_19.addWidget(self.show_structure, 1, 0, 1, 1)
        self.show_structure_3d = QtWidgets.QPushButton(self.tab_4)
        self.show_structure_3d.setObjectName("show_structure_3d")
        self.gridLayout_19.addWidget(self.show_structure_3d, 1, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.nsuper_struct = QtWidgets.QLineEdit(self.tab_4)
        self.nsuper_struct.setObjectName("nsuper_struct")
        self.gridLayout_3.addWidget(self.nsuper_struct, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab_4)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.gridLayout_19.addLayout(self.gridLayout_3, 0, 0, 1, 2)
        self.tabWidget_3.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.show_bands = QtWidgets.QPushButton(self.tab_5)
        self.show_bands.setObjectName("show_bands")
        self.gridLayout_20.addWidget(self.show_bands, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_15 = QtWidgets.QLabel(self.tab_5)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 0, 0, 1, 1)
        self.bands_color = QtWidgets.QComboBox(self.tab_5)
        self.bands_color.setObjectName("bands_color")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.gridLayout_2.addWidget(self.bands_color, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab_5)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)
        self.nk_bands = QtWidgets.QLineEdit(self.tab_5)
        self.nk_bands.setObjectName("nk_bands")
        self.gridLayout_2.addWidget(self.nk_bands, 1, 1, 1, 1)
        self.gridLayout_20.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.tab_9)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.delta_kbands = QtWidgets.QLineEdit(self.tab_9)
        self.delta_kbands.setObjectName("delta_kbands")
        self.gridLayout_11.addWidget(self.delta_kbands, 0, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.tab_9)
        self.label_27.setObjectName("label_27")
        self.gridLayout_11.addWidget(self.label_27, 0, 0, 1, 1)
        self.ne_kbands = QtWidgets.QLineEdit(self.tab_9)
        self.ne_kbands.setObjectName("ne_kbands")
        self.gridLayout_11.addWidget(self.ne_kbands, 1, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.tab_9)
        self.label_28.setObjectName("label_28")
        self.gridLayout_11.addWidget(self.label_28, 1, 0, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.tab_9)
        self.label_29.setObjectName("label_29")
        self.gridLayout_11.addWidget(self.label_29, 2, 0, 1, 1)
        self.window_kbands = QtWidgets.QLineEdit(self.tab_9)
        self.window_kbands.setObjectName("window_kbands")
        self.gridLayout_11.addWidget(self.window_kbands, 2, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.tab_9)
        self.label_30.setObjectName("label_30")
        self.gridLayout_11.addWidget(self.label_30, 3, 0, 1, 1)
        self.scale_kbands = QtWidgets.QLineEdit(self.tab_9)
        self.scale_kbands.setObjectName("scale_kbands")
        self.gridLayout_11.addWidget(self.scale_kbands, 3, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.tab_9)
        self.label_31.setObjectName("label_31")
        self.gridLayout_11.addWidget(self.label_31, 4, 0, 1, 1)
        self.nv_kbands = QtWidgets.QLineEdit(self.tab_9)
        self.nv_kbands.setObjectName("nv_kbands")
        self.gridLayout_11.addWidget(self.nv_kbands, 4, 1, 1, 1)
        self.show_dosbands = QtWidgets.QPushButton(self.tab_9)
        self.show_dosbands.setObjectName("show_dosbands")
        self.gridLayout_11.addWidget(self.show_dosbands, 6, 0, 1, 2)
        self.operator_kdos = QtWidgets.QComboBox(self.tab_9)
        self.operator_kdos.setObjectName("operator_kdos")
        self.operator_kdos.addItem("")
        self.operator_kdos.addItem("")
        self.operator_kdos.addItem("")
        self.gridLayout_11.addWidget(self.operator_kdos, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_9)
        self.label_4.setObjectName("label_4")
        self.gridLayout_11.addWidget(self.label_4, 5, 0, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_11, 0, 0, 1, 1)
        self.tabWidget_3.addTab(self.tab_9, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_36 = QtWidgets.QGridLayout()
        self.gridLayout_36.setObjectName("gridLayout_36")
        self.label_50 = QtWidgets.QLabel(self.tab_6)
        self.label_50.setObjectName("label_50")
        self.gridLayout_36.addWidget(self.label_50, 0, 0, 1, 1)
        self.label_51 = QtWidgets.QLabel(self.tab_6)
        self.label_51.setObjectName("label_51")
        self.gridLayout_36.addWidget(self.label_51, 1, 0, 1, 1)
        self.dos_ewindow = QtWidgets.QLineEdit(self.tab_6)
        self.dos_ewindow.setObjectName("dos_ewindow")
        self.gridLayout_36.addWidget(self.dos_ewindow, 1, 1, 1, 1)
        self.dos_delta = QtWidgets.QLineEdit(self.tab_6)
        self.dos_delta.setObjectName("dos_delta")
        self.gridLayout_36.addWidget(self.dos_delta, 2, 1, 1, 1)
        self.label_48 = QtWidgets.QLabel(self.tab_6)
        self.label_48.setObjectName("label_48")
        self.gridLayout_36.addWidget(self.label_48, 2, 0, 1, 1)
        self.dos_nk = QtWidgets.QLineEdit(self.tab_6)
        self.dos_nk.setObjectName("dos_nk")
        self.gridLayout_36.addWidget(self.dos_nk, 0, 1, 1, 1)
        self.dos_mode = QtWidgets.QComboBox(self.tab_6)
        self.dos_mode.setObjectName("dos_mode")
        self.dos_mode.addItem("")
        self.dos_mode.addItem("")
        self.gridLayout_36.addWidget(self.dos_mode, 3, 1, 1, 1)
        self.label_47 = QtWidgets.QLabel(self.tab_6)
        self.label_47.setObjectName("label_47")
        self.gridLayout_36.addWidget(self.label_47, 3, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_36)
        self.show_dos = QtWidgets.QPushButton(self.tab_6)
        self.show_dos.setObjectName("show_dos")
        self.verticalLayout_2.addWidget(self.show_dos)
        self.tabWidget_3.addTab(self.tab_6, "")
        self.tab_14 = QtWidgets.QWidget()
        self.tab_14.setObjectName("tab_14")
        self.gridLayout_28 = QtWidgets.QGridLayout(self.tab_14)
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.gridLayout_27 = QtWidgets.QGridLayout()
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.multildos_delta = QtWidgets.QLineEdit(self.tab_14)
        self.multildos_delta.setObjectName("multildos_delta")
        self.gridLayout_27.addWidget(self.multildos_delta, 3, 1, 1, 1)
        self.label_43 = QtWidgets.QLabel(self.tab_14)
        self.label_43.setObjectName("label_43")
        self.gridLayout_27.addWidget(self.label_43, 3, 0, 1, 1)
        self.label_44 = QtWidgets.QLabel(self.tab_14)
        self.label_44.setObjectName("label_44")
        self.gridLayout_27.addWidget(self.label_44, 0, 0, 1, 1)
        self.multildos_nk = QtWidgets.QLineEdit(self.tab_14)
        self.multildos_nk.setObjectName("multildos_nk")
        self.gridLayout_27.addWidget(self.multildos_nk, 1, 1, 1, 1)
        self.show_multildos = QtWidgets.QPushButton(self.tab_14)
        self.show_multildos.setObjectName("show_multildos")
        self.gridLayout_27.addWidget(self.show_multildos, 6, 0, 1, 2)
        self.multildos_ewindow = QtWidgets.QLineEdit(self.tab_14)
        self.multildos_ewindow.setObjectName("multildos_ewindow")
        self.gridLayout_27.addWidget(self.multildos_ewindow, 0, 1, 1, 1)
        self.label_45 = QtWidgets.QLabel(self.tab_14)
        self.label_45.setObjectName("label_45")
        self.gridLayout_27.addWidget(self.label_45, 1, 0, 1, 1)
        self.label_46 = QtWidgets.QLabel(self.tab_14)
        self.label_46.setObjectName("label_46")
        self.gridLayout_27.addWidget(self.label_46, 2, 0, 1, 1)
        self.multildos_nrep = QtWidgets.QLineEdit(self.tab_14)
        self.multildos_nrep.setObjectName("multildos_nrep")
        self.gridLayout_27.addWidget(self.multildos_nrep, 2, 1, 1, 1)
        self.basis_ldos = QtWidgets.QComboBox(self.tab_14)
        self.basis_ldos.setObjectName("basis_ldos")
        self.basis_ldos.addItem("")
        self.basis_ldos.addItem("")
        self.gridLayout_27.addWidget(self.basis_ldos, 4, 1, 1, 1)
        self.label_58 = QtWidgets.QLabel(self.tab_14)
        self.label_58.setObjectName("label_58")
        self.gridLayout_27.addWidget(self.label_58, 4, 0, 1, 1)
        self.ratomic_ldos = QtWidgets.QLineEdit(self.tab_14)
        self.ratomic_ldos.setObjectName("ratomic_ldos")
        self.gridLayout_27.addWidget(self.ratomic_ldos, 5, 1, 1, 1)
        self.label_59 = QtWidgets.QLabel(self.tab_14)
        self.label_59.setObjectName("label_59")
        self.gridLayout_27.addWidget(self.label_59, 5, 0, 1, 1)
        self.gridLayout_28.addLayout(self.gridLayout_27, 0, 0, 1, 1)
        self.tabWidget_3.addTab(self.tab_14, "")
        self.tab_16 = QtWidgets.QWidget()
        self.tab_16.setObjectName("tab_16")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.tab_16)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.fs_ewindow = QtWidgets.QLineEdit(self.tab_16)
        self.fs_ewindow.setObjectName("fs_ewindow")
        self.gridLayout_5.addWidget(self.fs_ewindow, 0, 1, 1, 1)
        self.fs_delta = QtWidgets.QLineEdit(self.tab_16)
        self.fs_delta.setObjectName("fs_delta")
        self.gridLayout_5.addWidget(self.fs_delta, 1, 1, 1, 1)
        self.fs_nk = QtWidgets.QLineEdit(self.tab_16)
        self.fs_nk.setObjectName("fs_nk")
        self.gridLayout_5.addWidget(self.fs_nk, 2, 1, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.tab_16)
        self.label_42.setObjectName("label_42")
        self.gridLayout_5.addWidget(self.label_42, 0, 0, 1, 1)
        self.label_49 = QtWidgets.QLabel(self.tab_16)
        self.label_49.setObjectName("label_49")
        self.gridLayout_5.addWidget(self.label_49, 1, 0, 1, 1)
        self.label_52 = QtWidgets.QLabel(self.tab_16)
        self.label_52.setObjectName("label_52")
        self.gridLayout_5.addWidget(self.label_52, 2, 0, 1, 1)
        self.show_fermi_surface = QtWidgets.QPushButton(self.tab_16)
        self.show_fermi_surface.setObjectName("show_fermi_surface")
        self.gridLayout_5.addWidget(self.show_fermi_surface, 4, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.tab_16)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 3, 0, 1, 1)
        self.fs_operator = QtWidgets.QComboBox(self.tab_16)
        self.fs_operator.setObjectName("fs_operator")
        self.fs_operator.addItem("")
        self.fs_operator.addItem("")
        self.fs_operator.addItem("")
        self.gridLayout_5.addWidget(self.fs_operator, 3, 1, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.tabWidget_3.addTab(self.tab_16, "")
        self.tab_18 = QtWidgets.QWidget()
        self.tab_18.setObjectName("tab_18")
        self.gridLayout_33 = QtWidgets.QGridLayout(self.tab_18)
        self.gridLayout_33.setObjectName("gridLayout_33")
        self.gridLayout_32 = QtWidgets.QGridLayout()
        self.gridLayout_32.setObjectName("gridLayout_32")
        self.qpi_ewindow = QtWidgets.QLineEdit(self.tab_18)
        self.qpi_ewindow.setObjectName("qpi_ewindow")
        self.gridLayout_32.addWidget(self.qpi_ewindow, 0, 1, 1, 1)
        self.qpi_delta = QtWidgets.QLineEdit(self.tab_18)
        self.qpi_delta.setObjectName("qpi_delta")
        self.gridLayout_32.addWidget(self.qpi_delta, 1, 1, 1, 1)
        self.qpi_nk = QtWidgets.QLineEdit(self.tab_18)
        self.qpi_nk.setObjectName("qpi_nk")
        self.gridLayout_32.addWidget(self.qpi_nk, 2, 1, 1, 1)
        self.label_55 = QtWidgets.QLabel(self.tab_18)
        self.label_55.setObjectName("label_55")
        self.gridLayout_32.addWidget(self.label_55, 0, 0, 1, 1)
        self.label_56 = QtWidgets.QLabel(self.tab_18)
        self.label_56.setObjectName("label_56")
        self.gridLayout_32.addWidget(self.label_56, 1, 0, 1, 1)
        self.label_57 = QtWidgets.QLabel(self.tab_18)
        self.label_57.setObjectName("label_57")
        self.gridLayout_32.addWidget(self.label_57, 2, 0, 1, 1)
        self.show_qpi = QtWidgets.QPushButton(self.tab_18)
        self.show_qpi.setObjectName("show_qpi")
        self.gridLayout_32.addWidget(self.show_qpi, 3, 0, 1, 2)
        self.gridLayout_33.addLayout(self.gridLayout_32, 0, 0, 1, 1)
        self.tabWidget_3.addTab(self.tab_18, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.kdos_ewindow = QtWidgets.QLineEdit(self.tab)
        self.kdos_ewindow.setObjectName("kdos_ewindow")
        self.gridLayout_9.addWidget(self.kdos_ewindow, 0, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.tab)
        self.label_20.setObjectName("label_20")
        self.gridLayout_9.addWidget(self.label_20, 0, 0, 1, 1)
        self.kdos_mesh = QtWidgets.QLineEdit(self.tab)
        self.kdos_mesh.setObjectName("kdos_mesh")
        self.gridLayout_9.addWidget(self.kdos_mesh, 1, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.tab)
        self.label_21.setObjectName("label_21")
        self.gridLayout_9.addWidget(self.label_21, 1, 0, 1, 1)
        self.gridLayout_22.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.show_kdos = QtWidgets.QPushButton(self.tab)
        self.show_kdos.setObjectName("show_kdos")
        self.gridLayout_22.addWidget(self.show_kdos, 1, 0, 1, 1)
        self.tabWidget_3.addTab(self.tab, "")
        self.gridLayout_6.addWidget(self.tabWidget_3, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1308, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.bands_color.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "2D systems"))
        self.exchange.setToolTip(_translate("MainWindow", "d-vector of the spin triplet order p-wave order. The momentum dependence is taken of the form px + i py"))
        self.exchange.setText(_translate("MainWindow", "0.0"))
        self.label_60.setText(_translate("MainWindow", "Hoppings"))
        self.label_39.setText(_translate("MainWindow", "Exchange coupling"))
        self.label.setText(_translate("MainWindow", "Fermi energy"))
        self.fermi.setText(_translate("MainWindow", "0.0"))
        self.hoppings.setToolTip(_translate("MainWindow", "Hoppings of the system. If you put several numbers separated by commas, the first number is the 1st NN hopping, the second number the 2nd NN hopping, etc"))
        self.hoppings.setText(_translate("MainWindow", "1.0"))
        self.kondo.setToolTip(_translate("MainWindow", "spin-singlet s-wave superconducting order"))
        self.kondo.setText(_translate("MainWindow", "0.0"))
        self.label_26.setText(_translate("MainWindow", "Kondo hybridization"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("MainWindow", "Terms in the Hamiltonian"))
        self.label_8.setText(_translate("MainWindow", "Type of lattice"))
        self.lattice.setItemText(0, _translate("MainWindow", "Triangular"))
        self.lattice.setItemText(1, _translate("MainWindow", "Honeycomb"))
        self.lattice.setItemText(2, _translate("MainWindow", "Honeycomb 4 sites"))
        self.lattice.setItemText(3, _translate("MainWindow", "Honeycomb 6 sites"))
        self.lattice.setItemText(4, _translate("MainWindow", "Square"))
        self.lattice.setItemText(5, _translate("MainWindow", "Single square"))
        self.lattice.setItemText(6, _translate("MainWindow", "Triangular tripartite"))
        self.lattice.setItemText(7, _translate("MainWindow", "Kagome"))
        self.lattice.setItemText(8, _translate("MainWindow", "Lieb"))
        self.nsuper.setText(_translate("MainWindow", "1"))
        self.label_6.setText(_translate("MainWindow", "Supercell"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Geometry"))
        self.remove_single_bonded.setToolTip(_translate("MainWindow", "Remove atoms that have a single bond in the structure"))
        self.remove_single_bonded.setText(_translate("MainWindow", "Remove single bonds"))
        self.remove_selected.setText(_translate("MainWindow", "Remove selected atoms"))
        self.select_atoms_removal.setText(_translate("MainWindow", "Select atoms to remove"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("MainWindow", "Modify geometry"))
        self.show_structure.setText(_translate("MainWindow", "Show structure"))
        self.show_structure_3d.setText(_translate("MainWindow", "Show structure 3D"))
        self.nsuper_struct.setText(_translate("MainWindow", "5"))
        self.label_7.setText(_translate("MainWindow", "Supercell"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), _translate("MainWindow", "Structure"))
        self.show_bands.setText(_translate("MainWindow", "Band structure"))
        self.label_15.setText(_translate("MainWindow", "Operator"))
        self.bands_color.setItemText(0, _translate("MainWindow", "None"))
        self.bands_color.setItemText(1, _translate("MainWindow", "dispersive_electrons"))
        self.bands_color.setItemText(2, _translate("MainWindow", "kondo_sites"))
        self.label_9.setText(_translate("MainWindow", "# kpoints"))
        self.nk_bands.setText(_translate("MainWindow", "500"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), _translate("MainWindow", "Bands"))
        self.delta_kbands.setText(_translate("MainWindow", "0.03"))
        self.label_27.setText(_translate("MainWindow", "Smearing"))
        self.ne_kbands.setText(_translate("MainWindow", "400"))
        self.label_28.setText(_translate("MainWindow", "# of energies"))
        self.label_29.setText(_translate("MainWindow", "Energy window"))
        self.window_kbands.setText(_translate("MainWindow", "3.0"))
        self.label_30.setText(_translate("MainWindow", "KPM scale"))
        self.scale_kbands.setText(_translate("MainWindow", "10.0"))
        self.label_31.setText(_translate("MainWindow", "# vectors"))
        self.nv_kbands.setText(_translate("MainWindow", "10"))
        self.show_dosbands.setToolTip(_translate("MainWindow", "This is equivalent to band structure calculation, but it can be applied for very large systems"))
        self.show_dosbands.setText(_translate("MainWindow", "Show DOS Bands"))
        self.operator_kdos.setItemText(0, _translate("MainWindow", "dispersive_electrons"))
        self.operator_kdos.setItemText(1, _translate("MainWindow", "None"))
        self.operator_kdos.setItemText(2, _translate("MainWindow", "kondo_sites"))
        self.label_4.setText(_translate("MainWindow", "Operator"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_9), _translate("MainWindow", "DOS Bands"))
        self.label_50.setText(_translate("MainWindow", "Number of kpoints"))
        self.label_51.setText(_translate("MainWindow", "Energy window"))
        self.dos_ewindow.setText(_translate("MainWindow", "4.0"))
        self.dos_delta.setText(_translate("MainWindow", "0.03"))
        self.label_48.setText(_translate("MainWindow", "Smearing"))
        self.dos_nk.setText(_translate("MainWindow", "100"))
        self.dos_mode.setItemText(0, _translate("MainWindow", "ED"))
        self.dos_mode.setItemText(1, _translate("MainWindow", "Green"))
        self.label_47.setText(_translate("MainWindow", "Mode"))
        self.show_dos.setText(_translate("MainWindow", "Density of states"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), _translate("MainWindow", "DOS"))
        self.multildos_delta.setToolTip(_translate("MainWindow", "Energy smearing"))
        self.multildos_delta.setText(_translate("MainWindow", "0.03"))
        self.label_43.setText(_translate("MainWindow", "Smearing"))
        self.label_44.setText(_translate("MainWindow", "Energy window"))
        self.multildos_nk.setToolTip(_translate("MainWindow", "Number of kpoints used"))
        self.multildos_nk.setText(_translate("MainWindow", "10"))
        self.show_multildos.setText(_translate("MainWindow", "Show LDOS"))
        self.multildos_ewindow.setToolTip(_translate("MainWindow", "Energy window"))
        self.multildos_ewindow.setText(_translate("MainWindow", "1.5"))
        self.label_45.setText(_translate("MainWindow", "Number of kpoints"))
        self.label_46.setText(_translate("MainWindow", "Number of unit cells"))
        self.multildos_nrep.setToolTip(_translate("MainWindow", "Number of replicas of the unit cell to plot"))
        self.multildos_nrep.setText(_translate("MainWindow", "5"))
        self.basis_ldos.setItemText(0, _translate("MainWindow", "TB"))
        self.basis_ldos.setItemText(1, _translate("MainWindow", "Real space atomic orbitals"))
        self.label_58.setText(_translate("MainWindow", "Basis for the LDOS"))
        self.ratomic_ldos.setText(_translate("MainWindow", "1.5"))
        self.label_59.setText(_translate("MainWindow", "Atomic radii"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_14), _translate("MainWindow", "LDOS"))
        self.fs_ewindow.setText(_translate("MainWindow", "4.0"))
        self.fs_delta.setText(_translate("MainWindow", "0.05"))
        self.fs_nk.setText(_translate("MainWindow", "60"))
        self.label_42.setText(_translate("MainWindow", "Energy window"))
        self.label_49.setText(_translate("MainWindow", "Smearing"))
        self.label_52.setText(_translate("MainWindow", "Number of kpoints"))
        self.show_fermi_surface.setText(_translate("MainWindow", "Show Fermi surface"))
        self.label_5.setText(_translate("MainWindow", "Operator"))
        self.fs_operator.setItemText(0, _translate("MainWindow", "dispersive_electrons"))
        self.fs_operator.setItemText(1, _translate("MainWindow", "kondo_sites"))
        self.fs_operator.setItemText(2, _translate("MainWindow", "None"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_16), _translate("MainWindow", "FS"))
        self.qpi_ewindow.setText(_translate("MainWindow", "4.0"))
        self.qpi_delta.setText(_translate("MainWindow", "0.05"))
        self.qpi_nk.setText(_translate("MainWindow", "60"))
        self.label_55.setText(_translate("MainWindow", "Energy window"))
        self.label_56.setText(_translate("MainWindow", "Smearing"))
        self.label_57.setText(_translate("MainWindow", "Number of kpoints"))
        self.show_qpi.setToolTip(_translate("MainWindow", "Compute the quasiparticle interference"))
        self.show_qpi.setText(_translate("MainWindow", "Show QPI"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_18), _translate("MainWindow", "QPI"))
        self.kdos_ewindow.setText(_translate("MainWindow", "0.5"))
        self.label_20.setText(_translate("MainWindow", "Energy window"))
        self.kdos_mesh.setText(_translate("MainWindow", "100"))
        self.label_21.setText(_translate("MainWindow", "# of points"))
        self.show_kdos.setText(_translate("MainWindow", "Show Surface DOS"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab), _translate("MainWindow", "SDOS"))
