import json
import requests
from bs4 import BeautifulSoup
from bs4 import Tag


url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")
count = 1
countries = soup.find_all("div", class_="col-md-4 country")
data = []
for country in countries:
    country_name = country.find("h3").get_text(strip=True)
    capital = country.find("span", class_="country-capital").get_text(strip=True)
    print(f"{count}. Country: {country_name}; Capital: {capital};")
    count += 1
    data.append({"country": country_name, "capital": capital})


with open("dump.json", "w+", encoding="utf-8") as file:
    json.dump(data, file, indent=3, ensure_ascii=False)


with open('template.html', 'r', encoding='utf-8') as file:
    filedata = file.read()

soup = BeautifulSoup(filedata, "html.parser")

element_to_paste = soup.find("bodytable", id="bodytable")


for idx, item in enumerate(data, start=1):
    new_el = Tag(name="tr")
    new_el['class'] = 'country'
    new_el.append(Tag(name="td"))
    new_el.contents[0].string = str(idx)
    new_el.append(Tag(name="td"))
    new_el.contents[1].string = item["country"]
    new_el.append(Tag(name="td"))
    new_el.contents[2].string = item["capital"]
    
    element_to_paste.append(new_el)


with open("Index.html", "w+", encoding="utf-8") as file:
    file.write(soup.prettify())