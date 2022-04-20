from funzioni.LEGGI_SCRIVI_DIC import *
from funzioni.Selenium_google_maps.estrai_negozi_da_GM import *
from funzioni.Selenium_google_maps.estrai_reviews_Google_maps import *
import sys

TENTATIVI = 5
PRE_LINK = 'https://www.google.com/maps/search/'
# LINK = 'https://www.google.com/maps/search/KFC/@40.546364,-74.8041465,9z/data=!3m1!4b1'

# print(sys.argv)
def controllo_negozio(negozio_cerca):
    negozi_tpl = carica("negozi")

    for i in negozi_tpl:
        for negozio in negozi_tpl[i]:
            if negozio_cerca == negozio:
                return True
    return False

def controllo_parametri(src, lnk, nome):
  
    if not ((src == 'google') or  (src == 'jupyter')):
        sys.exit("Primo parametro non valido. Valori del primo paramtero: [google / jupyter]")
    elif not (lnk[:len(PRE_LINK+"/"+nome)] == (PRE_LINK+"/"+nome)):
        sys.exit("Secondo parametro non valido. Il link deve essere del tipo: 'https://www.google.com/maps/search/[nome_negozio]/...' ")
    elif controllo_negozio(nome) == False:
        sys.exit("Terzo parametro non valido. Il nome del negozio non è presente nei negozi Trustpilot")
    else:
        print("\t\tParametri OK .....\n")

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:',sys.argv[i])

if len(sys.argv)==3:
    source = sys.argv[1]
    LINK = sys.argv[2]
    NOME_NEGOZIO = sys.argv[3]
    print("source: %s\tLINK: %s\tNome_negozio: %s\n"%(source,LINK,NOME_NEGOZIO))

    # ---------- Controllo parametri inseriti
    controllo_parametri(source, LINK, NOME_NEGOZIO)

    # ----------  controllo source
    if source == 'google':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    elif source == 'jupyter':
        PATH_DRIVER = 'chromedriver_win32/chromedriver.exe'
        driver = webdriver.Chrome(PATH_DRIVER)
else:
    sys.exit("Numero di parametri non validi. Inserire 3 parametri dopo il nome del file python: [google/jupyter] [LINK google maps] [Nome_negozio]")      
    
driver = init_driver(LINK, driver)

# ------------------------------------------------INIZIO


## ----------------------------------------  TROVO I NEGOZI
negozi = []

print("File ",end='')
try :
    negozi = carica_v2(("NEGOZI_"+nome_negozio+"_trustpilot"),"../files_web_scraping/Negozi_Google_Maps")
    print("  Trovato\n")
except Exception as e:
    
    print(" ......  non Trovato\n")
    print("\tErrore [MAIN]: ",e)

    while continua_view_celle(driver):
        vis_neg(driver)
        negozi = estrai_links(driver,negozi)
        print(len(negozi))
        driver.find_element_by_id('ppdPk-Ej1Yeb-LgbsSe-tJiF1e').click()
        
    negozi1 = list(dict.fromkeys(negozi))
    salva_v2(("NEGOZI_"+nome_negozio+"_trustpilot"),"../files_web_scraping/Negozi_Google_Maps")
    # salva_dic(negozi1, "NEGOZI_KFC")
    print("\tfile salvato: ",("NEGOZI_"+nome_negozio+"_trustpilot"))
print("trovati :",len(negozi), " negozi")

## ----------------------------------------  Navigo tra i link dei negozi
link_negozi = []

# print("\n\t\t\tMOSTRA LONGITUDINE")
for link_negozio in negozi:
    s = link_negozio.find('!4d') + len('!4d')
    t = link_negozio.find('?')
    if float(link_negozio[s:t]) < 0:
#         print(link_negozio[s:t]
        link_negozi.append(link_negozio)
print("\t",len(link_negozi),"/",len(negozi)," negozi utili")

## ----------------------------------------  Estraggo le reviews dai negozi GOOGLE MAPS
print("\nFile ",end='')
try :
    reviews_google_maps = carica_v2(("reviews_"+nome_negozio+"_google_maps"),"../files_web_scraping/Reviews_dato_grezzo")
    print("  Trovato\n")
except Exception as e:
    reviews_google_maps = {"contenuto":[], "last_lnk":""}
    print("  non Trovato\n")
    print("Errore [MAIN]: ",e)
    
print("dim dizionario negozi reviews: %s negozi salvati\n"%len(reviews_google_maps["contenuto"]))

ultimo_lnk_letto = reviews_google_maps["last_lnk"]

temp_link_negozi = link_negozi[link_negozi.index(ultimo_lnk_letto):]
negozi_andati_in_errore = {}

for link in temp_link_negozi:
    
    driver = store_pages(link, driver)        
    driver.switch_to.window(driver.window_handles[1])
    key = componi_key(driver)
    chiave_review = key[0]
    print("key : ",chiave_review)
    if chiave_review not in reviews_google_maps["contenuto"]:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "Yr7JMd-pane-hSRGPd", " " ))]'))).click()

        print("\n",link)
        ### ----------------------------------------  visualizza tutte le review disponibili
        celle_reviews = scorri_reviews(driver, int(key[1]), TENTATIVI)
        ## ----------------------------------------  click more nelle review
        estrai_review(driver)
        ### ----------------------------------------  leggo le review
        reviews = []
        div_reviews = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "ODSEW-ShBeI-text", " " ))]')
        for i in div_reviews:
            reviews.append(i.text)    
        ### ----------------------------------------  salva le reviews per il negozio X 
        (reviews_google_maps["contenuto"])[chiave_review] = reviews

        print("\t dim diz: %s\t%s\n"%(len(reviews_google_maps["contenuto"]), type(reviews_google_maps["contenuto"])))
        reviews_google_maps["last_lnk"] = link
        salva_v2(reviews_google_maps,("reviews_"+nome_negozio+"_google_maps"),"../files_web_scraping/Reviews_dato_grezzo")
        if len(celle_reviews) != int(key[1]):
            print("\nCi sono stati degli errori durante il caricamento delle Reviews!! per il negozio",chiave_review," salviamo una copia della chiave con il link nel dizionario dei negozi con errori")
            negozi_andati_in_errore[chiave_review] = link
            salva_v2(reviews_google_maps,("reviews_"+nome_negozio+"_google_maps_negozi_andati_in_errore"),"../files_web_scraping/Reviews_dato_grezzo")
    else:
        print("NEGIZIO GIA' SALVATO")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])