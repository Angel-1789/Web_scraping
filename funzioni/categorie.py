import bs4 # Beautiful Soup v4 -> libreria di websraping, ci permette di estrarre i dati dalle pagine HTML, pesino dati nascosti
import requests # libreria standard di Python per accedere ai siti web, tramitte richieste HTTP
import webbrowser # ci da la possibilità di aprire automaticamente il sito web su un browser a piacere
from funzioni.vai_a_page import vai_a_page

def trova_ultima_categoria(origin, key, origin_negozi):
    temp = key.split(";")
    ult_cat = temp[0]
    ult_sott_cat = temp[1] 
    
    # print(len(origin))
    # print(ult_cat)
    # print(ult_sott_cat)
    for sottocategoria in origin[ult_cat]:
        print(sottocategoria)
    keys = origin.keys()
    
    categoria_cercata = list(keys).index(ult_cat)
    print("\n1: ",categoria_cercata)
    print("\n",list(keys)[categoria_cercata:],"\n\n\tSOTTOCATEGORIA_CERCATA:\n")
    
# copy ultimo contenuto ultima_categoria
    index = 0
    copy = {}
    
    for sottocategoria in origin[ult_cat]:
        # print(sottocategoria)
        if sottocategoria[0] == ult_sott_cat:
            temp = (origin[ult_cat])[index:]
            
            ultimo_negozio = list(origin_negozi[key])[-1]
            page_ultimo_store = (((origin_negozi[key])[ultimo_negozio])[2])[0]    
            (temp[0])[1] = page_ultimo_store
            # print("\nCategoria: ",ult_cat,"\n\t\t",temp)
            copy[ult_cat] = temp
            break
        index+=1
        

    index = 0
# copia resto dizionario 
    for categoria in origin:
        if index > categoria_cercata:
            copy[categoria] = origin[categoria]
            # print("\nCategoria: ",categoria,"\n\t\t",origin[categoria])
        index +=1

    return copy

def estrai_categorie(LINK, PRE_LINK_ANNUNCIO, sec_errore):
    FILTRI_PAGINA = '?numberofreviews=0&status=all&timeperiod=0'
    
    soup = vai_a_page(str(LINK+FILTRI_PAGINA),sec_errore)

    # div contenente la lista delle categorie
    div_categorie = soup.find('div', class_ = 'styles_list__1wa5I')

    categorie = {}

    for categoria in div_categorie :
        lnk_categorie = []
        main_cat = categoria.find('h2').get_text()
        links_cate = categoria.find('ul').find_all('a')
        for lnk in links_cate:
            nome = lnk.get_text()
            lnk_cate = PRE_LINK_ANNUNCIO+str(lnk.get('href'))+FILTRI_PAGINA
            lnk_categorie.append([nome,lnk_cate])
        categorie[main_cat] = lnk_categorie
        
    return categorie