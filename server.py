from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    url = f"https://web.telegram.org/{path}"
    if request.query_string:
        url += "?" + request.query_string.decode()
    
    headers = {}
    for k, v in request.headers:
        if k.lower() not in ['host', 'origin', 'referer']:
            headers[k] = v
    
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True,
            timeout=15
        )
        excluded = ['content-encoding', 'transfer-encoding', 'content-length']
        response_headers = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded]
        return Response(resp.content, resp.status_code, response_headers)
    except:
        return Response("Ошибка", 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
