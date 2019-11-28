# -*- coding: ISO-8859-1 -*-
"""
Created on Thu Jun 14 16:25:39 2018

@author: nmito
"""

import urllib.request
import csv
import time, random

def csv_extract(filename, d=";"):
    with open(filename, 'r') as csvfile:
        data = []
        reader = csv.reader(csvfile, delimiter=d)
        for row in reader:
            data.append(row[0])
    return data

def csv_write(data, filename):
    u = ""
    with open(filename, 'w') as output:
        for r in data:
            for j in r:
                u = u + str(j) + ";"
            u = u+"\n"
        output.write(u)

adresses = csv_extract("adresses2.csv")
good_adresses = []
for n,a in enumerate(adresses):
    if len(a)==71:
        good_adresses.append(a)
   
extract = []
errors= []

for i in range(len(good_adresses)):
    try: 
        with open("export/"+str(i)+".html", 'r') as txt:
            pass
    except:
        print(i)
        site= good_adresses[i]
        
        if random.random()>0.5:
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'fr-FR,fr;q=0.8',
                   'Connection': 'keep-alive'}
        else:
            hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'fr-FR,fr;q=0.8',
                   'Connection': 'keep-alive'}
        
        req = urllib.request.Request(site, headers=hdr)
        #if random.random() > 0.9:
        #    reqbidon = urllib.request.Request("https://www.pagesjaunes.fr/annuaireinverse", headers=hdr)
        #    with urllib.request.urlopen(reqbidon) as f:
        #        time.sleep(0.5+random.random()*2)
        
        with open("export/"+str(i)+".html", 'w', encoding="utf-8") as txt:        
            try:
                with urllib.request.urlopen(req, timeout=15) as f:
                    contenu=f.read().decode('utf-8')
                    print(contenu[0:100])
                    extract.append(contenu)
                    time.sleep(4+random.random()*8)
                    txt.write(contenu)
            except:
                errors.append(i)
            time.sleep(random.random()*1)
    

