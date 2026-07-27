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
        MainWindow.resize(1041, 600)
        MainWindow.setMinimumSize(QSize(878, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_8 = QGridLayout(self.tab_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.crystalfield = LineEdit(self.tab_3)
        self.crystalfield.setObjectName(u"crystalfield")

        self.gridLayout.addWidget(self.crystalfield, 2, 2, 1, 1)

        self.label_24 = BodyLabel(self.tab_3)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout.addWidget(self.label_24, 7, 0, 1, 1)

        self.fermi_image = BodyLabel(self.tab_3)
        self.fermi_image.setObjectName(u"fermi_image")
        self.fermi_image.setMinimumSize(QSize(30, 0))

        self.gridLayout.addWidget(self.fermi_image, 0, 1, 1, 1)

        self.mAF = LineEdit(self.tab_3)
        self.mAF.setObjectName(u"mAF")

        self.gridLayout.addWidget(self.mAF, 10, 2, 1, 1)

        self.label_25 = BodyLabel(self.tab_3)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout.addWidget(self.label_25, 8, 0, 1, 1)

        self.peierls = LineEdit(self.tab_3)
        self.peierls.setObjectName(u"peierls")
        self.peierls.setEnabled(True)

        self.gridLayout.addWidget(self.peierls, 3, 2, 1, 1)

        self.swave = LineEdit(self.tab_3)
        self.swave.setObjectName(u"swave")

        self.gridLayout.addWidget(self.swave, 11, 2, 1, 1)

        self.kanemele_image = BodyLabel(self.tab_3)
        self.kanemele_image.setObjectName(u"kanemele_image")

        self.gridLayout.addWidget(self.kanemele_image, 6, 1, 1, 1)

        self.label_11 = BodyLabel(self.tab_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 6, 0, 1, 1)

        self.label_10 = BodyLabel(self.tab_3)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 5, 0, 1, 1)

        self.label_13 = BodyLabel(self.tab_3)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 10, 0, 1, 1)

        self.bfield_image = BodyLabel(self.tab_3)
        self.bfield_image.setObjectName(u"bfield_image")

        self.gridLayout.addWidget(self.bfield_image, 3, 1, 1, 1)

        self.pwave_image = BodyLabel(self.tab_3)
        self.pwave_image.setObjectName(u"pwave_image")

        self.gridLayout.addWidget(self.pwave_image, 12, 1, 1, 1)

        self.fermi = LineEdit(self.tab_3)
        self.fermi.setObjectName(u"fermi")
        self.fermi.setEnabled(True)

        self.gridLayout.addWidget(self.fermi, 0, 2, 1, 1)

        self.exchange = LineEdit(self.tab_3)
        self.exchange.setObjectName(u"exchange")

        self.gridLayout.addWidget(self.exchange, 4, 2, 1, 1)

        self.label_38 = BodyLabel(self.tab_3)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout.addWidget(self.label_38, 1, 0, 1, 1)

        self.label_26 = BodyLabel(self.tab_3)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout.addWidget(self.label_26, 11, 0, 1, 1)

        self.mAB = LineEdit(self.tab_3)
        self.mAB.setObjectName(u"mAB")

        self.gridLayout.addWidget(self.mAB, 9, 2, 1, 1)

        self.rashba = LineEdit(self.tab_3)
        self.rashba.setObjectName(u"rashba")

        self.gridLayout.addWidget(self.rashba, 5, 2, 1, 1)

        self.swave_image = BodyLabel(self.tab_3)
        self.swave_image.setObjectName(u"swave_image")

        self.gridLayout.addWidget(self.swave_image, 11, 1, 1, 1)

        self.label_37 = BodyLabel(self.tab_3)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout.addWidget(self.label_37, 12, 0, 1, 1)

        self.haldane_image = BodyLabel(self.tab_3)
        self.haldane_image.setObjectName(u"haldane_image")

        self.gridLayout.addWidget(self.haldane_image, 7, 1, 1, 1)

        self.label = BodyLabel(self.tab_3)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.mAB_image = BodyLabel(self.tab_3)
        self.mAB_image.setObjectName(u"mAB_image")

        self.gridLayout.addWidget(self.mAB_image, 9, 1, 1, 1)

        self.hopping_image = BodyLabel(self.tab_3)
        self.hopping_image.setObjectName(u"hopping_image")

        self.gridLayout.addWidget(self.hopping_image, 1, 1, 1, 1)

        self.label_17 = BodyLabel(self.tab_3)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 2, 0, 1, 1)

        self.mAF_image = BodyLabel(self.tab_3)
        self.mAF_image.setObjectName(u"mAF_image")

        self.gridLayout.addWidget(self.mAF_image, 10, 1, 1, 1)

        self.rashba_image = BodyLabel(self.tab_3)
        self.rashba_image.setObjectName(u"rashba_image")

        self.gridLayout.addWidget(self.rashba_image, 5, 1, 1, 1)

        self.antihaldane = LineEdit(self.tab_3)
        self.antihaldane.setObjectName(u"antihaldane")

        self.gridLayout.addWidget(self.antihaldane, 8, 2, 1, 1)

        self.pwave = LineEdit(self.tab_3)
        self.pwave.setObjectName(u"pwave")

        self.gridLayout.addWidget(self.pwave, 12, 2, 1, 1)

        self.kanemele = LineEdit(self.tab_3)
        self.kanemele.setObjectName(u"kanemele")

        self.gridLayout.addWidget(self.kanemele, 6, 2, 1, 1)

        self.hoppings = LineEdit(self.tab_3)
        self.hoppings.setObjectName(u"hoppings")

        self.gridLayout.addWidget(self.hoppings, 1, 2, 1, 1)

        self.antihaldane_image = BodyLabel(self.tab_3)
        self.antihaldane_image.setObjectName(u"antihaldane_image")

        self.gridLayout.addWidget(self.antihaldane_image, 8, 1, 1, 1)

        self.label_3 = BodyLabel(self.tab_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.cf_image = BodyLabel(self.tab_3)
        self.cf_image.setObjectName(u"cf_image")

        self.gridLayout.addWidget(self.cf_image, 2, 1, 1, 1)

        self.haldane = LineEdit(self.tab_3)
        self.haldane.setObjectName(u"haldane")

        self.gridLayout.addWidget(self.haldane, 7, 2, 1, 1)

        self.label_12 = BodyLabel(self.tab_3)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 9, 0, 1, 1)

        self.label_14 = BodyLabel(self.tab_3)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 3, 0, 1, 1)

        self.exchange_image = BodyLabel(self.tab_3)
        self.exchange_image.setObjectName(u"exchange_image")

        self.gridLayout.addWidget(self.exchange_image, 4, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_14 = QWidget()
        self.tab_14.setObjectName(u"tab_14")
        self.gridLayout_25 = QGridLayout(self.tab_14)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_24 = QGridLayout()
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.label_35 = BodyLabel(self.tab_14)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_24.addWidget(self.label_35, 0, 0, 1, 1)

        self.gridLayout_27 = QGridLayout()
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.strain_strength = LineEdit(self.tab_14)
        self.strain_strength.setObjectName(u"strain_strength")

        self.gridLayout_27.addWidget(self.strain_strength, 0, 1, 1, 1)

        self.label_36 = BodyLabel(self.tab_14)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_27.addWidget(self.label_36, 0, 0, 1, 1)

        self.label_39 = BodyLabel(self.tab_14)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout_27.addWidget(self.label_39, 1, 0, 1, 1)

        self.strain_decay = LineEdit(self.tab_14)
        self.strain_decay.setObjectName(u"strain_decay")

        self.gridLayout_27.addWidget(self.strain_decay, 1, 1, 1, 1)

        self.show_hoppings = PushButton(self.tab_14)
        self.show_hoppings.setObjectName(u"show_hoppings")

        self.gridLayout_27.addWidget(self.show_hoppings, 3, 0, 1, 2)

        self.strain_type = ComboBox(self.tab_14)
        self.strain_type.addItem("")
        self.strain_type.addItem("")
        self.strain_type.setObjectName(u"strain_type")

        self.gridLayout_27.addWidget(self.strain_type, 2, 1, 1, 1)

        self.label_42 = BodyLabel(self.tab_14)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_27.addWidget(self.label_42, 2, 0, 1, 1)


        self.gridLayout_24.addLayout(self.gridLayout_27, 0, 1, 1, 1)


        self.gridLayout_25.addLayout(self.gridLayout_24, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_14, "")

        self.gridLayout_3.addWidget(self.tabWidget_2, 0, 0, 2, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_16 = QGridLayout(self.tab_2)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_7 = BodyLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4.addWidget(self.label_7, 3, 0, 1, 1)

        self.nsides = LineEdit(self.tab_2)
        self.nsides.setObjectName(u"nsides")

        self.gridLayout_4.addWidget(self.nsides, 2, 1, 1, 1)

        self.label_6 = BodyLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)

        self.label_8 = BodyLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)

        self.lattice = ComboBox(self.tab_2)
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.setObjectName(u"lattice")

        self.gridLayout_4.addWidget(self.lattice, 0, 1, 1, 1)

        self.label_2 = BodyLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)

        self.width = LineEdit(self.tab_2)
        self.width.setObjectName(u"width")

        self.gridLayout_4.addWidget(self.width, 1, 1, 1, 1)

        self.rotation = LineEdit(self.tab_2)
        self.rotation.setObjectName(u"rotation")

        self.gridLayout_4.addWidget(self.rotation, 3, 1, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.horizontalLayout_2 = QHBoxLayout(self.tab_8)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.remove_single_bonded = CheckBox(self.tab_8)
        self.remove_single_bonded.setObjectName(u"remove_single_bonded")
        self.remove_single_bonded.setChecked(True)

        self.gridLayout_15.addWidget(self.remove_single_bonded, 0, 0, 1, 1)

        self.remove_selected = CheckBox(self.tab_8)
        self.remove_selected.setObjectName(u"remove_selected")

        self.gridLayout_15.addWidget(self.remove_selected, 1, 0, 1, 1)

        self.select_atoms_removal = PushButton(self.tab_8)
        self.select_atoms_removal.setObjectName(u"select_atoms_removal")

        self.gridLayout_15.addWidget(self.select_atoms_removal, 2, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_15)

        self.tabWidget.addTab(self.tab_8, "")

        self.gridLayout_3.addWidget(self.tabWidget, 1, 1, 1, 1)

        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.horizontalLayout = QHBoxLayout(self.tab_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.show_structure = PushButton(self.tab_4)
        self.show_structure.setObjectName(u"show_structure")

        self.horizontalLayout.addWidget(self.show_structure)

        self.show_structure_3d = PushButton(self.tab_4)
        self.show_structure_3d.setObjectName(u"show_structure_3d")

        self.horizontalLayout.addWidget(self.show_structure_3d)

        self.tabWidget_3.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_9 = QGridLayout(self.tab_5)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.show_bands = PushButton(self.tab_5)
        self.show_bands.setObjectName(u"show_bands")

        self.gridLayout_9.addWidget(self.show_bands, 0, 0, 1, 1)

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
        self.bands_color.addItem("")
        self.bands_color.setObjectName(u"bands_color")

        self.gridLayout_2.addWidget(self.bands_color, 0, 1, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.gridLayout_11 = QGridLayout(self.tab_7)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.multildos_delta = LineEdit(self.tab_7)
        self.multildos_delta.setObjectName(u"multildos_delta")

        self.gridLayout_6.addWidget(self.multildos_delta, 1, 1, 1, 1)

        self.label_20 = BodyLabel(self.tab_7)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_6.addWidget(self.label_20, 1, 0, 1, 1)

        self.label_19 = BodyLabel(self.tab_7)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 0, 0, 1, 1)

        self.multildos_ewindow = LineEdit(self.tab_7)
        self.multildos_ewindow.setObjectName(u"multildos_ewindow")

        self.gridLayout_6.addWidget(self.multildos_ewindow, 0, 1, 1, 1)

        self.show_interactive_ldos = PushButton(self.tab_7)
        self.show_interactive_ldos.setObjectName(u"show_interactive_ldos")

        self.gridLayout_6.addWidget(self.show_interactive_ldos, 4, 0, 1, 2)

        self.label_30 = BodyLabel(self.tab_7)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_6.addWidget(self.label_30, 2, 0, 1, 1)

        self.basis_ldos = ComboBox(self.tab_7)
        self.basis_ldos.addItem("")
        self.basis_ldos.addItem("")
        self.basis_ldos.setObjectName(u"basis_ldos")

        self.gridLayout_6.addWidget(self.basis_ldos, 2, 1, 1, 1)

        self.label_31 = BodyLabel(self.tab_7)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_6.addWidget(self.label_31, 3, 0, 1, 1)

        self.ratomic_ldos = LineEdit(self.tab_7)
        self.ratomic_ldos.setObjectName(u"ratomic_ldos")

        self.gridLayout_6.addWidget(self.ratomic_ldos, 3, 1, 1, 1)


        self.gridLayout_11.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_7, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.gridLayout_18 = QGridLayout(self.tab_9)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.label_16 = BodyLabel(self.tab_9)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_17.addWidget(self.label_16, 0, 0, 1, 1)

        self.dos_delta = LineEdit(self.tab_9)
        self.dos_delta.setObjectName(u"dos_delta")

        self.gridLayout_17.addWidget(self.dos_delta, 0, 1, 1, 1)

        self.dos_ewindow = LineEdit(self.tab_9)
        self.dos_ewindow.setObjectName(u"dos_ewindow")

        self.gridLayout_17.addWidget(self.dos_ewindow, 1, 1, 1, 1)

        self.label_41 = BodyLabel(self.tab_9)
        self.label_41.setObjectName(u"label_41")

        self.gridLayout_17.addWidget(self.label_41, 1, 0, 1, 1)

        self.label_dos_mode = BodyLabel(self.tab_9)
        self.label_dos_mode.setObjectName(u"label_dos_mode")

        self.gridLayout_17.addWidget(self.label_dos_mode, 2, 0, 1, 1)

        self.dos_mode = ComboBox(self.tab_9)
        self.dos_mode.addItem("")
        self.dos_mode.addItem("")
        self.dos_mode.addItem("")
        self.dos_mode.setObjectName(u"dos_mode")

        self.gridLayout_17.addWidget(self.dos_mode, 2, 1, 1, 1)

        self.label_dos_operator = BodyLabel(self.tab_9)
        self.label_dos_operator.setObjectName(u"label_dos_operator")

        self.gridLayout_17.addWidget(self.label_dos_operator, 3, 0, 1, 1)

        self.dos_operator = ComboBox(self.tab_9)
        self.dos_operator.setObjectName(u"dos_operator")

        self.gridLayout_17.addWidget(self.dos_operator, 3, 1, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_17, 0, 0, 1, 1)

        self.show_dos = PushButton(self.tab_9)
        self.show_dos.setObjectName(u"show_dos")

        self.gridLayout_18.addWidget(self.show_dos, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_9, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_5 = QGridLayout(self.tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.tabWidget_4 = QTabWidget(self.tab)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        self.tab_12 = QWidget()
        self.tab_12.setObjectName(u"tab_12")
        self.gridLayout_14 = QGridLayout(self.tab_12)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.scf_initialization = ComboBox(self.tab_12)
        self.scf_initialization.addItem("")
        self.scf_initialization.addItem("")
        self.scf_initialization.addItem("")
        self.scf_initialization.addItem("")
        self.scf_initialization.addItem("")
        self.scf_initialization.setObjectName(u"scf_initialization")

        self.gridLayout_10.addWidget(self.scf_initialization, 0, 1, 1, 1)

        self.label_22 = BodyLabel(self.tab_12)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_10.addWidget(self.label_22, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_21 = BodyLabel(self.tab_12)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_3.addWidget(self.label_21)

        self.U = LineEdit(self.tab_12)
        self.U.setObjectName(u"U")

        self.horizontalLayout_3.addWidget(self.U)

        self.label_23 = BodyLabel(self.tab_12)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_3.addWidget(self.label_23)

        self.V1 = LineEdit(self.tab_12)
        self.V1.setObjectName(u"V1")

        self.horizontalLayout_3.addWidget(self.V1)

        self.label_40 = BodyLabel(self.tab_12)
        self.label_40.setObjectName(u"label_40")

        self.horizontalLayout_3.addWidget(self.label_40)

        self.V2 = LineEdit(self.tab_12)
        self.V2.setObjectName(u"V2")

        self.horizontalLayout_3.addWidget(self.V2)


        self.gridLayout_10.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_29 = BodyLabel(self.tab_12)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_7.addWidget(self.label_29, 0, 2, 1, 1)

        self.filling_scf = LineEdit(self.tab_12)
        self.filling_scf.setObjectName(u"filling_scf")

        self.gridLayout_7.addWidget(self.filling_scf, 0, 1, 1, 1)

        self.label_28 = BodyLabel(self.tab_12)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_7.addWidget(self.label_28, 0, 0, 1, 1)

        self.extra_electron = LineEdit(self.tab_12)
        self.extra_electron.setObjectName(u"extra_electron")

        self.gridLayout_7.addWidget(self.extra_electron, 0, 3, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_7, 2, 0, 1, 2)


        self.gridLayout_14.addLayout(self.gridLayout_10, 0, 0, 1, 2)

        self.do_scf = CheckBox(self.tab_12)
        self.do_scf.setObjectName(u"do_scf")

        self.gridLayout_14.addWidget(self.do_scf, 1, 0, 1, 1)

        self.solve_scf = PushButton(self.tab_12)
        self.solve_scf.setObjectName(u"solve_scf")

        self.gridLayout_14.addWidget(self.solve_scf, 1, 1, 1, 1)

        self.tabWidget_4.addTab(self.tab_12, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.gridLayout_21 = QGridLayout(self.tab_11)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_32 = BodyLabel(self.tab_11)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_12.addWidget(self.label_32, 0, 0, 1, 1)

        self.label_27 = BodyLabel(self.tab_11)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_12.addWidget(self.label_27, 1, 0, 1, 1)

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


        self.gridLayout_21.addLayout(self.gridLayout_12, 0, 0, 1, 1)

        self.tabWidget_4.addTab(self.tab_11, "")

        self.gridLayout_5.addWidget(self.tabWidget_4, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_13 = QGridLayout(self.tab_6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_26 = QGridLayout()
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.label_43 = BodyLabel(self.tab_6)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_26.addWidget(self.label_43, 1, 0, 1, 1)

        self.magnetization_plot_mode = ComboBox(self.tab_6)
        self.magnetization_plot_mode.addItem("")
        self.magnetization_plot_mode.addItem("")
        self.magnetization_plot_mode.setObjectName(u"magnetization_plot_mode")

        self.gridLayout_26.addWidget(self.magnetization_plot_mode, 1, 1, 1, 1)

        self.show_magnetism = PushButton(self.tab_6)
        self.show_magnetism.setObjectName(u"show_magnetism")

        self.gridLayout_26.addWidget(self.show_magnetism, 0, 0, 1, 2)


        self.gridLayout_13.addLayout(self.gridLayout_26, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_6, "")
        self.tab_13 = QWidget()
        self.tab_13.setObjectName(u"tab_13")
        self.gridLayout_23 = QGridLayout(self.tab_13)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_22 = QGridLayout()
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.operator_chern = ComboBox(self.tab_13)
        self.operator_chern.addItem("")
        self.operator_chern.addItem("")
        self.operator_chern.addItem("")
        self.operator_chern.setObjectName(u"operator_chern")

        self.gridLayout_22.addWidget(self.operator_chern, 0, 1, 1, 1)

        self.label_34 = BodyLabel(self.tab_13)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_22.addWidget(self.label_34, 0, 0, 1, 1)

        self.show_local_chern = PushButton(self.tab_13)
        self.show_local_chern.setObjectName(u"show_local_chern")

        self.gridLayout_22.addWidget(self.show_local_chern, 1, 0, 1, 2)


        self.gridLayout_23.addLayout(self.gridLayout_22, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_13, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.gridLayout_20 = QGridLayout(self.tab_10)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.tmax_time_evolution = LineEdit(self.tab_10)
        self.tmax_time_evolution.setObjectName(u"tmax_time_evolution")

        self.gridLayout_19.addWidget(self.tmax_time_evolution, 0, 1, 1, 1)

        self.label_9 = BodyLabel(self.tab_10)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_19.addWidget(self.label_9, 0, 0, 1, 1)

        self.channel_time_evolution = ComboBox(self.tab_10)
        self.channel_time_evolution.addItem("")
        self.channel_time_evolution.addItem("")
        self.channel_time_evolution.setObjectName(u"channel_time_evolution")

        self.gridLayout_19.addWidget(self.channel_time_evolution, 1, 1, 1, 1)

        self.label_18 = BodyLabel(self.tab_10)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_19.addWidget(self.label_18, 1, 0, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_19, 0, 0, 1, 2)

        self.select_atom_time_evolution = PushButton(self.tab_10)
        self.select_atom_time_evolution.setObjectName(u"select_atom_time_evolution")

        self.gridLayout_20.addWidget(self.select_atom_time_evolution, 1, 0, 1, 1)

        self.show_time_evolution = PushButton(self.tab_10)
        self.show_time_evolution.setObjectName(u"show_time_evolution")

        self.gridLayout_20.addWidget(self.show_time_evolution, 1, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab_10, "")
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


        self.verticalLayout_site_dos.addLayout(self.gridLayout_site_dos)

        self.show_site_dos = PushButton(self.tab_site_dos)
        self.show_site_dos.setObjectName(u"show_site_dos")

        self.verticalLayout_site_dos.addWidget(self.show_site_dos)

        self.tabWidget_3.addTab(self.tab_site_dos, "")

        self.gridLayout_3.addWidget(self.tabWidget_3, 0, 1, 1, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_3.addWidget(self.save_results, 2, 0, 1, 2)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_3.addWidget(self.load_results, 3, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1041, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.bands_color.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"0D systems", None))
        self.crystalfield.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Haldane", None))
        self.fermi_image.setText("")
        self.mAF.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Anti-Haldane", None))
        self.peierls.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.swave.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.kanemele_image.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Kane-Mele", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Rashba", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Antiferromagnetism", None))
        self.bfield_image.setText("")
        self.pwave_image.setText("")
        self.fermi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.exchange.setText(QCoreApplication.translate("MainWindow", u"0.0, 0.0, 0.0", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Hoppings", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"swave superconductivity", None))
        self.mAB.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.rashba.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.swave_image.setText("")
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"pwave superconductivity", None))
        self.haldane_image.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
        self.mAB_image.setText("")
        self.hopping_image.setText("")
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Crystal field", None))
        self.mAF_image.setText("")
        self.rashba_image.setText("")
        self.antihaldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.pwave.setText(QCoreApplication.translate("MainWindow", u"0.0,0.0,0.0", None))
        self.kanemele.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.hoppings.setText(QCoreApplication.translate("MainWindow", u"1.0", None))
        self.antihaldane_image.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Exchange", None))
        self.cf_image.setText("")
        self.haldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Sublattice imbalance", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Magnetic field", None))
        self.exchange_image.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Terms in the Hamiltonian", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Non-uniform strain", None))
        self.strain_strength.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Strength", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Decay length", None))
        self.strain_decay.setText(QCoreApplication.translate("MainWindow", u"3.0", None))
        self.show_hoppings.setText(QCoreApplication.translate("MainWindow", u"Show hoppings", None))
        self.strain_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Radial scalar", None))
        self.strain_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Radial vector", None))

        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Strain type", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_14), QCoreApplication.translate("MainWindow", u"Additional terms", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.nsides.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Number of sides", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Type of lattice", None))
        self.lattice.setItemText(0, QCoreApplication.translate("MainWindow", u"Honeycomb", None))
        self.lattice.setItemText(1, QCoreApplication.translate("MainWindow", u"Square", None))
        self.lattice.setItemText(2, QCoreApplication.translate("MainWindow", u"Triangular", None))
        self.lattice.setItemText(3, QCoreApplication.translate("MainWindow", u"Kagome", None))
        self.lattice.setItemText(4, QCoreApplication.translate("MainWindow", u"Lieb", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Width", None))
        self.width.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.rotation.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Geometry", None))
#if QT_CONFIG(tooltip)
        self.remove_single_bonded.setToolTip(QCoreApplication.translate("MainWindow", u"Remove atoms that have a single bond in the structure", None))
#endif // QT_CONFIG(tooltip)
        self.remove_single_bonded.setText(QCoreApplication.translate("MainWindow", u"Remove single bonds", None))
        self.remove_selected.setText(QCoreApplication.translate("MainWindow", u"Remove selected atoms", None))
        self.select_atoms_removal.setText(QCoreApplication.translate("MainWindow", u"Select atoms to remove", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"Modify geometry", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.show_structure_3d.setText(QCoreApplication.translate("MainWindow", u"Show structure 3D", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Structure", None))
        self.show_bands.setText(QCoreApplication.translate("MainWindow", u"Eigenvalues", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.bands_color.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.bands_color.setItemText(1, QCoreApplication.translate("MainWindow", u"Sx", None))
        self.bands_color.setItemText(2, QCoreApplication.translate("MainWindow", u"Sy", None))
        self.bands_color.setItemText(3, QCoreApplication.translate("MainWindow", u"Sz", None))
        self.bands_color.setItemText(4, QCoreApplication.translate("MainWindow", u"Valley", None))
        self.bands_color.setItemText(5, QCoreApplication.translate("MainWindow", u"IPR", None))
        self.bands_color.setItemText(6, QCoreApplication.translate("MainWindow", u"Bulk", None))
        self.bands_color.setItemText(7, QCoreApplication.translate("MainWindow", u"Edge", None))

        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Eigenvalues", None))
        self.multildos_delta.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.multildos_ewindow.setText(QCoreApplication.translate("MainWindow", u"1.5", None))
        self.show_interactive_ldos.setText(QCoreApplication.translate("MainWindow", u"Show LDOS", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Basis", None))
        self.basis_ldos.setItemText(0, QCoreApplication.translate("MainWindow", u"Tight binding", None))
        self.basis_ldos.setItemText(1, QCoreApplication.translate("MainWindow", u"Real space atomic orbitals", None))

#if QT_CONFIG(tooltip)
        self.basis_ldos.setToolTip(QCoreApplication.translate("MainWindow", u"Choose the basis of the LDOS, projection onto the tight binding basis, or directly in true real space assuming a certain atomic-like wavefunction", None))
#endif // QT_CONFIG(tooltip)
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Local orbital radii", None))
#if QT_CONFIG(tooltip)
        self.ratomic_ldos.setToolTip(QCoreApplication.translate("MainWindow", u"Radii of the atomic-like wavefunctions put in every site. Only affects the result for ht eBasis \"Real space atomic orbitals\"", None))
#endif // QT_CONFIG(tooltip)
        self.ratomic_ldos.setText(QCoreApplication.translate("MainWindow", u"1.5", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"LDOS", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.label_dos_mode.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.dos_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"ED", None))
        self.dos_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"Green", None))
        self.dos_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"KPM", None))

        self.label_dos_operator.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.show_dos.setText(QCoreApplication.translate("MainWindow", u"Density of states", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"DOS", None))
        self.scf_initialization.setItemText(0, QCoreApplication.translate("MainWindow", u"antiferro", None))
        self.scf_initialization.setItemText(1, QCoreApplication.translate("MainWindow", u"ferroX", None))
        self.scf_initialization.setItemText(2, QCoreApplication.translate("MainWindow", u"ferroY", None))
        self.scf_initialization.setItemText(3, QCoreApplication.translate("MainWindow", u"ferroZ", None))
        self.scf_initialization.setItemText(4, QCoreApplication.translate("MainWindow", u"random", None))

        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Initialization", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"U", None))
#if QT_CONFIG(tooltip)
        self.U.setToolTip(QCoreApplication.translate("MainWindow", u"Local Hubbard interaction", None))
#endif // QT_CONFIG(tooltip)
        self.U.setText(QCoreApplication.translate("MainWindow", u"2.0", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"V1", None))
#if QT_CONFIG(tooltip)
        self.V1.setToolTip(QCoreApplication.translate("MainWindow", u"First neighbor interaction", None))
#endif // QT_CONFIG(tooltip)
        self.V1.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"V2", None))
#if QT_CONFIG(tooltip)
        self.V2.setToolTip(QCoreApplication.translate("MainWindow", u"Second neighbor interaction", None))
#endif // QT_CONFIG(tooltip)
        self.V2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Extra electron", None))
        self.filling_scf.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"FIlling", None))
        self.extra_electron.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.do_scf.setText(QCoreApplication.translate("MainWindow", u"Include mean field", None))
        self.solve_scf.setText(QCoreApplication.translate("MainWindow", u"Solve SCF", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_12), QCoreApplication.translate("MainWindow", u"Basic", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Mixing", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"# of kpoints", None))
        self.nk_scf.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.mix_scf.setText(QCoreApplication.translate("MainWindow", u"0.1", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.smearing_scf.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_11), QCoreApplication.translate("MainWindow", u"Convergence", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"SCF", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Plotting mode", None))
        self.magnetization_plot_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"2D", None))
        self.magnetization_plot_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"3D", None))

        self.show_magnetism.setText(QCoreApplication.translate("MainWindow", u"Show magnetism", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Magnetism", None))
        self.operator_chern.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.operator_chern.setItemText(1, QCoreApplication.translate("MainWindow", u"Valley", None))
        self.operator_chern.setItemText(2, QCoreApplication.translate("MainWindow", u"Sz", None))

        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.show_local_chern.setText(QCoreApplication.translate("MainWindow", u"Show local Chern number", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_13), QCoreApplication.translate("MainWindow", u"Topology", None))
        self.tmax_time_evolution.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Maximum time", None))
        self.channel_time_evolution.setItemText(0, QCoreApplication.translate("MainWindow", u"Up", None))
        self.channel_time_evolution.setItemText(1, QCoreApplication.translate("MainWindow", u"Down", None))

        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Channel", None))
        self.select_atom_time_evolution.setText(QCoreApplication.translate("MainWindow", u"Select atom", None))
        self.show_time_evolution.setText(QCoreApplication.translate("MainWindow", u"Perform time evolution", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_10), QCoreApplication.translate("MainWindow", u"Time evolution", None))
        self.label_site_dos_info.setText(QCoreApplication.translate("MainWindow", u"Click a site in the structure plot to compute the DOS there", None))
        self.label_site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.site_dos_ewindow.setText(QCoreApplication.translate("MainWindow", u"4.0", None))
        self.label_site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.site_dos_delta.setText(QCoreApplication.translate("MainWindow", u"0.03", None))
        self.show_site_dos.setText(QCoreApplication.translate("MainWindow", u"Site DOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_site_dos), QCoreApplication.translate("MainWindow", u"Site DOS", None))
#if QT_CONFIG(tooltip)
        self.save_results.setToolTip(QCoreApplication.translate("MainWindow", u"Save all the results in a local folder called QH_save, pressing the button overrides the folder!", None))
#endif // QT_CONFIG(tooltip)
        self.save_results.setText(QCoreApplication.translate("MainWindow", u"Save results", None))
#if QT_CONFIG(tooltip)
        self.load_results.setToolTip(QCoreApplication.translate("MainWindow", u"Restore the parameters and results from the last saved state", None))
#endif // QT_CONFIG(tooltip)
        self.load_results.setText(QCoreApplication.translate("MainWindow", u"Load results", None))
    # retranslateUi

