from funzioni.categorie import estrai_categorie
from funzioni.LEGGI_SCRIVI_DIC import salva,carica
from funzioni.Aziende_2 import estrai_aziende
import time
import json
from itertools import islice

sec_categoria = 30
sec_sottocategoria = 20
sec_pages = 10
sec_pausa_errore = 60
categorie_test = 3

LINK = 'https://www.trustpilot.com/categories/'
PRE_LINK_ANNUNCIO = 'https://www.trustpilot.com'

#---------------------------------------------------------------------------------------------------------------------
"""Controllo se il file contenente le diverse CATEGORIE e SOTTOCATGORIE esiste.
Se non esiste proseguo con lo scraping della pagina altrimenti carico ciò che avevo già scaricato."""

print("CATEGORIE")
try:
    # LEGGO FILE
    categorie = carica("categorie")
    print("\n\tFILE dizionario delle CATEGORIE trovato, carico i dati scaricati precedentemente\n")
    
    last_category = list(categorie.keys())[-1]
    last_subcategory = ((categorie[last_category])[-1])[0]
    
    print(last_category)
    print(last_subcategory,type(last_subcategory),"\n\n\n")
    
    for categoria in categorie:
        print("\t%s:"%(categoria))
        for sottocategoria in categorie[categoria]:
            print("\t\t%s , lnk %s"%(sottocategoria[0],sottocategoria[1]))
            
except IOError as e:
    
    print("File non trovato : %s\n\tScarico i dati."%(e))
    
    #ESTRAI i link delle diverse sottocategorie#
    categorie = estrai_categorie(LINK,PRE_LINK_ANNUNCIO)
    
    #SALVA FILE CATEGORIE
    print("\n\tpreparo file per il salvataggio del dizionario delle categorie   ......   ",end='')
    salva(categorie,"categorie")
    print("\tfile salvato")
    
except Exception as r:
    print("\nErrore: ",r)