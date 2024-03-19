import sys
import numpy as np
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPen, QPainterPath, QBrush, QColor
import sympy as sp
import textwrap

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
        self.barva_pozadi = Qt.GlobalColor.white
        self.barva_mrizi = Qt.GlobalColor.black
        self.darkmode = False

        # vypocitani hodnot aby se nepocitaly pokazde
        self.stred_grafu_x = self.sirka_grafu/2 #prostredek grafu na ose x
        self.stred_grafu_y = self.vyska_grafu/2 #prostredek grafu na ose y


        self.setWindowTitle('Grafická kalkulačka')
        self.setGeometry(100, 100, self.sirka_grafu + 200,self.vyska_grafu + 200)
        
        self.UiComponents()
        self.vykresliKartezskouSoustavu()

    def UiComponents(self):
        self.vytvorTlacitko(self, "MODE", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y - self.velikost_tlacitka, self.velikost_tlacitka*2, self.velikost_tlacitka, self.changeMode, self.font, "")
        #tlacitko plus
        self.vytvorTlacitko(self, "+", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y, self.velikost_tlacitka, self.velikost_tlacitka, self.priblizeni, self.font, "")
        #tlacitko minus
        self.vytvorTlacitko(self, "-", self.sirka_grafu + self.kraj_x, self.kraj_y, self.velikost_tlacitka, self.velikost_tlacitka, self.oddaleni, self.font, "")
        #tlacitko = cervene
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka,  self.kraj_y + self.velikost_tlacitka * 4, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.red), self.font, "background-color: red")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x,  self.kraj_y + self.velikost_tlacitka * 4, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.darkRed), self.font, "background-color: darkRed")
        # tlacitko = zelene
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x , self.kraj_y + self.velikost_tlacitka * 3, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.darkGreen), self.font, "background-color: darkGreen")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + self.velikost_tlacitka * 3, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.green), self.font, "background-color: green")
        # tlaciko = zlute
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + self.velikost_tlacitka, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.magenta), self.font, "background-color: magenta")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x, self.kraj_y + self.velikost_tlacitka, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.darkMagenta), self.font, "background-color: darkMagenta")
        # tlacitko = cyan a darkCyan
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka,  self.kraj_y + self.velikost_tlacitka * 2, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.cyan), self.font, "background-color: cyan")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x ,  self.kraj_y + self.velikost_tlacitka * 2, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.darkCyan), self.font, "background-color: darkCyan")
        # Pole na vypisovani
        self.multiTlacitko = QPushButton("PyQt button", self)
        self.multiTlacitko.setText("Po zmáčknutí\nse vše smaže")
        self.multiTlacitko.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + self.velikost_tlacitka * 6, self.velikost_tlacitka*2, self.velikost_tlacitka*6)
        self.multiTlacitko.clicked.connect(self.smazani)#Co se stane kdyz zmacknu tlacitko
        self.multiTlacitko.setFont(QFont("Arial", 11))
        self.multiTlacitko.setStyleSheet("text-align:top")
        #Textove pole    
        self.textove_pole = QLineEdit(self)
        self.textove_pole.setGeometry(self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + self.velikost_tlacitka * 5, self.velikost_tlacitka * 2, self.velikost_tlacitka)
        self.textove_pole.setFont(self.font)
    
    def vytvorTlacitko(self, tlacitko, text : str, ax : int, ay: int, aw : int, ah : int, funkce, font, styl):
        tlacitko = QPushButton("Pyqt button", self)
        tlacitko.setText(text)
        tlacitko.setGeometry(ax, ay, aw, ah)
        tlacitko.clicked.connect(funkce)
        tlacitko.setFont(font)
        tlacitko.setStyleSheet(styl)
        return tlacitko
    
    def changeMode(self) -> None:
        if self.darkmode == True:
            self.barva_pozadi = Qt.GlobalColor.white
            self.barva_mrizi = Qt.GlobalColor.black
            self.darkmode = False
        else:
            self.barva_pozadi = Qt.GlobalColor.black
            self.barva_mrizi = Qt.GlobalColor.white
            self.darkmode = True
        self.vyhodnotVyrazy(self.vyrazy)

    # Co se stane kdyz zmacknu priblizeni
    def priblizeni(self):
        if self.priblizeni_pocet <= 4:
            self.pole_grafu = self.pole_grafu * 2
            self.vykresliKartezskouSoustavu()
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
            self.vykresliKartezskouSoustavu()
            self.vyhodnotVyrazy(self.vyrazy)
            self.priblizeni_pocet -= 1
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Více nelze oddálit")
            msg.setInformativeText('Je to pro bezpečnost vašeho PC')
            msg.setWindowTitle("Chyba")
            msg.exec_()

    def smazani(self):
        self.vyrazy = []
        self.multiTlacitko.setText("Vymazání")
        self.vyhodnotVyrazy(self.vyrazy)

    def potvrzeni(self, barva):
            self.vyraz = self.textove_pole.text()
            self.vyrazy.append(self.vyraz)
            if self.obsahujeX(self.vyraz):
                self.vyrazy_barvy[self.vyraz] = barva
            self.vyhodnotVyrazy(self.vyrazy)

    def vykresliKartezskouSoustavu(self):
        # Vytvoreni pera
        pero = QPen()
        pero.setColor(Qt.red)
        pero.setWidth(2)

        # Vytvareni tras protoze jsou ctyri ruzne barvy
        trasa_mrizi = QPainterPath()
        trasa_pozadi = QPainterPath()
        trasa_os = QPainterPath()

        self.vykresliPozadi(trasa_pozadi, pero, self.barva_pozadi)
        self.vykresliMriz(trasa_mrizi, pero, self.barva_mrizi)
        self.vykresliOsy(trasa_os,pero)
    
    def vyhodnotVyrazy(self, vyrazy : list):
        self.vykresliKartezskouSoustavu()
        for vyraz in vyrazy:  
            if self.obsahujeX(vyraz):
                self.barva = self.vyrazy_barvy[vyraz]
                try:
                    self.vykresliKrivkuGrafu(vyraz, self.barva)
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
                    except:
                            try:
                                novy_vyraz = "math." + str(vyraz)
                                vysledek = eval(novy_vyraz)
                                vysledek  = round(vysledek, 3)
                                self.vyrazy.remove(vyraz)
                                self.novy_vyraz = str(vyraz) + " = " + str(vysledek)
                                self.vyrazy.append(self.novy_vyraz)
                                self.vyrazy_jednoduche.append(self.novy_vyraz)
                            except:
                                self.vyrazy.remove(vyraz)
                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Critical)
                                msg.setText("Nelze vyhodnotit vloženou hodnotu")
                                msg.setWindowTitle("Chyba")
                                msg.exec_()
        self.multiTlacitko.setText(self.listTextOdstavce(self.vyrazy))

    def listTextOdstavce(self, list :list) -> str:
        wrapper = textwrap.TextWrapper(width=10)
        mezi_list = ""
        for i in list:
            mezi_list += i
            mezi_list += "\n "
        return wrapper.fill(text=mezi_list)

    def jeVGrafu (self, pozice_y):
        if self.kraj_y <= pozice_y <= (self.kraj_y + self.vyska_grafu):
            return True
        else:
            return False

    def vykresliKrivkuGrafu(self, vyraz, barva) -> None:
        pero = QPen()
        trasa = QPainterPath()
        predchozi_v_grafu = 0 # Pokud byla None 0, pokud v 1, pokud nad 2 a pokud pod 3
        pero.setWidth(2)
        pero.setColor(barva)

        x_hodnoty = np.arange(-(self.stred_grafu_x)/self.pole_grafu, self.stred_grafu_x/self.pole_grafu, 1/100)
        f = sp.lambdify(sp.Symbol("x"), vyraz, "math") 
        y_hodnoty = []
        for a in x_hodnoty:
            try:
                y_hodnoty.append(sp.N(f(a)))
            except ValueError:
                # handle division by zero error
                y_hodnoty.append(None)
      
        #vytvor path pro vyraz
        #pro kazde číslo na ose
        for i in range(len(x_hodnoty)):
            # převeď normální osu na velikost grafu (vzdálenost od kraje + pulka grafu jelikoz hodnoty jsou od minus do plusu ale grafove hodnoty jsou jen od nuly do plusu + hodnota
            pozice_x = self.kraj_x + self.stred_grafu_x + (x_hodnoty[i]*self.pole_grafu)
            if y_hodnoty[i] is None:
                pozice_y = 1000
                trasa.moveTo(pozice_x, pozice_y)
                predchozi_v_grafu = 0
            else:    
                pozice_y = self.kraj_y + self.stred_grafu_y - (y_hodnoty[i] * self.pole_grafu) # vytvor y od kraje grafu pulka + pul
                
                if self.jeVGrafu(pozice_y):
                    if predchozi_v_grafu == 0:
                        trasa.moveTo(pozice_x, pozice_y)
                    elif predchozi_v_grafu  == 2:
                        trasa.moveTo(pozice_x, self.kraj_y)
                        trasa.lineTo(pozice_x, pozice_y)
                    elif predchozi_v_grafu == 3:
                        trasa.moveTo(pozice_x, self.kraj_y + self.vyska_grafu)
                        trasa.lineTo(pozice_x, pozice_y)
                    else:
                        trasa.lineTo(pozice_x, pozice_y)
                    predchozi_v_grafu = 1
                elif predchozi_v_grafu == 1:
                    if pozice_y < self.kraj_y:
                        trasa.lineTo(pozice_x, self.kraj_y)
                        predchozi_v_grafu = 2
                    elif pozice_y > self.kraj_y + self.vyska_grafu:
                        trasa.lineTo(pozice_x, self.kraj_y + self.vyska_grafu)
                        predchozi_v_grafu = 3  
                elif predchozi_v_grafu == 2:  
                    if pozice_y < self.kraj_y:
                        pass
                    elif pozice_y > self.kraj_y + self.vyska_grafu:
                        predchozi_v_grafu = 3
                elif predchozi_v_grafu == 3:
                    if pozice_y > self.kraj_y + self.vyska_grafu:
                        pass
                    elif pozice_y < self.kraj_y:
                        predchozi_v_grafu = 3            
                else:
                    predchozi_v_grafu = 0
        polozka_grafu = QGraphicsPathItem(trasa)
        polozka_grafu.setPen(pero)
        self.scene.addItem(polozka_grafu)

    def obsahujeX(self, vyraz) -> bool:
        for element in vyraz:
            if element == "x":
                return True
        return False
    
    def vykresliMriz(self, trasa, pero, barva):
        pero.setColor(barva)
        pero.setWidth(1)
        # Vytvoreni hodnot na ose x a samotnych vertikalnich os do prvni pulky
        for i  in np.arange (self.stred_grafu_x, self.sirka_grafu, 50) :
            x_popisek_text = (i - self.stred_grafu_x) / self.pole_grafu # Co bude na danem popisku
            self.pozice_pera_x = self.kraj_x + i #Pozice pera na ose x
        
            if -1 < x_popisek_text < 1: # Pokud je cislo mensi nez 1 zvetsim pocet cisel za desetinou carkou
                pocet_zaokrouhlenych_mist = 3
            else: # Jinak pouze jedno cislo za desetinou carkou
                pocet_zaokrouhlenych_mist = 1
            
            x_popisek = QGraphicsTextItem(str(round(x_popisek_text, pocet_zaokrouhlenych_mist))) # Zaokrouhleni a nasledne vytvoreni popisku osy
            x_popisek.setDefaultTextColor(barva)
            x_popisek.setPos(self.pozice_pera_x, self.kraj_y + self.stred_grafu_y)
            self.scene.addItem(x_popisek)
            trasa.moveTo(self.pozice_pera_x, self.kraj_y)
            trasa.lineTo(self.pozice_pera_x, self.vyska_grafu + self.kraj_y)
    
        pocet_zaokrouhlenych_mist = 1

        # Vytvoreni hodnot na ose y a samotnych vertikalnich os
        for i  in reversed(np.arange (self.kraj_x - 50, self.stred_grafu_x, 50)) : # serazena cisla od  
            x_popisek_text = (i - self.stred_grafu_x) / self.pole_grafu
            if -1 < x_popisek_text < 1:
                pocet_zaokrouhlenych_mist = 3
            else:
                pocet_zaokrouhlenych_mist = 1   
            x_popisek = QGraphicsTextItem(str (round (x_popisek_text, pocet_zaokrouhlenych_mist)))
            x_popisek.setDefaultTextColor(barva)
            x_popisek.setPos(self.kraj_x + i, self.kraj_y + self.stred_grafu_y)
            self.scene.addItem(x_popisek)
            # Zacni ve stredu a udelej caru dolu
            self.pozice_pera_x = self.kraj_x + i
            trasa.moveTo(self.pozice_pera_x, self.kraj_y)
            trasa.lineTo(self.pozice_pera_x, self.vyska_grafu + self.kraj_y)    

        # Horizontalni cary
        for i  in np.arange (self.stred_grafu_y + self.kraj_y - 50, self.vyska_grafu, 50) :
            y_popisek_text = (((i - self.stred_grafu_y) / self.pole_grafu) * - 1)
            if -1 < y_popisek_text < 1:
                round(y_popisek_text, 3)
            else:
                round(y_popisek_text, 1)
            y_popisek = QGraphicsTextItem(str (round (y_popisek_text, pocet_zaokrouhlenych_mist)))
            y_popisek.setPos(self.kraj_x + self.stred_grafu_x, self.kraj_y + i)
            y_popisek.setDefaultTextColor(barva)
            self.scene.addItem(y_popisek)
            self.graph_y_pen = self.kraj_y + i
            trasa.moveTo(self.kraj_x, self.graph_y_pen)
            trasa.lineTo(self.sirka_grafu + self.kraj_x, self.graph_y_pen)

        for i  in reversed(np.arange (self.kraj_y - 50, self.stred_grafu_y, 50)) :
            y_popisek_text = (i - self.stred_grafu_y) / self.pole_grafu * - 1
            if -1 < y_popisek_text < 1:
                round(y_popisek_text, 3)
            else:
                round(y_popisek_text, 1)
            y_popisek = QGraphicsTextItem(str (round (y_popisek_text, pocet_zaokrouhlenych_mist)))
            y_popisek.setPos(self.kraj_x + self.stred_grafu_x, self.kraj_y + i)
            y_popisek.setDefaultTextColor(barva)
            self.scene.addItem(y_popisek)
            self.graph_y_pen = self.kraj_y + i
            trasa.moveTo(self.kraj_x, self.graph_y_pen)
            trasa.lineTo(self.sirka_grafu + self.kraj_x, self.graph_y_pen)
    
        # Create a QGraphicsPathItem to display the graph
        polozka_grafu = QGraphicsPathItem(trasa)
        polozka_grafu.setPen(pero)
        self.scene.addItem(polozka_grafu)
        
    def vykresliPozadi(self, trasa, pero, barva):
        trasa.addRect(self.kraj_x, self.kraj_y, self.sirka_grafu, self.vyska_grafu)
        polozka_grafu = QGraphicsPathItem(trasa)
        polozka_grafu.setPen(pero)
        polozka_grafu.setBrush(QBrush(QColor(barva)))
        self.scene.addItem(polozka_grafu)

    def vykresliOsy(self, trasa, pero):

        pero.setWidth(3)
        pero.setColor(Qt.darkBlue)
        trasa.moveTo(self.kraj_x + self.stred_grafu_x, self.kraj_y)
        trasa.lineTo(self.kraj_x + self.stred_grafu_x, self.kraj_y + self.vyska_grafu)
        trasa.moveTo(self.kraj_x, self.kraj_y + self.stred_grafu_y)
        trasa.lineTo(self.kraj_x + self.sirka_grafu,  self.kraj_y + self.stred_grafu_y)
        
        polozka_grafu = QGraphicsPathItem(trasa)
        polozka_grafu.setPen(pero)
        self.scene.addItem(polozka_grafu)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MathGraphApp()
    ex.show()
    sys.exit(app.exec_())