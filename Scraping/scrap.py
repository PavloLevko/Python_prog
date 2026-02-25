import requests
from bs4 import BeautifulSoup

url = "https://allo.ua/ua/products/mobile/serija_smartfony-iphone_air/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

#Витягуємо заголовки (h2)
for h2 in soup.find_all("h2"):
    print(h2.text)


#Витягуємо ціни  (sum, price...)
prices = soup.find_all("span", class_="sum")


for price in prices:
    print(price.text)





