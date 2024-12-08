import handler.http_files as file_handler
import handler.http_apis as api_handler

# Handle HTTP requests
async def handle(scope, receive, send):
  path = scope["path"]

  handled = False

  # Get posted body
  body = b""
  more = True
  while more:
    message = await receive()
    body += message.get("body", b"")
    more = message.get("more_body", False)
  body = body.decode("utf-8")

  # Assume index.html
  if path == "/":
    path = "/index.html"

  # Do we have any APIs?
  if api_handler.is_api(path):
    handled = await api_handler.handle(path, body, send)

  # Serve files
  if not handled and file_handler.is_file(path):
    handled = await file_handler.handle(path, body, send)

  # Handle 404
  if not handled:
    await send({
      'type': 'http.response.start',
      'status': 404,
      'headers': [ [b'content-type', b'text/plain'] ],
    })
    await send({
      'type': 'http.response.body',
      'body': 'not found'.encode('utf-8'),
    })

