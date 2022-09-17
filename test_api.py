import requests


# url = "https://garbage-classify-2187015-1313534064.ap-shanghai.run.tcloudbase.com/get_device_info"
url = "http://39.105.109.174"

# data= {
#     "deviceUrl":"https://39.105.109.174"
# }
# data = {}
res = requests.post(url=url)
print(type(res.json()))