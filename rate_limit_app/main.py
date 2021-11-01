from time import sleep
from flask import Flask, request, make_response

from requests.exceptions import Timeout,  ConnectionError
import requests

# rate limit
from datetime import timedelta
from redis import Redis


def request_is_limited(r: Redis, key: str, limit: int, period: timedelta):
    if r.setnx(key, limit):
        r.expire(key, int(period.total_seconds()))

    bucket_val = r.get(key)

    if bucket_val and int(bucket_val) > 0:
        r.decrby(key, 1)
        return False
    return True


redis = Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)


@app.route("/", methods=['POST'])
def reverse_proxy():

    response_body = 'Too Many Requests'
    response_status_code = 429

    try:
        if not request_is_limited(r=redis, key=request.headers['X-Forwarded-For'],
                                  limit=100, period=timedelta(seconds=60)):

            response = requests.post('http://127.0.0.1:6000',
                                     json=request.json,
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
    app.run(debug=True)
