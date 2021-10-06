import requests

response = requests.get("https://randomuser.me/api/")
out = response.json()
print(len(out["results"]))

for i in out["results"][0]:
    print(i, out["results"][0][i], '\n')

