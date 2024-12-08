import uvicorn
#from dotenv import load_dotenv

import handler.lifespan
import handler.http
import handler.ws

def init():
  #load_dotenv()
  pass

async def app(scope, receive, send):
  if scope["type"] == "lifespan":
    await handler.lifespan.handle(scope, receive, send)
  elif scope["type"] == "http":
    await handler.http.handle(scope, receive, send)
  elif scope["type"] == "websocket":
    await handler.ws.handle(scope, receive, send)

if __name__ == "__main__":
  init()
  uvicorn.run("server:app",
    host="localhost",
    port=8000,
    workers=1,
    ws_max_queue=1,
    log_level="info",
  )
