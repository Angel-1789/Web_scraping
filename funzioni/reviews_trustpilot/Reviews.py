import bs4 # Beautiful Soup v4 -> libreria di websraping, ci permette di estrarre i dati dalle pagine HTML, pesino dati nascosti
import requests # libreria standard di Python per accedere ai siti web, tramitte richieste HTTP
import webbrowser # ci da la possibilità di aprire automaticamente il sito web su un browser a piacere
import time
import sys
from funzioni.vai_a_page import vai_a_page
from funzioni.LEGGI_SCRIVI_DIC import *

MAX_PAGES = 10


def estrai_dati(div_reviews, reviews,PRE_LINK_ANNUNCIO):
    conta = 0

    for review in div_reviews:
        if len(review)==1:
            username = review.find('aside').find('a').find('div',class_='typography_typography__QgicV typography_bodysmall__irytL typography_weight-medium__UNMDK typography_fontstyle-normal__kHyN3 styles_consumerName__dP8Um').get_text()
            paese = review.find('aside').find('a').find('div',class_='styles_consumerExtraDetails__fxS4S').find_all('span',class_='typography_typography__QgicV typography_weight-inherit__iX6Fc typography_fontstyle-inherit__ly_HV')[1].text        
            titolo = review.find('section').find('div', class_='styles_reviewContent__0Q2Tg').find('h2').get_text()
            contenuto = review.find('section').find('div', class_='styles_reviewContent__0Q2Tg').find('p')
            if contenuto is not None:
                contenuto = contenuto.get_text()
            else:
                contenuto = ""
            data = str(review.find('section').find('div', class_='styles_reviewHeader__iU9Px').find('time').attrs['datetime']).replace('T',' ')[:19]
            conta += 1
            reviews[str(username)+";"+str(paese)+";"+str(data)] = contenuto
    return [reviews,conta]

def estrai_reviews(LINK,PRE_LINK_ANNUNCIO, last_page, sec_pages,sec_pausa_errore, tentativi, reviews, nome_negozio):
    no_problem = False
    USCITA = 0

    while no_problem is False:
        try :
            soup = vai_a_page(LINK,sec_pausa_errore)
            tot_reviews = soup.find('div',class_='styles_mainContent__nFxAv').find('section').find('div',class_='paper_paper__1PY90 card_card__lQWDv styles_reviewsOverview__mVIJQ').find('div',class_='styles_header__yrrqf').find('h2').find('span').get_text()
            controllo_nav = soup.find('section',class_='styles_reviewsContainer__3_GQw').find('div',class_="styles_pagination__6VmQv").find('nav')

            if controllo_nav is not None:
                div_reviews = soup.find('section', class_ = 'styles_reviewsContainer__3_GQw').find_all('div',class_='paper_paper__1PY90 paper_square__lJX8a card_card__lQWDv card_noPadding__D8PcU styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ')
                pages = soup.find('section',class_='styles_reviewsContainer__3_GQw').find('div',class_="styles_pagination__6VmQv").find('nav').find_all('a')
                next_page = PRE_LINK_ANNUNCIO+str(pages[len(pages)-1].get('href'))
                n_pages = int(pages[len(pages)-2].text)

                print("\t\t\t\tpage %7s"%(str(1)+"/"+str(n_pages)),end ='')
                temp = estrai_dati(div_reviews, reviews["contenuto"],PRE_LINK_ANNUNCIO)
                reviews["contenuto"] = temp[0]
                reviews["modifiche"] = [LINK,1,n_pages]
                salva_v2(("reviews_"+nome_negozio+"_trustpilot"),"../files_web_scraping/Reviews_dato_grezzo/")
                print("   |  trovate: %2s reviews | %14s reviews | %s"%(str(temp[1]),(str(len(reviews))+" / "+str(tot_reviews)),LINK))

                for page in range((last_page+1), (n_pages+1)):
                    print("\t\t\t\tpage %7s"%(str(page)+"/"+str(n_pages)),end =' ')
                    soup = vai_a_page(next_page,sec_pausa_errore)
                    pages = soup.find('section',class_='styles_reviewsContainer__3_GQw').find('div',class_="styles_pagination__6VmQv").find('nav').find_all('a')
                    div_reviews = soup.find('section', class_ = 'styles_reviewsContainer__3_GQw').find_all('div',class_='paper_paper__1PY90 paper_square__lJX8a card_card__lQWDv card_noPadding__D8PcU styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ')
                    temp = estrai_dati(div_reviews, reviews["contenuto"],PRE_LINK_ANNUNCIO)
                    reviews["contenuto"] = temp[0]
                    reviews["modifiche"] = [next_page,page,n_pages]
                    salva_v2(("reviews_"+nome_negozio+"_trustpilot"),"../files_web_scraping/Reviews_dato_grezzo/")
                    print("  |  trovate: %2s reviews | %14s reviews | %s"%(str(temp[1]),(str(len(reviews))+" / "+str(tot_reviews)),next_page))
                    next_page = PRE_LINK_ANNUNCIO+str(pages[len(pages)-1].get('href'))
                    if(page%MAX_PAGES==0):
                        print("\t\t\t\t\t\t\t\tPAUSA DI ",sec_pages," SECONDI [ogni ",MAX_PAGES," pagine]",end ='.')
                        time.sleep(sec_pages)
                        print("\tFINE PAUSA")
            else:
                print("\t\t\t\tpage %7s"%(str(1)+"/"+str(1)),end ='')
                temp = estrai_dati(div_reviews, reviews["contenuto"],PRE_LINK_ANNUNCIO)
                reviews["contenuto"] = temp[0]
                reviews["modifiche"] = [next_page,page,n_pages]
                salva_v2(("reviews_"+nome_negozio+"_trustpilot"),"../files_web_scraping/Reviews_dato_grezzo/")
                print("  |  trovate: %2s reviews | %14s reviews | %s"%(str(temp[1]),(str(len(reviews))+" / "+str(tot_reviews)),LINK))
            no_problem = True
            return reviews
        except Exception as err:
            print("\nerrore durante il download delle reviews: %s\n\tSi riprovera il download della pagina tra %s secondi."%(err,sec_pausa_errore),end='')
            USCITA += 1
            print("\n\t\tUSCITA",USCITA)
            time.sleep(sec_pausa_errore)
            if USCITA==tentativi:
                sys.exit("\n\n\t\tERRORE DURANTE IL DOWNLOAD DEI DATI\n\n")
            print("\tFine pausa")