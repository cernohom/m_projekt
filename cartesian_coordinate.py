import sys
import typing
from PyQt5 import QtGui
import numpy as np
import sympy as sp
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPathItem, QGraphicsTextItem, QPushButton, QLineEdit, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QPen, QPainterPath, QBrush, QColor

class MathGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.view = QGraphicsView(self)
        self.setCentralWidget(self.view)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        # Hodnoty pro graf

        self.pole_grafu = 50
        """
        #pokud bych chtel podle velikosti obrazovky nutne?
        self.screen = app.primaryScreen()
        self.size = self.screen.size()
        self.sirka_grafu =  self.size.width()
        self.vyska_grafu = self.size.height()
        """

        self.sirka_grafu = 1200
        self.vyska_grafu = 800
        self.kraj_x = 100
        self.kraj_y = 100
        self.velikost_tlacitka = 50
        self.sila_priblizeni = 50
        self.vyrazy = []

        # vypocitani hodnot aby se nepocitaly pokazde
        self.stred_grafu_x = self.sirka_grafu/2 #prostredek grafu na ose x
        self.stred_grafu_y = self.vyska_grafu/2 #prostredek grafu na ose y

        self.setWindowTitle('Grafická kalkulačka')
        self.setGeometry(100, 100, self.sirka_grafu + 200,self.vyska_grafu + 200)
        
        self.UiComponents()
        self.vykresliGraf()

    def UiComponents(self):

        # Tlacitko na priblizeni
        priblizeni = QPushButton("PyQt button", self)
        priblizeni.setText("+")
        priblizeni.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y, self.velikost_tlacitka, self.velikost_tlacitka)
        priblizeni.clicked.connect(self.priblizeni) #Co se stane kdyz zmacknu tlacitko

        # Tlacitko na oddaleni
        oddaleni = QPushButton("PyQt button", self)
        oddaleni.setText("-")
        oddaleni.setGeometry(self.sirka_grafu + self.kraj_x, self.kraj_y , self.velikost_tlacitka, self.velikost_tlacitka)
        oddaleni.clicked.connect(self.oddaleni) # Co se stane kdyz zmacknu tlacitko
            
        self.textove_pole = QLineEdit(self)
        self.textove_pole.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + 100, 140, 30)

        # Tlacitko na priblizeni
        self.potvrzeni = QPushButton("PyQt button", self)
        self.potvrzeni.setText("Vyrazy")
        self.potvrzeni.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + 300, 150, 300)
        self.potvrzeni.clicked.connect(self.zmacknutoPotvrzeni) #Co se stane kdyz zmacknu tlacitko
        
        self.seznam_vyrazu = QLabel()
        self.seznam_vyrazu.setText("seznam vyrazu")
        self.seznam_vyrazu.setAutoFillBackground(True)
        self.seznam_vyrazu.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + 150, 140, 30)

    def keyPressEvent(self, event) -> None:
        print("AH")
        if (event.key() == 16777220) or (event.key() == 43):
            self.zmacknutoPotvrzeni
        
    # Co se stane kdyz zmacknu priblizeni
    def priblizeni(self):
        self.pole_grafu = self.pole_grafu * 2
        self.vykresliGraf()
        self.vykresliKrivkuGrafu(self.vyrazy)
        
    # Co se stane kdyz zmacknu priblizeni
    def oddaleni(self):
        self.pole_grafu = self.pole_grafu / 2
        self.vykresliGraf()
        self.vykresliKrivkuGrafu(self.vyrazy)

    def zmacknutoPotvrzeni(self):
            self.vyraz = self.textove_pole.text()
            self.vyrazy.append(self.vyraz)
            self.vykresliKrivkuGrafu(self.vyrazy)

            seznam_vyrazu_text = ""
            for i in self.vyrazy:
                seznam_vyrazu_text += i
                seznam_vyrazu_text += "\n"
            self.potvrzeni.setText(seznam_vyrazu_text)
            print(seznam_vyrazu_text)
    
    def vykresliGraf(self):
        # Vytvoreni pera
        pero = QPen()
        pero.setColor(Qt.red)
        pero.setWidth(2)

        # Vytvareni tras protoze jsou ctyri ruzne barvy
        trasa_mrizi = QPainterPath()
        trasa_pozadi = QPainterPath()
        trasa_os = QPainterPath()

        self.vykresliPozadi(trasa_pozadi, pero)
        self.vykresliKartezskouSoustavu(trasa_mrizi, pero)
        self.vykresliOsy(trasa_os,pero)
    
    def vykresliKrivkuGrafu(self, vyrazy : list):
        pero = QPen()
        trasa = QPainterPath()


        pero.setWidth(2)
        pero.setColor(Qt.red)

        #draw the graph
        #TODO not manual input of the expression
        print(vyrazy)
        x_values = np.arange(-(self.stred_grafu_x)/self.pole_grafu, self.stred_grafu_x/self.pole_grafu, 1/100)
        for vyraz in vyrazy:
            try:
                y_values = [eval(vyraz) for x in x_values]
                #vytvor path pro vyraz
                for i in range(len(x_values)):
                    x = self.kraj_x + self.stred_grafu_x + (x_values[i]*self.pole_grafu) # vzdalenost od kraje + pulka grafu jelikoz hodnoty jsou od - do plusu ale tady pracuji jen v plusu + hodnota
                    if (y_values[i] * self.pole_grafu) > self.stred_grafu_y and i != 0: # pokud je hodnota y vetsi nez vyska grafu a neni to prvni cislo tak cara na kraj grafu nahoru a posun pero na hodnotu x a na kraj grafu nahore
                        trasa.lineTo(x, self.kraj_y)
                        trasa.moveTo(x, self.kraj_y)
                    elif (y_values[i] * self.pole_grafu) < -self.stred_grafu_y and i != 0: # pokud je mensi na x a kraj grafu dole posun na x a na graf dole
                        trasa.moveTo(x, self.kraj_y + self.vyska_grafu)
                    else:       
                        y = self.kraj_y + self.stred_grafu_y - (y_values[i] * self.pole_grafu) # vytvor y od kraje grafu pulka + pul
                        if i == 0: #pokud prvni posun na xy pozici
                            trasa.moveTo(x, y)
                        else:
                            trasa.lineTo(x, y) #pokud dalsi caru na aktualni xy pozici
            
                graph_item = QGraphicsPathItem(trasa)
                graph_item.setPen(pero)
                self.scene.addItem(graph_item)
            except Exception as e1:
                vysledek = eval(vyraz)
                print(vysledek)
                self.vyrazy.pop(vyraz)
                self.vyrazy.append(vyraz + " = " + vysledek)
            except Exception as e2:
                print("ahoj")



    def vykresliKartezskouSoustavu(self, trasa, pero):
        pero.setColor(Qt.black)
        pero.setWidth(1)
        # Vytvoreni hodnot na ose x a samotnych vertikalnich os do prvni pulky
        for i  in np.arange (self.stred_grafu_x, self.sirka_grafu, 50) :
            x_label_text = (i - self.stred_grafu_x) / self.pole_grafu # Co bude na danem popisku
            self.pozice_pera_x = self.kraj_x + i #Pozice pera na ose x
        
            if -1 < x_label_text < 1: # Pokud je cislo mensi nez 1 zvetsim pocet cisel za desetinou carkou
                pocet_zaokrouhlenych_mist = 3
            else: # Jinak pouze jedno cislo za desetinou carkou
                pocet_zaokrouhlenych_mist = 1
            
            x_label = QGraphicsTextItem(str(round(x_label_text, pocet_zaokrouhlenych_mist))) # Zaokrouhleni a nasledne vytvoreni popisku osy
            x_label.setPos(self.pozice_pera_x, self.kraj_y + self.stred_grafu_y)
            self.scene.addItem(x_label)

            # Prvni caru zacni v levem hornim rohu a udelej caru dolu
            if i == 0:
                trasa.moveTo(self.kraj_x,self.kraj_y)
                trasa.lineTo(self.kraj_x, self.vyska_grafu + self.kraj_y)
            
            # Presun nahoru posun o jedno policko a udelej caru dolu
            else:
                trasa.moveTo(self.pozice_pera_x, self.kraj_y)
                trasa.lineTo(self.pozice_pera_x, self.vyska_grafu + self.kraj_y)
        
        pocet_zaokrouhlenych_mist = 1

        # Vytvoreni hodnot na ose y a samotnych vertikalnich os
        for i  in reversed(np.arange (self.kraj_x - 50, self.stred_grafu_x, 50)) : # serazena cisla od  
            x_label_text = (i - self.stred_grafu_x) / self.pole_grafu
            if -1 < x_label_text < 1:
                pocet_zaokrouhlenych_mist = 3
            else:
                pocet_zaokrouhlenych_mist = 1   
            x_label = QGraphicsTextItem(str (round (x_label_text, pocet_zaokrouhlenych_mist)))
            x_label.setPos(self.kraj_x + i, self.kraj_y + self.stred_grafu_y)
            self.scene.addItem(x_label)
            # Zacni ve stredu a udelej caru dolu
            if i == 0:
                trasa.moveTo(self.kraj_x,self.kraj_y)
                trasa.lineTo(self.kraj_x, self.vyska_grafu + self.kraj_y)
            # Presun nahoru do noveho pole a udelej caru dolu
            else:
                self.graph_x_pen = self.kraj_x + i
                trasa.moveTo(self.graph_x_pen, self.kraj_y)
                trasa.lineTo(self.graph_x_pen, self.vyska_grafu + self.kraj_y)    

        # Horizontalni cary
        for i  in np.arange (self.stred_grafu_y + self.kraj_y - 50, self.vyska_grafu, 50) :
            y_label_text = (((i - self.stred_grafu_y) / self.pole_grafu) * - 1)
            if -1 < y_label_text < 1:
                round(y_label_text, 3)
            else:
                round(y_label_text, 1)
            y_label = QGraphicsTextItem(str(y_label_text))
            y_label.setPos(self.kraj_x + self.stred_grafu_x, self.kraj_y + i)
            self.scene.addItem(y_label)
            if i == 0:
                trasa.moveTo(self.kraj_x,self.kraj_y)
                trasa.lineTo(self.sirka_grafu + self.kraj_x, self.kraj_y)
            else:
                self.graph_y_pen = self.kraj_y + i
                trasa.moveTo(self.kraj_x, self.graph_y_pen)
                trasa.lineTo(self.sirka_grafu + self.kraj_x, self.graph_y_pen)

        for i  in reversed(np.arange (self.kraj_y - 50, self.stred_grafu_y, 50)) :
            y_label_text = (i - self.stred_grafu_y) / self.pole_grafu * - 1
            if -1 < y_label_text < 1:
                round(y_label_text, 3)
            else:
                round(y_label_text, 1)
            y_label = QGraphicsTextItem(str (round (y_label_text, pocet_zaokrouhlenych_mist)))
            y_label.setPos(self.kraj_x + self.stred_grafu_x, self.kraj_y + i)
            self.scene.addItem(y_label)
            if i == 0:
                trasa.moveTo(self.kraj_x,self.kraj_y)
                trasa.lineTo(self.sirka_grafu + self.kraj_x, self.kraj_y)
            else:
                self.graph_y_pen = self.kraj_y + i
                trasa.moveTo(self.kraj_x, self.graph_y_pen)
                trasa.lineTo(self.sirka_grafu + self.kraj_x, self.graph_y_pen)
        
        # Create a QGraphicsPathItem to display the graph
        graph_item = QGraphicsPathItem(trasa)
        graph_item.setPen(pero)
        self.scene.addItem(graph_item)
        
    def vykresliPozadi(self, trasa, pero):
        trasa.addRect(self.kraj_x, self.kraj_y, self.sirka_grafu, self.vyska_grafu)
        graph_item = QGraphicsPathItem(trasa)
        graph_item.setPen(pero)
        graph_item.setBrush(QBrush(QColor(Qt.white)))
        self.scene.addItem(graph_item)

    def vykresliOsy(self, trasa, pero):

        pero.setWidth(2)
        pero.setColor(Qt.darkBlue)
        trasa.moveTo(self.kraj_x + self.stred_grafu_x, self.kraj_y)
        trasa.lineTo(self.kraj_x + self.stred_grafu_x, self.kraj_y + self.vyska_grafu)
        trasa.moveTo(self.kraj_x, self.kraj_y + self.stred_grafu_y)
        trasa.lineTo(self.kraj_x + self.sirka_grafu,  self.kraj_y + self.stred_grafu_y)
        
        graph_item = QGraphicsPathItem(trasa)
        graph_item.setPen(pero)
        self.scene.addItem(graph_item)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MathGraphApp()
    ex.show()
    sys.exit(app.exec_())
