import bs4 # Beautiful Soup v4 -> libreria di websraping, ci permette di estrarre i dati dalle pagine HTML, pesino dati nascosti
import requests # libreria standard di Python per accedere ai siti web, tramitte richieste HTTP
import webbrowser # ci da la possibilità di aprire automaticamente il sito web su un browser a piacere
import time

def vai_a_page(LINK, pausa_errore):
    no_problem = False

    while no_problem is False:
        try:
            response = requests.get(LINK)
            response.raise_for_status() # genera un'eccezione se la risposta è in stato di errore
            soup = bs4.BeautifulSoup(response.text, 'html.parser') #Estraiamo il testo dalla risposta. Il testo è in formato html e lo salviamo in una variabile soup
            no_problem = True
        except requests.exceptions.HTTPError as err:
            print("\n\nPAUSA ERRORE DI ",pausa_errore," SECONDI")
            print(err)
            time.sleep(pausa_errore)
            print("\n\t\tFINE PAUSA\n%17s"%(' '),end='\t\t\t\t')
            
    return soup