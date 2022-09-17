import requests


url = "http://39.105.109.174"

data= {
}

res = requests.post(url=url, data=data)
print(res.json())