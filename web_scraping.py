from funzioni.categorie import estrai_categorie
from funzioni.Aziende import estrai_aziende
import time
import json

sec_categoria = 30
sec_sottocategoria = 20
sec_pages = 10
sec_pausa_errore = 60

LINK = 'https://www.trustpilot.com/categories/'
PRE_LINK_ANNUNCIO = 'https://www.trustpilot.com'

#---------------------------------------------------------------------------------------------------------------------
"""Controllo se il file contenente le diverse CATEGORIE e SOTTOCATGORIE esiste.
Se non esiste proseguo con lo scraping della pagina altrimenti carico ciò che avevo già scaricato."""
print("CATEGORIE")
try:
    # LEGGO FILE
    with open("./file/categorie.json") as f:
        print("\n\tFILE dizionario delle CATEGORIE trovato, carico i dati scaricati precedentemente\n")
        categorie = f.read()
        #print(categorie)
except Exception as e:
    print("File non trovato : ", e)
    #ESTRAI i link delle diverse sottocategorie#
    categorie = estrai_categorie(LINK,PRE_LINK_ANNUNCIO,sec_pausa_errore)

    #SALVA FILE CATEGORIE
    print("\n\tpreparo file per il salvataggio del dizionario delle categorie   ......   ",end='')
    with open("./file/categorie.json", "w") as write_file:
        json.dump(categorie, write_file, indent=4)
    print("\tfile salvato")


#---------------------------------------------------------------------------------------------------------------------
"""Controllo se il file contenente le diverse i NOMI dei NEGOZI presente nelle diverse SOTTOCATGORIE esiste.
Se non esiste proseguo con lo scraping della pagina altrimenti carico ciò che avevo già scaricato."""
print("NEGOZI")
try:
    # LEGGO FILE
    with open("./file/negozi.json") as f:
        print("\n\tFILE dizionario dei NEGOZI trovato, carico i dati scaricati precedentemente")
        aziende = f.read()
except Exception as e:
    print("File non trovato : %s\n\tScarico i dati."%(e))
    
    #Estrai i link e i nomi dei negozi presenti nelle diverse sottocategorie
    for categoria in categorie:
        print('\033[1m'+"Categoria: ",categoria,"\n")
        sottocategorie = categorie[categoria]
        for sottocategoria in sottocategorie:
            print(sottocategoria)
            print('\033[1m'+"\tSottocategoria:",sottocategoria[0],"\tlink:",sottocategoria[1])
            aziende = estrai_aziende(sottocategoria[1],PRE_LINK_ANNUNCIO,sec_pages,sec_pausa_errore)
            #categorie[categoria].append(aziende)
            """print("\n\n\t\t\t\t\tPAUSA SOTTOCATEGORIA DI ",sec_sottocategoria," SECONDI", end ='')
            time.sleep(sec_sottocategoria)
            print("\tFINE PAUSA\n")"""
        print("\n\n\t\t\t\t\tPAUSA CATEGORIA DI ",sec_categoria," SECONDI", end ='')
        time.sleep(sec_categoria)
        print("\tFINE PAUSA\n\n")

    #SALVA FILE CATEGORIE
    print("\n\tpreparo file per il salvataggio del dizionario dei NEGOZI   ......   ",end='')
    with open("./file/negozi.json", "w") as write_file:
        json.dump(aziende, write_file, indent=4)
    print("\tfile salvato")

#---------------------------------------------------------------------------------------------------------------------
#Estrai le reviews dei diversi negozi presenti nelle diverse sottocategorie
"""for categoria in categorie:
    print('\033[1m'+"Categoria: ",categoria,"\n")
    sottocategorie = categorie[categoria]
    for sottocategoria in sottocategorie:
        print('\033[1m'+"\tSottocategoria:",sottocategoria[0],"\tlink:",sottocategoria[1])
        aziende = estrai_aziende(sottocategoria[1],PRE_LINK_ANNUNCIO,sec_pages,sec_pausa_errore)
        categorie[categoria].append(aziende)
        print("\n\n\t\t\t\t\tPAUSA SOTTOCATEGORIA DI ",sec_sottocategoria," SECONDI", end ='')
        time.sleep(sec_sottocategoria)
        print("\tFINE PAUSA\n")
    print("\n\n\t\t\t\t\tPAUSA CATEGORIA DI ",sec_categoria," SECONDI", end ='')
    time.sleep(sec_categoria)
    print("\tFINE PAUSA\n\n")"""

    
"""print("preparo file per il salvataggio del dizionario.. ",end='')
with open("./file/web_scraping.json", "w") as write_file:
    json.dump(reviews, write_file, indent=4)
print("\tfile salvato")"""