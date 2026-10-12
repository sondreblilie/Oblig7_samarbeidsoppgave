from matplotlib import pyplot as plt
from datetime import datetime
import csv

datoer = []
makstemperatur = []
nedbør = []
høyeste_middelvind = []
snødybde = []
middeltemperatur = []

dager_skiføre = 0
min_temp = 5
plante_vekst = 0
periode = 0
lengste_periode = 0
trope_dager = 0
sommer_dager = 0
høy_sommer_dager = 0

start_dato_varme = None
slutt_dato_varme = None
start_dato_lengde = None
startdato_uten_nedbør = None
sluttdato_uten_nedbør = None
høyeste_dato = None

while True:
    try:
        år = int(input("Skriv inn årstall: "))
        break
    except ValueError:
        print("Du må skrive inn et gyldig årstall.")