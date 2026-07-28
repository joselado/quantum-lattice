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
        MainWindow.resize(735, 614)
        MainWindow.setBaseSize(QSize(0, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_6 = QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
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
        self.lattice.setObjectName(u"lattice")

        self.gridLayout_4.addWidget(self.lattice, 0, 1, 1, 1)

        self.label_width = BodyLabel(self.tab_2)
        self.label_width.setObjectName(u"label_width")

        self.gridLayout_4.addWidget(self.label_width, 1, 0, 1, 1)

        self.width = LineEdit(self.tab_2)
        self.width.setObjectName(u"width")

        self.gridLayout_4.addWidget(self.width, 1, 1, 1, 1)

        self.nsuper = LineEdit(self.tab_2)
        self.nsuper.setObjectName(u"nsuper")

        self.gridLayout_4.addWidget(self.nsuper, 2, 1, 1, 1)

        self.label_6 = BodyLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)


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

        self.info_tab = BodyLabel(self.centralwidget)
        self.info_tab.setObjectName(u"info_tab")

        self.gridLayout_6.addWidget(self.info_tab, 6, 0, 1, 2)

        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_24 = QGridLayout(self.tab_3)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.mAB = LineEdit(self.tab_3)
        self.mAB.setObjectName(u"mAB")

        self.gridLayout.addWidget(self.mAB, 7, 2, 1, 1)

        self.label_fermi = BodyLabel(self.tab_3)
        self.label_fermi.setObjectName(u"label_fermi")

        self.gridLayout.addWidget(self.label_fermi, 0, 0, 1, 1)

        self.label_antikanemele = BodyLabel(self.tab_3)
        self.label_antikanemele.setObjectName(u"label_antikanemele")

        self.gridLayout.addWidget(self.label_antikanemele, 6, 0, 1, 1)

        self.pwave_image = BodyLabel(self.tab_3)
        self.pwave_image.setObjectName(u"pwave_image")

        self.gridLayout.addWidget(self.pwave_image, 10, 1, 1, 1)

        self.haldane = LineEdit(self.tab_3)
        self.haldane.setObjectName(u"haldane")

        self.gridLayout.addWidget(self.haldane, 4, 2, 1, 1)

        self.rashba_image = BodyLabel(self.tab_3)
        self.rashba_image.setObjectName(u"rashba_image")

        self.gridLayout.addWidget(self.rashba_image, 2, 1, 1, 1)

        self.antihaldane_image = BodyLabel(self.tab_3)
        self.antihaldane_image.setObjectName(u"antihaldane_image")

        self.gridLayout.addWidget(self.antihaldane_image, 5, 1, 1, 1)

        self.label_rashba = BodyLabel(self.tab_3)
        self.label_rashba.setObjectName(u"label_rashba")

        self.gridLayout.addWidget(self.label_rashba, 2, 0, 1, 1)

        self.label_exchange = BodyLabel(self.tab_3)
        self.label_exchange.setObjectName(u"label_exchange")

        self.gridLayout.addWidget(self.label_exchange, 1, 0, 1, 1)

        self.mAB_image = BodyLabel(self.tab_3)
        self.mAB_image.setObjectName(u"mAB_image")

        self.gridLayout.addWidget(self.mAB_image, 7, 1, 1, 1)

        self.mAF_image = BodyLabel(self.tab_3)
        self.mAF_image.setObjectName(u"mAF_image")

        self.gridLayout.addWidget(self.mAF_image, 8, 1, 1, 1)

        self.exchange = LineEdit(self.tab_3)
        self.exchange.setObjectName(u"exchange")
        self.exchange.setEnabled(True)

        self.gridLayout.addWidget(self.exchange, 1, 2, 1, 1)

        self.kanemele_image = BodyLabel(self.tab_3)
        self.kanemele_image.setObjectName(u"kanemele_image")

        self.gridLayout.addWidget(self.kanemele_image, 3, 1, 1, 1)

        self.pwave = LineEdit(self.tab_3)
        self.pwave.setObjectName(u"pwave")
        self.pwave.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.pwave, 10, 2, 1, 1)

        self.label_antihaldane = BodyLabel(self.tab_3)
        self.label_antihaldane.setObjectName(u"label_antihaldane")

        self.gridLayout.addWidget(self.label_antihaldane, 5, 0, 1, 1)

        self.swave_image = BodyLabel(self.tab_3)
        self.swave_image.setObjectName(u"swave_image")

        self.gridLayout.addWidget(self.swave_image, 9, 1, 1, 1)

        self.mAF = LineEdit(self.tab_3)
        self.mAF.setObjectName(u"mAF")
        self.mAF.setEnabled(True)

        self.gridLayout.addWidget(self.mAF, 8, 2, 1, 1)

        self.fermi_image = BodyLabel(self.tab_3)
        self.fermi_image.setObjectName(u"fermi_image")
        self.fermi_image.setMinimumSize(QSize(30, 0))

        self.gridLayout.addWidget(self.fermi_image, 0, 1, 1, 1)

        self.label_mAF = BodyLabel(self.tab_3)
        self.label_mAF.setObjectName(u"label_mAF")

        self.gridLayout.addWidget(self.label_mAF, 8, 0, 1, 1)

        self.label_swave = BodyLabel(self.tab_3)
        self.label_swave.setObjectName(u"label_swave")

        self.gridLayout.addWidget(self.label_swave, 9, 0, 1, 1)

        self.kanemele = LineEdit(self.tab_3)
        self.kanemele.setObjectName(u"kanemele")
        self.kanemele.setEnabled(True)

        self.gridLayout.addWidget(self.kanemele, 3, 2, 1, 1)

        self.antikanemele_image = BodyLabel(self.tab_3)
        self.antikanemele_image.setObjectName(u"antikanemele_image")

        self.gridLayout.addWidget(self.antikanemele_image, 6, 1, 1, 1)

        self.label_haldane = BodyLabel(self.tab_3)
        self.label_haldane.setObjectName(u"label_haldane")

        self.gridLayout.addWidget(self.label_haldane, 4, 0, 1, 1)

        self.exchange_image = BodyLabel(self.tab_3)
        self.exchange_image.setObjectName(u"exchange_image")

        self.gridLayout.addWidget(self.exchange_image, 1, 1, 1, 1)

        self.rashba = LineEdit(self.tab_3)
        self.rashba.setObjectName(u"rashba")
        self.rashba.setEnabled(True)

        self.gridLayout.addWidget(self.rashba, 2, 2, 1, 1)

        self.antihaldane = LineEdit(self.tab_3)
        self.antihaldane.setObjectName(u"antihaldane")

        self.gridLayout.addWidget(self.antihaldane, 5, 2, 1, 1)

        self.label_mAB = BodyLabel(self.tab_3)
        self.label_mAB.setObjectName(u"label_mAB")

        self.gridLayout.addWidget(self.label_mAB, 7, 0, 1, 1)

        self.antikanemele = LineEdit(self.tab_3)
        self.antikanemele.setObjectName(u"antikanemele")
        self.antikanemele.setEnabled(True)

        self.gridLayout.addWidget(self.antikanemele, 6, 2, 1, 1)

        self.label_pwave = BodyLabel(self.tab_3)
        self.label_pwave.setObjectName(u"label_pwave")

        self.gridLayout.addWidget(self.label_pwave, 10, 0, 1, 1)

        self.swave = LineEdit(self.tab_3)
        self.swave.setObjectName(u"swave")
        self.swave.setEnabled(True)

        self.gridLayout.addWidget(self.swave, 9, 2, 1, 1)

        self.fermi = LineEdit(self.tab_3)
        self.fermi.setObjectName(u"fermi")
        self.fermi.setEnabled(True)

        self.gridLayout.addWidget(self.fermi, 0, 2, 1, 1)

        self.label_kanemele = BodyLabel(self.tab_3)
        self.label_kanemele.setObjectName(u"label_kanemele")

        self.gridLayout.addWidget(self.label_kanemele, 3, 0, 1, 1)

        self.haldane_image = BodyLabel(self.tab_3)
        self.haldane_image.setObjectName(u"haldane_image")

        self.gridLayout.addWidget(self.haldane_image, 4, 1, 1, 1)


        self.gridLayout_24.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_2 = QGridLayout(self.tab_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.fermi_impurity_image = BodyLabel(self.tab_5)
        self.fermi_impurity_image.setObjectName(u"fermi_impurity_image")
        self.fermi_impurity_image.setBaseSize(QSize(40, 0))

        self.gridLayout_2.addWidget(self.fermi_impurity_image, 0, 1, 1, 1)

        self.label_19 = BodyLabel(self.tab_5)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_2.addWidget(self.label_19, 2, 0, 1, 1)

        self.label_2 = BodyLabel(self.tab_5)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.impurity_potential = LineEdit(self.tab_5)
        self.impurity_potential.setObjectName(u"impurity_potential")

        self.gridLayout_2.addWidget(self.impurity_potential, 0, 2, 1, 1)

        self.select_impurity_sites = PushButton(self.tab_5)
        self.select_impurity_sites.setObjectName(u"select_impurity_sites")

        self.gridLayout_2.addWidget(self.select_impurity_sites, 3, 0, 1, 3)

        self.nsuper_impurity = LineEdit(self.tab_5)
        self.nsuper_impurity.setObjectName(u"nsuper_impurity")
        self.nsuper_impurity.setEnabled(False)

        self.gridLayout_2.addWidget(self.nsuper_impurity, 2, 2, 1, 1)

        self.label_3 = BodyLabel(self.tab_5)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.impurity_exchange = LineEdit(self.tab_5)
        self.impurity_exchange.setObjectName(u"impurity_exchange")

        self.gridLayout_2.addWidget(self.impurity_exchange, 1, 2, 1, 1)

        self.exchange_impurity_image = BodyLabel(self.tab_5)
        self.exchange_impurity_image.setObjectName(u"exchange_impurity_image")
        self.exchange_impurity_image.setBaseSize(QSize(40, 0))

        self.gridLayout_2.addWidget(self.exchange_impurity_image, 1, 1, 1, 1)

        self.tabWidget_2.addTab(self.tab_5, "")

        self.gridLayout_6.addWidget(self.tabWidget_2, 0, 0, 2, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_6.addWidget(self.save_results, 5, 0, 1, 2)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_6.addWidget(self.load_results, 6, 0, 1, 2)

        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tabWidget_3.setEnabled(True)
        self.tabWidget_3.setMinimumSize(QSize(400, 0))
        self.tabWidget_3.setBaseSize(QSize(0, 0))
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
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_7 = QGridLayout(self.tab)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_9 = BodyLabel(self.tab)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_5.addWidget(self.label_9, 0, 0, 1, 1)

        self.show_embedding_ldos = PushButton(self.tab)
        self.show_embedding_ldos.setObjectName(u"show_embedding_ldos")

        self.gridLayout_5.addWidget(self.show_embedding_ldos, 4, 0, 1, 2)

        self.label_14 = BodyLabel(self.tab)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_5.addWidget(self.label_14, 1, 0, 1, 1)

        self.energy_embedding_ldos = LineEdit(self.tab)
        self.energy_embedding_ldos.setObjectName(u"energy_embedding_ldos")

        self.gridLayout_5.addWidget(self.energy_embedding_ldos, 0, 1, 1, 1)

        self.label_15 = BodyLabel(self.tab)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_5.addWidget(self.label_15, 2, 0, 1, 1)

        self.delta_embedding_ldos = LineEdit(self.tab)
        self.delta_embedding_ldos.setObjectName(u"delta_embedding_ldos")

        self.gridLayout_5.addWidget(self.delta_embedding_ldos, 1, 1, 1, 1)

        self.nk_scaling_embedding_ldos = LineEdit(self.tab)
        self.nk_scaling_embedding_ldos.setObjectName(u"nk_scaling_embedding_ldos")

        self.gridLayout_5.addWidget(self.nk_scaling_embedding_ldos, 2, 1, 1, 1)

        self.ncells_embedding_ldos = LineEdit(self.tab)
        self.ncells_embedding_ldos.setObjectName(u"ncells_embedding_ldos")

        self.gridLayout_5.addWidget(self.ncells_embedding_ldos, 3, 1, 1, 1)

        self.label_17 = BodyLabel(self.tab)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_5.addWidget(self.label_17, 3, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab, "")
        self.tab_14 = QWidget()
        self.tab_14.setObjectName(u"tab_14")
        self.gridLayout_28 = QGridLayout(self.tab_14)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_27 = QGridLayout()
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.label_44 = BodyLabel(self.tab_14)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_27.addWidget(self.label_44, 0, 0, 1, 1)

        self.nk_scaling_embedding_ldos_sweep = LineEdit(self.tab_14)
        self.nk_scaling_embedding_ldos_sweep.setObjectName(u"nk_scaling_embedding_ldos_sweep")

        self.gridLayout_27.addWidget(self.nk_scaling_embedding_ldos_sweep, 3, 1, 1, 1)

        self.show_embedding_ldos_sweep = PushButton(self.tab_14)
        self.show_embedding_ldos_sweep.setObjectName(u"show_embedding_ldos_sweep")
        self.show_embedding_ldos_sweep.setEnabled(True)

        self.gridLayout_27.addWidget(self.show_embedding_ldos_sweep, 6, 0, 1, 2)

        self.energy_window_embedding_ldos_sweep = LineEdit(self.tab_14)
        self.energy_window_embedding_ldos_sweep.setObjectName(u"energy_window_embedding_ldos_sweep")

        self.gridLayout_27.addWidget(self.energy_window_embedding_ldos_sweep, 0, 1, 1, 1)

        self.label_45 = BodyLabel(self.tab_14)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_27.addWidget(self.label_45, 3, 0, 1, 1)

        self.label_46 = BodyLabel(self.tab_14)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_27.addWidget(self.label_46, 4, 0, 1, 1)

        self.ncells_embedding_ldos_sweep = LineEdit(self.tab_14)
        self.ncells_embedding_ldos_sweep.setObjectName(u"ncells_embedding_ldos_sweep")

        self.gridLayout_27.addWidget(self.ncells_embedding_ldos_sweep, 4, 1, 1, 1)

        self.delta_embedding_ldos_sweep = LineEdit(self.tab_14)
        self.delta_embedding_ldos_sweep.setObjectName(u"delta_embedding_ldos_sweep")

        self.gridLayout_27.addWidget(self.delta_embedding_ldos_sweep, 2, 1, 1, 1)

        self.label_43 = BodyLabel(self.tab_14)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_27.addWidget(self.label_43, 2, 0, 1, 1)

        self.label_18 = BodyLabel(self.tab_14)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_27.addWidget(self.label_18, 1, 0, 1, 1)

        self.num_energies_embedding_ldos_sweep = LineEdit(self.tab_14)
        self.num_energies_embedding_ldos_sweep.setObjectName(u"num_energies_embedding_ldos_sweep")

        self.gridLayout_27.addWidget(self.num_energies_embedding_ldos_sweep, 1, 1, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_27, 0, 0, 1, 1)

        self.tabWidget_3.addTab(self.tab_14, "")

        self.gridLayout_6.addWidget(self.tabWidget_3, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 735, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Ribbon embedding", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Type of lattice", None))
        self.lattice.setItemText(0, QCoreApplication.translate("MainWindow", u"Chain", None))
        self.lattice.setItemText(1, QCoreApplication.translate("MainWindow", u"Bichain", None))
        self.lattice.setItemText(2, QCoreApplication.translate("MainWindow", u"Honeycomb zigzag", None))
        self.lattice.setItemText(3, QCoreApplication.translate("MainWindow", u"Honeycomb armchair", None))
        self.lattice.setItemText(4, QCoreApplication.translate("MainWindow", u"Square", None))
        self.lattice.setItemText(5, QCoreApplication.translate("MainWindow", u"Triangular", None))
        self.lattice.setItemText(6, QCoreApplication.translate("MainWindow", u"Kagome", None))
        self.lattice.setItemText(7, QCoreApplication.translate("MainWindow", u"Lieb", None))

        self.label_width.setText(QCoreApplication.translate("MainWindow", u"Ribbon width", None))
#if QT_CONFIG(tooltip)
        self.width.setToolTip(QCoreApplication.translate("MainWindow", u"Number of unit cells across the ribbon's finite direction", None))
#endif // QT_CONFIG(tooltip)
        self.width.setText(QCoreApplication.translate("MainWindow", u"4", None))
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
        self.info_tab.setText("")
        self.mAB.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_fermi.setText(QCoreApplication.translate("MainWindow", u"Fermi energy", None))
        self.label_antikanemele.setText(QCoreApplication.translate("MainWindow", u"Anti Kane-Mele", None))
        self.pwave_image.setText("")
        self.haldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.rashba_image.setText("")
        self.antihaldane_image.setText("")
        self.label_rashba.setText(QCoreApplication.translate("MainWindow", u"Rashba", None))
        self.label_exchange.setText(QCoreApplication.translate("MainWindow", u"Exchange field", None))
        self.mAB_image.setText("")
        self.mAF_image.setText("")
        self.exchange.setText(QCoreApplication.translate("MainWindow", u"0.0, 0.0, 0.0", None))
        self.kanemele_image.setText("")
        self.pwave.setText(QCoreApplication.translate("MainWindow", u"0.0, 0.0, 0.0", None))
        self.label_antihaldane.setText(QCoreApplication.translate("MainWindow", u"Anti-Haldane", None))
        self.swave_image.setText("")
        self.mAF.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.fermi_image.setText("")
        self.label_mAF.setText(QCoreApplication.translate("MainWindow", u"Antiferromagnetism", None))
        self.label_swave.setText(QCoreApplication.translate("MainWindow", u"swave pairing", None))
        self.kanemele.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.antikanemele_image.setText("")
        self.label_haldane.setText(QCoreApplication.translate("MainWindow", u"Haldane", None))
        self.exchange_image.setText("")
        self.rashba.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.antihaldane.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_mAB.setText(QCoreApplication.translate("MainWindow", u"Sublattice imbalance", None))
        self.antikanemele.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_pwave.setText(QCoreApplication.translate("MainWindow", u"pwave pairing", None))
        self.swave.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.fermi.setText(QCoreApplication.translate("MainWindow", u"-3.5", None))
        self.label_kanemele.setText(QCoreApplication.translate("MainWindow", u"Kane-Mele", None))
        self.haldane_image.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Pristine Hamiltonian", None))
        self.fermi_impurity_image.setText("")
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Supercell with impurities", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Impurity potential", None))
        self.impurity_potential.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.select_impurity_sites.setText(QCoreApplication.translate("MainWindow", u"Select the sites with impurities", None))
        self.nsuper_impurity.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Impurity exchange", None))
        self.impurity_exchange.setText(QCoreApplication.translate("MainWindow", u"0.0, 0.0, 0.0", None))
        self.exchange_impurity_image.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Impurity", None))
        self.save_results.setText(QCoreApplication.translate("MainWindow", u"Save Results", None))
        self.load_results.setText(QCoreApplication.translate("MainWindow", u"Load Results", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.show_structure_3d.setText(QCoreApplication.translate("MainWindow", u"Show structure 3D", None))
        self.nsuper_struct.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Supercell", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Pristine structure", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Energy", None))
        self.show_embedding_ldos.setText(QCoreApplication.translate("MainWindow", u"Show LDOS", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.energy_embedding_ldos.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"k-mesh accuracy", None))
        self.delta_embedding_ldos.setText(QCoreApplication.translate("MainWindow", u"0.01", None))
#if QT_CONFIG(tooltip)
        self.nk_scaling_embedding_ldos.setToolTip(QCoreApplication.translate("MainWindow", u"Accuracy in the k-mesh, higher values are more accurate yet more computationally expensive", None))
#endif // QT_CONFIG(tooltip)
        self.nk_scaling_embedding_ldos.setText(QCoreApplication.translate("MainWindow", u"1.0", None))
        self.ncells_embedding_ldos.setText(QCoreApplication.translate("MainWindow", u"21", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Number of unit cells", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Single LDOS", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Energy window", None))
#if QT_CONFIG(tooltip)
        self.nk_scaling_embedding_ldos_sweep.setToolTip(QCoreApplication.translate("MainWindow", u"Number of kpoints used", None))
#endif // QT_CONFIG(tooltip)
        self.nk_scaling_embedding_ldos_sweep.setText(QCoreApplication.translate("MainWindow", u"1.0", None))
        self.show_embedding_ldos_sweep.setText(QCoreApplication.translate("MainWindow", u"Show LDOS", None))
#if QT_CONFIG(tooltip)
        self.energy_window_embedding_ldos_sweep.setToolTip(QCoreApplication.translate("MainWindow", u"Energy window", None))
#endif // QT_CONFIG(tooltip)
        self.energy_window_embedding_ldos_sweep.setText(QCoreApplication.translate("MainWindow", u"0.5", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"k-mesh accuracy", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Number of unit cells", None))
#if QT_CONFIG(tooltip)
        self.ncells_embedding_ldos_sweep.setToolTip(QCoreApplication.translate("MainWindow", u"Number of replicas of the unit cell to plot", None))
#endif // QT_CONFIG(tooltip)
        self.ncells_embedding_ldos_sweep.setText(QCoreApplication.translate("MainWindow", u"11", None))
#if QT_CONFIG(tooltip)
        self.delta_embedding_ldos_sweep.setToolTip(QCoreApplication.translate("MainWindow", u"Energy smearing", None))
#endif // QT_CONFIG(tooltip)
        self.delta_embedding_ldos_sweep.setText(QCoreApplication.translate("MainWindow", u"0.05", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Smearing", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Number of energies", None))
        self.num_energies_embedding_ldos_sweep.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_14), QCoreApplication.translate("MainWindow", u"LDOS", None))
    # retranslateUi

