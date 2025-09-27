from bs4 import BeautifulSoup
import requests
import json

def getDiseasePage(url):
    page_html = requests.get(url).text
    page_soup = BeautifulSoup(page_html, "html.parser")
    page_div = page_soup.find("div", class_="field-name-body")
    return str(page_div)

def getDiseaseInfo(div):
    title = div.div.h3.a.text
    desc = div.find("div", class_="field-content").text
    return title,desc

url = "https://www.atlasdasaude.pt/doencasAaZ"
url2 = "https://www.atlasdasaude.pt"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

divs = soup.find_all("div", class_="views-summary views-summary-unformatted")

urls = []
for div in divs:
    urls.append(url2 + div.a["href"])

lista = []
for u in urls:
    print(u)
    html_=requests.get(u).text
    soup_=BeautifulSoup(html_,"html.parser")
    divs = soup_.find_all("div", class_="views-row")
    for div in divs:
        page_url= url2 + div.div.h3.a["href"]
        page_info = getDiseasePage(page_url)
        title, desc = getDiseaseInfo(div)
        lista.append({title:{"desc":desc,"page":page_info}})
file = open("doencas.json", "w", encoding="utf-8")
json.dump(lista,file, ensure_ascii=False, indent = 4)
file.close()