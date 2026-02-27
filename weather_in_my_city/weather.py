import requests

city = "London"

#wttr.in - це відкритий API який дозволяє отримувати погоду у вашому місті.
url = f"https://wttr.in/{city}?format=4"

result = requests.get(url)

print("Надсилаємо запит до сервера...")
print(result.text)