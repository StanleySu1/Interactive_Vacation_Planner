import os

CONTENT_TYPES = {
  ".html" : b"text/html",
  ".htm" : b"text/html",
  ".css" : b"text/css",
  ".txt" : b"text/plain",
  ".js" : b"text/javascript",
  ".json" : b"application/json",
  ".png" : b"image/png",
  ".jpg" : b"image/jpeg",
  ".ico" : b"image/x-icon",
}

# Check whether the path points to a file
def is_file(path):
  full_path = "client/build/" + path
  return os.path.exists(full_path) and ".." not in full_path

# Handle file requests
async def handle(path, body, send):
  full_path = "client/build/" + path
  ext = os.path.splitext(path)[1]
  # Serve the file
  await send({
    "type": "http.response.start",
    "status": 200,
    "headers": [ [b"content-type", CONTENT_TYPES.get(ext, b"text/plain")] ],
  })
  try:
    with open(full_path, "rb") as fh:
      data = fh.read()
      await send({
        "type": "http.response.body",
        "body": data,
      })
      return True
  except:
    pass

  return False
