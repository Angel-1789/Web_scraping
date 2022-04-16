import pymongo
from pymongo import MongoClient
import os.path
import sys
from funzioni.LEGGI_SCRIVI_DIC import *

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:',sys.argv[i])

if len(sys.argv)==2:
    source = sys.argv[1]
    print("source: ",source)
    
    if os.path.exists("../files_web_scraping/Reviews/"+source+".json") == "False":
        sys.exit("Il nome del file passato come parametro non esiste!!")
else:
    sys.exit("inserire solo il nome del file delle reviews che si vogliono caricare al DB")
    
NOME_FILE_REVIEWS = source

CL_Mongo = "mongodb+srv://angel:Progetto_web_scraping@webscraping.qwsu7.mongodb.net/test?authSource=admin&replicaSet=atlas-9a8hek-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"

cluster = pymongo.MongoClient(CL_Mongo)
# print("DB names\n",cluster.list_database_names())
# print("DB collections names\n",db.list_collection_names())

db = cluster["WebScraping"]

# -------------------------------    NEGOZI
# def carica_negoziDB(nome_file):
#     collection_negozi = db["negozi"]
#     negozi_salvati = carica(nome_file)

#     count = 0
#     negozi_DB = []
#     for i in negozi_salvati:
#         for x in negozi_salvati[i]:
#             count+=1
#             temp = i.split(";")
#             negozi_DB.append({"Negozio": x, "categoria":temp[0], "sottocategoria":temp[1]})

#     collection_negozi.insert_many(negozi_DB)

# -------------------------------    REVIEWS
def carica_reviewsDB(nome_file):
    collection_reviews = db["reviews"]
    reviews_salvate = carica_v2(nome_file,"../files_web_scraping/Reviews/")

    # count = 0
    reviews_DB = []
    for i in reviews_salvate:
        temp = i.split(";")
        for x in reviews_salvate[i]:
            reviews_DB.append({"contenuto":x, "Negozio":temp[0], "Indirizzo":temp[1]})

    collection_reviews.insert_many(reviews_DB)
    print("caricamento effettuato: %s reviews"%(str(len(reviews_DB))))
    
# carica_negoziDB(nome_file)
carica_reviewsDB(NOME_FILE_REVIEWS)