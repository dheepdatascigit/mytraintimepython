import requests

response = requests.get("https://randomuser.me/api/")
out = response.json()
print(out["results"])

for i in out["results"]:
    print(i)

