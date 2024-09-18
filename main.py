import traceback

import toml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ff3 import FF3Cipher
from pydantic import BaseModel

import random

class Text(BaseModel):
    text: str

config_path = "./config.toml"

cfg_read = toml.loads(open(config_path, 'r', encoding='utf-8').read())


key = cfg_read['secret']['key']
tweak = cfg_read['secret']['tweak']
alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
c = FF3Cipher.withCustomAlphabet(key, tweak, alphabet)


def random_string(length: int) -> str:
    return ''.join(random.choices(alphabet, k=length))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/encrypt/')
async def encrypt(text: Text):
    try:
        j_t = random_string(2) + ':'+text.text+':' + random_string(2)
        texts = []
        # split text for each 28 characters
        for i in range(0, len(j_t), 28):
            texts.append(j_t[i:i+28])
        if len(texts[-1]) < 4:
            texts[-1] = texts[-1].ljust(4, '0')
        encrypted_texts = []
        for t in texts:
            encrypted_texts.append(c.encrypt(t))
        return {"encrypted": ''.join(encrypted_texts)}
    except Exception:
        fm  = traceback.format_exc()
        print(fm)
        return JSONResponse(status_code=500, content={
            "detail": "Internal Server Error",
            "message": fm
        })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=cfg_read['secret'].get('port', 5000), log_level="info")