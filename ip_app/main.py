from typing import Optional, Dict
from fastapi import FastAPI, Header, Body

app = FastAPI(title="IP app",
              version="0.0.2")


@app.post("/", tags=['get_client_data'])
async def get_ip(user_data: Optional[Dict] = Body(None),
                 X_Forwarded_For: Optional[str] = Header(None)):

    output = {'ip': X_Forwarded_For}
    if user_data:
        output.update(user_data)
    return output
