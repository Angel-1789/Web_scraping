from funzioni.LEGGI_SCRIVI_DIC import *
from funzioni.Selenium_google_maps.estrai_negozi_da_GM import *
from funzioni.Selenium_google_maps.estrai_reviews_Google_maps import *
import sys

TENTATIVI = 5
LINK = 'https://www.google.com/maps/search/KFC/@40.546364,-74.8041465,9z/data=!3m1!4b1'

# print(sys.argv)

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:',sys.argv[i])

if len(sys.argv)>1:
    source = sys.argv[1]
    print("source: ",source)
    
    if source == 'google':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    else:
        sys.exit("Sei su google colab ma hai inserito un parametro sbagliato : RIPROVA inserendo 'google' dopo il nome del file")
else:
    if '/content/drive/' in sys.path[0] :
        sys.exit("Sei su google colab: RIPROVA inserendo 'google' dopo il nome del file")
    else:
        PATH_DRIVER = 'chromedriver_win32/chromedriver.exe'
        driver = webdriver.Chrome(PATH_DRIVER)
    
driver = init_driver(LINK, driver)

# ------------------------------------------------INIZIO


## ----------------------------------------  TROVO I NEGOZI
negozi = []

print("File ",end='')
try :
    negozi = carica("NEGOZI_KFC")
    print("  Trovato\n")
except Exception as e:
    
    print("  non Trovato\n")
    print("\tErrore [MAIN]: ",e)

    while continua_view_celle(driver):
        vis_neg(driver)
        negozi = estrai_links(driver,negozi)
        print(len(negozi))
        driver.find_element_by_id('ppdPk-Ej1Yeb-LgbsSe-tJiF1e').click()
        
    negozi1 = list(dict.fromkeys(negozi))
    salva_dic(negozi1, "NEGOZI_KFC")
    print("\tfile salvato_ NEGOZI_KFC")
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
reviews_google_maps = {}

print("\nFile ",end='')
try :
    reviews_google_maps = carica("reviews_KFC_google_maps")
    print("  Trovato\n")
except Exception as e:
    print("  non Trovato\n")
    print("Errore [MAIN]: ",e)
    
print("dim dizionario negozi reviews: %s negozi salvati\n"%len(reviews_google_maps))

ultimo_lnk_letto = carica("ULTIMO_NEG_REVIEWS")

temp_link_negozi = link_negozi[link_negozi.index(ultimo_lnk_letto):]
negozi_andati_in_errore = {}

for link in temp_link_negozi:
    
    driver = store_pages(link, driver)        
    driver.switch_to.window(driver.window_handles[1])
    chiave_review = componi_key(driver)
    print("key : ",chiave_review)
    if chiave_review not in reviews_google_maps:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "Yr7JMd-pane-hSRGPd", " " ))]'))).click()

        print("\n",link)
        ### ----------------------------------------  visualizza tutte le review disponibili
        celle_reviews = scorri_reviews(driver, int((chiave_review.split(";"))[2]), TENTATIVI)
        ## ----------------------------------------  click more nelle review
        estrai_review(driver)
        ### ----------------------------------------  leggo le review
        reviews = []
        reviews_grezzo = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "ODSEW-ShBeI-text", " " ))]')
        for i in reviews_grezzo:
            reviews.append(i.text)    
        ### ----------------------------------------  salva le reviews per il negozio X 
        reviews_google_maps[chiave_review] = reviews

        print("\t dim diz: %s\t%s\n"%(len(reviews_google_maps), type(reviews_google_maps)))
        salva_dic(link,"ULTIMO_NEG_REVIEWS")
        salva_dic(reviews_google_maps, "reviews_KFC_google_maps")
        if len(celle_reviews) != int((chiave_review.split(";"))[2]):
            print("\nCi sono stati degli errori durante il caricamento delle Reviews!! per il negozio",chiave_review," salviamo una copia della chiave con il link nel dizionario dei negozi con errori")
            negozi_andati_in_errore[chiave_review] = link
            salva_dic(negozi_andati_in_errore, "reviews_KFC_google_maps_negozi_andati_in_errore")
    else:
        print("NEGIZIO GIA' SALVATO")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])