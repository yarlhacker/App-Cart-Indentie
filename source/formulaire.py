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

FORM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),'apps/formulaire.ui'))

photo = {1 : ""}
ligne = ""

class Cart(QMainWindow,FORM_CLASS):
    def __init__(self,id_user=-1):
        super().__init__()
        QMainWindow.__init__(self)
        self.id_user = id_user
        self.setupUi(self)
        self.database_ = store.DataConfig()
        self.group_button()
        self.update()

    def update(self):
        if self.id_user != -1 :

            valeur = self.database_.recupereID(self.id_user)

            if valeur != None:
                date_string = valeur[3]
                date_list = [int(i) for i in re.findall(r"-?\d+\.?\d*", date_string)]
                self.nom.setText(str(valeur[1]).title())
                self.prenom.setText(str(valeur[2]).title())
                sexe =str (valeur[5])
                self.taille.setText(str(valeur[11]).title())
                self.date_naissance.setDate(QtCore.QDate(date_list[2], date_list[1], date_list[0]))
                self.lieu_naissance.setText(str(valeur[4]).title())
                self.domicile.setText(str(valeur[6]).title())
                self.profession.setText(str(valeur[11]).title())
                self.nationalite.setText(str(valeur[7]).title())
                self.pere.setText(str(valeur[8]).title())
                self.mere.setText(str(valeur[9]).title())
                image = valeur[10]
                pixmap = QPixmap()
                pixmap.loadFromData(image)
                self.photo.setPixmap(pixmap)

                if sexe == 'M':
                    self.homme.setChecked(True)
                    self.femme.setChecked(False)
                else:
                    self.homme.setChecked(False)
                    self.femme.setChecked(True)

                
        

    def group_button(self):   
        self.valider.clicked.connect(self.inscription)
        self.photo_profil.clicked.connect(self.choix_photo)

    
    def choix_photo(self):

        nom_photo = QFileDialog.getOpenFileName(self, "Choisir photo", "c://", "images (*.png *.jpg *.jpeg *.gif)")
        photo[1] = nom_photo[0]
        self.photo.setPixmap(QPixmap(photo[1]))
        self.photo.setScaledContents(True)



    def inscription(self):
        nom = self.nom.text()
        prenom = self.prenom.text()
        sexe = self.homme.isChecked()
        date_naissance = self.date_naissance.text()
        lieu_naissance =  self.lieu_naissance.text()
        taille = self.taille.text()
        domicile = self.domicile.text()
        profession = self.profession.text()
        nationalite = self.nationalite.text()
        pere = self.pere.text()
        mere = self.mere.text()
        if sexe:
            genre = "M"
        else:
            genre = "F"
        
        # db = sqlite3.connect(path.join(path.dirname("__file__"), "base_donnee/base.db"))
        # cursor = db.cursor()
        image = open(photo[1], "rb")

        if self.id_user != -1 :

            liste = (nom,prenom,date_naissance,lieu_naissance, sexe,domicile,nationalite,pere,mere, sqlite3.Binary(image.read()),taille, profession , nom)
            self.database_.modifieData(liste)
            # commande = """ UPDATE register SET Nom=?, Prenom=?, Date_de_naissance=?, Lieu_de_naissance=?, Genre=?, Domicile=?,Nationalite=?, Nom_pere=?, Nom_mere=?,  Photo=? , taille=? , profession=?   WHERE Nom=? """
            # cursor.execute(commande, liste)
            # db.commit()

            QtWidgets.QMessageBox.information(self, "Succès", "Modification effectué avec succès")
            self.close()

        else:
            liste = (nom,prenom,date_naissance,lieu_naissance, sexe,domicile,nationalite,pere,mere, sqlite3.Binary(image.read()),taille, profession)

            command = """ INSERT INTO register (Nom,Prenom,Date_de_naissance,Lieu_de_naissance,Genre,Domicile, Nationalite,Nom_pere,Nom_mere,Photo,taille,profession) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""

            cursor.execute(command,liste)
            db.commit()
            QMessageBox.information(self, "Succès", "Enregistrement effectué")
            self.close()

    