from flask import Flask
import requests
import proxy.converter as conv


app = Flask('Habr-Proxy')
port = 8080
habr_url = 'https://habrahabr.ru/'


# Transform urls from 'https://habrahabr.ru/article...' to
# 'localhost:{port}/article...' and change pages
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    req = requests.get(habr_url + path)
    return conv.transform_request(req.content, port)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
