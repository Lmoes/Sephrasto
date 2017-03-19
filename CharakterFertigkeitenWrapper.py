# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:33:11 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterFertigkeiten
import TalentPicker
from PyQt5 import QtWidgets, QtCore, QtGui

class FertigkeitenWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.formFert = QtWidgets.QWidget()
        self.uiFert = CharakterFertigkeiten.Ui_Form()
        self.uiFert.setupUi(self.formFert)
        header = self.uiFert.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, 1)
        header.setSectionResizeMode(1, 3)
        header.setSectionResizeMode(2, 3)
        
        self.model = QtGui.QStandardItemModel(self.uiFert.listTalente)
        self.uiFert.listTalente.setModel(self.model)
        
        #Signals
        self.uiFert.spinFW.valueChanged.connect(self.fwChanged)
        self.uiFert.tableWidget.currentItemChanged.connect(self.tableClicked)   
        self.uiFert.buttonAdd.clicked.connect(self.editTalents)
        
        self.availableFerts = []
        self.rowRef = {}
        
        #If there is an ability already, then we take it to display already
        try:
            self.currentFertName = Wolke.Char.fertigkeiten.__iter__().__next__()
        except StopIteration:
            self.currentFertName = ''
        self.loadFertigkeiten()
            
    def updateFertigkeiten(self):
        #Already implemented for the individual events
        pass
        
    def loadFertigkeiten(self):
        temp = [el for el in Wolke.DB.fertigkeiten 
                if Wolke.Char.voraussetzungenPrüfen(Wolke.DB.fertigkeiten[el].voraussetzungen)]
        if temp != self.availableFerts:
            self.availableFerts = temp
            self.uiFert.tableWidget.clear()
            
            self.uiFert.tableWidget.setRowCount(len(self.availableFerts))
            self.uiFert.tableWidget.setColumnCount(3)
            self.uiFert.tableWidget.verticalHeader().setVisible(False)
            item = QtWidgets.QTableWidgetItem()
            item.setText("Bezeichnung")
            self.uiFert.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("FW")
            self.uiFert.tableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText("Talente")
            self.uiFert.tableWidget.setHorizontalHeaderItem(2, item)
    
            count = 0
            
            #Remove Abilities for which the conditions are not met
            for el in Wolke.Char.fertigkeiten:
                if el not in self.availableFerts:
                    Wolke.Char.fertigkeiten.pop(el,None)
            
            for el in self.availableFerts:
                #Add abilities that werent there before
                if el not in Wolke.Char.fertigkeiten:
                    Wolke.Char.fertigkeiten.update({el: Wolke.DB.fertigkeiten[el].__deepcopy__()})
                    Wolke.Char.fertigkeiten[el].wert = 0
                    Wolke.Char.fertigkeiten[el].aktualisieren()
                self.uiFert.tableWidget.setItem(count, 0, QtWidgets.QTableWidgetItem(Wolke.Char.fertigkeiten[el].name))
                self.uiFert.tableWidget.setItem(count,1,QtWidgets.QTableWidgetItem(str(Wolke.Char.fertigkeiten[el].wert)))
                self.uiFert.tableWidget.setItem(count,2,QtWidgets.QTableWidgetItem(str(len(Wolke.Char.fertigkeiten[el].gekaufteTalente))))
                self.rowRef.update({Wolke.Char.fertigkeiten[el].name: count})
                count += 1
            self.uiFert.tableWidget.cellClicked.connect(self.tableClicked) 
        self.updateInfo()
        self.updateTalents()
            
    def tableClicked(self,new,old):
        self.currentFertName = new.text()
        self.updateInfo()
        
    def fwChanged(self):
        if self.currentFertName != "":
            Wolke.Char.fertigkeiten[self.currentFertName].wert = self.uiFert.spinFW.value()
            Wolke.Char.fertigkeiten[self.currentFertName].aktualisieren()
            self.uiFert.spinPW.setValue(Wolke.Char.fertigkeiten[self.currentFertName].probenwert)
            self.uiFert.spinPWT.setValue(Wolke.Char.fertigkeiten[self.currentFertName].probenwertTalent)
            self.modified.emit()
            self.uiFert.tableWidget.setItem(self.rowRef[self.currentFertName],1,QtWidgets.QTableWidgetItem(str(Wolke.Char.fertigkeiten[self.currentFertName].wert)))
        
    def updateInfo(self):
        if self.currentFertName != "":
            fert = Wolke.Char.fertigkeiten[self.currentFertName]
            fert.aktualisieren()
            self.uiFert.labelFertigkeit.setText(self.currentFertName)
            self.uiFert.labelAttribute.setText(fert.attribute[0] + "/" 
                                               + fert.attribute[1] + "/" 
                                               + fert.attribute[2])
            self.uiFert.spinSF.setValue(fert.steigerungsfaktor)
            self.uiFert.spinBasis.setValue(fert.basiswert)
            self.uiFert.spinFW.setValue(fert.wert)
            self.uiFert.spinFW.setMaximum(fert.maxWert)
            self.uiFert.spinPW.setValue(fert.probenwert)
            self.uiFert.spinPWT.setValue(fert.probenwertTalent)
            self.uiFert.plainText.setPlainText(fert.text)
            self.updateTalents()
        
    def updateTalents(self):
        if self.currentFertName != "":
            self.model.clear()
            for el in Wolke.Char.fertigkeiten[self.currentFertName].gekaufteTalente:
                item = QtGui.QStandardItem(el)
                item.setEditable(False)
                self.model.appendRow(item)
        
    def editTalents(self):
        if self.currentFertName != "":
            tal = TalentPicker.TalentPicker(self.currentFertName, False)
            if tal.gekaufteTalente is not None:
                #Wolke.Char.fertigkeiten[self.currentFertName].gekaufteTalente = tal.gekaufteTalente
                self.modified.emit()
                self.updateTalents()
                #TODO: Fill other talents with the same ferts as well!
                self.uiFert.tableWidget.setItem(self.rowRef[self.currentFertName],2,QtWidgets.QTableWidgetItem(str(len(Wolke.Char.fertigkeiten[self.currentFertName].gekaufteTalente))))