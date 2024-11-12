import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from schemes import MarkupResponse
import os
from os.path import dirname
import sys


# sys.path.append(dirname('/model'))
# from model.model_api import model_api


BACKEND_URL = os.getenv('BACKEND_URL', default='/')

app = FastAPI(root_path='/')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["0.0.0.0", "localhost", "127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/predict/markup', response_model=MarkupResponse)
async def train_on_syntetic_dataset(text: str):
    # response = model_api(text)
    # print(response)
    # return response
    return None

from fastapi.responses import JSONResponse
@app.get('/test')
async def test():
    return JSONResponse(content='1234567890')

if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0')
