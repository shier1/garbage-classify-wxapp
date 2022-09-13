import requests


url = "https://garbage-classify-2187015-1313534064.ap-shanghai.run.tcloudbase.com/user_login"

data= {
  "userAccount": "test",
  "userPassword": "1234567890123456"
}

res = requests.post(url=url, data=data)
print(res.content)