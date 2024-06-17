import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncpg_listen
import asyncio
import asyncpg
import time
import requests



async def handle_notifications(notification: asyncpg_listen.NotificationOrTimeout) -> None:
    requests.post("http://server2:8001/")
    print(f"{notification} has been received at {time.time()}")


@asynccontextmanager
async def mehere(app: FastAPI):
    listener = asyncpg_listen.NotificationListener(asyncpg_listen.connect_func(host="db",port="5432",user="postgres",password="postgres",database="postgres"))
    listener_task = asyncio.create_task(
        listener.run(
            {"the_notification_channel": handle_notifications},
            policy=asyncpg_listen.ListenPolicy.LAST,
            notification_timeout=3600
        )
    )
    print(listener_task)
    yield
    print('cancelling')
    listener_task.cancel()
    

app = FastAPI(lifespan=mehere)

@app.get("/")
async def read_root():
    connection = await asyncpg.connect(user="postgres")
    try:
        for i in range(42):
            await connection.execute(f"NOTIFY the_notification_channel, '{i}'")
    finally:
        await connection.close()
# @app.on_event("shutdown")
# async def main2():
#     print(listener_task_min)
#     listener_task_min.cancel()

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port= 8000)