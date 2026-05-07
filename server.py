from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/<path:url>')
def proxy(url):
    target = "https://" + url
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'origin', 'referer']}
    try:
        resp = requests.get(target, headers=headers, cookies=request.cookies, allow_redirects=True, timeout=10)
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('content-type',''))
    except:
        return Response("Ошибка загрузки", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
