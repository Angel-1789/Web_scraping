"""Controllo se il file contenente le reviews dei NEGOZI presente nelle diverse SOTTOCATGORIE esiste.
Se non esiste proseguo con lo scraping della pagina altrimenti carico ciò che avevo già scaricato.

Eseuguiamo un ulteriore controllo sulle REVIEWS dei NEGOZI presenti nel file negozi.json , 
cosi da sapere se si deve continuare a scaricare i dati o se sono completi
"""

import sys
from funzioni.LEGGI_SCRIVI_DIC import *
from funzioni.reviews_trustpilot.Reviews import estrai_reviews 

LINK = ''
PRE_LINK_ANNUNCIO = 'https://www.trustpilot.com'
SEC_PAGES = 10
SEC_PAUSA_ERRORE = 10
TENTATIVI = 3

# --------------------------  CONTROLLO ESISTENZA NEGOZIO
def controllo_negozio(negozio_cerca):
    negozi_tpl = carica("negozi")

    for i in negozi_tpl:
        for negozio in negozi_tpl[i]:
            if negozio_cerca == negozio:
                LINK = ((negozi_tpl[i])[negozio])[0]
                # print("\tLINK[0]: ",((negozi_tpl[i])[negozio])[0])
                # print("\tLINK[0]: ",LINK)
                return [True,LINK]
    return False

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:',sys.argv[i])
    
if len(sys.argv)==2:
    temp = controllo_negozio(sys.argv[1]) 
    if temp[0]:
        print("\n\tNegozio Trovato\n\tInizio a scaricare le reviews da Trustpilot")
        LINK = temp[1]
    else:
        sys.exit("Negozio non trovato/ non presente nella lista dei negozi (negozi.json) riprova")
else:
    sys.exit("Pasare come parametro (solo 1) il nome del negozio dal quale si vogliono scaricare le reviews da Trustpilot")

# --------------------------- SCARICA REVIEWS
reviews_negozio = {"contenuto":{},"modifiche":["","",""] }

print("\nREVIEWS -- %s -- Trustpilot\n"%(sys.argv[1]))
try:
    # LEGGO FILE
    reviews_negozio = carica_v2(("reviews_"+sys.argv[1]+"_trustpilot"),"../files_web_scraping/Reviews_dato_grezzo/")
    print("\n\tFILE del NEGOZIO -- %s -- Trustpilot trovato, carico i dati scaricati precedentemente"%(sys.argv[1]))
    
    last_page = (reviews_negozio["modifiche"])[1]
    tot_page = (reviews_negozio["modifiche"])[2]
    
    if last_page < tot_page:
        reviews_negozio = estrai_reviews((reviews_negozio["modifiche"])[0], last_page, PRE_LINK_ANNUNCIO, SEC_PAGES, SEC_PAUSA_ERRORE, TENTATIVI,reviews_negozio, sys.argv[1])
except IOError as e:
    
    print("\nFile non trovato : %s\n\tScarico i dati."%(e))
    #Estrai i link e i nomi dei negozi presenti nelle diverse sottocategorie
    reviews_negozio = estrai_reviews(LINK, PRE_LINK_ANNUNCIO, 1, SEC_PAGES, SEC_PAUSA_ERRORE, TENTATIVI,reviews_negozio, sys.argv[1])

except Exception as r:
    print("\nErrore in MAIN [NEGOZI]: ",r)













# # ---------------------------------------------------------------------------------------------------
# import bs4 # Beautiful Soup v4 -> libreria di websraping, ci permette di estrarre i dati dalle pagine HTML, pesino dati nascosti
# import requests # libreria standard di Python per accedere ai siti web, tramitte richieste HTTP
# import webbrowser # ci da la possibilità di aprire automaticamente il sito web su un browser a piacere
# import time
# from vai_a_page import vai_a_page
# import json

# def estrai_dati(div_reviews, reviews,PRE_LINK_ANNUNCIO):
#     conta = 0
#     for review in div_reviews:
#         if len(review)==1:
#             username = review.find('aside').find('a').find('div',class_='typography_typography__QgicV typography_bodysmall__irytL typography_weight-medium__UNMDK typography_fontstyle-normal__kHyN3 styles_consumerName__dP8Um').get_text()
#             paese = review.find('aside').find('a').find('div',class_='styles_consumerExtraDetails__fxS4S').find_all('span',class_='typography_typography__QgicV typography_weight-inherit__iX6Fc typography_fontstyle-inherit__ly_HV')[1].text        
#             titolo = review.find('section').find('div', class_='styles_reviewContent__0Q2Tg').find('h2').get_text()
#             contenuto = review.find('section').find('div', class_='styles_reviewContent__0Q2Tg').find('p')
#             if contenuto is not None:
#                 contenuto = contenuto.get_text()
#             else:
#                 contenuto = ""
#             data = str(review.find('section').find('div', class_='styles_reviewHeader__iU9Px').find('time').attrs['datetime']).replace('T',' ')[:19]
#             conta += 1
#             reviews[str(username)+";"+str(data)] = [username,paese,titolo,contenuto,data]
#     return [reviews,conta]

