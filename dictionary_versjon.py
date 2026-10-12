import matplotlib.pyplot as plt
import sys
import csv
from datetime import datetime

FILSTI = "Obligatoriske Innleveringer/Oblig7/sinnes_2014_2025_med_makstemperatur.csv"

def tall(x):
    try:
        tallet = float(x.replace(",", ".").strip())
        return tallet
    except (ValueError, TypeError, AttributeError):
        tallet = float("nan")
        return tallet


def skriv_inn_årstall():
    while True:
        årstall = input("Skriv inn årstall:").strip()
        try:
            datetime.strptime(årstall, "%Y")
            return årstall
        except (ValueError, AttributeError):
            print("Årstallet må ha 4 siffer")


try:
    fil = open(FILSTI, encoding="utf-8-sig", newline="")
except FileNotFoundError:
    print("Fant ikke filen")
    sys.exit(1)

bibliotek = {}

with fil:
    leser = csv.DictReader(fil, delimiter=";")

    for rad in leser:
        dato = rad.get("Tid(norsk normaltid)")
        try:
            datetime.strptime(dato, "%d.%m.%Y")
        except (ValueError, TypeError):
            continue

        navn = rad.get("Navn")
        max_temp = rad.get("Maksimumstemperatur (døgn)")
        mid_temp = rad.get("Middeltemperatur (døgn)")
        nedbør = rad.get("Nedbør (døgn)")
        mid_vind = rad.get("Høyeste middelvind (døgn)")
        snødybde = rad.get("Snødybde")

        bibliotek[dato] = navn, max_temp, mid_temp, nedbør, mid_vind, snødybde

bibliotek = dict(sorted(bibliotek.items(), key=lambda par: (par[0][-4:], par[0][3:5], par[0][0:2])))


år = int(skriv_inn_årstall())

startdato_snø = datetime.strptime(f"01.11.{år-1}", "%d.%m.%Y")
sluttdato_snø = datetime.strptime(f"01.05.{år}", "%d.%m.%Y")
antall_snødager = 0

curr_sum_plante = 0
max_sum_plante = float("-inf")

periode_regn = 0
lengste_periode_regn = 0
startdato_regn_rekord = sluttdato_regn_rekord = 0
startdato_periode_regn = 0

sommerdager = 0
høysommerdager = 0
tropedager = 0

x_datoer = []
snødybde_liste = []
nedbør_liste = []
mid_temp_liste = []
mid_vind_liste = []

for dato, verdier in bibliotek.items():
    dato_obj = datetime.strptime(dato, "%d.%m.%Y")
    i_året = dato_obj.year == år

    max_temp = tall(verdier[1])
    mid_temp = tall(verdier[2])
    nedbør = tall(verdier[3])
    mid_vind = tall(verdier[4])
    snødybde = tall(verdier[5])
    
    # Dager med minst 20cm snødybde telles
    if dato_obj >= startdato_snø and dato_obj < sluttdato_snø and snødybde >= 20:
        antall_snødager += 1

    #Finner lengste periode uten regn i hele filen
    if nedbør == 0:
        periode_regn += 1

        if periode_regn == 1:
            startdato_periode_regn = dato
        
        if periode_regn > lengste_periode_regn:
            lengste_periode_regn = periode_regn
            startdato_regn_rekord = startdato_periode_regn
            sluttdato_regn_rekord = dato       
    else:
        periode_regn = 0
    
    if i_året:

        # Plantevekst beregnes (Finner beste periode med høyest sum av plantevekst, ubestemt start og slutt)
        # (Kadanes algoritme)
        if mid_temp > 5:
            plante_verdi = mid_temp - 5
        elif mid_temp < 0:
            plante_verdi = mid_temp
        else:
            plante_verdi = 0
        
        if curr_sum_plante == 0:
            startdato_plante = dato
        
        curr_sum_plante += plante_verdi

        if curr_sum_plante > max_sum_plante:
            max_sum_plante = curr_sum_plante
            best_start_plante = startdato_plante
            best_slutt_plante = dato

        if curr_sum_plante < 0:
            curr_sum_plante = 0

        #Teller sommerdager, høysommerdager og tropedager. Oppgaven definerer sommerdag som OVER 20 grader.
        if max_temp > 20:
            sommerdager += 1
        if max_temp > 25:
            høysommerdager += 1
        if max_temp > 30:
            tropedager += 1

        x_datoer.append(dato_obj)
        snødybde_liste.append(snødybde)
        nedbør_liste.append(nedbør)
        mid_temp_liste.append(mid_temp)
        mid_vind_liste.append(mid_vind)

if not x_datoer:
    print("Ingen data tilgjengelig for dette året.")
    sys.exit(2)

#Printing
print(f"-Perioden med best plantevekst i {år} var fra {best_start_plante[0:5]} til {best_slutt_plante[0:5]}, med plantevekst på {max_sum_plante:.1f}.")
print(f"-Det var {antall_snødager} dager med minst 20cm snødybde fra 01.11.{år-1} til 30.04.{år}.")        
print(f"-Lengste periode uten regn var på {lengste_periode_regn} dager, fra {startdato_regn_rekord} til {sluttdato_regn_rekord}.")
print(f"-Sommerdager: {sommerdager}. Høysommerdager: {høysommerdager}. Tropedager: {tropedager}")

#Plotting
fig, ax = plt.subplots(4, 1, figsize=(12, 8))

ax[0].plot(x_datoer, snødybde_liste)
ax[1].plot(x_datoer, nedbør_liste)
ax[2].plot(x_datoer, mid_temp_liste)
ax[3].plot(x_datoer, mid_vind_liste)

ax[0].set_ylabel("cm")
ax[1].set_ylabel("mm")
ax[2].set_ylabel("°C")
ax[3].set_ylabel("m/s")

ax[0].set_title("Snødybde")
ax[1].set_title("Nedbør")
ax[2].set_title("Middeltemperatur")
ax[3].set_title("Høyeste Middelvind")

plt.tight_layout()
plt.show()