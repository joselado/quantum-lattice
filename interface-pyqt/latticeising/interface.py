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
        MainWindow.resize(735, 614)
        MainWindow.setBaseSize(QSize(0, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_1 = QGridLayout(self.centralwidget)
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_geometry = QWidget()
        self.tab_geometry.setObjectName(u"tab_geometry")
        self.gridLayout_geometry = QGridLayout(self.tab_geometry)
        self.gridLayout_geometry.setObjectName(u"gridLayout_geometry")
        self.gridLayout_geometry_fields = QGridLayout()
        self.gridLayout_geometry_fields.setObjectName(u"gridLayout_geometry_fields")
        self.label_lattice = BodyLabel(self.tab_geometry)
        self.label_lattice.setObjectName(u"label_lattice")

        self.gridLayout_geometry_fields.addWidget(self.label_lattice, 0, 0, 1, 1)

        self.lattice = ComboBox(self.tab_geometry)
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.addItem("")
        self.lattice.setObjectName(u"lattice")

        self.gridLayout_geometry_fields.addWidget(self.lattice, 0, 1, 1, 1)

        self.label_supercell_size = BodyLabel(self.tab_geometry)
        self.label_supercell_size.setObjectName(u"label_supercell_size")

        self.gridLayout_geometry_fields.addWidget(self.label_supercell_size, 1, 0, 1, 1)

        self.supercell_size = LineEdit(self.tab_geometry)
        self.supercell_size.setObjectName(u"supercell_size")

        self.gridLayout_geometry_fields.addWidget(self.supercell_size, 1, 1, 1, 1)

        self.label_magnetization = BodyLabel(self.tab_geometry)
        self.label_magnetization.setObjectName(u"label_magnetization")

        self.gridLayout_geometry_fields.addWidget(self.label_magnetization, 2, 0, 1, 1)

        self.magnetization = LineEdit(self.tab_geometry)
        self.magnetization.setObjectName(u"magnetization")

        self.gridLayout_geometry_fields.addWidget(self.magnetization, 2, 1, 1, 1)


        self.gridLayout_geometry.addLayout(self.gridLayout_geometry_fields, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_geometry, "")
        self.tab_interactions = QWidget()
        self.tab_interactions.setObjectName(u"tab_interactions")
        self.gridLayout_interactions = QGridLayout(self.tab_interactions)
        self.gridLayout_interactions.setObjectName(u"gridLayout_interactions")
        self.gridLayout_interactions_fields = QGridLayout()
        self.gridLayout_interactions_fields.setObjectName(u"gridLayout_interactions_fields")
        self.label_Jij_ising = BodyLabel(self.tab_interactions)
        self.label_Jij_ising.setObjectName(u"label_Jij_ising")

        self.gridLayout_interactions_fields.addWidget(self.label_Jij_ising, 0, 0, 1, 1)

        self.Jij_ising = LineEdit(self.tab_interactions)
        self.Jij_ising.setObjectName(u"Jij_ising")

        self.gridLayout_interactions_fields.addWidget(self.Jij_ising, 0, 1, 1, 1)

        self.label_field_profile = BodyLabel(self.tab_interactions)
        self.label_field_profile.setObjectName(u"label_field_profile")

        self.gridLayout_interactions_fields.addWidget(self.label_field_profile, 1, 0, 1, 1)

        self.field_profile = LineEdit(self.tab_interactions)
        self.field_profile.setObjectName(u"field_profile")

        self.gridLayout_interactions_fields.addWidget(self.field_profile, 1, 1, 1, 1)


        self.gridLayout_interactions.addLayout(self.gridLayout_interactions_fields, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_interactions, "")
        self.tab_anneal_settings = QWidget()
        self.tab_anneal_settings.setObjectName(u"tab_anneal_settings")
        self.gridLayout_anneal_settings = QGridLayout(self.tab_anneal_settings)
        self.gridLayout_anneal_settings.setObjectName(u"gridLayout_anneal_settings")
        self.gridLayout_anneal_settings_fields = QGridLayout()
        self.gridLayout_anneal_settings_fields.setObjectName(u"gridLayout_anneal_settings_fields")
        self.label_temp = BodyLabel(self.tab_anneal_settings)
        self.label_temp.setObjectName(u"label_temp")

        self.gridLayout_anneal_settings_fields.addWidget(self.label_temp, 0, 0, 1, 1)

        self.temp = LineEdit(self.tab_anneal_settings)
        self.temp.setObjectName(u"temp")

        self.gridLayout_anneal_settings_fields.addWidget(self.temp, 0, 1, 1, 1)

        self.label_ntries = BodyLabel(self.tab_anneal_settings)
        self.label_ntries.setObjectName(u"label_ntries")

        self.gridLayout_anneal_settings_fields.addWidget(self.label_ntries, 1, 0, 1, 1)

        self.ntries = LineEdit(self.tab_anneal_settings)
        self.ntries.setObjectName(u"ntries")

        self.gridLayout_anneal_settings_fields.addWidget(self.ntries, 1, 1, 1, 1)

        self.label_n_snapshots = BodyLabel(self.tab_anneal_settings)
        self.label_n_snapshots.setObjectName(u"label_n_snapshots")

        self.gridLayout_anneal_settings_fields.addWidget(self.label_n_snapshots, 2, 0, 1, 1)

        self.n_snapshots = LineEdit(self.tab_anneal_settings)
        self.n_snapshots.setObjectName(u"n_snapshots")

        self.gridLayout_anneal_settings_fields.addWidget(self.n_snapshots, 2, 1, 1, 1)


        self.gridLayout_anneal_settings.addLayout(self.gridLayout_anneal_settings_fields, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_anneal_settings, "")

        self.gridLayout_1.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setMinimumSize(QSize(400, 0))
        self.tab_structure = QWidget()
        self.tab_structure.setObjectName(u"tab_structure")
        self.gridLayout_structure = QGridLayout(self.tab_structure)
        self.gridLayout_structure.setObjectName(u"gridLayout_structure")
        self.show_structure = PushButton(self.tab_structure)
        self.show_structure.setObjectName(u"show_structure")

        self.gridLayout_structure.addWidget(self.show_structure, 1, 0, 1, 1)

        self.show_structure_3d = PushButton(self.tab_structure)
        self.show_structure_3d.setObjectName(u"show_structure_3d")

        self.gridLayout_structure.addWidget(self.show_structure_3d, 1, 1, 1, 1)

        self.tabWidget_2.addTab(self.tab_structure, "")
        self.tab_anneal_results = QWidget()
        self.tab_anneal_results.setObjectName(u"tab_anneal_results")
        self.verticalLayout_anneal_results = QVBoxLayout(self.tab_anneal_results)
        self.verticalLayout_anneal_results.setObjectName(u"verticalLayout_anneal_results")
        self.show_spin_configuration = PushButton(self.tab_anneal_results)
        self.show_spin_configuration.setObjectName(u"show_spin_configuration")

        self.verticalLayout_anneal_results.addWidget(self.show_spin_configuration)

        self.show_spin_relaxation = PushButton(self.tab_anneal_results)
        self.show_spin_relaxation.setObjectName(u"show_spin_relaxation")

        self.verticalLayout_anneal_results.addWidget(self.show_spin_relaxation)

        self.show_spin_correlator_relaxation = PushButton(self.tab_anneal_results)
        self.show_spin_correlator_relaxation.setObjectName(u"show_spin_correlator_relaxation")

        self.verticalLayout_anneal_results.addWidget(self.show_spin_correlator_relaxation)

        self.tabWidget_2.addTab(self.tab_anneal_results, "")

        self.gridLayout_1.addWidget(self.tabWidget_2, 0, 1, 1, 1)

        self.save_results = PushButton(self.centralwidget)
        self.save_results.setObjectName(u"save_results")

        self.gridLayout_1.addWidget(self.save_results, 1, 0, 1, 1)

        self.load_results = PushButton(self.centralwidget)
        self.load_results.setObjectName(u"load_results")

        self.gridLayout_1.addWidget(self.load_results, 1, 1, 1, 1)

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


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Ising model", None))
        self.label_lattice.setText(QCoreApplication.translate("MainWindow", u"Type of lattice", None))
        self.lattice.setItemText(0, QCoreApplication.translate("MainWindow", u"Chain", None))
        self.lattice.setItemText(1, QCoreApplication.translate("MainWindow", u"Square", None))
        self.lattice.setItemText(2, QCoreApplication.translate("MainWindow", u"Triangular", None))
        self.lattice.setItemText(3, QCoreApplication.translate("MainWindow", u"Honeycomb", None))
        self.lattice.setItemText(4, QCoreApplication.translate("MainWindow", u"Kagome", None))
        self.lattice.setItemText(5, QCoreApplication.translate("MainWindow", u"Lieb", None))

        self.label_supercell_size.setText(QCoreApplication.translate("MainWindow", u"Supercell size", None))
        self.supercell_size.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.label_magnetization.setText(QCoreApplication.translate("MainWindow", u"Initial magnetization", None))
        self.magnetization.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_geometry), QCoreApplication.translate("MainWindow", u"Geometry", None))
        self.label_Jij_ising.setText(QCoreApplication.translate("MainWindow", u"Neighbor couplings (J1, J2, J3)", None))
        self.Jij_ising.setText(QCoreApplication.translate("MainWindow", u"1.0, 0.0, 0.0", None))
        self.label_field_profile.setText(QCoreApplication.translate("MainWindow", u"External field profile", None))
        self.field_profile.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_interactions), QCoreApplication.translate("MainWindow", u"Interactions", None))
        self.label_temp.setText(QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.temp.setText(QCoreApplication.translate("MainWindow", u"3.0", None))
        self.label_ntries.setText(QCoreApplication.translate("MainWindow", u"Number of attempts", None))
        self.ntries.setText(QCoreApplication.translate("MainWindow", u"10000", None))
        self.label_n_snapshots.setText(QCoreApplication.translate("MainWindow", u"Number of snapshots", None))
        self.n_snapshots.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_anneal_settings), QCoreApplication.translate("MainWindow", u"Anneal settings", None))
        self.show_structure.setText(QCoreApplication.translate("MainWindow", u"Show structure", None))
        self.show_structure_3d.setText(QCoreApplication.translate("MainWindow", u"Show structure 3D", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_structure), QCoreApplication.translate("MainWindow", u"Structure", None))
        self.show_spin_configuration.setText(QCoreApplication.translate("MainWindow", u"Show configuration", None))
        self.show_spin_relaxation.setText(QCoreApplication.translate("MainWindow", u"Show relaxation", None))
        self.show_spin_correlator_relaxation.setText(QCoreApplication.translate("MainWindow", u"Show correlator relaxation", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_anneal_results), QCoreApplication.translate("MainWindow", u"Results", None))
        self.save_results.setText(QCoreApplication.translate("MainWindow", u"Save Results", None))
        self.load_results.setText(QCoreApplication.translate("MainWindow", u"Load Results", None))
    # retranslateUi
