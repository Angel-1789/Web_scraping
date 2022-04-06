import bs4 # Beautiful Soup v4 -> libreria di websraping, ci permette di estrarre i dati dalle pagine HTML, pesino dati nascosti
import requests # libreria standard di Python per accedere ai siti web, tramitte richieste HTTP
import webbrowser # ci da la possibilità di aprire automaticamente il sito web su un browser a piacere
import time
from funzioni.vai_a_page import vai_a_page
from funzioni.Reviews import estrai_reviews
    
def estrai_dati(div_aziende, aziende,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore):
    conta = 0
    reviews = {}
    for azienda in div_aziende :
        n_r = azienda.find_all('p')
        #estrai solo le aziende che hanno reviews
        if (len(n_r)>1):
            lnk_azienda = PRE_LINK_ANNUNCIO+str(azienda.find('a').get('href'))
            nome_azienda = n_r[0].text
            if (nome_azienda not in aziende):
                print("\t\t\tNome negozio: ",nome_azienda,"\tLink:",lnk_azienda)
                #reviews = estrai_reviews(lnk_azienda,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore)
                aziende[nome_azienda] = [lnk_azienda,reviews,1]#+"\n"+str(pages)
                conta += 1
    print("\n\t\t\t\ttrovate e caricate: ",conta," aziende non presenti nel dizionario")
    return aziende

def estrai_aziende(LINK,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore):
    no_problem = False
    count = 0
    
    while (no_problem is False) and (count<=5):
        try:
            soup = vai_a_page(LINK,sec_pausa_errore)
            controllo_nav = soup.find('div',class_='styles_categoryBusinessBody__3fm2a').find('nav')
            aziende = {}
            div_aziende = soup.find('div', class_ = 'styles_businessUnitCardsContainer__1ggaO').find_all('div',class_='paper_paper__29o4A card_card__2F_07 card_noPadding__1tkWv styles_wrapper__2QC-c styles_businessUnitCard__1-z5m')

            if controllo_nav is not None:
                pages = soup.find('div',class_='styles_categoryBusinessBody__3fm2a').find('nav').find_all('a')
                next_page = PRE_LINK_ANNUNCIO+str(pages[len(pages)-1].get('href'))
                n_pages = int(pages[len(pages)-2].text)

                print("\n\t\tpage  1 /",n_pages,"\t",LINK)
                aziende = estrai_dati(div_aziende, aziende,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore)
                for page in range(2,n_pages+1):
                    print("\n\t\tpage ",page,"/",n_pages,"\t",next_page)
                    soup = vai_a_page(next_page,sec_pausa_errore)
                    pages = soup.find('div',class_='styles_categoryBusinessBody__3fm2a').find('nav').find_all('a')
                    div_aziende = soup.find('div', class_ = 'styles_businessUnitCardsContainer__1ggaO').find_all('div',class_='paper_paper__29o4A card_card__2F_07 card_noPadding__1tkWv styles_wrapper__2QC-c styles_businessUnitCard__1-z5m')
                    aziende = estrai_dati(div_aziende, aziende,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore)
                    next_page = PRE_LINK_ANNUNCIO+str(pages[len(pages)-1].get('href'))
                    if(page%10==0):
                        print("\n\t\t\t\t\tPAUSA DI ",sec," SECONDI [ogni 10 PAGES]", end='')
                        time.sleep(sec)
                        print("\tFINE PAUSA")
            else:
                print("\n\t\tpage  1 / 1\t",LINK)
                aziende = estrai_dati(div_aziende, aziende,PRE_LINK_ANNUNCIO,sec,sec_pausa_errore)

            return aziende
        except Exception as e:
            print("errore durante il download dei negozi: %s.\n\tSi riprovera il download della pagina tra %s secondi.\t%s%s"%(e,sec_pausa_errore,str(no_problem),str(count)),end='')
            time.sleep(sec_pausa_errore)
            print("\tFine pausa")
            count+=1
    return aziende