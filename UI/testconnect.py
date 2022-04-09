from sanic import json
import requests

print('hello world')


url = 'http://0.0.0.0:5005/webhooks/rest/webhook'

payload = {
    "sender":"test_user",
    "message": "I want a cup of coffee"
}


r = requests.post(url, json = payload)
#rget = requests.get('http://0.0.0.0:5005/domain')
#print(rget.content )
#print(type(rget.content))
for i in r.json():
    print(i['text'])
print(r.status_code)
print(r.content)