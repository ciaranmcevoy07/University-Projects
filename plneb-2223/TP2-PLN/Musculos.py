import requests
from bs4 import BeautifulSoup
import json
import re


url = "https://pt.wikipedia.org/wiki/Lista_de_m%C3%BAsculos_do_corpo_humano"
page_html = requests.get(url).text
page_html = BeautifulSoup(page_html, "html.parser")
soup = page_html.find_all("div", class_='mw-parser-output')

title = ""
for ele in soup:
    ul_elements = ele.find_all("ul")  # Find all 'ul' elements within the current 'div' element
    for ul in ul_elements:
        li_elements = ul.find_all("li")  # Find all 'li' elements within the current 'ul' element
        for li in li_elements:
            if li.text not in title:
                title = title + li.text + "\n"

title = re.sub(r"(\(\d.*)", r"", title)
title = title.split("\n")

print(title)

file = open("Musculos.json", "w", encoding="utf-8")
json.dump(title, file, ensure_ascii=False, indent= 4)
file.close()