from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains # usare i tasti e le operazioni con il mouse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

def scorri_reviews(driver, n_reviews, tentativi):
    celle_reviews = []
    controllo = [0,0]

    try:
        s = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"(//div[@class='siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc']//div[@class='siAUzd-neVct'])[last()]")))
        a = ActionChains(driver)
        a.move_to_element(s).context_click().perform()
    except Exception as e:
        print("Errore 1: ",e)

    b = ActionChains(driver)
    
    start = datetime.datetime.now()
    inizio = time.time()
    print("\n\tSTART: %s \n"%(start))

    while (len(celle_reviews) < n_reviews) and (controllo[1] <= tentativi):
        try:
            r = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,"(//div[@class='siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc']//div[@class='siAUzd-neVct'])[last()]")))
            b.move_to_element(r).context_click().perform()
            b.key_down(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            celle_reviews = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "jJc9Ad", " " ))]')
            if len(celle_reviews) == controllo[0]:
                controllo[1] +=1
                print("\ttentativo: ",controllo[1])
            else: 
                controllo[1] = 0
            print("\t\tcarico: ",len(celle_reviews)," / ",str(n_reviews)," reviews",end='\t\t')
            print("\t\ttempo trascorso: %25s secondi"%(time.time()-inizio))
            controllo[0] = len(celle_reviews)
        except Exception as e:
            print("\n\t\t\t\t\t\tERRORE DURANTE IL CARICAMENTO DELLE REVIEW: ",e,"\n")
            break

    if controllo[1] >= tentativi:
        print("\n\t\t\t\t\t\tERRORE DURANTE IL CARICAMENTO DELLE REVIEW: si procede a salvare tutto quello che si è letto fino ad ora \n")

    print("inizio: ",start)
    print("fine: ",datetime.datetime.now())
    print("tempo trascorso: ",time.time()-inizio," secondi")
    
    return celle_reviews

def componi_key(driver):
    try :
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "Yr7JMd-pane-hSRGPd", " " ))]')))
        nome = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "fontHeadlineLarge", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "fontHeadlineLarge", " " ))]//span').text
        address = (driver.find_elements_by_xpath("//div[@class='Io6YTe fontBodyMedium']"))[0].text

        n = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "Yr7JMd-pane-hSRGPd", " " ))]').text
        if ("reviews" in n) or ("recensioni" in n):
            n_reviews = ((n.split())[0]).replace('.','')
        else:
            n_reviews = 0
            print("QUESTO NEGOZIO NON HA RECENSIONI")
    except:
        print("errore durante click visualizzazioni reviews")

    return str(nome)+";"+str(address)+";"+str(n_reviews)

def estrai_review(driver):
    s = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gXqMYb-hSRGPd", " " ))]')
    for i in s:
        try :     
            i.click()
        except Exception as e:
            print("\t\t\terrore durante click more nelle reviews")