# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 10:45:29 2018

@author: nmito
"""

from bs4 import BeautifulSoup

def csv_write(data, filename):
    u = ""
    with open(filename, 'w',  encoding="utf-8") as output:
        for r in data:
            for j in r:
                u = u + str(j) + ";"
            u = u+"\n"
        output.write(u)

data = []
k=0

while 1:
    try:
        with open("export/"+str(k)+".html", "r",  encoding="utf-8") as file:
        #with open("export/11.html", "r") as file:
            content = file.read()
            if len(content)>0:
                if len(content)>35000:
                    soup = BeautifulSoup(content, 'html.parser')
                    numero = soup.h1.strong.get_text()
                    titre = soup.find_all("header")[1].div.h2.find_all("a")[1].get_text().strip()
                    adresse = soup.find_all("header")[1].find_all("div")[2].a.get_text().strip()
                    if "\navis" in adresse:
                        adresse = soup.find_all("header")[1].find_all("div")[-2].a.get_text().strip()
                        print("#"+str(k), numero, titre,adresse)
                    data.append([numero, titre,adresse])
                else:
                    numero = soup.h1.strong.get_text()
                    #print("#"+str(k), numero, "Numéro sans correspondance")
                    data.append([numero, "No result", "No result"])
            else:
                #print("Fichier vide.")
                pass
        k=k+1
    except:
        break
    
csv_write(data, "output num and adress3.csv")