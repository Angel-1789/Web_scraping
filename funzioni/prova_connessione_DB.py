import pymongo

CL_Mongo = "mongodb+srv://angel:Progetto_web_scraping@webscraping.qwsu7.mongodb.net/test?authSource=admin&replicaSet=atlas-9a8hek-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"

client = pymongo.MongoClient(CL_Mongo)
db = client['WebScraping']
col = db['test1']

print("DB names\n",client.list_database_names())
print("DB collections names\n",db.list_collection_names())