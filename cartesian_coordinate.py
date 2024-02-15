import sys
import typing
from PyQt5 import QtGui
import numpy as np
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sympy as sp

def safe_eval(expr):
    try:
        return eval(expr)
    except ValueError as e:
        # Handle the exception or return a default value
        return None

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


        """
        #pokud bych chtel podle velikosti obrazovky nutne?
        self.screen = app.primaryScreen()
        self.size = self.screen.size()
        self.sirka_grafu =  self.size.width()
        self.vyska_grafu = self.size.height()
        """
        self.pole_grafu = 50
        self.sirka_grafu = 1200
        self.vyska_grafu = 800
        self.kraj_x = 100
        self.kraj_y = 100
        self.velikost_tlacitka = 50
        self.sila_priblizeni = 50
        self.vyrazy = []
        self.vyrazy_jednoduche = []
        self.vyrazy_barvy = {}
        self.font = QFont("Arial", 15)
        self.priblizeni_pocet = 0

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
        priblizeni.setFont(self.font)

        # Tlacitko na oddaleni
        oddaleni = QPushButton("PyQt button", self)
        oddaleni.setText("-")
        oddaleni.setGeometry(self.sirka_grafu + self.kraj_x, self.kraj_y, self.velikost_tlacitka, self.velikost_tlacitka)
        oddaleni.clicked.connect(self.oddaleni) # Co se stane kdyz zmacknu tlacitko
        oddaleni.setFont(self.font)
        
        #Textove pole    
        self.textove_pole = QLineEdit(self)
        self.textove_pole.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + 3 * self.velikost_tlacitka, self.velikost_tlacitka * 2, self.velikost_tlacitka)
        self.textove_pole.setFont(self.font)
        
        # Pole na vypisovani
        self.potvrzeni = QPushButton("PyQt button", self)
        self.potvrzeni.setText("Vyrazy")
        self.potvrzeni.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + self.velikost_tlacitka * 4, self.velikost_tlacitka*2, self.velikost_tlacitka*6)
        self.potvrzeni.clicked.connect(lambda: self.zmacknutoPotvrzeni(Qt.red))#Co se stane kdyz zmacknu tlacitko
        self.potvrzeni.setFont(QFont("Arial", 12))
        self.potvrzeni.setStyleSheet("text-align:top")

        #tlacitko na vymazani historie
        historie = QPushButton("PyQt button", self)
        historie.setText("AC")
        historie.setGeometry(self.sirka_grafu + self.kraj_x,  self.kraj_y + self.velikost_tlacitka * 2, self.velikost_tlacitka, self.velikost_tlacitka)
        historie.clicked.connect(self.zmacknutoAC) #Co se stane kdyz zmacknu tlacitko
        historie.setFont(self.font)

        # Tlacitko na zelenou
        zelena = QPushButton("PyQt button", self)
        zelena.setText("=")
        zelena.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + self.velikost_tlacitka, self.velikost_tlacitka, self.velikost_tlacitka)
        zelena.clicked.connect(lambda: self.zmacknutoPotvrzeni(Qt.green)) # Co se stane kdyz zmacknu tlacitko
        zelena.setFont(self.font)
        zelena.setStyleSheet("background-color: green")        

        # Tlacitko na zlutou
        zluta = QPushButton("PyQt button", self)
        zluta.setText("=")
        zluta.setGeometry(self.sirka_grafu + self.kraj_x, self.kraj_y + self.velikost_tlacitka, self.velikost_tlacitka, self.velikost_tlacitka)
        zluta.clicked.connect(lambda: self.zmacknutoPotvrzeni(Qt.yellow)) # Co se stane kdyz zmacknu tlacitko
        zluta.setFont(self.font)
        zluta.setStyleSheet("background-color: yellow")

        cyan = QPushButton("PyQt button", self)
        cyan.setText("=")
        cyan.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka,  self.kraj_y + self.velikost_tlacitka * 2, self.velikost_tlacitka, self.velikost_tlacitka)
        cyan.clicked.connect(lambda: self.zmacknutoPotvrzeni(Qt.cyan)) # Co se stane kdyz zmacknu tlacitko
        cyan.setFont(self.font)
        cyan.setStyleSheet("background-color: cyan")
    """
    zjistit jak dat enter
    def keyPressEvent(self, event) -> None:
        if event.key() == (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter): 
            self.zmacknutoPotvrzeni
    """

    # Co se stane kdyz zmacknu priblizeni
    def priblizeni(self):
        if self.priblizeni_pocet <= 4:
            self.pole_grafu = self.pole_grafu * 2
            self.vykresliGraf()
            self.vyhodnotVyrazy(self.vyrazy)
            self.priblizeni_pocet += 1
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Více nelze přiblížit")
            msg.setInformativeText('Je to pro bezpečnost vašeho PC')
            msg.setWindowTitle("Chyba")
            msg.exec_()
    # Co se stane kdyz zmacknu priblizeni
    def oddaleni(self):
        if self.priblizeni_pocet >= -4:
            self.pole_grafu = self.pole_grafu / 2
            self.vykresliGraf()
            self.vyhodnotVyrazy(self.vyrazy)
            self.priblizeni_pocet -= 1
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Více nelze oddálit")
            msg.setInformativeText('Je to pro bezpečnost vašeho PC')
            msg.setWindowTitle("Chyba")
            msg.exec_()

    def zmacknutoAC(self):
        self.vyrazy = []
        self.potvrzeni.setText("vymazani")
        self.vyhodnotVyrazy(self.vyrazy)

    def zmacknutoPotvrzeni(self, barva):
            self.vyraz = self.textove_pole.text()
            self.vyrazy.append(self.vyraz)
            if self.obsahujeX(self.vyraz):
                self.vyrazy_barvy[self.vyraz] = barva
            self.vyhodnotVyrazy(self.vyrazy)

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
    
    def vyhodnotVyrazy(self, vyrazy : list):
        if not vyrazy:
            self.vykresliGraf()
        else:
            for vyraz in vyrazy:
                
                if self.obsahujeX(vyraz):
                    self.barva = self.vyrazy_barvy[vyraz]
                    try:
                        self.vykresliKrivkuGrafu(vyraz, self.barva)
                        self.potvrzeni.setText(self.listNaTextOdstavce(self.vyrazy))
                    except:
                        try:
                            novy_vyraz = "math." + str(vyraz)
                            self.vykresliKrivkuGrafu(novy_vyraz, self.barva)
                            self.potvrzeni.setText(self.listNaTextOdstavce(self.vyrazy))
                        except:
                            self.vyrazy.remove(vyraz)
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Critical)
                            msg.setText("Nelze vyhodnotit vloženou hodnotu")
                            msg.setWindowTitle("Chyba")
                            msg.exec_()
                else:
                    if vyraz not in self.vyrazy_jednoduche:      
                        try:
                            vysledek = eval(vyraz)
                            self.vyrazy.remove(vyraz)
                            vysledek  = round(vysledek, 3)
                            self.novy_vyraz = str(vyraz) + " = " + str(vysledek)
                            self.vyrazy.append(self.novy_vyraz)
                            self.vyrazy_jednoduche.append(self.novy_vyraz)
                            self.potvrzeni.setText(self.listNaTextOdstavce(self.vyrazy))
                        except:
                                try:
                                    novy_vyraz = "math." + str(vyraz)
                                    vysledek = eval(novy_vyraz)
                                    vysledek  = round(vysledek, 3)
                                    self.vyrazy.remove(vyraz)
                                    self.novy_vyraz = str(vyraz) + " = " + str(vysledek)
                                    self.vyrazy.append(self.novy_vyraz)
                                    self.vyrazy_jednoduche.append(self.novy_vyraz)
                                    self.potvrzeni.setText(self.listNaTextOdstavce(self.vyrazy))
                                except:
                                    self.vyrazy.remove(vyraz)
                                    msg = QMessageBox()
                                    msg.setIcon(QMessageBox.Critical)
                                    msg.setText("Nelze vyhodnotit vloženou hodnotu")
                                    msg.setWindowTitle("Chyba")
                                    msg.exec_()
    
    def listNaTextOdstavce(self, list :list) -> str:
            string = ""
            for i in list:
                string += i
                string += "\n"
            return string
    
    def jeVGrafu (self, pozice_y):
        if self.kraj_y < pozice_y < (self.kraj_y + self.vyska_grafu):
            return True
        else:
            return False

    def vykresliKrivkuGrafu(self, vyraz, barva) -> None:
        pero = QPen()
        trasa = QPainterPath()
        malovat_priste = False
        predchozi_pozice_y = None
        predchozi_v_grafu = False
        predchozi_pozice_x = self.kraj_x




        pero.setWidth(2)
        pero.setColor(barva)

        def checkifcontinus(func,x,symbol):
            return (sp.limit(func, symbol, x).is_real)

        x_values = np.arange(-(self.stred_grafu_x)/self.pole_grafu, self.stred_grafu_x/self.pole_grafu, 1/100)
        """!!! Je lepší použít tuto funkci než eval(), umožňuje mnohem více funkcí
            Teď se tam přidává None, pokud nemá funkce v daném bodě definiční obor"""
        f = sp.lambdify(sp.Symbol("x"), vyraz, "math") 
        y_values = []
        for a in x_values:
            try:
                y_values.append(sp.N(f(a)))
            except ValueError:
                # handle division by zero error
                # leave empty for now
                y_values.append(None)
      

        """!!! Zde je přidána podmínka pro ten None, že se to v tom případě nevykresluje, pouze se to pero posouvá po ose x
            Dále byly provedené menší úpravy, které upravují některé nedokreslování, či naopak nevyžádané čáry navíc"""
        #vytvor path pro vyraz
        #pro kazde číslo na ose
        for i in range(len(x_values)):
            # převeď normální osu na velikost grafu (vzdálenost od kraje + pulka grafu jelikoz hodnoty jsou od minus do plusu ale grafove hodnoty jsou jen od nuly do plusu + hodnota
            pozice_x = self.kraj_x + self.stred_grafu_x + (x_values[i]*self.pole_grafu)
            # pokud hodnota y není (dělení nulou) přesuň pero
            
            pozice_y = self.kraj_y + self.stred_grafu_y - (y_values[i] * self.pole_grafu) # vytvor y od kraje grafu pulka + pul
            
            if self.jeVGrafu(pozice_y):
                if predchozi_pozice_y is None:
                    trasa.moveTo(pozice_x, pozice_y)
                elif predchozi_pozice_y < self.kraj_y:
                    trasa.moveTo(pozice_x, self.kraj_y)
                    trasa.lineTo(pozice_x, pozice_y)
                elif predchozi_pozice_y > self.kraj_y + self.vyska_grafu:
                    trasa.moveTo(pozice_x, self.kraj_y + self.vyska_grafu)
                    trasa.lineTo(pozice_x, pozice_y)
                else:
                    trasa.lineTo(pozice_x, pozice_y)
                predchozi_v_grafu = True
            elif predchozi_v_grafu:
                if pozice_y < self.kraj_y:
                    trasa.lineTo(pozice_x, self.kraj_y)
                elif pozice_y > self.kraj_y + self.vyska_grafu:
                    trasa.lineTo(pozice_x, self.kraj_y + self.vyska_grafu)
                predchozi_v_grafu = False
            else:
                predchozi_v_grafu = False
            predchozi_pozice_y = pozice_y

            """
            # pokud ma priste malovat
            if malovat_priste is True:
                print("sulin")
                # pokud presahuje nahore udelej caru nahoru
                if pozice_y < self.kraj_y:
                    trasa.lineTo(pozice_x, self.kraj_y)
                    malovat_priste = False
                # pokud presahuje dole udelej caru dolu
                elif pozice_y > self.kraj_y + self.vyska_grafu:
                    trasa.lineTo(pozice_x, self.kraj_y + self.vyska_grafu)
                    malovat_priste = False
                else:
                    trasa.lineTo(pozice_x, pozice_y)
            else:
                # jestli funkce nebyla predtim presun na novy bod
                if predchozi_pozice_y is None:
                    trasa.moveTo(pozice_x, pozice_y)
                # jestli byla funkce nad grafem presun na predchozi horni kraj a udelej z nej caru
                elif predchozi_pozice_y < self.kraj_y:
                    trasa.moveTo(predchozi_pozice_x, self.kraj_y)
                    malovat_priste = True
                # pokud presahovala dole presun na predchozi spodni kraj a udelej z nej caru
                elif predchozi_pozice_y > self.kraj_y + self.vyska_grafu:
                    trasa.moveTo(predchozi_pozice_x, self.kraj_y + self.vyska_grafu)
                    malovat_priste = True
                else:
                    print("cowboy")
                    trasa.lineTo(pozice_x, pozice_y)
                    
            predchozi_pozice_y = pozice_y
            predchozi_pozice_x = pozice_x
            """
        
        
        graph_item = QGraphicsPathItem(trasa)
        graph_item.setPen(pero)
        self.scene.addItem(graph_item)

    def obsahujeX(self, vyraz) -> bool:
        for element in vyraz:
            if element == "x":
                return True
        return False
    
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
