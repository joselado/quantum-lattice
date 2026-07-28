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
        self.swave = LineEdit(self.tab_3)
        self.swave.setObjectName(u"swave")

        self.gridLayout.addWidget(self.swave, 8, 1, 1, 1)

        self.Bz = LineEdit(self.tab_3)
        self.Bz.setObjectName(u"Bz")

        self.gridLayout.addWidget(self.Bz, 5, 1, 1, 1)

        self.Bx = LineEdit(self.tab_3)
        self.Bx.setObjectName(u"Bx")

        self.gridLayout.addWidget(self.Bx, 3, 1, 1, 1)

        self.label_5 = BodyLabel(self.tab_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.By = LineEdit(self.tab_3)
        self.By.setObjectName(u"By")

        self.gridLayout.addWidget(self.By, 4, 1, 1, 1)

        self.label_fermi = BodyLabel(self.tab_3)
        self.label_fermi.setObjectName(u"label_fermi")

        self.gridLayout.addWidget(self.label_fermi, 0, 0, 1, 1)

        self.label_swave = BodyLabel(self.tab_3)
        self.label_swave.setObjectName(u"label_swave")

        self.gridLayout.addWidget(self.label_swave, 8, 0, 1, 1)

        self.fermi = LineEdit(self.tab_3)
        self.fermi.setObjectName(u"fermi")
        self.fermi.setEnabled(True)

        self.gridLayout.addWidget(self.fermi, 0, 1, 1, 1)

        self.rashba = LineEdit(self.tab_3)
        self.rashba.setObjectName(u"rashba")

        self.gridLayout.addWidget(self.rashba, 6, 1, 1, 1)

        self.label_rashba = BodyLabel(self.tab_3)
        self.label_rashba.setObjectName(u"label_rashba")

        self.gridLayout.addWidget(self.label_rashba, 6, 0, 1, 1)

        self.label_3 = BodyLabel(self.tab_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_4 = BodyLabel(self.tab_3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.ising_SOC = LineEdit(self.tab_3)
        self.ising_SOC.setObjectName(u"ising_SOC")

        self.gridLayout.addWidget(self.ising_SOC, 1, 1, 1, 1)

        self.label_11 = BodyLabel(self.tab_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.label_2 = BodyLabel(self.tab_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.cdw = LineEdit(self.tab_3)
        self.cdw.setObjectName(u"cdw")

        self.gridLayout.addWidget(self.cdw, 2, 1, 1, 1)


        self.gridLayout_24.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")

        self.gridLayout_6.addWidget(self.tabWidget_2, 0, 0, 2, 1)

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


        self.gridLayout_18.addLayout(self.gridLayout_11, 0, 0, 1, 1)

        self.show_dosbands = PushButton(self.tab_9)
        self.show_dosbands.setObjectName(u"show_dosbands")

        self.gridLayout_18.addWidget(self.show_dosbands, 0, 1, 1, 1)

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

        self.gridLayout_5.addWidget(self.show_fermi_surface, 3, 0, 1, 2)


        self.gridLayout_17.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_16, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.gridLayout_21 = QGridLayout(self.tab_10)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.topology_nk = LineEdit(self.tab_10)
        self.topology_nk.setObjectName(u"topology_nk")

        self.gridLayout_8.addWidget(self.topology_nk, 0, 1, 1, 1)

        self.label_19 = BodyLabel(self.tab_10)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_8.addWidget(self.label_19, 0, 0, 1, 1)

        self.label_35 = BodyLabel(self.tab_10)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_8.addWidget(self.label_35, 1, 0, 1, 1)

        self.topology_operator = ComboBox(self.tab_10)
        self.topology_operator.addItem("")
        self.topology_operator.addItem("")
        self.topology_operator.addItem("")
        self.topology_operator.setObjectName(u"topology_operator")

        self.gridLayout_8.addWidget(self.topology_operator, 1, 1, 1, 1)


        self.gridLayout_21.addLayout(self.gridLayout_8, 0, 0, 1, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.show_chern = PushButton(self.tab_10)
        self.show_chern.setObjectName(u"show_chern")
        self.show_chern.setEnabled(True)

        self.gridLayout_7.addWidget(self.show_chern, 3, 0, 1, 1)

        self.show_z2 = PushButton(self.tab_10)
        self.show_z2.setObjectName(u"show_z2")

        self.gridLayout_7.addWidget(self.show_z2, 2, 0, 1, 1)

        self.show_berry2d = PushButton(self.tab_10)
        self.show_berry2d.setObjectName(u"show_berry2d")

        self.gridLayout_7.addWidget(self.show_berry2d, 1, 0, 1, 1)

        self.show_berry1d = PushButton(self.tab_10)
        self.show_berry1d.setObjectName(u"show_berry1d")

        self.gridLayout_7.addWidget(self.show_berry1d, 0, 0, 1, 1)


        self.gridLayout_21.addLayout(self.gridLayout_7, 0, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab_10, "")
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

        self.gridLayout_6.addWidget(self.save_results, 1, 0, 1, 2)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_6.addWidget(self.load_results, 2, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1308, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.bands_color.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TMDC", None))
#if QT_CONFIG(tooltip)
        self.swave.setToolTip(QCoreApplication.translate("MainWindow", u"swave superconducting order", None))
#endif // QT_CONFIG(tooltip)
        self.swave.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.Bz.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
#if QT_CONFIG(tooltip)
        self.Bx.setToolTip(QCoreApplication.translate("MainWindow", u"Exchange proximity in x direction", None))
#endif // QT_CONFIG(tooltip)
        self.Bx.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jz", None))
        self.By.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_fermi.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
        self.label_swave.setText(QCoreApplication.translate("MainWindow", u"Superconducting pairing", None))
#if QT_CONFIG(tooltip)
        self.fermi.setToolTip(QCoreApplication.translate("MainWindow", u"CHemical potential with respect to charge neutrality", None))
#endif // QT_CONFIG(tooltip)
        self.fermi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
#if QT_CONFIG(tooltip)
        self.rashba.setToolTip(QCoreApplication.translate("MainWindow", u"Rashba spin orbit coupling", None))
#endif // QT_CONFIG(tooltip)
        self.rashba.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_rashba.setText(QCoreApplication.translate("MainWindow", u"Rashba SOC", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jx", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jy", None))
#if QT_CONFIG(tooltip)
        self.ising_SOC.setToolTip(QCoreApplication.translate("MainWindow", u"Ising SOC", None))
#endif // QT_CONFIG(tooltip)
        self.ising_SOC.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Ising SOC", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Charge density wave", None))
#if QT_CONFIG(tooltip)
        self.cdw.setToolTip(QCoreApplication.translate("MainWindow", u"Charge density wave order (currently in a 3x3 supercell)", None))
#endif // QT_CONFIG(tooltip)
        self.cdw.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Terms in the Hamiltonian", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.show_structure_3d.setText(QCoreApplication.translate("MainWindow", u"Show structure 3D", None))
        self.nsuper_struct.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Structure", None))
        self.show_bands.setText(QCoreApplication.translate("MainWindow", u"Band structure", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.bands_color.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.bands_color.setItemText(1, QCoreApplication.translate("MainWindow", u"Berry", None))
        self.bands_color.setItemText(2, QCoreApplication.translate("MainWindow", u"Sx", None))
        self.bands_color.setItemText(3, QCoreApplication.translate("MainWindow", u"Sy", None))
        self.bands_color.setItemText(4, QCoreApplication.translate("MainWindow", u"Sz", None))
        self.bands_color.setItemText(5, QCoreApplication.translate("MainWindow", u"Valley", None))
        self.bands_color.setItemText(6, QCoreApplication.translate("MainWindow", u"IPR", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.nk_bands.setText(QCoreApplication.translate("MainWindow", u"300", None))
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
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
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
        self.multildos_delta.setText(QCoreApplication.translate("MainWindow", u"0.2", None))
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
        self.fs_delta.setText(QCoreApplication.translate("MainWindow", u"0.2", None))
        self.fs_nk.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.show_fermi_surface.setText(QCoreApplication.translate("MainWindow", u"Show Fermi surface", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_16), QCoreApplication.translate("MainWindow", u"FS", None))
        self.topology_nk.setText(QCoreApplication.translate("MainWindow", u"400", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.topology_operator.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.topology_operator.setItemText(1, QCoreApplication.translate("MainWindow", u"Sz", None))
        self.topology_operator.setItemText(2, QCoreApplication.translate("MainWindow", u"Valley", None))

        self.show_chern.setText(QCoreApplication.translate("MainWindow", u"Chern number", None))
        self.show_z2.setText(QCoreApplication.translate("MainWindow", u"Z2 invariant", None))
        self.show_berry2d.setText(QCoreApplication.translate("MainWindow", u"2D Berry curvature", None))
        self.show_berry1d.setText(QCoreApplication.translate("MainWindow", u"1D Berry curvature", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_10), QCoreApplication.translate("MainWindow", u"Topology 2D", None))
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

