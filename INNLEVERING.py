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

start_dato_snødybde = datetime(år - 1, 11, 1)
slutt_dato_snødybde = datetime(år, 5, 31)

with open("sinnes_2014_2025_med_makstemperatur.csv", "r", encoding="utf-8", newline="") as fil:
    leser = csv.reader(fil, delimiter=";")

    next(leser)

    for rad in leser:

        if rad[2].strip() == "":
            continue
        dato = datetime.strptime(rad[2], "%d.%m.%Y")
        if høyeste_dato is not None and dato <= høyeste_dato:
            continue
        høyeste_dato = dato

        if rad[7].strip() != "-":
            snødybde_verdi = float(rad[7].replace(",", "."))

            if start_dato_snødybde <= dato <= slutt_dato_snødybde:
                if snødybde_verdi >= 20:
                    dager_skiføre += 1

        if dato.year == år:
            datoer.append(dato)

            if rad[3] == "-":
                makstemperatur.append(None)
            else:
                makstemperatur.append(float(rad[3].strip().replace(",", ".")))

            if rad[4] == "-":
                middeltemperatur.append(None)
            else:
                middeltemperatur.append(float(rad[4].strip().replace(",", ".")))

            if rad[5] == "-":
                nedbør.append(None)
            else:
                nedbør.append(float(rad[5].strip().replace(",", ".")))

            if rad[6] == "-":
                høyeste_middelvind.append(None)
            else:
                høyeste_middelvind.append(float(rad[6].strip().replace(",", ".")))

            if rad[7] == "-":
                snødybde.append(None)
            else:
                snødybde.append(float(rad[7].strip().replace(",", ".")))

            if rad[4].strip() != "-":
                middeltemperatur_verdi = float(rad[4].replace(",", "."))

                if middeltemperatur_verdi >= min_temp:
                    plante_vekst += middeltemperatur_verdi - min_temp

            if rad[3].strip() != "-":
                makstemperatur_verdi = float(rad[3].replace(",", "."))

                if makstemperatur_verdi > 20:
                    sommer_dager += 1
                    if makstemperatur_verdi > 25:
                        høy_sommer_dager += 1
                        if makstemperatur_verdi > 30:
                            trope_dager += 1

        if rad[5].strip() != "-":
            nedbør_verdi = float(rad[5].replace(",", "."))

            if nedbør_verdi == 0:
                periode += 1

                if periode == 1:
                    start_dato_lengde = dato

                if periode > lengste_periode:
                    lengste_periode = periode
                    startdato_uten_nedbør = start_dato_lengde
                    sluttdato_uten_nedbør = dato
            else:
                periode = 0
        else:
            periode = 0