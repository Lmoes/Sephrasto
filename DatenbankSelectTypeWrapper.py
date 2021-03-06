# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:33:39 2017

@author: Aeolitus
"""
from PyQt5 import QtWidgets, QtCore
import DatenbankSelectType

class DatenbankSelectTypeWrapper(object):
    def __init__(self):
        super().__init__()
        Dialog = QtWidgets.QDialog()
        ui = DatenbankSelectType.Ui_Dialog()
        ui.setupUi(Dialog)
        
        Dialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        Dialog.show()
        ret = Dialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            if ui.buttonTalent.isChecked():
                self.entryType = "Talent"
            elif ui.buttonVorteil.isChecked():
                self.entryType = "Vorteil"
            elif ui.buttonFertigkeit.isChecked():
                self.entryType = "Fertigkeit"
            elif ui.buttonUebernatuerlich.isChecked():
                self.entryType = "Uebernatuerlich"
            elif ui.buttonManoever.isChecked():
                self.entryType = "Manoever"
            elif ui.buttonWaffeneigenschaft.isChecked():
                self.entryType = "Waffeneigenschaft"
            else:
                self.entryType = "Waffe"
        else: 
            self.entryType = None
        
        