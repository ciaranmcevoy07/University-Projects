from bs4 import BeautifulSoup
import requests
import json
import re

def getDiseasePage(url):
    page_html = requests.get(url).text
    page_soup = BeautifulSoup(page_html, "html.parser")
    div = str(page_soup.find("div", class_="entry-content"))
    headings = page_soup.find_all("h2")
    div = div.splitlines()
    return headings, div

url = "https://www.mdsaude.com/doencas-a-z/"
url2 = "https://www.mdsaude.com/"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")
new = []

divs = soup.find_all("div", class_="entry-content")
for i in divs:
    new_i = str(i)
sent = re.findall(r"(?<=<li>)(.+)(?=</li>)", new_i)
listaurls = []
listaterms = []
for i in sent:
    urls = re.search(r'(?<=www.mdsaude.com/)(.+)(?=")', i)
    if urls:
        u = urls.group()
        listaurls.append(u)
    terms = re.search(r'(?<=>)(.+)(?=<)', i)
    if terms:
        t = terms.group()
        listaterms.append(t)
dict = {}
for u, t in zip(listaurls, listaterms):
    urldisease = url2 + u
    headings, div = getDiseasePage(urldisease)
    if t not in dict:
        dict[t] = {} 
    for h in headings:
        text = ''
        count = 0
        for i in div:
            if str(h) in i:
                while count != -1:
                    count +=1
                    position = div.index(i)
                    match = re.search(r"(?<=<p>)(.*)(?=</p>)", div[position+count])
                    match2 = re.search(r"h3", div[position+count])
                    if match:
                        frase = match.group()
                        text += frase
                    else:
                        if match2:
                            print()
                        else:
                            break
        dict[t][h.text] = text




file = open("mdsaude.json", "w", encoding="utf-8")
json.dump(dict,file, ensure_ascii=False, indent = 4)
file.close()