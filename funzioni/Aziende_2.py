import bs4 # Beautiful Soup v4 -> libreria di websraping, ci permette di estrarre i dati dalle pagine HTML, pesino dati nascosti
import requests # libreria standard di Python per accedere ai siti web, tramitte richieste HTTP
import webbrowser # ci da la possibilità di aprire automaticamente il sito web su un browser a piacere
import time
from funzioni.vai_a_page import vai_a_page
from funzioni.Reviews import estrai_reviews
from funzioni.LEGGI_SCRIVI_DIC import salva_dic
    
def estrai_dati(div_aziende, aziende,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore, page_link,page_attuale, tot_page):
    conta = 0
    reviews = {}
    try :
        for azienda in div_aziende :
            n_r = azienda.find_all('p')
            #estrai solo le aziende che hanno reviews
            if (len(n_r)>1):
                lnk_azienda = PRE_LINK_ANNUNCIO+str(azienda.find('a').get('href'))
                nome_azienda = n_r[0].text
                if (nome_azienda not in aziende):
                    print("\t\t\tNome negozio: ",nome_azienda,"\tLink:",lnk_azienda)
                    #reviews = estrai_reviews(lnk_azienda,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore)
                    aziende[nome_azienda] = [lnk_azienda,reviews,[page_link,page_attuale,tot_page]]
                    conta += 1
                else:
                    print("Azienda già salvata")
            
        print("\n\t\t\t\ttrovate e caricate: ",conta," aziende non presenti nel dizionario")
    except Exception as e:
        print("ERRORE [estrai_dati]: ",e)
    return aziende


def estrai_aziende(LINK, PRE_LINK_ANNUNCIO, sec, sec_pausa_errore,tentativi):
    no_problem = False
    count = 1
    aziende = {}
    
    while (no_problem is False) and (count<=tentativi):
        try:
            soup = vai_a_page(LINK,sec_pausa_errore)
            controllo_nav = soup.find('div',class_='styles_categoryBusinessBody__3fm2a').find('nav')
            div_aziende = soup.find('div', class_ = 'styles_businessUnitCardsContainer__1ggaO')
            
            if div_aziende is not None:
                div_aziende = div_aziende.find_all('div',class_='paper_paper__29o4A card_card__2F_07 card_noPadding__1tkWv styles_wrapper__2QC-c styles_businessUnitCard__1-z5m')

                if controllo_nav is not None:
                    pages = soup.find('div',class_='styles_categoryBusinessBody__3fm2a').find('nav').find_all('a')
                    n_page = int(soup.find('div',class_='styles_categoryBusinessBody__3fm2a').find('nav').find('a',class_='link_internal__YpiJI link_disabled__2Q9Ub button_button__3sN8k button_medium__252Ld button_primary__2eJ8_ link_button__13BH6 pagination-link_current__2H33l pagination-link_item__1wvr8').get_text())
                    next_page = PRE_LINK_ANNUNCIO+str(pages[len(pages)-1].get('href'))
                    n_pages = int(pages[len(pages)-2].text)

                    print("\n\t\tpage %s / %s \t%s"%(str(n_page),str(n_pages),LINK))
                    aziende = estrai_dati(div_aziende, aziende,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore, LINK,n_page,n_pages)

                    for page in range((n_page+1),n_pages+1):

                        print("\n\t\tpage %s / %s\t%s"%(str(page),str(n_pages),next_page))
                        soup = vai_a_page(next_page,sec_pausa_errore)
                        pages = soup.find('div',class_='styles_categoryBusinessBody__3fm2a').find('nav').find_all('a')
                        n_page = int(soup.find('div',class_='styles_categoryBusinessBody__3fm2a').find('nav').find('a',class_='link_internal__YpiJI link_disabled__2Q9Ub button_button__3sN8k button_medium__252Ld button_primary__2eJ8_ link_button__13BH6 pagination-link_current__2H33l pagination-link_item__1wvr8').get_text())
                        div_aziende = soup.find('div', class_ = 'styles_businessUnitCardsContainer__1ggaO')
                        print("FOR: ",div_aziende)

                        if div_aziende is not None:
                          div_aziende = div_aziende.find_all('div',class_='paper_paper__29o4A card_card__2F_07 card_noPadding__1tkWv styles_wrapper__2QC-c styles_businessUnitCard__1-z5m')
                          aziende = estrai_dati(div_aziende, aziende,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore, next_page,n_page,n_pages)

                        next_page = PRE_LINK_ANNUNCIO+str(pages[len(pages)-1].get('href'))
                        if(page%10==0):
                            print("\n\t\t\t\t\tPAUSA DI ",sec," SECONDI [ogni 10 PAGES]", end='')
                            time.sleep(sec)
                            print("\tFINE PAUSA")
                else:
                    print("\n\t\tpage  1 / 1\t%s"%LINK)
                    aziende = estrai_dati(div_aziende, aziende,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore, LINK,1,1)
                return [aziende,(count-1)]
        except Exception as e:
            print("errore durante il download dei negozi [ESTRAI AZIENDE 23]: %s.\n\tSi riprovera il download della pagina tra %s secondi.\t%s %s "%(e,sec_pausa_errore,str(no_problem),str(count)),end='')
            time.sleep(sec_pausa_errore)
            print("\tFine pausa")
            count+=1
    return [aziende,(count-1)]

def estrai_negozi_sottocategorie(categorie, PRE_LINK_ANNUNCIO,sec_categoria, sec_sottocategoria, sec_pages, sec_pausa_errore, tentativi, categorie_negozi):
#     count = 0
    controllo_uscita = False
    
    for categoria in categorie:
#         if count <=3:
#             print(count)
            print('\033[1m'+"Categoria: ",categoria,"\n")
            sottocategorie = categorie[categoria]
            for sottocategoria in sottocategorie:
                print('\033[1m'+"\tSottocategoria:",sottocategoria[0],"\tlink:",sottocategoria[1])
                controllo = estrai_aziende(sottocategoria[1],PRE_LINK_ANNUNCIO,sec_pages,sec_pausa_errore,tentativi)

                temp_sottocategoria = str(categoria)+";"+str(sottocategoria[0])
                
                if controllo[1]<tentativi:
                    aziende = controllo[0]
                    if (temp_sottocategoria not in categorie_negozi):
                        categorie_negozi[temp_sottocategoria] = aziende
                        salva_dic(categorie_negozi, "NEGOZI")
                    else:
                        for negozio in aziende:
                            (categorie_negozi[temp_sottocategoria])[negozio] = aziende[negozio]
                        salva_dic(categorie_negozi, "NEGOZI")
                else:
                    controllo_uscita = True
                    break
#             count+=1
            if controllo_uscita is True:
                break
            print("\n\n\t\t\t\t\tPAUSA CATEGORIA DI ",sec_categoria," SECONDI", end ='')
            time.sleep(sec_categoria)
            print("\tFINE PAUSA\n\n")
    return categorie_negozi