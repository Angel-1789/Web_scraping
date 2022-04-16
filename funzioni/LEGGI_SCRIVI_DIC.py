import json
# import os, datetime
PATH_FILE = "../files_web_scraping/"

#   ------------------------------------------------------------------------------------------------------     CATEGORIE
def carica(nome_dic):
    print(nome_dic, end ='')
    with open(PATH_FILE+nome_dic.lower()+".json") as f:
        dic = json.loads(f.read())
    return dic

def carica_v2(nome_dic,path):
    print(nome_dic, end ='')
    with open(path+nome_dic.lower()+".json") as f:
        dic = json.loads(f.read())
    return dic

def salva(dic,nome_dic):
    with open(PATH_FILE+nome_dic.lower()+".json","w") as f:
        f.write(json.dumps(dic))

def salva_dic(dic, nome):
    print("\n\tpreparo file per il salvataggio del file:  %s   ......   "%(nome),end='')
    salva(dic,nome)
    print("\tfile salvato")
    
# -------------------------------------------------------------------------------------
def salva_v2(obj, nome,path):
    print("\n\tpreparo file per il salvataggio del file:  %s   ......   "%(nome),end='')
    with open(path+nome.lower()+".json","w") as f:
        f.write(json.dumps(obj))
    print("\tfile salvato")
    

#   ------------------------------------------------------------------------------------------------------  NEGOZI
# def salva(dic,nome_dic):
#     print("\nFILE SALVA")
#     h = (str(datetime.datetime.now())[:19]).replace(' ','_').replace(':','')
#     with open("./file/"+nome_dic+"/"+nome_dic.lower()+"_"+h+".json","w") as f:
#         f.write(json.dumps(dic))
#     print("FINE FILE SALVA")

# def carica(nome_dic):
#     max_file = [datetime.datetime.strptime('1990-01-01_000000','%Y-%m-%d_%H%M%S'),'']

#     for file in os.listdir("./file/"+nome_dic.lower()):
#         if (file.lower()).startswith(nome_dic.lower()):
#             data = file[(file.find('_')+1):file.find('.')]
#             time = datetime.datetime.strptime(data,'%Y-%m-%d_%H%M%S')
#             # print(file,"\t",data,"\t",time)
#             if time > max_file[0]:
#                 max_file[0] = time
#                 max_file[1] = file

#     print("FILE CARICA")
#     with open("./file/"+nome_dic.lower()+"/"+max_file[1]) as f:
#         print(f)
#         dic = json.loads(f.read())
#     print("FINE FILE CARICA")
#     return dic

# def salva_dic(dic, nome):
#     print("\n\tpreparo file per il salvataggio del dizionario %s   ......   "%(nome),end='')
#     salva(dic,nome)
#     print("\tfile salvato")