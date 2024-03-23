import sys
import numpy as np
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPen, QPainterPath, QBrush, QColor
import sympy as sp
import textwrap

class MathGraphApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        # Inicializace listů a slovníků pro uchování výrazů a jejich nastavení
        self.vyrazy : list = []  # Seznam výrazů
        self.vyrazy_jednoduche : list = []  # Seznam jednoduchých vyhodnocených výrazů
        self.vyrazy_barvy : dict[str, Qt.GlobalColor] = {}  # Slovník pro ukládání barev pro každý výraz
        self.initUI()

    def initUI(self) -> None:
        # Nastavení hodnot pro graf
        self.pole_grafu : float = 50  # Velikost pole grafu
        self.sirka_grafu : int = 1200  # Šířka grafu
        self.vyska_grafu : int = 800  # Výška grafu
        self.kraj_x : int = 100  # Okraj x
        self.kraj_y : int = 100  # Okraj y
        self.velikost_tlacitka : int = 50  # Velikost tlačítek
        self.sila_priblizeni : int = 50  # Zvětšení nebo zmenšení grafu při přiblížení nebo oddálení
        self.font_textu = QFont("Arial", 15)  # Font pro text
        self.priblizeni_pocet : float = 0  # Počet přiblížení nebo oddálení
        self.barva_pozadi = Qt.GlobalColor.white  # Barva pozadí
        self.barva_mrizi = Qt.GlobalColor.black  # Barva mřížky
        self.darkmode = False  # Režim tmavého módu
        self.sirka_krivky = 2 # Šířka křivky

        # Vypočítání středu grafu
        self.stred_grafu_x = self.sirka_grafu / 2
        self.stred_grafu_y = self.vyska_grafu / 2        
        
        # Nastavení okna
        self.view = QGraphicsView(self)
        self.setCentralWidget(self.view)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.setWindowTitle('Grafická kalkulačka')
        self.setGeometry(0, 0, self.sirka_grafu + 200, self.vyska_grafu + 20)
        self.UiComponents()
    
    # Funkce na vytváření komponent okna
    def UiComponents(self) -> None: 
        # Tlačítko MODE pro změnu módu (světlý/tmavý)
        self.vytvorTlacitko(self, "MODE", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y - self.velikost_tlacitka, self.velikost_tlacitka*2, self.velikost_tlacitka, self.changeMode, self.font_textu, "")

        # Tlačítka pro přiblížení a oddálení
        self.vytvorTlacitko(self, "+", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y, self.velikost_tlacitka, self.velikost_tlacitka, self.priblizeni, self.font_textu, "")
        self.vytvorTlacitko(self, "-", self.sirka_grafu + self.kraj_x, self.kraj_y, self.velikost_tlacitka, self.velikost_tlacitka, self.oddaleni, self.font_textu, "")

        # Tlačítka pro volbu barev
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka,  self.kraj_y + self.velikost_tlacitka * 4, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.GlobalColor.red), self.font_textu, "background-color: red")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x,  self.kraj_y + self.velikost_tlacitka * 4, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.GlobalColor.darkRed), self.font_textu, "background-color: darkRed")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x , self.kraj_y + self.velikost_tlacitka * 3, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.GlobalColor.darkGreen), self.font_textu, "background-color: darkGreen")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + self.velikost_tlacitka * 3, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.GlobalColor.green), self.font_textu, "background-color: green")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka, self.kraj_y + self.velikost_tlacitka, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.GlobalColor.magenta), self.font_textu, "background-color: magenta")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x, self.kraj_y + self.velikost_tlacitka, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.GlobalColor.darkMagenta), self.font_textu, "background-color: darkMagenta")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x - self.velikost_tlacitka,  self.kraj_y + self.velikost_tlacitka * 2, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.GlobalColor.cyan), self.font_textu, "background-color: cyan")
        self.vytvorTlacitko(self, "=", self.sirka_grafu + self.kraj_x ,  self.kraj_y + self.velikost_tlacitka * 2, self.velikost_tlacitka, self.velikost_tlacitka, lambda: self.potvrzeni(Qt.GlobalColor.darkCyan), self.font_textu, "background-color: darkCyan")
        
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
        self.textove_pole.setFont(self.font_textu)
        
        # Vykreslení Kartézské soustavy 
        self.vykresliKartezskouSoustavu()
    
    # Vytvoření tlačítka s danými vlastnostmi 
    def vytvorTlacitko(self, tlacitko, text : str, ax : int, ay: int, aw : int, ah : int, funkce, font, styl : str) -> QPushButton:
        """
        Parametry:
            text (str): Text na tlačítku.
            ax (int): X-ová souřadnice tlačítka.
            ay (int): Y-ová souřadnice tlačítka.
            aw (int): Šířka tlačítka.
            ah (int): Výška tlačítka.
            funkce: Funkce, která se má spustit po stisknutí tlačítka.
            font (QFont): Font textu na tlačítku.
            styl (str): Styl tlačítka (volitelné).
        """
        tlacitko = QPushButton(text, self)
        tlacitko.setGeometry(ax, ay, aw, ah)
        tlacitko.setFont(font)
        tlacitko.clicked.connect(funkce)
        if styl:
            tlacitko.setStyleSheet(styl)
        return tlacitko

    # Změna módu aplikace (světlý/temný režim).
    def changeMode(self) -> None:
        if self.darkmode:
            self.barva_pozadi = Qt.GlobalColor.white
            self.barva_mrizi = Qt.GlobalColor.black
            self.darkmode = False
        else:
            self.barva_pozadi = Qt.GlobalColor.black
            self.barva_mrizi = Qt.GlobalColor.white
            self.darkmode = True
        self.vyhodnotVyrazy(self.vyrazy)

    # Přiblížení grafu
    def priblizeni(self) -> None:
        if self.priblizeni_pocet <= 4:
            self.pole_grafu = self.pole_grafu * 2

            self.vyhodnotVyrazy(self.vyrazy)
            self.priblizeni_pocet += 1
        else:
            self.vytvorChyboveOkno("Více nelze přiblížit")

    # Co se stane když zmáčknu oddálení
    def oddaleni(self) -> None:
        if self.priblizeni_pocet >= -4:
            self.pole_grafu = self.pole_grafu / 2
            self.vykresliKartezskouSoustavu()
            self.vyhodnotVyrazy(self.vyrazy)
            self.priblizeni_pocet -= 1
        else:
            self.vytvorChyboveOkno("Více nelze oddálit")
    
    # Smazání všech dříve zadaných výrazů
    def smazani(self) -> None:
        self.vyrazy = []
        self.multiTlacitko.setText("Vymazání")
        self.vyhodnotVyrazy(self.vyrazy)
    
    # Potvrzení vloženého výrazu
    def potvrzeni(self, barva : Qt.GlobalColor) -> None:
            self.vyraz = self.textove_pole.text()
            self.vyrazy.append(self.vyraz)
            if self.obsahujeX(self.vyraz):
                self.vyrazy_barvy[self.vyraz] = barva
            self.vyhodnotVyrazy(self.vyrazy)

    # Vykreslení kartézské soustavy
    def vykresliKartezskouSoustavu(self) -> None:
        # Vytvoření pera
        pero = QPen()
        pero.setColor(Qt.GlobalColor.red)
        pero.setWidth(2)

        # Vytváření tras pro pera
        trasa_mrizi = QPainterPath()
        trasa_pozadi = QPainterPath()
        trasa_os = QPainterPath()

        self.vykresliPozadi(trasa_pozadi, pero, self.barva_pozadi)
        self.vykresliMriz(trasa_mrizi, pero, self.barva_mrizi)
        self.vykresliOsy(trasa_os,pero)

    # Vykreslí pozadí grafu se zadanou barvou
    def vykresliPozadi(self, trasa : QPainterPath, pero : QColor, barva : Qt.GlobalColor) -> None:
        trasa.addRect(self.kraj_x, self.kraj_y, self.sirka_grafu, self.vyska_grafu)
        polozka_grafu = QGraphicsPathItem(trasa)
        polozka_grafu.setPen(pero)
        polozka_grafu.setBrush(QBrush(QColor(barva)))
        self.scene.addItem(polozka_grafu)
        
    # Vykreslí mříž grafu se zadanou barvou a s popisky
    def vykresliMriz(self, trasa: QPainterPath, pero: QColor, barva: Qt.GlobalColor) -> None:
        pero.setColor(barva)  # Nastavení barvy pera
        pero.setWidth(1)  # Nastavení tloušťky pera
        
        # Vykreslení vertikálních čar a popisků na ose x
        for i in np.arange(self.stred_grafu_x, self.sirka_grafu, self.pole_grafu):
            x_popisek_text = (i - self.stred_grafu_x) / self.pole_grafu  # Výpočet hodnoty popisku osy x
            self.pozice_pera_x = self.kraj_x + i  # Nastavení pozice pera na ose x
            
            # Určení počtu desetinných míst v závislosti na hodnotě popisku
            if -1 < x_popisek_text < 1:
                pocet_zaokrouhlenych_mist = 3
            else:
                pocet_zaokrouhlenych_mist = 1
                
            # Vytvoření popisku osy x
            x_popisek = QGraphicsTextItem(str(round(x_popisek_text, pocet_zaokrouhlenych_mist)))
            x_popisek.setDefaultTextColor(barva)  # Nastavení barvy popisku
            x_popisek.setPos(self.pozice_pera_x, self.kraj_y + self.stred_grafu_y)  # Nastavení pozice popisku
            self.scene.addItem(x_popisek)  # Přidání popisku do scény
            trasa.moveTo(self.pozice_pera_x, self.kraj_y)  # Přesun na počáteční bod čáry
            trasa.lineTo(self.pozice_pera_x, self.vyska_grafu + self.kraj_y)  # Nakreslení čáry
            
        pocet_zaokrouhlenych_mist = 1
        
        # Vykreslení vertikálních čar a popisků na ose y
        for i in reversed(np.arange(self.kraj_x - 50, self.stred_grafu_x, self.pole_grafu)):
            x_popisek_text = (i - self.stred_grafu_x) / self.pole_grafu
            if -1 < x_popisek_text < 1:
                pocet_zaokrouhlenych_mist = 3
            else:
                pocet_zaokrouhlenych_mist = 1   
            x_popisek = QGraphicsTextItem(str(round(x_popisek_text, pocet_zaokrouhlenych_mist)))
            x_popisek.setDefaultTextColor(barva)
            x_popisek.setPos(self.kraj_x + i, self.kraj_y + self.stred_grafu_y)
            self.scene.addItem(x_popisek)
            self.pozice_pera_x = self.kraj_x + i
            trasa.moveTo(self.pozice_pera_x, self.kraj_y)
            trasa.lineTo(self.pozice_pera_x, self.vyska_grafu + self.kraj_y)    

        # Vykreslení horizontálních čar a popisků na ose y
        for i in np.arange(self.stred_grafu_y + self.kraj_y - 50, self.vyska_grafu, 50):
            y_popisek_text = (((i - self.stred_grafu_y) / self.pole_grafu) * - 1)
            if -1 < y_popisek_text < 1:
                round(y_popisek_text, 3)
            else:
                round(y_popisek_text, 1)
            y_popisek = QGraphicsTextItem(str(round(y_popisek_text, pocet_zaokrouhlenych_mist)))
            y_popisek.setPos(self.kraj_x + self.stred_grafu_x, self.kraj_y + i)
            y_popisek.setDefaultTextColor(barva)
            self.scene.addItem(y_popisek)
            self.graph_y_pen = self.kraj_y + i
            trasa.moveTo(self.kraj_x, self.graph_y_pen)
            trasa.lineTo(self.sirka_grafu + self.kraj_x, self.graph_y_pen)

        for i in reversed(np.arange(self.kraj_y - 50, self.stred_grafu_y, self.pole_grafu)):
            y_popisek_text = (i - self.stred_grafu_y) / self.pole_grafu * - 1
            if -1 < y_popisek_text < 1:
                round(y_popisek_text, 3)
            else:
                round(y_popisek_text, 1)
            y_popisek = QGraphicsTextItem(str(round(y_popisek_text, pocet_zaokrouhlenych_mist)))
            y_popisek.setPos(self.kraj_x + self.stred_grafu_x, self.kraj_y + i)
            y_popisek.setDefaultTextColor(barva)
            self.scene.addItem(y_popisek)
            self.graph_y_pen = self.kraj_y + i
            trasa.moveTo(self.kraj_x, self.graph_y_pen)
            trasa.lineTo(self.sirka_grafu + self.kraj_x, self.graph_y_pen)
        
        # Vytvoření QGraphicsPathItem pro zobrazení grafu
        polozka_grafu = QGraphicsPathItem(trasa)
        polozka_grafu.setPen(pero)
        self.scene.addItem(polozka_grafu)

    # Vykreslí osy grafu pomocí zadané cesty a pera
    def vykresliOsy(self, trasa : QPainterPath, pero : QPen) -> None:

        pero.setWidth(3)
        pero.setColor(Qt.GlobalColor.darkBlue)
        trasa.moveTo(self.kraj_x + self.stred_grafu_x, self.kraj_y)
        trasa.lineTo(self.kraj_x + self.stred_grafu_x, self.kraj_y + self.vyska_grafu)
        trasa.moveTo(self.kraj_x, self.kraj_y + self.stred_grafu_y)
        trasa.lineTo(self.kraj_x + self.sirka_grafu,  self.kraj_y + self.stred_grafu_y)
        
        polozka_grafu = QGraphicsPathItem(trasa)
        polozka_grafu.setPen(pero)
        self.scene.addItem(polozka_grafu)

    # Vyhodnocení a zobrazení všech výrazů
    def vyhodnotVyrazy(self, vyrazy: list) -> None:
        self.vykresliKartezskouSoustavu()  # Vyresetování vykreslení kartézské soustavy
        for vyraz in vyrazy:  # Procházení všech výrazů
            if self.obsahujeX(vyraz):  # Pokud výraz obsahuje proměnnou x
                self.barva = self.vyrazy_barvy[vyraz]  # Získání barvy výrazu
                try:
                    self.vykresliKrivkuGrafu(vyraz, self.barva)  # Vykreslení křivky grafu v dané barvě
                except:
                    self.vytvorChyboveOkno("Nelze vyhodnotit vloženou hodnotu")  # Pokud se nepodaří vyhodnotit výraz, zobrazí se chybové okno
            else:  # Pokud výraz neobsahuje proměnnou x
                if vyraz not in self.vyrazy_jednoduche:  # Pokud výraz není již vyhodnocen
                    try:
                        vysledek = eval(vyraz)  # Vyhodnocení výrazu
                        self.vyrazy.remove(vyraz)  # Odebrání nevyhodnoceného výrazu
                        self.novy_vyraz = str(vyraz) + " = " + str(round(vysledek, 3))  # Vytvoření nového výrazu s výsledkem
                        self.vyrazy.append(self.novy_vyraz)  # Přidání nového výrazu do seznamu výrazů
                        self.vyrazy_jednoduche.append(self.novy_vyraz)  # Přidání nového výrazu do seznamu již jednoduše vyhodnocených výrazů
                    except:
                        try:
                            novy_vyraz = "math." + str(vyraz)  # Přidání matematického prefixu k výrazu
                            vysledek = eval(novy_vyraz)  # Vyhodnocení výrazu
                            vysledek = round(vysledek, 3)  # Zaokrouhlení výsledku
                            self.vyrazy.remove(vyraz)  # Odebrání vyhodnoceného výrazu
                            self.novy_vyraz = str(vyraz) + " = " + str(vysledek)  # Vytvoření nového řetězce s výsledkem
                            self.vyrazy.append(self.novy_vyraz)  # Přidání nového řetězce do seznamu výrazů
                            self.vyrazy_jednoduche.append(self.novy_vyraz)  # Přidání nového řetězce do seznamu již jednoduše vyhodnocených výrazů
                        except:
                            self.vyrazy.remove(vyraz)  # Odebrání výrazu, který nelze vyhodnotit
                            self.vytvorChyboveOkno("Nelze vyhodnotit vloženou hodnotu")  # Zobrazení chybového okna
        self.multiTlacitko.setText(self.listTextNaOdstavce(self.vyrazy))  # Aktualizace textu víceúčelového tlačítka

    # Ověřuje, zda v zadaném výrazu existuje proměnná x.
    def obsahujeX(self, vyraz) -> bool:
        for element in vyraz:
            if element == "x":
                return True
        return False

    # Vytváří chybové okno s daným textem
    def vytvorChyboveOkno(self, text : str) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle("Chyba")
        msg.exec_()

    # Převádí seznam textových prvků na formátovaný text s odsazením
    def listTextNaOdstavce(self, list : list) -> str:
        wrapper = textwrap.TextWrapper(width=10)
        text_odstavce = ""
        for i in list:
            text_odstavce += wrapper.fill(text=i)
            text_odstavce += "\n "
        return text_odstavce

    # Vykreslí křivku grafu na základě zadaného výrazu a barvy
    def vykresliKrivkuGrafu(self, vyraz, barva) -> None:
        pero = QPen()
        trasa = QPainterPath()
        predchozi_v_grafu = 0 # Pokud byla None 0, pokud v 1, pokud nad 2 a pokud pod 3
        pero.setWidth(self.sirka_krivky)
        pero.setColor(barva)

        x_hodnoty = np.arange(-(self.stred_grafu_x)/self.pole_grafu, self.stred_grafu_x/self.pole_grafu, 1/100)
        f = sp.lambdify(sp.Symbol("x"), vyraz, "math") 
        y_hodnoty = []
        for a in x_hodnoty:
            try:
                y_hodnoty.append(sp.N(f(a)))
            except ValueError:
                # Řešení chyby dělení nulou
                y_hodnoty.append(None)
    
        # Vytvoří cestu pro vykreslení křivky
        # Pro každé číslo na ose
        for i in range(len(x_hodnoty)):
            # Převede normální osu na velikost grafu (vzdálenost od kraje + polovina grafu, jelikož hodnoty jsou od mínusu do plusu, ale grafické hodnoty jsou jen od nuly do plusu, plus hodnota)
            pozice_x = self.kraj_x + self.stred_grafu_x + (x_hodnoty[i]*self.pole_grafu)
            if y_hodnoty[i] is None:
                pozice_y = 1000
                trasa.moveTo(pozice_x, pozice_y)
                predchozi_v_grafu = 0
            else:    
                pozice_y = self.kraj_y + self.stred_grafu_y - (y_hodnoty[i] * self.pole_grafu) # Vytvoří y od kraje grafu, polovina + hodnota
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

    # Ověřuje, zda zadaná pozice na ose y leží uvnitř grafu
    def jeVGrafu (self, pozice_y) -> bool:
        if self.kraj_y <= pozice_y <= (self.kraj_y + self.vyska_grafu):
            return True
        else:
            return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MathGraphApp()
    ex.show()
    sys.exit(app.exec_())