import requests

r = requests.get("https://api.modrinth.com/")
print(r.text)