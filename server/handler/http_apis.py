import json
import sqlite3

# Check if we want to call an API
def is_api(path):
  return path.startswith("/api/")

# Utility to get an attraction's details by its database id
def get_attraction(id):
  connection = sqlite3.connect("data/attractions.db")
  cursor = connection.cursor()
  rows = cursor.execute("SELECT name, description, category, rating, hours, duration, address, url FROM attraction a,image i WHERE a.id=? and a.id=i.attraction_id", (id,))
  for (name, description, category, rating, hours, duration, address, url) in rows:
    attraction = {
      "id": id,
      "name": name,
      "description": description,
      "category": category,
      "rating": rating,
      "hours": hours,
      "duration": duration,
      "address": address,
      "image": url,
    }
    cursor.close()
    connection.close()
    return attraction

  return {}

# Handle HTTP api requests
async def handle(path, body, send):
  handler = APIS.get(path)
  if handler:
    return await handler(body, send)
  return False

# Get attraction details by its database id
async def handle_attraction(body, send):
  try:
    data = json.loads(body)
    id = data.get("id", None)
  except:
    id = ""
  if id:
    attraction = get_attraction(id)
    await send({
      "type": "http.response.start",
      "status": 200,
      "headers": [
        [b"content-type", b"application/json"],
        [b"access-control-allow-origin", b"http://localhost:3000"], # for CORS during dev
      ],
    })
    await send({
      "type": "http.response.body",
      "body": json.dumps(attraction).encode("utf-8")
    })
    return True
  return False

APIS = {
  "/api/attraction": handle_attraction
}

