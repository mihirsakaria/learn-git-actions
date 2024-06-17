import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncpg_listen
import asyncio
import asyncpg
import time
import requests



app = FastAPI()

@app.post("/")
async def read_root():
    print(f"received a notification at {time.time()}")

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port= 8001)