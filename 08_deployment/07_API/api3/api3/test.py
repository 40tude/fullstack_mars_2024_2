import requests

r = requests.get("http://localhost:4000/blog-articles/0")
print(r.content)