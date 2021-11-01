from datetime import timedelta, datetime

from fastapi import FastAPI, Header, Body, HTTPException
from pydantic import BaseModel
from redis import Redis

DEBUG = True
redis = Redis(host='localhost', port=6379, db=0)

app = FastAPI(title="change ip limit",
              version="0.0.1")


def request_is_limited(r: Redis, key: str, value: str, limit: int, period: timedelta):
    if r.scard(key) < limit:
        r.sadd(key, value)
        r.expire(key, int(period.total_seconds()))
        return False

    return True


class User(BaseModel):
    username: str


@app.post("/", tags=['get_client_data'], status_code=200)
async def ip_day_limit(user: User = Body(None),
                       X_Forwarded_For=Header(None)
                       ):
    '''rate limit by ip per day'''

    if DEBUG:
        period_time = timedelta(seconds=60)
        client_key = f"{user.username}_min_{datetime.now().minute}"
        print(client_key)

    else:
        period_time = timedelta(days=1)
        client_key = f"{user.username}_day_{datetime.today().day}"

    if request_is_limited(r=redis, key=client_key,
                          value=X_Forwarded_For,
                          limit=20, period=period_time):
        raise HTTPException(429, "Too Many Requests")

    return {"status": "ok", "ip": X_Forwarded_For}
