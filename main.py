import traceback

import toml
from ff3 import FF3Cipher
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseModel

class Text(BaseModel):
    text: str

config_path = "./config.toml"

cfg_read = toml.loads(open(config_path, 'r', encoding='utf-8').read())


key = cfg_read['secret']['key']
tweak = cfg_read['secret']['tweak']
c = FF3Cipher.withCustomAlphabet(key, tweak, "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")

app = FastAPI()


@app.post('/encrypt/')
async def encrypt(text: Text):
    try:
        return {"encrypted": c.encrypt(text.text)}
    except Exception:
        return JSONResponse(status_code=500, content={
            "detail": "Internal Server Error",
            "message": traceback.format_exc()
        })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=cfg_read['secret'].get('port', 5000), log_level="info")