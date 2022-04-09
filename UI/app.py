from flask import Flask,render_template,request,jsonify
import requests
#from chat import get_response
#import  coffee.qa_predict
#import re
app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("index.html")

@app.post("/predict")
def predict():
    input_message = request.get_json().get("message")
    # TODO: check if text is valid
    output_message = []
    try:
      payload = {
                "sender": "test_user",
                "message": input_message
            }
      r= requests.post('http://localhost:5005/webhooks/rest/webhook', json=payload)
      for i in r.json():
        output_message.append(i['text'])
    except:
      output_message = 'There is an exception'
    message = {"answer": output_message}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)