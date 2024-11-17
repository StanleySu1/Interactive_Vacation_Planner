import os
import json
from sentence_transformers import SentenceTransformer, util
import sqlite3
import pickle

import pandas as pd
import numpy as np
import faiss

from model import Review, Attraction

import ollama

tools=[{
  "type":"function",
  "function":{
    "name":"search",
    "description":"Search for potential attractions of interest",
    "parameters":{
      "type":"object",
      "properties":{
        "city":{
          "type":"string",
          "description":"The name of the city. Use only the full name of the city: Amsterdam, Barcelona, Dubai, Lisbon, London, Marrakech, New York City, Paris, Rome, Las Vegas",
        },
        "interests":{
          "type":"string",
          "description":"The type of attractions the traveller is interested in",
        }
      },
      "required": ["city", "interests"]
    }
  }
}]

messages=[
{
  "role": "system",
  "content": """
You are a travel concierge, adept at recommending activities for a visitor. You will enter into a conversation with the traveller.  Start a friendly conversation by introducing yourself as "Bob". Then ask the following questions to find out where the traveller is going to and what types of activities they're interested in. You only know have information on the following cities:
Amsterdam, Barcelona, Dubai, Lisbon, Lonndon, Marrakech, New York City, Paris, Rome, Las Vegas
""",
},
{
  "role": "assistant",
  "content": "How may I help you."
},
]

def search(city:str, interests:str) -> str:
  connection = sqlite3.connect("data/attractions.db")
  cursor = connection.cursor()

  encoder = SentenceTransformer("all-MiniLM-L6-v2")

  # Get the city from the database
  print(city, interests)
  ids = []
  embeddings = []
  rows = cursor.execute("SELECT attraction.id, attraction.embedding FROM city, attraction WHERE city.id=attraction.city_id AND city.name=?", (city,))
  for (id, embedding) in rows:
    ids.append(id)
    embeddings.append(pickle.loads(embedding))
  embeddings = np.array(embeddings).astype(np.float32)

  # Build embeddings on the fly and index
  vector_dimension = embeddings.shape[1]
  document_index = faiss.IndexFlatL2(vector_dimension)
  faiss.normalize_L2(embeddings)
  document_index.add(embeddings)

  # The search vector
  search_vector = np.array([encoder.encode(interests)])
  faiss.normalize_L2(search_vector)

  # Search
  k = 10
  (distances, approx_nearest_neighbor) = document_index.search(search_vector, k=k)
  text = "Here are some interesting attractions:\n\n"
  for id in [ids[row] for row in approx_nearest_neighbor[0]]:
    row = cursor.execute("SELECT name, description FROM attraction WHERE id=?", (id,))
    (name, description) = next(row)
    text += f"Attraction Name: {name}\nDescription: {description}\n\n"
  cursor.close()
  connection.close()

  return text

available_tools = {
  "search":search
}

def chat():
  global messages

  response = ollama.chat(
    model="llama3.2",
    messages=messages,
    tools=tools,
    options={
      "temperature": 0
    },
    stream=False,
  )

  if response["message"].get("tool_calls"):
    for tool in response["message"]["tool_calls"]:
      fn_call = available_tools[tool["function"]["name"]]
      fn_args = tool["function"]["arguments"]
      fn_response = fn_call(**fn_args)
      messages.append({
        "role": "tool",
        "content": fn_response,
      })
    return False
  else:
    messages.append({
      "role": "assistant",
      "content": response["message"]["content"],
    })
    print(response["message"]["content"])
    return True

if __name__ == "__main__":
  while True:
    if chat():
      msg = input("> ")
      messages.append({
        "role": "user",
        "content": msg,
      })
