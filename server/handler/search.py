import sqlite3
import pandas as pd
import numpy as np
import pickle

from sentence_transformers import SentenceTransformer, util
import faiss

# TODO: use model instead of raw database query
from model import Review, Attraction

encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Look for attractions in the database
# Then rank them by the interests using vector similarity
def search_attractions(city:str, interests:str) -> str:
  connection = sqlite3.connect("data/attractions.db")
  cursor = connection.cursor()

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
  k = 10 # Top k results
  (distances, approx_nearest_neighbor) = document_index.search(search_vector, k=k)
  ranked_results = []
  for id in [ids[row] for row in approx_nearest_neighbor[0]]:
    row = cursor.execute("SELECT name, description FROM attraction WHERE id=?", (id,))
    (name, description) = next(row)
    ranked_results.append({
      "id": id,
      "name": name,
      "description": description,
    })
  cursor.close()
  connection.close()

  return ranked_results
