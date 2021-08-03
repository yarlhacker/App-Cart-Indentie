from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets 
from PyQt5.QtCore import * 
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from datas import store
import re

import sys

from os import path

from PyQt5.uic import loadUiType

import sqlite3  

from source.formulaire import Cart

FORM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),'apps/app.ui'))

ligne = ""

class App(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(App,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.database = store.DataConfig()
        self.Handel_Buttons()
        self.data_()
        


    def Handel_Buttons(self):
        self.add_button.clicked.connect(self.Enregristrement)
        self.search_button.clicked.connect(self.recherche)
        self.list_perso.cellClicked.connect(self.voir)
        self.edit_button.clicked.connect(self.Modifier)
        self.save_button.clicked.connect(self.imprimer)
        self.remove_button.clicked.connect(self.supprimer)
        


    def Enregristrement(self,):
        self.windowData = Cart()
        self.windowData.show()
    

    def data_(self):
        values = self.database.recupereData()
        self.list_perso.setRowCount(0)

        for row_number, row_data in enumerate(values):
            self.list_perso.insertRow(row_number)
            for colum_number, data in enumerate(row_data):
                self.list_perso.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

    

    def recherche(self):

        nom = str(self.search_bar.text())
        if not nom :
            self.data_()
        else:
            db = sqlite3.connect(path.join(path.dirname("__file__"), "base_donnee/base.db"))
            cursor = db.cursor()
       
            commande = """ SELECT  nom from register WHERE nom =?"""
            values = cursor.execute(commande,[nom])
            
            self.list_perso.setRowCount(0)

            for row_number, row_data in enumerate(values):
                self.list_perso.insertRow(row_number)
                for colum_number, data in enumerate(row_data):
                    self.list_perso.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

    def Apercu(self,id_element):
        valeur = self.database.recupereID(id_element)

        self.immatriculation.setText(str(valeur[0]))
        self.nom.setText(str(valeur[1]))
        self.prenom.setText(str(valeur[2]))
        self.sexe.setText(str(valeur[5]))
        self.taille.setText(str(valeur[11]))
        self.date_naissance.setText(str(valeur[3]))
        self.lieu_naissance.setText(str(valeur[4]))

        image = valeur[10]
        pixmap = QPixmap()
        pixmap.loadFromData(image)
        self.profil.setPixmap(pixmap)

    def voir(self):
        ligne = self.list_perso.currentRow()
        if ligne == "":
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez selectionner une personne s'il vous plaît !")
        else :
            id_ligne = self.list_perso.item(ligne, 0).text()
            self.Apercu(id_ligne)

    def Modifier(self):
        ligne = self.list_perso.currentRow()
        if ligne == "":
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez selectionner une personne s'il vous plaît !")
        else :
            id_ligne = self.list_perso.item(ligne, 0).text()
            self.lancer_modification(id_ligne)

    def lancer_modification(self,id_element):
        self.windowData = Cart(id_element)
        self.windowData.show()

    def imprimer(self):
        dimension = self.carte_identite.frameGeometry()
        img,_ = QtWidgets.QFileDialog.getSaveFileName(self, "Enregistrer sous", filter="PNG(*.png);; JPEG(*.jpg)")
        if sys.platform == "darwin":
            if img[-3:] == "png":
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(dimension)
                screenshot.save(img, 'png')
            elif img[-3:] == "jpg":
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(dimension)
                screenshot.save(img, 'jpg')
        else:
            if img[-3:] == "png":
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.carte_identite.winId())
                screenshot.save(img, 'png')
            elif img[-3:] == "jpg":
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.carte_identite.winId())
                screenshot.save(img, 'jpg')
                QtWidgets.QMessageBox.information(self, "Succès", "Capture enregistrer avec succès.")
                self.close()
        

    def supprimer(self):
        ligne = self.list_perso.currentRow()
        id_ligne = self.list_perso.item(ligne, 0).text()
        reponse = QtWidgets.QMessageBox.question(self, "Danger", "Voulez-vous vraiment supprimer ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reponse == 16384:
            db = sqlite3.connect(path.join(path.dirname("__file__"), "base_donnee/base.db"))
            cursor = db.cursor()
            commande = """ DELETE FROM register WHERE Nom=? """
            cursor.execute(commande, (id_ligne,))
            db.commit()
            self.data_()
