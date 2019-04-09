import requests

from bs4 import BeautifulSoup

from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify

from config import token


app = Flask(__name__)
sslify = SSLify(app)

URL = f"https://api.telegram.org/bot{token}/"


def get_search_result_stat(word):
    url = f'https://www.google.com/search?q={word}'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.find('div', {'id': 'resultStats'}).contents[0]
    data = data.split(' ')[-2]
    result = (data.encode('ascii', 'ignore')).decode('utf-8')

    return result


def send_message(chat_id, text='Wait, please...'):
    url = URL + 'sendMessage'
    reply = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=reply)
    return r.json()


@app.route(f'/{token}', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        text = r['message']['text']

        result = get_search_result_stat(text)

        reply = f'{result} results in Google for word \"{text}\" '
        send_message(chat_id, text=reply)

        return jsonify(r)
    return '<h1>LazukinTestBot</h1>'


if __name__ == '__main__':
    app.run()
