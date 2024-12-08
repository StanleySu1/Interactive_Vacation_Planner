
async def handle(scope, receive, send):
  while True:
    message = await receive()
    if message['type'] == 'lifespan.startup':
      await send({'type': 'lifespan.startup.complete'})
      #initialize()
    elif message['type'] == 'lifespan.shutdown':
      await send({'type': 'lifespan.shutdown.complete'})

