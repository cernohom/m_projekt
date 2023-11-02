import numpy as np

#definovana poslednim cislem na ose x bude vzdy ctvercovy zakladne 10
velikost_grafu = 10
vysledky = {}

#objevi se vysledek v danem grafu jestli ne tak to nebudu pocitat pro vsechny hodnoty a reknu ze neni v danem grafu
def je_reseni_v_grafu(mat_fnkce):
    for x in np.arange(-velikost_grafu, velikost_grafu+0.1, 0.1):
        try:
            vysledek = mat_fnkce(x)
            if -velikost_grafu <= vysledek <= velikost_grafu:
                return True
        except ZeroDivisionError:
            pass  # neresit deleni nulou
    print("vysledek neni v danem grafu")
    return False

def mat_vyr(x):
    return x ** 2 - 5 * x

#funkce na vytvoreni dictionary s dvema hodnotama pro dana cisla po desetitisicinach velikosti grafu pote
def vysledky_funkce(mat_fnkce):
    for x in np.arange(-velikost_grafu, velikost_grafu+0.1, velikost_grafu/1000):
        try:
            vysledek = mat_fnkce(x)
            if -velikost_grafu <= vysledek <= velikost_grafu:
                vysledky[x] = vysledek
        #TODO kolecko v grafu ze v tomto miste funkce nema reseni
        except ZeroDivisionError:
            pass  # neresit deleni nulou

def mat_vyr(x):
    return x ** 2 - 5 * x

#TODO connect with PyQt use PyQt pen and draw the graph guidance in the gptgraf.py
#TODO get rid of dictionary it is linear and create two list of x and y values

a = je_reseni_v_grafu(mat_vyr)
vysledky_funkce(mat_vyr)
print(a)
print(vysledky)