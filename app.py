from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

@app.route('/webhook', methods=['GET'])
def verify():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if token == VERIFY_TOKEN:
        return challenge, 200

    return 'Wrong token', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    try:
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        sender = msg['from']
        text = msg['text']['body'].lower()

        if 'hello' in text:
            answer = 'Hello! I am your WhatsApp bot.'
        elif 'hi' in text:
            answer = 'Hi there!'
        else:
            answer = 'You said: ' + text

        requests.post(
            f'https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages',
            headers={
                'Authorization': f'Bearer {TOKEN}',
                'Content-Type': 'application/json'
            },
            json={
                'messaging_product': 'whatsapp',
                'to': sender,
                'type': 'text',
                'text': {'body': answer}
            }
        )
    except Exception as e:
        print(e)

    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
