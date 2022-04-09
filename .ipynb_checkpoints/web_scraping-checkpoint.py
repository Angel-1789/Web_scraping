from funzioni.categorie import estrai_categorie, trova_ultima_categoria
from funzioni.LEGGI_SCRIVI_DIC import carica, salva_dic
from funzioni.Aziende_2 import estrai_negozi_sottocategorie
from funzioni.Reviews import estrai_reviews
import time
import json
from itertools import islice

sec_categoria = 30
sec_sottocategoria = 20
sec_pages = 10
sec_pausa_errore = 10
categorie_test = 3
tentativi = 3

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

except IOError as e:

    print("File non trovato : %s\n\tScarico i dati."%(e))

    #ESTRAI i link delle diverse sottocategorie#
    categorie = estrai_categorie(LINK,PRE_LINK_ANNUNCIO)

    #SALVA FILE CATEGORIE
    salva_dic(categorie, "CATEGORIE")
    print("\tfile salvato")

except Exception as r:
    print("\nErrore in MAIN [CATEGORIE]: ",r)

    
#---------------------------------------------------------------------------------------------------------------------
"""Controllo se il file contenente le diverse i NOMI dei NEGOZI presente nelle diverse SOTTOCATGORIE esiste.
Se non esiste proseguo con lo scraping della pagina altrimenti carico ciò che avevo già scaricato.

Eseuguiamo un ulteriore controllo sulle categorie e le sottocategorie presenti file negozi.json , cosi da 
sapere se si deve continuare a scaricare i dati o se sono completi
"""

categorie_negozi = {}

print("NEGOZI")
try:
    last_category = list(categorie.keys())[-1]
    last_subcategory = ((categorie[last_category])[-1])[0] 
    
    # LEGGO FILE
    # print("QUI -1")
    categorie_negozi = carica("negozi")

    # print(len(categorie_negozi))

    if len(categorie_negozi)==0:
        print("\n\tFILE dizionario dei NEGOZI trovato, Ma è vuoto")
        # categorie_negozi = estrai_negozi_sottocategorie(categorie, PRE_LINK_ANNUNCIO,sec_categoria, sec_sottocategoria, sec_pages, sec_pausa_errore, tentativi, categorie_negozi)
    else:
        # print("QUI 0")
        print("\n\tFILE dizionario dei NEGOZI trovato, carico i dati scaricati precedentemente")
        
        last_key_categoria = list(categorie_negozi.keys())[-1]
        temp = last_key_categoria.split(";")
        
        last_key_sottocategoria = list((categorie_negozi[last_key_categoria]).keys())[-1]
        last_category_negozi = temp[0]
        last_subcategory_negozi = temp[1]
        page_att = (((categorie_negozi[last_key_categoria])[last_key_sottocategoria])[-1])[-2]
        tot_page = (((categorie_negozi[last_key_categoria])[last_key_sottocategoria])[-1])[-1]
        
        # print("QUI 1")
        print(" %s : %s ; %s : %s ; %s : %s"%(last_category_negozi,last_category,last_subcategory_negozi,last_subcategory,page_att,tot_page))
        print((last_category_negozi!=last_category) or (last_subcategory_negozi!=last_subcategory) or (page_att < tot_page))

        if (last_category_negozi!=last_category) or (last_subcategory_negozi!=last_subcategory) or (page_att < tot_page):
            temp = (list(categorie_negozi.keys())[-1])
            # print("QUI 2")
            temp_categorie = trova_ultima_categoria(categorie, temp, categorie_negozi)
            # print("QUI 3")
            categorie_negozi = estrai_negozi_sottocategorie(temp_categorie, PRE_LINK_ANNUNCIO,sec_categoria, sec_sottocategoria, sec_pages, sec_pausa_errore, tentativi, categorie_negozi)

except IOError as e:
    
    print("File non trovato : %s\n\tScarico i dati."%(e))
    
    #Estrai i link e i nomi dei negozi presenti nelle diverse sottocategorie
    categorie_negozi = estrai_negozi_sottocategorie(categorie, PRE_LINK_ANNUNCIO,sec_categoria, sec_sottocategoria, sec_pages, sec_pausa_errore, tentativi, categorie_negozi)
            
    #SALVA FILE CATEGORIE
    if len(categorie_negozi)==0:
        print("Dizionario vuoto!")
#         print(count)
#         salva_dic(categorie_negozi, "NEGOZI")
except Exception as r:
    print("\nErrore in MAIN [NEGOZI]: ",r)
    
    
#---------------------------------------------------------------------------------------------------------------------
"""Controllo se il file contenente le reviews dei NEGOZI presente nelle diverse SOTTOCATGORIE esiste.
Se non esiste proseguo con lo scraping della pagina altrimenti carico ciò che avevo già scaricato.

Eseuguiamo un ulteriore controllo sulle REVIEWS dei NEGOZI presenti nel file negozi.json , 
cosi da sapere se si deve continuare a scaricare i dati o se sono completi
"""

# negozi_reviews = {}

# print("REVIEWS")
# try:
#     # LEGGO FILE
#     negozi_reviews = carica("reviews")
#     print("\n\tFILE dizionario dei NEGOZI trovato, carico i dati scaricati precedentemente")
    
#     last_key_categoria = list(categorie_negozi.keys())[-1]
#     temp = last_key_categoria.split(";")
    
#     last_key_sottocategoria = list((categorie_negozi[last_key_categoria]).keys())[-1]
#     last_category_negozi = temp[0]
#     last_subcategory_negozi = temp[1]
#     page_att = (((categorie_negozi[last_key_categoria])[last_key_sottocategoria])[-1])[-2]
#     tot_page = (((categorie_negozi[last_key_categoria])[last_key_sottocategoria])[-1])[-1]
    
#     if (last_category_negozi!=last_category) and (last_subcategory_negozi!=last_subcategory) and (page_att < tot_page):
#         temp = (list(categorie_negozi.keys())[-1])
#         temp_categorie = trova_ultima_categoria(categorie, temp, categorie_negozi)
#         categorie_negozi = estrai_negozi_sottocategorie(temp_categorie, LINK, PRE_LINK_ANNUNCIO,sec_categoria, sec_sottocategoria, sec_pages, sec_pausa_errore, tentativi, categorie_negozi)

# except IOError as e:
    
#     print("File non trovato : %s\n\tScarico i dati."%(e))
    
#     #Estrai i link e i nomi dei negozi presenti nelle diverse sottocategorie
#     categorie_negozi = estrai_negozi_sottocategorie(categorie, LINK, PRE_LINK_ANNUNCIO,sec_categoria, sec_sottocategoria, sec_pages, sec_pausa_errore, tentativi, categorie_negozi)
            
#     #SALVA FILE CATEGORIE
#     if len(categorie_negozi)==0:
#         print("Dizionario vuoto!")
# #         print(count)
# #         salva_dic(categorie_negozi, "NEGOZI")
# except Exception as r:
#     print("\nErrore in MAIN [NEGOZI]: ",r)