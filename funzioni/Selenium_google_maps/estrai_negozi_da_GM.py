from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains # usare i tasti e le operazioni con il mouse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# visualizza tutti i 20 negozi
def vis_neg(driver):
    s = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd", " " ))]')))
    a = ActionChains(driver)
    a.move_to_element(s).context_click().perform()
    a.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()

    for _ in range(9):
        a.key_down(Keys.PAGE_DOWN).perform()
        time.sleep(2)

# -----------------------------
def estrai_links(driver, links_negozi):
    celle = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "ecceSd", " " ))]').find_elements_by_class_name('a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd')
    for i in celle:
        links_negozi.append(i.get_attribute('href'))
    return links_negozi

def continua_view_celle(driver):
    coordinate = driver.current_url[driver.current_url.find('@')+1:].split(',')
    latitudine = coordinate[0]
    longitudine = coordinate[1]
    ris = (driver.find_element_by_id('ppdPk-Ej1Yeb-LgbsSe-tJiF1e').is_enabled()) and (float(longitudine)>=-75 and float(longitudine)<=-70)
    print(longitudine, driver.find_element_by_id('ppdPk-Ej1Yeb-LgbsSe-tJiF1e').is_enabled(), ris, end='\tLEN: ')  
    return ris


def init_driver(link, driver):
    driver.get(link)
    driver.maximize_window()
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label=\"Acconsento all'utilizzo dei cookie e di altri dati per le finalità descritte\"]"))).click()
    except Exception as e:
        print("\nnon trovo la pagina 'accept cookies'")
    return driver

def store_pages(link, driver):
    driver.execute_script("window.open('"+str(link)+"');")
    driver.maximize_window()
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label=\"Acconsento all'utilizzo dei cookie e di altri dati per le finalità descritte\"]"))).click()
    except Exception as e:
        print("\n\t\t\tnon trovo la pagina 'accept cookies' oppure è già stata gestita dalla funzione 'init_driver'\n")
    return driver