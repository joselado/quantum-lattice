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
    PushButton, RadioButton)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(973, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_17 = QGridLayout(self.centralwidget)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.gridLayout_14 = QGridLayout(self.tab_12)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = BodyLabel(self.tab_12)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = BodyLabel(self.tab_12)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_fermi = BodyLabel(self.tab_12)
        self.label_fermi.setObjectName(u"label_fermi")

        self.gridLayout.addWidget(self.label_fermi, 2, 0, 1, 1)

        self.tinter = LineEdit(self.tab_12)
        self.tinter.setObjectName(u"tinter")

        self.gridLayout.addWidget(self.tinter, 0, 1, 1, 1)

        self.interlayer_bias = LineEdit(self.tab_12)
        self.interlayer_bias.setObjectName(u"interlayer_bias")

        self.gridLayout.addWidget(self.interlayer_bias, 1, 1, 1, 1)

        self.fermi = LineEdit(self.tab_12)
        self.fermi.setObjectName(u"fermi")

        self.gridLayout.addWidget(self.fermi, 2, 1, 1, 1)

        self.set_half_filling = RadioButton(self.tab_12)
        self.set_half_filling.setObjectName(u"set_half_filling")

        self.gridLayout.addWidget(self.set_half_filling, 6, 1, 1, 1)

        self.label_3 = BodyLabel(self.tab_12)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.crystalfield = LineEdit(self.tab_12)
        self.crystalfield.setObjectName(u"crystalfield")

        self.gridLayout.addWidget(self.crystalfield, 3, 1, 1, 1)

        self.label_20 = BodyLabel(self.tab_12)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 5, 0, 1, 1)

        self.inplaneb_phi = LineEdit(self.tab_12)
        self.inplaneb_phi.setObjectName(u"inplaneb_phi")

        self.gridLayout.addWidget(self.inplaneb_phi, 5, 1, 1, 1)

        self.label_18 = BodyLabel(self.tab_12)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout.addWidget(self.label_18, 4, 0, 1, 1)

        self.inplaneb = LineEdit(self.tab_12)
        self.inplaneb.setObjectName(u"inplaneb")
        self.inplaneb.setEnabled(False)

        self.gridLayout.addWidget(self.inplaneb, 4, 1, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_12, "")

        self.gridLayout_17.addWidget(self.tabWidget_3, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_8 = QGridLayout(self.tab_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.show_structure = PushButton(self.tab_2)
        self.show_structure.setObjectName(u"show_structure")

        self.gridLayout_8.addWidget(self.show_structure, 1, 0, 1, 1)

        self.show_structure_3d = PushButton(self.tab_2)
        self.show_structure_3d.setObjectName(u"show_structure_3d")

        self.gridLayout_8.addWidget(self.show_structure_3d, 1, 1, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.nsuper_struct = LineEdit(self.tab_2)
        self.nsuper_struct.setObjectName(u"nsuper_struct")

        self.gridLayout_5.addWidget(self.nsuper_struct, 0, 1, 1, 1)

        self.label_12 = BodyLabel(self.tab_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_5.addWidget(self.label_12, 0, 0, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_5, 0, 0, 1, 2)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_9 = QGridLayout(self.tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_7 = BodyLabel(self.tab)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 2, 0, 1, 1)

        self.label_6 = BodyLabel(self.tab)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)

        self.nbands = LineEdit(self.tab)
        self.nbands.setObjectName(u"nbands")

        self.gridLayout_3.addWidget(self.nbands, 2, 1, 1, 1)

        self.nk_bands = LineEdit(self.tab)
        self.nk_bands.setObjectName(u"nk_bands")

        self.gridLayout_3.addWidget(self.nk_bands, 1, 1, 1, 1)

        self.label_16 = BodyLabel(self.tab)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_3.addWidget(self.label_16, 0, 0, 1, 1)

        self.bands_color = ComboBox(self.tab)
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.addItem("")
        self.bands_color.setObjectName(u"bands_color")

        self.gridLayout_3.addWidget(self.bands_color, 0, 1, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.show_bands = PushButton(self.tab)
        self.show_bands.setObjectName(u"show_bands")

        self.gridLayout_9.addWidget(self.show_bands, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_10 = QGridLayout(self.tab_3)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.delta_ldos_single = LineEdit(self.tab_3)
        self.delta_ldos_single.setObjectName(u"delta_ldos_single")

        self.gridLayout_4.addWidget(self.delta_ldos_single, 0, 1, 1, 1)

        self.label_9 = BodyLabel(self.tab_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 1, 0, 1, 1)

        self.nsuper_ldos_single = LineEdit(self.tab_3)
        self.nsuper_ldos_single.setObjectName(u"nsuper_ldos_single")

        self.gridLayout_4.addWidget(self.nsuper_ldos_single, 3, 1, 1, 1)

        self.label_10 = BodyLabel(self.tab_3)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 3, 0, 1, 1)

        self.energy_ldos_single = LineEdit(self.tab_3)
        self.energy_ldos_single.setObjectName(u"energy_ldos_single")

        self.gridLayout_4.addWidget(self.energy_ldos_single, 1, 1, 1, 1)

        self.label_8 = BodyLabel(self.tab_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)

        self.label_11 = BodyLabel(self.tab_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 2, 0, 1, 1)

        self.nk_ldos_single = LineEdit(self.tab_3)
        self.nk_ldos_single.setObjectName(u"nk_ldos_single")

        self.gridLayout_4.addWidget(self.nk_ldos_single, 2, 1, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.show_ldos_single = PushButton(self.tab_3)
        self.show_ldos_single.setObjectName(u"show_ldos_single")

        self.gridLayout_10.addWidget(self.show_ldos_single, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.gridLayout_19 = QGridLayout(self.tab_7)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.multildos_nk = LineEdit(self.tab_7)
        self.multildos_nk.setObjectName(u"multildos_nk")

        self.gridLayout_18.addWidget(self.multildos_nk, 1, 1, 1, 1)

        self.multildos_delta = LineEdit(self.tab_7)
        self.multildos_delta.setObjectName(u"multildos_delta")

        self.gridLayout_18.addWidget(self.multildos_delta, 4, 1, 1, 1)

        self.label_23 = BodyLabel(self.tab_7)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_18.addWidget(self.label_23, 4, 0, 1, 1)

        self.label_24 = BodyLabel(self.tab_7)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_18.addWidget(self.label_24, 0, 0, 1, 1)

        self.show_multildos = PushButton(self.tab_7)
        self.show_multildos.setObjectName(u"show_multildos")

        self.gridLayout_18.addWidget(self.show_multildos, 5, 0, 1, 2)

        self.multildos_ewindow = LineEdit(self.tab_7)
        self.multildos_ewindow.setObjectName(u"multildos_ewindow")

        self.gridLayout_18.addWidget(self.multildos_ewindow, 0, 1, 1, 1)

        self.label_25 = BodyLabel(self.tab_7)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_18.addWidget(self.label_25, 1, 0, 1, 1)

        self.label_26 = BodyLabel(self.tab_7)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_18.addWidget(self.label_26, 2, 0, 1, 1)

        self.multildos_nrep = LineEdit(self.tab_7)
        self.multildos_nrep.setObjectName(u"multildos_nrep")

        self.gridLayout_18.addWidget(self.multildos_nrep, 2, 1, 1, 1)

        self.multildos_numw = LineEdit(self.tab_7)
        self.multildos_numw.setObjectName(u"multildos_numw")

        self.gridLayout_18.addWidget(self.multildos_numw, 3, 1, 1, 1)

        self.label_32 = BodyLabel(self.tab_7)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_18.addWidget(self.label_32, 3, 0, 1, 1)


        self.gridLayout_19.addLayout(self.gridLayout_18, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_7, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_12 = QGridLayout(self.tab_4)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.show_dos = PushButton(self.tab_4)
        self.show_dos.setObjectName(u"show_dos")

        self.gridLayout_12.addWidget(self.show_dos, 1, 0, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.delta_dos = LineEdit(self.tab_4)
        self.delta_dos.setObjectName(u"delta_dos")
        self.delta_dos.setEnabled(True)

        self.gridLayout_6.addWidget(self.delta_dos, 0, 1, 1, 1)

        self.label_17 = BodyLabel(self.tab_4)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_6.addWidget(self.label_17, 1, 0, 1, 1)

        self.label_13 = BodyLabel(self.tab_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setEnabled(True)

        self.gridLayout_6.addWidget(self.label_13, 0, 0, 1, 1)

        self.nk_dos = LineEdit(self.tab_4)
        self.nk_dos.setObjectName(u"nk_dos")

        self.gridLayout_6.addWidget(self.nk_dos, 1, 1, 1, 1)

        self.mode_dos = ComboBox(self.tab_4)
        self.mode_dos.addItem("")
        self.mode_dos.addItem("")
        self.mode_dos.setObjectName(u"mode_dos")

        self.gridLayout_6.addWidget(self.mode_dos, 3, 1, 1, 1)

        self.label_14 = BodyLabel(self.tab_4)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_6.addWidget(self.label_14, 3, 0, 1, 1)

        self.label_15 = BodyLabel(self.tab_4)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_6.addWidget(self.label_15, 2, 0, 1, 1)

        self.numw_dos = LineEdit(self.tab_4)
        self.numw_dos.setObjectName(u"numw_dos")

        self.gridLayout_6.addWidget(self.numw_dos, 2, 1, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_16 = QGridLayout(self.tab_6)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.fs_nk = LineEdit(self.tab_6)
        self.fs_nk.setObjectName(u"fs_nk")

        self.gridLayout_15.addWidget(self.fs_nk, 2, 1, 1, 1)

        self.fs_ewindow = LineEdit(self.tab_6)
        self.fs_ewindow.setObjectName(u"fs_ewindow")

        self.gridLayout_15.addWidget(self.fs_ewindow, 0, 1, 1, 1)

        self.label_52 = BodyLabel(self.tab_6)
        self.label_52.setObjectName(u"label_52")

        self.gridLayout_15.addWidget(self.label_52, 2, 0, 1, 1)

        self.show_fermi_surface = PushButton(self.tab_6)
        self.show_fermi_surface.setObjectName(u"show_fermi_surface")

        self.gridLayout_15.addWidget(self.show_fermi_surface, 4, 0, 1, 2)

        self.label_49 = BodyLabel(self.tab_6)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_15.addWidget(self.label_49, 1, 0, 1, 1)

        self.fs_delta = LineEdit(self.tab_6)
        self.fs_delta.setObjectName(u"fs_delta")

        self.gridLayout_15.addWidget(self.fs_delta, 1, 1, 1, 1)

        self.label_42 = BodyLabel(self.tab_6)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_15.addWidget(self.label_42, 0, 0, 1, 1)

        self.label_22 = BodyLabel(self.tab_6)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_15.addWidget(self.label_22, 3, 0, 1, 1)

        self.fs_numw = LineEdit(self.tab_6)
        self.fs_numw.setObjectName(u"fs_numw")

        self.gridLayout_15.addWidget(self.fs_numw, 3, 1, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_15, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_13 = QGridLayout(self.tab_5)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.delta_kbands = LineEdit(self.tab_5)
        self.delta_kbands.setObjectName(u"delta_kbands")

        self.gridLayout_11.addWidget(self.delta_kbands, 1, 1, 1, 1)

        self.label_29 = BodyLabel(self.tab_5)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_11.addWidget(self.label_29, 3, 0, 1, 1)

        self.window_kbands = LineEdit(self.tab_5)
        self.window_kbands.setObjectName(u"window_kbands")

        self.gridLayout_11.addWidget(self.window_kbands, 3, 1, 1, 1)

        self.label_31 = BodyLabel(self.tab_5)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_11.addWidget(self.label_31, 5, 0, 1, 1)

        self.nv_kbands = LineEdit(self.tab_5)
        self.nv_kbands.setObjectName(u"nv_kbands")

        self.gridLayout_11.addWidget(self.nv_kbands, 5, 1, 1, 1)

        self.label_27 = BodyLabel(self.tab_5)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_11.addWidget(self.label_27, 1, 0, 1, 1)

        self.ne_kbands = LineEdit(self.tab_5)
        self.ne_kbands.setObjectName(u"ne_kbands")

        self.gridLayout_11.addWidget(self.ne_kbands, 2, 1, 1, 1)

        self.label_28 = BodyLabel(self.tab_5)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_11.addWidget(self.label_28, 2, 0, 1, 1)

        self.label_30 = BodyLabel(self.tab_5)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_11.addWidget(self.label_30, 4, 0, 1, 1)

        self.scale_kbands = LineEdit(self.tab_5)
        self.scale_kbands.setObjectName(u"scale_kbands")

        self.gridLayout_11.addWidget(self.scale_kbands, 4, 1, 1, 1)

        self.nk_kbands = LineEdit(self.tab_5)
        self.nk_kbands.setObjectName(u"nk_kbands")

        self.gridLayout_11.addWidget(self.nk_kbands, 0, 1, 1, 1)

        self.label_19 = BodyLabel(self.tab_5)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_11.addWidget(self.label_19, 0, 0, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_11, 0, 0, 1, 1)

        self.show_dosbands = PushButton(self.tab_5)
        self.show_dosbands.setObjectName(u"show_dosbands")

        self.gridLayout_13.addWidget(self.show_dosbands, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_5, "")
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

        self.tabWidget.addTab(self.tab_site_dos, "")

        self.gridLayout_17.addWidget(self.tabWidget, 0, 1, 2, 1)

        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.horizontalLayout = QHBoxLayout(self.tab_8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_5 = BodyLabel(self.tab_8)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)

        self.cell_size = LineEdit(self.tab_8)
        self.cell_size.setObjectName(u"cell_size")

        self.gridLayout_2.addWidget(self.cell_size, 0, 1, 1, 1)

        self.multilayer_type = ComboBox(self.tab_8)
        self.multilayer_type.setObjectName(u"multilayer_type")

        self.gridLayout_2.addWidget(self.multilayer_type, 1, 1, 1, 1)

        self.label_33 = BodyLabel(self.tab_8)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_2.addWidget(self.label_33, 1, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.horizontalLayout_2 = QHBoxLayout(self.tab_9)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout_27 = QGridLayout()
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.remove_single_bonded = CheckBox(self.tab_9)
        self.remove_single_bonded.setObjectName(u"remove_single_bonded")
        self.remove_single_bonded.setEnabled(True)
        self.remove_single_bonded.setChecked(False)

        self.gridLayout_27.addWidget(self.remove_single_bonded, 0, 0, 1, 1)

        self.remove_selected = CheckBox(self.tab_9)
        self.remove_selected.setObjectName(u"remove_selected")

        self.gridLayout_27.addWidget(self.remove_selected, 1, 0, 1, 1)

        self.select_atoms_removal = PushButton(self.tab_9)
        self.select_atoms_removal.setObjectName(u"select_atoms_removal")

        self.gridLayout_27.addWidget(self.select_atoms_removal, 2, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_27)

        self.tabWidget_2.addTab(self.tab_9, "")

        self.gridLayout_17.addWidget(self.tabWidget_2, 1, 0, 1, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_17.addWidget(self.save_results, 3, 0, 1, 2)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_17.addWidget(self.load_results, 4, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 973, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Twisted multilayer graphene", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Interlayer", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Electric bias", None))
        self.label_fermi.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
        self.tinter.setText(QCoreApplication.translate("MainWindow", u"0.4", None))
        self.interlayer_bias.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.fermi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.set_half_filling.setText(QCoreApplication.translate("MainWindow", u"Measure with respect to half filling", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Crystal field", None))
#if QT_CONFIG(tooltip)
        self.crystalfield.setToolTip(QCoreApplication.translate("MainWindow", u"Crystal field Hartree term, makes the edge atoms inequivalent", None))
#endif // QT_CONFIG(tooltip)
        self.crystalfield.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Angle inplane B field", None))
        self.inplaneb_phi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Inplane B field", None))
        self.inplaneb.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_12), QCoreApplication.translate("MainWindow", u"Hamiltonian", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.show_structure_3d.setText(QCoreApplication.translate("MainWindow", u"Show structure 3D", None))
        self.nsuper_struct.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Structure", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"nbands", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"nkpoints", None))
        self.nbands.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.nk_bands.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.bands_color.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.bands_color.setItemText(1, QCoreApplication.translate("MainWindow", u"Valley", None))
        self.bands_color.setItemText(2, QCoreApplication.translate("MainWindow", u"IPR", None))
        self.bands_color.setItemText(3, QCoreApplication.translate("MainWindow", u"Layer", None))
        self.bands_color.setItemText(4, QCoreApplication.translate("MainWindow", u"Berry", None))

        self.show_bands.setText(QCoreApplication.translate("MainWindow", u"Bandstructure", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Bands", None))
        self.delta_ldos_single.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Energy", None))
        self.nsuper_ldos_single.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.energy_ldos_single.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.nk_ldos_single.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.show_ldos_single.setText(QCoreApplication.translate("MainWindow", u"Show LDOS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Single LDOS", None))
#if QT_CONFIG(tooltip)
        self.multildos_nk.setToolTip(QCoreApplication.translate("MainWindow", u"Number of kpoints used", None))
#endif // QT_CONFIG(tooltip)
        self.multildos_nk.setText(QCoreApplication.translate("MainWindow", u"10", None))
#if QT_CONFIG(tooltip)
        self.multildos_delta.setToolTip(QCoreApplication.translate("MainWindow", u"Energy smearing", None))
#endif // QT_CONFIG(tooltip)
        self.multildos_delta.setText(QCoreApplication.translate("MainWindow", u"0.003", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.show_multildos.setText(QCoreApplication.translate("MainWindow", u"Show LDOS", None))
#if QT_CONFIG(tooltip)
        self.multildos_ewindow.setToolTip(QCoreApplication.translate("MainWindow", u"Energy window", None))
#endif // QT_CONFIG(tooltip)
        self.multildos_ewindow.setText(QCoreApplication.translate("MainWindow", u"0.3", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Number of unit cells", None))
#if QT_CONFIG(tooltip)
        self.multildos_nrep.setToolTip(QCoreApplication.translate("MainWindow", u"Number of replicas of the unit cell to plot", None))
#endif // QT_CONFIG(tooltip)
        self.multildos_nrep.setText(QCoreApplication.translate("MainWindow", u"6", None))
#if QT_CONFIG(tooltip)
        self.multildos_numw.setToolTip(QCoreApplication.translate("MainWindow", u"Number of wavefunctions computed around E=0 to calculate the LDOS", None))
#endif // QT_CONFIG(tooltip)
        self.multildos_numw.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Number of waves", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"LDOS", None))
        self.show_dos.setText(QCoreApplication.translate("MainWindow", u"Show DOS", None))
        self.delta_dos.setText(QCoreApplication.translate("MainWindow", u"0.005", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.nk_dos.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.mode_dos.setItemText(0, QCoreApplication.translate("MainWindow", u"Lowest", None))
        self.mode_dos.setItemText(1, QCoreApplication.translate("MainWindow", u"KPM", None))

        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Calculation mode", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"# of waves for Lowest mode", None))
#if QT_CONFIG(tooltip)
        self.numw_dos.setToolTip(QCoreApplication.translate("MainWindow", u"Number of wavefunctions used for the calculation of DOS for the Lowest mode. Increase to see a bigger energy window", None))
#endif // QT_CONFIG(tooltip)
        self.numw_dos.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"DOS", None))
        self.fs_nk.setText(QCoreApplication.translate("MainWindow", u"60", None))
        self.fs_ewindow.setText(QCoreApplication.translate("MainWindow", u"0.05", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.show_fermi_surface.setText(QCoreApplication.translate("MainWindow", u"Show Fermi surface", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.fs_delta.setText(QCoreApplication.translate("MainWindow", u"0.0005", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Number of waves", None))
        self.fs_numw.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"FS", None))
        self.delta_kbands.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.window_kbands.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"# vectors", None))
#if QT_CONFIG(tooltip)
        self.nv_kbands.setToolTip(QCoreApplication.translate("MainWindow", u"Number of vectors in KPM, increase this number to remove noise", None))
#endif // QT_CONFIG(tooltip)
        self.nv_kbands.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.ne_kbands.setText(QCoreApplication.translate("MainWindow", u"400", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"KPM scale", None))
        self.scale_kbands.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.nk_kbands.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"# of kpoints", None))
#if QT_CONFIG(tooltip)
        self.show_dosbands.setToolTip(QCoreApplication.translate("MainWindow", u"This is equivalent to band structure calculation, but it can be applied for very large systems", None))
#endif // QT_CONFIG(tooltip)
        self.show_dosbands.setText(QCoreApplication.translate("MainWindow", u"Show DOS Bands", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"DOS Bands", None))
        self.label_site_dos_info.setText(QCoreApplication.translate("MainWindow", u"Click a site in the structure plot to compute the DOS there", None))
        self.label_site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.label_site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"Number of kpoints", None))
        self.site_dos_nk.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.show_site_dos.setText(QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_site_dos), QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Cell size", None))
        self.cell_size.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Multilayer type", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"Geometry", None))
#if QT_CONFIG(tooltip)
        self.remove_single_bonded.setToolTip(QCoreApplication.translate("MainWindow", u"Remove atoms that have a single bond in the structure", None))
#endif // QT_CONFIG(tooltip)
        self.remove_single_bonded.setText(QCoreApplication.translate("MainWindow", u"Remove single bonds", None))
        self.remove_selected.setText(QCoreApplication.translate("MainWindow", u"Remove selected atoms", None))
        self.select_atoms_removal.setText(QCoreApplication.translate("MainWindow", u"Select atoms to remove", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"Modify geometry", None))
        self.save_results.setText(QCoreApplication.translate("MainWindow", u"Save results", None))
        self.load_results.setText(QCoreApplication.translate("MainWindow", u"Load results", None))
    # retranslateUi

