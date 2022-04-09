import requests
from sanic import json

# url = "http://localhost:5005/model/parse"
url = "http://localhost:5005/webhooks/rest/webhook"

payload = {
  "sender": "test_user",  # sender ID of the user sending the message
  "message": "kopi ccc"
}

r = requests.post(url, json=payload)

print(r.status_code)
print(r.content)