# #LINK = 'https://www.trustpilot.com/review/gallant.com'
# #LINK = 'https://www.trustpilot.com/review/pawp.com'
# #LINK = 'https://www.trustpilot.com/review/dutch.com'
# LINK = 'https://www.trustpilot.com/review/ocvh.com'
# PRE_LINK_ANNUNCIO ='https://www.trustpilot.com'
# sec = 1
# sec_pausa_errore = 60
    
# soup = vai_a_page(LINK,sec_pausa_errore)
# tot_reviews = soup.find('div',class_='styles_mainContent__nFxAv').find('section').find('div',class_='paper_paper__1PY90 card_card__lQWDv styles_reviewsOverview__mVIJQ').find('div',class_='styles_header__yrrqf').find('h2').find('span').get_text()
# controllo_nav = soup.find('section',class_='styles_reviewsContainer__3_GQw').find('div',class_="styles_pagination__6VmQv").find('nav')
# reviews = {}
# div_reviews = soup.find('section', class_ = 'styles_reviewsContainer__3_GQw').find_all('div',class_='paper_paper__1PY90 paper_square__lJX8a card_card__lQWDv card_noPadding__D8PcU styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ')

# if controllo_nav is not None:
#     pages = soup.find('section',class_='styles_reviewsContainer__3_GQw').find('div',class_="styles_pagination__6VmQv").find('nav').find_all('a')
#     next_page = PRE_LINK_ANNUNCIO+str(pages[len(pages)-1].get('href'))
#     n_pages = int(pages[len(pages)-2].text)
    
#     print("\n\t\t\tpage %7s"%(str(1)+"/"+str(n_pages)),end ='')
#     temp = estrai_dati(div_reviews, reviews,PRE_LINK_ANNUNCIO)
#     reviews = temp[0]
#     print("   |  trovate: %2s reviews | %14s reviews | %s"%(str(temp[1]),(str(len(reviews))+" / "+str(tot_reviews)),LINK))
    
#     for page in range(2,n_pages+1):
#         print("\t\t\tpage %7s"%(str(page)+"/"+str(n_pages)),end =' ')
#         soup = vai_a_page(next_page,sec_pausa_errore)
#         pages = soup.find('section',class_='styles_reviewsContainer__3_GQw').find('div',class_="styles_pagination__6VmQv").find('nav').find_all('a')
#         div_reviews = soup.find('section', class_ = 'styles_reviewsContainer__3_GQw').find_all('div',class_='paper_paper__1PY90 paper_square__lJX8a card_card__lQWDv card_noPadding__D8PcU styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ')
#         temp = estrai_dati(div_reviews, reviews,PRE_LINK_ANNUNCIO)
#         reviews = temp[0]
#         print("  |  trovate: %2s reviews | %14s reviews | %s"%(str(temp[1]),(str(len(reviews))+" / "+str(tot_reviews)),next_page))
#         next_page = PRE_LINK_ANNUNCIO+str(pages[len(pages)-1].get('href'))
#         if(page%10==0):
#             print("\t\t\t\t\t\t\tPAUSA DI ",sec," SECONDI [ogni ",10," pagine]",end ='.')
#             time.sleep(sec)
#             #print("\t\t\t\t\t\t\t\tFINE PAUSA")
#             print("\tFINE PAUSA")
# else:
#     print("\t\t\t\tpage %7s"%(str(1)+"/"+str(1)),end ='')
#     temp = estrai_dati(div_reviews, reviews,PRE_LINK_ANNUNCIO)
#     reviews = temp[0]
#     print("  |  trovate: %2s reviews | %14s reviews | %s"%(str(temp[1]),(str(len(reviews))+" / "+str(tot_reviews)),LINK))

# """print("preparo file per il salvataggio..",end='')
# with open("./file/web_sc.json", "w") as write_file:
#     json.dump(reviews, write_file, indent=4)
# print("file salvato")"""