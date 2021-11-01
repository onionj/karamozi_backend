
from time import localtime, strftime
from flask import Flask, request, make_response

from requests.exceptions import Timeout,  ConnectionError
import requests
import jsonlines

app = Flask(__name__)


def save_jsonl(json_data):
    '''save Dict to requests_body.jsonl'''

    time_str = str(strftime("%d-%m-%Y %H-%M-%S", localtime()))
    json_data.update({'_LogTime': time_str})

    with jsonlines.open('requests_body.jsonl', mode='a') as writer:
        writer.write(json_data)


@app.route("/", methods=['POST'])
def reverse_proxy():
    body = request.json
    if body:
        save_jsonl(body.copy())

    response_body = 'Internal Server Error'
    response_status_code = 500
    try:
        response = requests.post('http://127.0.0.1:8000',
                                 json=body,
                                 headers=request.headers,
                                 timeout=20
                                 )

        response_status_code = response.status_code
        response_body = response.json()

    except Timeout:
        response_status_code = 504
        response_body = 'Gateway Timeout'

    except ConnectionError:
        response_status_code = 503
        response_body = 'Service Unavailable'

    except Exception:
        response_status_code = 500
        response_body = 'Internal Server Error'

    return make_response(response_body, response_status_code)


if __name__ == "__main__":
    app.run()
