import uvicorn
import streamsync.serve
from fastapi import FastAPI, Response

mode = "run" # run or edit

root_asgi_app = FastAPI()
sub_asgi_app_1 = streamsync.serve.get_asgi_app(".", "run")
sub_asgi_app_2 = streamsync.serve.get_asgi_app("../tutorial", "run")

root_asgi_app.mount("/testapp", sub_asgi_app_1)
root_asgi_app.mount("/tutorial", sub_asgi_app_2)

@root_asgi_app.get("/")
async def init():
    return Response("""
    <h1>Welcome to the App Hub</h1>
    """)

uvicorn.run(root_asgi_app,
    host="0.0.0.0",
    port=5328,
    log_level="warning",
    ws_max_size=streamsync.serve.MAX_WEBSOCKET_MESSAGE_SIZE)