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

from qfluentwidgets import (BodyLabel, ComboBox, LineEdit, PushButton)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(950, 659)
        MainWindow.setMinimumSize(QSize(950, 659))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_12 = QGridLayout(self.centralwidget)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
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
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.gridLayout_17 = QGridLayout(self.tab_8)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.fermi = LineEdit(self.tab_8)
        self.fermi.setObjectName(u"fermi")
        self.fermi.setEnabled(True)

        self.gridLayout.addWidget(self.fermi, 1, 1, 1, 1)

        self.rashba = LineEdit(self.tab_8)
        self.rashba.setObjectName(u"rashba")

        self.gridLayout.addWidget(self.rashba, 5, 1, 1, 1)

        self.mAB = LineEdit(self.tab_8)
        self.mAB.setObjectName(u"mAB")

        self.gridLayout.addWidget(self.mAB, 9, 1, 1, 1)

        self.label_kanemele = BodyLabel(self.tab_8)
        self.label_kanemele.setObjectName(u"label_kanemele")

        self.gridLayout.addWidget(self.label_kanemele, 6, 0, 1, 1)

        self.label_4 = BodyLabel(self.tab_8)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_3 = BodyLabel(self.tab_8)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_5 = BodyLabel(self.tab_8)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_antihaldane = BodyLabel(self.tab_8)
        self.label_antihaldane.setObjectName(u"label_antihaldane")

        self.gridLayout.addWidget(self.label_antihaldane, 8, 0, 1, 1)

        self.kanemele = LineEdit(self.tab_8)
        self.kanemele.setObjectName(u"kanemele")

        self.gridLayout.addWidget(self.kanemele, 6, 1, 1, 1)

        self.mAF = LineEdit(self.tab_8)
        self.mAF.setObjectName(u"mAF")

        self.gridLayout.addWidget(self.mAF, 10, 1, 1, 1)

        self.label_rashba = BodyLabel(self.tab_8)
        self.label_rashba.setObjectName(u"label_rashba")

        self.gridLayout.addWidget(self.label_rashba, 5, 0, 1, 1)

        self.label_mAF = BodyLabel(self.tab_8)
        self.label_mAF.setObjectName(u"label_mAF")

        self.gridLayout.addWidget(self.label_mAF, 10, 0, 1, 1)

        self.label_mAB = BodyLabel(self.tab_8)
        self.label_mAB.setObjectName(u"label_mAB")

        self.gridLayout.addWidget(self.label_mAB, 9, 0, 1, 1)

        self.label_haldane = BodyLabel(self.tab_8)
        self.label_haldane.setObjectName(u"label_haldane")

        self.gridLayout.addWidget(self.label_haldane, 7, 0, 1, 1)

        self.label_swave = BodyLabel(self.tab_8)
        self.label_swave.setObjectName(u"label_swave")

        self.gridLayout.addWidget(self.label_swave, 11, 0, 1, 1)

        self.haldane = LineEdit(self.tab_8)
        self.haldane.setObjectName(u"haldane")

        self.gridLayout.addWidget(self.haldane, 7, 1, 1, 1)

        self.By = LineEdit(self.tab_8)
        self.By.setObjectName(u"By")

        self.gridLayout.addWidget(self.By, 3, 1, 1, 1)

        self.label_fermi = BodyLabel(self.tab_8)
        self.label_fermi.setObjectName(u"label_fermi")

        self.gridLayout.addWidget(self.label_fermi, 1, 0, 1, 1)

        self.Bz = LineEdit(self.tab_8)
        self.Bz.setObjectName(u"Bz")

        self.gridLayout.addWidget(self.Bz, 4, 1, 1, 1)

        self.Bx = LineEdit(self.tab_8)
        self.Bx.setObjectName(u"Bx")

        self.gridLayout.addWidget(self.Bx, 2, 1, 1, 1)

        self.antihaldane = LineEdit(self.tab_8)
        self.antihaldane.setObjectName(u"antihaldane")

        self.gridLayout.addWidget(self.antihaldane, 8, 1, 1, 1)

        self.swave = LineEdit(self.tab_8)
        self.swave.setObjectName(u"swave")

        self.gridLayout.addWidget(self.swave, 11, 1, 1, 1)

        self.label_44 = BodyLabel(self.tab_8)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout.addWidget(self.label_44, 0, 0, 1, 1)

        self.strain = LineEdit(self.tab_8)
        self.strain.setObjectName(u"strain")

        self.gridLayout.addWidget(self.strain, 0, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget_4.addTab(self.tab_8, "")
        self.tab_11 = QWidget()
        self.tab_11.setObjectName(u"tab_11")
        self.gridLayout_16 = QGridLayout(self.tab_11)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_40 = BodyLabel(self.tab_11)
        self.label_40.setObjectName(u"label_40")

        self.gridLayout_10.addWidget(self.label_40, 8, 0, 1, 1)

        self.label_39 = BodyLabel(self.tab_11)
        self.label_39.setObjectName(u"label_39")

        self.gridLayout_10.addWidget(self.label_39, 10, 0, 1, 1)

        self.label_33 = BodyLabel(self.tab_11)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_10.addWidget(self.label_33, 6, 0, 1, 1)

        self.Bz_2 = LineEdit(self.tab_11)
        self.Bz_2.setObjectName(u"Bz_2")

        self.gridLayout_10.addWidget(self.Bz_2, 4, 1, 1, 1)

        self.mAF_2 = LineEdit(self.tab_11)
        self.mAF_2.setObjectName(u"mAF_2")

        self.gridLayout_10.addWidget(self.mAF_2, 10, 1, 1, 1)

        self.label_42 = BodyLabel(self.tab_11)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_10.addWidget(self.label_42, 11, 0, 1, 1)

        self.label_36 = BodyLabel(self.tab_11)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_10.addWidget(self.label_36, 2, 0, 1, 1)

        self.Bx_2 = LineEdit(self.tab_11)
        self.Bx_2.setObjectName(u"Bx_2")

        self.gridLayout_10.addWidget(self.Bx_2, 2, 1, 1, 1)

        self.label_37 = BodyLabel(self.tab_11)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_10.addWidget(self.label_37, 1, 0, 1, 1)

        self.rashba_2 = LineEdit(self.tab_11)
        self.rashba_2.setObjectName(u"rashba_2")

        self.gridLayout_10.addWidget(self.rashba_2, 5, 1, 1, 1)

        self.swave_2 = LineEdit(self.tab_11)
        self.swave_2.setObjectName(u"swave_2")

        self.gridLayout_10.addWidget(self.swave_2, 11, 1, 1, 1)

        self.label_41 = BodyLabel(self.tab_11)
        self.label_41.setObjectName(u"label_41")

        self.gridLayout_10.addWidget(self.label_41, 7, 0, 1, 1)

        self.haldane_2 = LineEdit(self.tab_11)
        self.haldane_2.setObjectName(u"haldane_2")

        self.gridLayout_10.addWidget(self.haldane_2, 7, 1, 1, 1)

        self.antihaldane_2 = LineEdit(self.tab_11)
        self.antihaldane_2.setObjectName(u"antihaldane_2")

        self.gridLayout_10.addWidget(self.antihaldane_2, 8, 1, 1, 1)

        self.By_2 = LineEdit(self.tab_11)
        self.By_2.setObjectName(u"By_2")

        self.gridLayout_10.addWidget(self.By_2, 3, 1, 1, 1)

        self.label_22 = BodyLabel(self.tab_11)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_10.addWidget(self.label_22, 9, 0, 1, 1)

        self.fermi_2 = LineEdit(self.tab_11)
        self.fermi_2.setObjectName(u"fermi_2")
        self.fermi_2.setEnabled(True)

        self.gridLayout_10.addWidget(self.fermi_2, 1, 1, 1, 1)

        self.label_34 = BodyLabel(self.tab_11)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_10.addWidget(self.label_34, 3, 0, 1, 1)

        self.mAB_2 = LineEdit(self.tab_11)
        self.mAB_2.setObjectName(u"mAB_2")

        self.gridLayout_10.addWidget(self.mAB_2, 9, 1, 1, 1)

        self.label_38 = BodyLabel(self.tab_11)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_10.addWidget(self.label_38, 4, 0, 1, 1)

        self.label_32 = BodyLabel(self.tab_11)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_10.addWidget(self.label_32, 5, 0, 1, 1)

        self.kanemele_2 = LineEdit(self.tab_11)
        self.kanemele_2.setObjectName(u"kanemele_2")

        self.gridLayout_10.addWidget(self.kanemele_2, 6, 1, 1, 1)

        self.label_45 = BodyLabel(self.tab_11)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_10.addWidget(self.label_45, 0, 0, 1, 1)

        self.strain_2 = LineEdit(self.tab_11)
        self.strain_2.setObjectName(u"strain_2")

        self.gridLayout_10.addWidget(self.strain_2, 0, 1, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_10, 0, 0, 1, 1)

        self.tabWidget_4.addTab(self.tab_11, "")

        self.gridLayout_15.addWidget(self.tabWidget_4, 1, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")

        self.gridLayout_12.addWidget(self.tabWidget_2, 0, 0, 3, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_14 = QGridLayout(self.tab_2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
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

        self.thickness = LineEdit(self.tab_2)
        self.thickness.setObjectName(u"thickness")

        self.gridLayout_4.addWidget(self.thickness, 2, 1, 1, 1)

        self.label_43 = BodyLabel(self.tab_2)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_4.addWidget(self.label_43, 2, 0, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_12.addWidget(self.tabWidget, 1, 1, 1, 1)

        self.label_46 = BodyLabel(self.centralwidget)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_12.addWidget(self.label_46, 2, 1, 1, 1)

        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_13 = QGridLayout(self.tab_4)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.show_structure = PushButton(self.tab_4)
        self.show_structure.setObjectName(u"show_structure")

        self.gridLayout_13.addWidget(self.show_structure, 1, 0, 1, 1)

        self.show_structure_3d = PushButton(self.tab_4)
        self.show_structure_3d.setObjectName(u"show_structure_3d")

        self.gridLayout_13.addWidget(self.show_structure_3d, 1, 1, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_7 = BodyLabel(self.tab_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.nsuper_struct = LineEdit(self.tab_4)
        self.nsuper_struct.setObjectName(u"nsuper_struct")

        self.gridLayout_3.addWidget(self.nsuper_struct, 0, 1, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_3, 0, 0, 1, 2)

        self.tabWidget_3.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_18 = QGridLayout(self.tab_5)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.show_bands = PushButton(self.tab_5)
        self.show_bands.setObjectName(u"show_bands")

        self.gridLayout_18.addWidget(self.show_bands, 0, 0, 1, 1)

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


        self.gridLayout_18.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_5, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.gridLayout_19 = QGridLayout(self.tab_9)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
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


        self.gridLayout_19.addLayout(self.gridLayout_11, 0, 0, 1, 1)

        self.show_dosbands = PushButton(self.tab_9)
        self.show_dosbands.setObjectName(u"show_dosbands")

        self.gridLayout_19.addWidget(self.show_dosbands, 0, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab_9, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_20 = QGridLayout(self.tab_6)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.show_dos = PushButton(self.tab_6)
        self.show_dos.setObjectName(u"show_dos")

        self.gridLayout_20.addWidget(self.show_dos, 0, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_16 = BodyLabel(self.tab_6)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_5.addWidget(self.label_16, 0, 0, 1, 1)

        self.DOS_smearing = LineEdit(self.tab_6)
        self.DOS_smearing.setObjectName(u"DOS_smearing")

        self.gridLayout_5.addWidget(self.DOS_smearing, 0, 1, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_5, 1, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.gridLayout_21 = QGridLayout(self.tab_7)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.nk_ldos = LineEdit(self.tab_7)
        self.nk_ldos.setObjectName(u"nk_ldos")

        self.gridLayout_6.addWidget(self.nk_ldos, 2, 1, 1, 1)

        self.delta_ldos = LineEdit(self.tab_7)
        self.delta_ldos.setObjectName(u"delta_ldos")

        self.gridLayout_6.addWidget(self.delta_ldos, 3, 1, 1, 1)

        self.label_17 = BodyLabel(self.tab_7)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_6.addWidget(self.label_17, 2, 0, 1, 1)

        self.label_18 = BodyLabel(self.tab_7)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_6.addWidget(self.label_18, 3, 0, 1, 1)

        self.label_2 = BodyLabel(self.tab_7)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_6.addWidget(self.label_2, 0, 0, 1, 1)

        self.window_ldos = LineEdit(self.tab_7)
        self.window_ldos.setObjectName(u"window_ldos")

        self.gridLayout_6.addWidget(self.window_ldos, 0, 1, 1, 1)

        self.label_35 = BodyLabel(self.tab_7)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_6.addWidget(self.label_35, 1, 0, 1, 1)

        self.ne_ldos = LineEdit(self.tab_7)
        self.ne_ldos.setObjectName(u"ne_ldos")

        self.gridLayout_6.addWidget(self.ne_ldos, 1, 1, 1, 1)


        self.gridLayout_21.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.show_ldos = PushButton(self.tab_7)
        self.show_ldos.setObjectName(u"show_ldos")

        self.gridLayout_21.addWidget(self.show_ldos, 0, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab_7, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.gridLayout_22 = QGridLayout(self.tab_10)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.topology_nk = LineEdit(self.tab_10)
        self.topology_nk.setObjectName(u"topology_nk")

        self.gridLayout_8.addWidget(self.topology_nk, 0, 1, 1, 1)

        self.label_19 = BodyLabel(self.tab_10)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_8.addWidget(self.label_19, 0, 0, 1, 1)

        self.label_47 = BodyLabel(self.tab_10)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_8.addWidget(self.label_47, 1, 0, 1, 1)

        self.topology_operator = ComboBox(self.tab_10)
        self.topology_operator.addItem("")
        self.topology_operator.addItem("")
        self.topology_operator.addItem("")
        self.topology_operator.setObjectName(u"topology_operator")

        self.gridLayout_8.addWidget(self.topology_operator, 1, 1, 1, 1)


        self.gridLayout_22.addLayout(self.gridLayout_8, 0, 0, 1, 1)

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


        self.gridLayout_22.addLayout(self.gridLayout_7, 0, 1, 1, 1)

        self.tabWidget_3.addTab(self.tab_10, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_23 = QGridLayout(self.tab)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
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


        self.gridLayout_23.addLayout(self.gridLayout_9, 0, 0, 1, 1)

        self.show_kdos = PushButton(self.tab)
        self.show_kdos.setObjectName(u"show_kdos")

        self.gridLayout_23.addWidget(self.show_kdos, 1, 0, 1, 1)

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

        self.gridLayout_12.addWidget(self.tabWidget_3, 0, 1, 1, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_12.addWidget(self.save_results, 3, 0, 1, 2)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_12.addWidget(self.load_results, 4, 0, 1, 2)

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
        self.tabWidget_4.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.bands_color.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"2D heterostructure", None))
        self.label_nparts.setText(QCoreApplication.translate("MainWindow", u"Number of parts", None))
        self.nparts.setItemText(0, QCoreApplication.translate("MainWindow", u"2", None))
        self.nparts.setItemText(1, QCoreApplication.translate("MainWindow", u"3", None))
        self.nparts.setItemText(2, QCoreApplication.translate("MainWindow", u"4", None))
        self.nparts.setItemText(3, QCoreApplication.translate("MainWindow", u"5", None))
        self.nparts.setItemText(4, QCoreApplication.translate("MainWindow", u"6", None))

        self.fermi.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.rashba.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mAB.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_kanemele.setText(QCoreApplication.translate("MainWindow", u"Kane-Mele", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jy", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jx", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jz", None))
        self.label_antihaldane.setText(QCoreApplication.translate("MainWindow", u"Anti-Haldane", None))
        self.kanemele.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mAF.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_rashba.setText(QCoreApplication.translate("MainWindow", u"Rashba", None))
        self.label_mAF.setText(QCoreApplication.translate("MainWindow", u"Antiferromagnetism", None))
        self.label_mAB.setText(QCoreApplication.translate("MainWindow", u"Sublattice imbalance", None))
        self.label_haldane.setText(QCoreApplication.translate("MainWindow", u"Haldane", None))
        self.label_swave.setText(QCoreApplication.translate("MainWindow", u"swave pairing", None))
        self.haldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.By.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_fermi.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
        self.Bz.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.Bx.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.antihaldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.swave.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Strain", None))
        self.strain.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"Upper", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Anti-Haldane", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Antiferromagnetism", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Kane-Mele", None))
        self.Bz_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.mAF_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"swave pairing", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jx", None))
        self.Bx_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
        self.rashba_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.swave_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"Haldane", None))
        self.haldane_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.antihaldane_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.By_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Sublattice imbalance", None))
        self.fermi_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jy", None))
        self.mAB_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Zeeman Jz", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Rashba", None))
        self.kanemele_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Strain", None))
        self.strain_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_11), QCoreApplication.translate("MainWindow", u"Lower", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Terms in the Hamiltonian", None))
        self.nsuper.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Type of lattice", None))
        self.lattice.setItemText(0, QCoreApplication.translate("MainWindow", u"Diamond", None))
        self.lattice.setItemText(1, QCoreApplication.translate("MainWindow", u"Cubic", None))
        self.lattice.setItemText(2, QCoreApplication.translate("MainWindow", u"Pyrochlore", None))
        self.lattice.setItemText(3, QCoreApplication.translate("MainWindow", u"Hyperhoneycomb", None))

        self.thickness.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Thickness", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Geometry", None))
#if QT_CONFIG(tooltip)
        self.label_46.setToolTip(QCoreApplication.translate("MainWindow", u"This module allows to compute heterostructures consisting of two different films. You have to specify the parameters of the two films", None))
#endif // QT_CONFIG(tooltip)
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.show_structure_3d.setText(QCoreApplication.translate("MainWindow", u"Show 3D structure", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.nsuper_struct.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Structure", None))
        self.show_bands.setText(QCoreApplication.translate("MainWindow", u"Band structure", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
        self.bands_color.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.bands_color.setItemText(1, QCoreApplication.translate("MainWindow", u"Interface", None))
        self.bands_color.setItemText(2, QCoreApplication.translate("MainWindow", u"z-position", None))
        self.bands_color.setItemText(3, QCoreApplication.translate("MainWindow", u"Sx", None))
        self.bands_color.setItemText(4, QCoreApplication.translate("MainWindow", u"Sy", None))
        self.bands_color.setItemText(5, QCoreApplication.translate("MainWindow", u"Sz", None))
        self.bands_color.setItemText(6, QCoreApplication.translate("MainWindow", u"Valley", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.nk_bands.setText(QCoreApplication.translate("MainWindow", u"100", None))
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
        self.show_dos.setText(QCoreApplication.translate("MainWindow", u"Density of states", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.DOS_smearing.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"DOS", None))
        self.nk_ldos.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.delta_ldos.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"# of kpoints", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
        self.window_ldos.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"# of energies", None))
        self.ne_ldos.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.show_ldos.setText(QCoreApplication.translate("MainWindow", u"Show LDOS", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"LDOS", None))
        self.topology_nk.setText(QCoreApplication.translate("MainWindow", u"400", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"# kpoints", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Operator", None))
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

