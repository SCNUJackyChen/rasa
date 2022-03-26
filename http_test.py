import requests
from sanic import json

url = "http://localhost:5005/model/parse"

payload = {"text":"hi"}

r = requests.post(url, json=payload)

print(r.status_code)
print(r.content)