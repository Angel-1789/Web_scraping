import json

def salva(dic,nome_dic):
    with open("./file/"+nome_dic+".json","w") as f:
        f.write(json.dumps(dic))
        
def carica(nome_dic):
    print("./file/"+nome_dic+".json")
    with open("./file/"+nome_dic+".json") as f:
            dic = json.loads(f.read())
    return dic

def salva_dic(dic, nome):
    print("\n\tpreparo file per il salvataggio del dizionario %s   ......   "%(nome),end='')
    salva(dic,nome)
    print("\tfile salvato")
