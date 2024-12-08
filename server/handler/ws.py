import asyncio
import json

import ollama
from ollama import AsyncClient

import handler.search as search

# Fetch attractions for a city (if applicable) and make a RAG prompt
def augment_city_search(messages):
  if messages[-1]["role"] == "user":
    # Save previous prompt
    last_message = messages[-1]
    prompt = messages[-1]["content"]

    # Replace last message with a new prompt
    messages[-1] = {
      "role": "user",
      "content": """This is my request:
""" + prompt + """

If it references a city and/or interest, return a JSON. Do not add additional commentary. Be concise. Output the JSON like this:
{
  "city": "<city name>",
  "interests": ["<interest1>","<interest2"]
}
If the request does not refer to a city and/or interest, just say this:
{
}
"""
    }
    response = ollama.chat(
      model="llama3.2",
      messages=messages,
      options={
        "temperature": 0.0,
      },
      stream=False,
    )
    try:
      data = json.loads(response["message"]["content"])
      if data.get("city"):
        ranked_results = search.search_attractions(data["city"], " ".join(data["interests"]))
        # Add the list of potential attractions for RAG
        text = "Here are some interesting attractions that the user might be interested in:\n\n"
        text += "\n\n".join([f"Attraction ID: {result['id']}\nAttraction Name: {result['name']}\nDescription: {result['description']}" for result in ranked_results])
        text += "\n\nUse the above results to answer the follow query from the user."
        messages.insert(-1, {
          "role": "system",
          "content": text,
        })
    except:
      pass

    # Replace last prompt with the original one
    messages[-1] = last_message
  return messages

# Get a list of attractions in JSON format that were mentioned so far
def get_mentioned_cities(messages):
  get_json_messages = messages[:]
  get_json_messages.append({
    "role": "user",
    "content": """Create a JSON of all the attractions that you (as an assistant) mentioned. Do not add additional commentary. Be concise. Output the JSON like this:
[
  {"id":<id>,"name":"<attraction1>"},
  {"id":<id>,"name":"<attraction2>"}
]
"""
  })
  response = ollama.chat(
    model="llama3.2",
    messages=get_json_messages,
    options={
      "temperature": 0.0,
    },
    stream=False,
  )
  try:
    attractions = json.loads(response["message"]["content"])
    return attractions
  except:
    pass

  return None

# Handle websockets
async def handle(scope, receive, send):
  path = scope["path"]
  message = await receive()
  await send({
    "type": "websocket.accept"
  });
  message = await receive()
  if message["type"] == "websocket.receive":
    json_data = json.loads(message["text"])
    messages = json_data.get("messages")

    # Apply RAG for attractions in a city
    augment_city_search(messages)

    # Stream
    full_text = ""
    async for part in await AsyncClient().chat(
        model="llama3.2",
        messages=messages,
        options={
          "temperature": 0.1,
        },
        stream=True,
      ):
      chunk = part["message"]["content"]
      if chunk:
        full_text += chunk
        #print(chunk, end="", flush=True)
        await send({
          "type": "websocket.send",
          "text": json.dumps({"chunk":chunk})
        })
        # This yields and makes it stream on chrome
        await asyncio.sleep(0)

    # Send back the final result
    messages.append({
      "role": "assistant",
      "content": full_text,
    })
    await send({
      "type": "websocket.send",
      "text": json.dumps({
        "messages": messages,
      })
    })
    await asyncio.sleep(0)

    # Now get a JSON of the cities in the last result
    attractions = get_mentioned_cities(messages)
    if attractions:
      await send({
        "type": "websocket.send",
        "text": json.dumps({
          "attractions": attractions
        })
      })
      await asyncio.sleep(0)

  await send({
    "type": "websocket.close",
  })

