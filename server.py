from flask import Flask, request, Response
import requests

app = Flask(__name__)

SITES = {
    'tg': 'https://web.telegram.org',
    'yt': 'https://youtube.com',
}

@app.route('/<site>/<path:url>')
def proxy(site, url):
    if site not in SITES:
        return "Неизвестный сайт", 404
    target = f"{SITES[site]}/{url}"
    try:
        resp = requests.get(target, timeout=15)
        return Response(resp.content, status=resp.status_code)
    except:
        return Response("Ошибка", 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
