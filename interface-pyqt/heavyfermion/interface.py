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
        MainWindow.resize(1308, 653)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_6 = QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_24 = QGridLayout(self.tab_3)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.kondo = LineEdit(self.tab_3)
        self.kondo.setObjectName(u"kondo")

        self.gridLayout.addWidget(self.kondo, 3, 2, 1, 1)

        self.hoppings = LineEdit(self.tab_3)
        self.hoppings.setObjectName(u"hoppings")

        self.gridLayout.addWidget(self.hoppings, 1, 2, 1, 1)

        self.label_39 = BodyLabel(self.tab_3)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout.addWidget(self.label_39, 4, 0, 1, 1)

        self.label_hopping = BodyLabel(self.tab_3)
        self.label_hopping.setObjectName(u"label_hopping")

        self.gridLayout.addWidget(self.label_hopping, 1, 0, 1, 1)

        self.fermi = LineEdit(self.tab_3)
        self.fermi.setObjectName(u"fermi")
        self.fermi.setEnabled(True)

        self.gridLayout.addWidget(self.fermi, 2, 2, 1, 1)

        self.label_kondo = BodyLabel(self.tab_3)
        self.label_kondo.setObjectName(u"label_kondo")

        self.gridLayout.addWidget(self.label_kondo, 3, 0, 1, 1)

        self.label_fermi = BodyLabel(self.tab_3)
        self.label_fermi.setObjectName(u"label_fermi")

        self.gridLayout.addWidget(self.label_fermi, 2, 0, 1, 1)

        self.exchange = LineEdit(self.tab_3)
        self.exchange.setObjectName(u"exchange")

        self.gridLayout.addWidget(self.exchange, 4, 2, 1, 1)

        self.hopping_image = BodyLabel(self.tab_3)
        self.hopping_image.setObjectName(u"hopping_image")
        self.hopping_image.setMinimumSize(QSize(20, 0))

        self.gridLayout.addWidget(self.hopping_image, 1, 1, 1, 1)

        self.fermi_image = BodyLabel(self.tab_3)
        self.fermi_image.setObjectName(u"fermi_image")

        self.gridLayout.addWidget(self.fermi_image, 2, 1, 1, 1)

        self.kondo_image = BodyLabel(self.tab_3)
        self.kondo_image.setObjectName(u"kondo_image")

        self.gridLayout.addWidget(self.kondo_image, 3, 1, 1, 1)

        self.kexchange_image = BodyLabel(self.tab_3)
        self.kexchange_image.setObjectName(u"kexchange_image")

        self.gridLayout.addWidget(self.kexchange_image, 4, 1, 1, 1)


        self.gridLayout_24.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")

        self.gridLayout_6.addWidget(self.tabWidget_2, 0, 0, 2, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_13 = QGridLayout(self.tab_2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
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


        self.gridLayout_13.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.verticalLayout = QVBoxLayout(self.tab_7)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_25 = QGridLayout()
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.remove_single_bonded = CheckBox(self.tab_7)
        self.remove_single_bonded.setObjectName(u"remove_single_bonded")
        self.remove_single_bonded.setChecked(True)

        self.gridLayout_25.addWidget(self.remove_single_bonded, 0, 0, 1, 1)

        self.remove_selected = CheckBox(self.tab_7)
        self.remove_selected.setObjectName(u"remove_selected")

        self.gridLayout_25.addWidget(self.remove_selected, 1, 0, 1, 1)

        self.select_atoms_removal = PushButton(self.tab_7)
        self.select_atoms_removal.setObjectName(u"select_atoms_removal")

        self.gridLayout_25.addWidget(self.select_atoms_removal, 2, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_25)

        self.tabWidget.addTab(self.tab_7, "")

        self.gridLayout_6.addWidget(self.tabWidget, 1, 1, 1, 1)

        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_19 = QGridLayout(self.tab_4)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.show_structure = PushButton(self.tab_4)
        self.show_structure.setObjectName(u"show_structure")

        self.gridLayout_19.addWidget(self.show_structure, 1, 0, 1, 1)

        self.show_structure_3d = PushButton(self.tab_4)
        self.show_structure_3d.setObjectName(u"show_structure_3d")

        self.gridLayout_19.addWidget(self.show_structure_3d, 1, 1, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.nsuper_struct = LineEdit(self.tab_4)
        self.nsuper_struct.setObjectName(u"nsuper_struct")

        self.gridLayout_3.addWidget(self.nsuper_struct, 0, 1, 1, 1)

        self.label_7 = BodyLabel(self.tab_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)


        self.gridLayout_19.addLayout(self.gridLayout_3, 0, 0, 1, 2)

        self.tabWidget_3.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_20 = QGridLayout(self.tab_5)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.show_bands = PushButton(self.tab_5)
        self.show_bands.setObjectName(u"show_bands")

        self.gridLayout_20.addWidget(self.show_bands, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_15 = BodyLabel(self.tab_5)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 0, 0, 1, 1)

        self.bands_color = ComboBox(self.tab_5)
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


        self.gridLayout_20.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.gridLayout_18 = QGridLayout(self.tab_9)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
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

        self.show_dosbands = PushButton(self.tab_9)
        self.show_dosbands.setObjectName(u"show_dosbands")

        self.gridLayout_11.addWidget(self.show_dosbands, 6, 0, 1, 2)

        self.operator_kdos = ComboBox(self.tab_9)
        self.operator_kdos.addItem("")
        self.operator_kdos.addItem("")
        self.operator_kdos.addItem("")
        self.operator_kdos.setObjectName(u"operator_kdos")

        self.gridLayout_11.addWidget(self.operator_kdos, 5, 1, 1, 1)

        self.label_4 = BodyLabel(self.tab_9)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_11.addWidget(self.label_4, 5, 0, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_11, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_9, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_2 = QVBoxLayout(self.tab_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_36 = QGridLayout()
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.label_50 = BodyLabel(self.tab_6)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_36.addWidget(self.label_50, 0, 0, 1, 1)

        self.label_51 = BodyLabel(self.tab_6)
        self.label_51.setObjectName(u"label_51")

        self.gridLayout_36.addWidget(self.label_51, 1, 0, 1, 1)

        self.dos_ewindow = LineEdit(self.tab_6)
        self.dos_ewindow.setObjectName(u"dos_ewindow")

        self.gridLayout_36.addWidget(self.dos_ewindow, 1, 1, 1, 1)

        self.dos_delta = LineEdit(self.tab_6)
        self.dos_delta.setObjectName(u"dos_delta")

        self.gridLayout_36.addWidget(self.dos_delta, 2, 1, 1, 1)

        self.label_48 = BodyLabel(self.tab_6)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_36.addWidget(self.label_48, 2, 0, 1, 1)

        self.dos_nk = LineEdit(self.tab_6)
        self.dos_nk.setObjectName(u"dos_nk")

        self.gridLayout_36.addWidget(self.dos_nk, 0, 1, 1, 1)

        self.dos_mode = ComboBox(self.tab_6)
        self.dos_mode.addItem("")
        self.dos_mode.addItem("")
        self.dos_mode.addItem("")
        self.dos_mode.setObjectName(u"dos_mode")

        self.gridLayout_36.addWidget(self.dos_mode, 3, 1, 1, 1)

        self.label_47 = BodyLabel(self.tab_6)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_36.addWidget(self.label_47, 3, 0, 1, 1)

        self.label_dos_operator = BodyLabel(self.tab_6)
        self.label_dos_operator.setObjectName(u"label_dos_operator")

        self.gridLayout_36.addWidget(self.label_dos_operator, 4, 0, 1, 1)

        self.dos_operator = ComboBox(self.tab_6)
        self.dos_operator.setObjectName(u"dos_operator")

        self.gridLayout_36.addWidget(self.dos_operator, 4, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_36)

        self.show_dos = PushButton(self.tab_6)
        self.show_dos.setObjectName(u"show_dos")

        self.verticalLayout_2.addWidget(self.show_dos)

        self.tabWidget_3.addTab(self.tab_6, "")
        self.tab_14 = QWidget()
        self.tab_14.setObjectName(u"tab_14")
        self.gridLayout_28 = QGridLayout(self.tab_14)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_27 = QGridLayout()
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.multildos_delta = LineEdit(self.tab_14)
        self.multildos_delta.setObjectName(u"multildos_delta")

        self.gridLayout_27.addWidget(self.multildos_delta, 3, 1, 1, 1)

        self.label_43 = BodyLabel(self.tab_14)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_27.addWidget(self.label_43, 3, 0, 1, 1)

        self.label_44 = BodyLabel(self.tab_14)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_27.addWidget(self.label_44, 0, 0, 1, 1)

        self.multildos_nk = LineEdit(self.tab_14)
        self.multildos_nk.setObjectName(u"multildos_nk")

        self.gridLayout_27.addWidget(self.multildos_nk, 1, 1, 1, 1)

        self.show_multildos = PushButton(self.tab_14)
        self.show_multildos.setObjectName(u"show_multildos")

        self.gridLayout_27.addWidget(self.show_multildos, 6, 0, 1, 2)

        self.multildos_ewindow = LineEdit(self.tab_14)
        self.multildos_ewindow.setObjectName(u"multildos_ewindow")

        self.gridLayout_27.addWidget(self.multildos_ewindow, 0, 1, 1, 1)

        self.label_45 = BodyLabel(self.tab_14)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_27.addWidget(self.label_45, 1, 0, 1, 1)

        self.label_46 = BodyLabel(self.tab_14)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_27.addWidget(self.label_46, 2, 0, 1, 1)

        self.multildos_nrep = LineEdit(self.tab_14)
        self.multildos_nrep.setObjectName(u"multildos_nrep")

        self.gridLayout_27.addWidget(self.multildos_nrep, 2, 1, 1, 1)

        self.basis_ldos = ComboBox(self.tab_14)
        self.basis_ldos.addItem("")
        self.basis_ldos.addItem("")
        self.basis_ldos.setObjectName(u"basis_ldos")

        self.gridLayout_27.addWidget(self.basis_ldos, 4, 1, 1, 1)

        self.label_58 = BodyLabel(self.tab_14)
        self.label_58.setObjectName(u"label_58")

        self.gridLayout_27.addWidget(self.label_58, 4, 0, 1, 1)

        self.ratomic_ldos = LineEdit(self.tab_14)
        self.ratomic_ldos.setObjectName(u"ratomic_ldos")

        self.gridLayout_27.addWidget(self.ratomic_ldos, 5, 1, 1, 1)

        self.label_59 = BodyLabel(self.tab_14)
        self.label_59.setObjectName(u"label_59")

        self.gridLayout_27.addWidget(self.label_59, 5, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_27, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_14, "")
        self.tab_16 = QWidget()
        self.tab_16.setObjectName(u"tab_16")
        self.gridLayout_17 = QGridLayout(self.tab_16)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.fs_ewindow = LineEdit(self.tab_16)
        self.fs_ewindow.setObjectName(u"fs_ewindow")

        self.gridLayout_5.addWidget(self.fs_ewindow, 0, 1, 1, 1)

        self.fs_delta = LineEdit(self.tab_16)
        self.fs_delta.setObjectName(u"fs_delta")

        self.gridLayout_5.addWidget(self.fs_delta, 1, 1, 1, 1)

        self.fs_nk = LineEdit(self.tab_16)
        self.fs_nk.setObjectName(u"fs_nk")

        self.gridLayout_5.addWidget(self.fs_nk, 2, 1, 1, 1)

        self.label_42 = BodyLabel(self.tab_16)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_5.addWidget(self.label_42, 0, 0, 1, 1)

        self.label_49 = BodyLabel(self.tab_16)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_5.addWidget(self.label_49, 1, 0, 1, 1)

        self.label_52 = BodyLabel(self.tab_16)
        self.label_52.setObjectName(u"label_52")

        self.gridLayout_5.addWidget(self.label_52, 2, 0, 1, 1)

        self.show_fermi_surface = PushButton(self.tab_16)
        self.show_fermi_surface.setObjectName(u"show_fermi_surface")

        self.gridLayout_5.addWidget(self.show_fermi_surface, 4, 0, 1, 2)

        self.label_5 = BodyLabel(self.tab_16)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_5.addWidget(self.label_5, 3, 0, 1, 1)

        self.fs_operator = ComboBox(self.tab_16)
        self.fs_operator.addItem("")
        self.fs_operator.addItem("")
        self.fs_operator.addItem("")
        self.fs_operator.setObjectName(u"fs_operator")

        self.gridLayout_5.addWidget(self.fs_operator, 3, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_16, "")
        self.tab_18 = QWidget()
        self.tab_18.setObjectName(u"tab_18")
        self.gridLayout_33 = QGridLayout(self.tab_18)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridLayout_32 = QGridLayout()
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.qpi_ewindow = LineEdit(self.tab_18)
        self.qpi_ewindow.setObjectName(u"qpi_ewindow")

        self.gridLayout_32.addWidget(self.qpi_ewindow, 0, 1, 1, 1)

        self.qpi_delta = LineEdit(self.tab_18)
        self.qpi_delta.setObjectName(u"qpi_delta")

        self.gridLayout_32.addWidget(self.qpi_delta, 1, 1, 1, 1)

        self.qpi_nk = LineEdit(self.tab_18)
        self.qpi_nk.setObjectName(u"qpi_nk")

        self.gridLayout_32.addWidget(self.qpi_nk, 2, 1, 1, 1)

        self.label_55 = BodyLabel(self.tab_18)
        self.label_55.setObjectName(u"label_55")

        self.gridLayout_32.addWidget(self.label_55, 0, 0, 1, 1)

        self.label_56 = BodyLabel(self.tab_18)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_32.addWidget(self.label_56, 1, 0, 1, 1)

        self.label_57 = BodyLabel(self.tab_18)
        self.label_57.setObjectName(u"label_57")

        self.gridLayout_32.addWidget(self.label_57, 2, 0, 1, 1)

        self.show_qpi = PushButton(self.tab_18)
        self.show_qpi.setObjectName(u"show_qpi")

        self.gridLayout_32.addWidget(self.show_qpi, 3, 0, 1, 2)


        self.gridLayout_33.addLayout(self.gridLayout_32, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_18, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_22 = QGridLayout(self.tab)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
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


        self.gridLayout_22.addLayout(self.gridLayout_9, 0, 0, 1, 1)

        self.show_kdos = PushButton(self.tab)
        self.show_kdos.setObjectName(u"show_kdos")

        self.gridLayout_22.addWidget(self.show_kdos, 1, 0, 1, 1)

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

        self.gridLayout_6.addWidget(self.tabWidget_3, 0, 1, 1, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_6.addWidget(self.save_results, 2, 0, 1, 2)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_6.addWidget(self.load_results, 3, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1308, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.bands_color.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"2D systems", None))
#if QT_CONFIG(tooltip)
        self.kondo.setToolTip(QCoreApplication.translate("MainWindow", u"The exchange coupling J_K between a localized (e.g. f-electron) magnetic moment and the spin of itinerant conduction electrons - the defining interaction of the Kondo/heavy-fermion problem. It screens the local moment and gives rise to the emergent heavy quasiparticle bands.", None))
#endif // QT_CONFIG(tooltip)
        self.kondo.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
#if QT_CONFIG(tooltip)
        self.hoppings.setToolTip(QCoreApplication.translate("MainWindow", u"Hoppings of the system. If you put several numbers separated by commas, the first number is the 1st NN hopping, the second number the 2nd NN hopping, etc", None))
#endif // QT_CONFIG(tooltip)
        self.hoppings.setText(QCoreApplication.translate("MainWindow", u"1.0", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Spinon Kondo dispersion", None))
        self.label_hopping.setText(QCoreApplication.translate("MainWindow", u"Hoppings", None))
        self.fermi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_kondo.setText(QCoreApplication.translate("MainWindow", u"Kondo hybridization", None))
        self.label_fermi.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
#if QT_CONFIG(tooltip)
        self.exchange.setToolTip(QCoreApplication.translate("MainWindow", u"An exchange coupling between neighboring localized magnetic moments, distinct from the conduction-electron Kondo coupling above. It sets the strength of direct or RKKY-mediated magnetic interactions between the localized moments, controlling whether they order magnetically.", None))
#endif // QT_CONFIG(tooltip)
        self.exchange.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.hopping_image.setText("")
        self.fermi_image.setText("")
        self.kondo_image.setText("")
        self.kexchange_image.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Terms in the Hamiltonian", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Type of lattice", None))
        self.lattice.setItemText(0, QCoreApplication.translate("MainWindow", u"Triangular", None))
        self.lattice.setItemText(1, QCoreApplication.translate("MainWindow", u"Honeycomb", None))
        self.lattice.setItemText(2, QCoreApplication.translate("MainWindow", u"Honeycomb 4 sites", None))
        self.lattice.setItemText(3, QCoreApplication.translate("MainWindow", u"Honeycomb 6 sites", None))
        self.lattice.setItemText(4, QCoreApplication.translate("MainWindow", u"Square", None))
        self.lattice.setItemText(5, QCoreApplication.translate("MainWindow", u"Single square", None))
        self.lattice.setItemText(6, QCoreApplication.translate("MainWindow", u"Triangular tripartite", None))
        self.lattice.setItemText(7, QCoreApplication.translate("MainWindow", u"Kagome", None))
        self.lattice.setItemText(8, QCoreApplication.translate("MainWindow", u"Lieb", None))

        self.nsuper.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Geometry", None))
#if QT_CONFIG(tooltip)
        self.remove_single_bonded.setToolTip(QCoreApplication.translate("MainWindow", u"Remove atoms that have a single bond in the structure", None))
#endif // QT_CONFIG(tooltip)
        self.remove_single_bonded.setText(QCoreApplication.translate("MainWindow", u"Remove single bonds", None))
        self.remove_selected.setText(QCoreApplication.translate("MainWindow", u"Remove selected atoms", None))
        self.select_atoms_removal.setText(QCoreApplication.translate("MainWindow", u"Select atoms to remove", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"Modify geometry", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.show_structure_3d.setText(QCoreApplication.translate("MainWindow", u"Show structure 3D", None))
        self.nsuper_struct.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Structure", None))
        self.show_bands.setText(QCoreApplication.translate("MainWindow", u"Band structure", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.bands_color.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.bands_color.setItemText(1, QCoreApplication.translate("MainWindow", u"dispersive_electrons", None))
        self.bands_color.setItemText(2, QCoreApplication.translate("MainWindow", u"kondo_sites", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.nk_bands.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Bands", None))
        self.delta_kbands.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
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
        self.operator_kdos.setItemText(0, QCoreApplication.translate("MainWindow", u"dispersive_electrons", None))
        self.operator_kdos.setItemText(1, QCoreApplication.translate("MainWindow", u"None", None))
        self.operator_kdos.setItemText(2, QCoreApplication.translate("MainWindow", u"kondo_sites", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"DOS Bands", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.dos_nk.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.dos_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"ED", None))
        self.dos_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"Green", None))
        self.dos_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"KPM", None))

        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.label_dos_operator.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.show_dos.setText(QCoreApplication.translate("MainWindow", u"Density of states", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"DOS", None))
#if QT_CONFIG(tooltip)
        self.multildos_delta.setToolTip(QCoreApplication.translate("MainWindow", u"Energy smearing", None))
#endif // QT_CONFIG(tooltip)
        self.multildos_delta.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
#if QT_CONFIG(tooltip)
        self.multildos_nk.setToolTip(QCoreApplication.translate("MainWindow", u"Number of kpoints used", None))
#endif // QT_CONFIG(tooltip)
        self.multildos_nk.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.show_multildos.setText(QCoreApplication.translate("MainWindow", u"Show LDOS", None))
#if QT_CONFIG(tooltip)
        self.multildos_ewindow.setToolTip(QCoreApplication.translate("MainWindow", u"Energy window", None))
#endif // QT_CONFIG(tooltip)
        self.multildos_ewindow.setText(QCoreApplication.translate("MainWindow", u"1.5", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Number of unit cells", None))
#if QT_CONFIG(tooltip)
        self.multildos_nrep.setToolTip(QCoreApplication.translate("MainWindow", u"Number of replicas of the unit cell to plot", None))
#endif // QT_CONFIG(tooltip)
        self.multildos_nrep.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.basis_ldos.setItemText(0, QCoreApplication.translate("MainWindow", u"TB", None))
        self.basis_ldos.setItemText(1, QCoreApplication.translate("MainWindow", u"Real space atomic orbitals", None))

        self.label_58.setText(QCoreApplication.translate("MainWindow", u"Basis for the LDOS", None))
        self.ratomic_ldos.setText(QCoreApplication.translate("MainWindow", u"1.5", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"Atomic radii", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_14), QCoreApplication.translate("MainWindow", u"LDOS", None))
        self.fs_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.fs_delta.setText(QCoreApplication.translate("MainWindow", u"0.05", None))
        self.fs_nk.setText(QCoreApplication.translate("MainWindow", u"60", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.show_fermi_surface.setText(QCoreApplication.translate("MainWindow", u"Show Fermi surface", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.fs_operator.setItemText(0, QCoreApplication.translate("MainWindow", u"dispersive_electrons", None))
        self.fs_operator.setItemText(1, QCoreApplication.translate("MainWindow", u"kondo_sites", None))
        self.fs_operator.setItemText(2, QCoreApplication.translate("MainWindow", u"None", None))

        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_16), QCoreApplication.translate("MainWindow", u"FS", None))
        self.qpi_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.qpi_delta.setText(QCoreApplication.translate("MainWindow", u"0.05", None))
        self.qpi_nk.setText(QCoreApplication.translate("MainWindow", u"60", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
#if QT_CONFIG(tooltip)
        self.show_qpi.setToolTip(QCoreApplication.translate("MainWindow", u"Compute the quasiparticle interference", None))
#endif // QT_CONFIG(tooltip)
        self.show_qpi.setText(QCoreApplication.translate("MainWindow", u"Show QPI", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_18), QCoreApplication.translate("MainWindow", u"QPI", None))
        self.kdos_ewindow.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.kdos_mesh.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"# of points", None))
        self.show_kdos.setText(QCoreApplication.translate("MainWindow", u"Show Surface DOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"SDOS", None))
        self.label_site_dos_info.setText(QCoreApplication.translate("MainWindow", u"Click a site in the structure plot to compute the DOS there", None))
        self.label_site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.label_site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.show_site_dos.setText(QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_site_dos), QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.save_results.setText(QCoreApplication.translate("MainWindow", u"Save results", None))
        self.load_results.setText(QCoreApplication.translate("MainWindow", u"Load results", None))
    # retranslateUi

