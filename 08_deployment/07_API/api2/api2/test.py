import requests
r = requests.get("http://localhost:4000/custom-greetings", params={"name":"Charles"})
print(r.content)