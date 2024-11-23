import os
import json
from sentence_transformers import SentenceTransformer, util
import pickle
import sqlite3

from model_yelp import Review, Attraction
from pydantic_core import from_json

PATH = "data/scraped/yelp"

connection = sqlite3.connect("data/attractions_yelp.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS city")
cursor.execute("DROP TABLE IF EXISTS attraction")
cursor.execute("DROP TABLE IF EXISTS review")
cursor.execute("CREATE TABLE city (id PRIMARY KEY, name TEXT, key TEXT)")
cursor.execute("CREATE TABLE attraction (id PRIMARY KEY, city_id INTEGER, name TEXT, category TEXT, rating NUMBER, hours TEXT, address TEXT, embedding BLOB)")
cursor.execute("CREATE TABLE review (id PRIMARY KEY, attraction_id INTEGER, review TEXT, rating NUMBER, visited TEXT)")

encoder = SentenceTransformer("all-MiniLM-L6-v2")

CITIES = (
  ("amsterdam", "Amsterdam"),
  ("dubai", "Dubai"),
  ("london", "London"),
  ("nyc", "New York City"),
  ("rome", "Rome"),
  ("barcelona", "Barcelona"),
  ("lisbon", "Lisbon"),
  ("marrakech", "Marrakech"),
  ("paris", "Paris"),
  ("vegas", "Las Vegas"),
)

unique_review_id = 0
for (city_id, (key, name)) in enumerate(CITIES):
  print(name)
  cursor.execute("INSERT INTO city VALUES (?,?,?)", (city_id, name, key))
  with open(os.path.join(PATH, f"{key}.jsonl"), "rt") as file:
    for (attraction_id, line) in enumerate(file):
      attraction = Attraction.model_validate(from_json(line))
      embedding = encoder.encode(f"{attraction.name}\n{attraction.category}").tolist()
      embedding_data = pickle.dumps(embedding)
      unique_key = city_id * 1000 + attraction_id
      cursor.execute("INSERT INTO attraction VALUES (?,?,?,?,?,?,?,?)", (unique_key, city_id, attraction.name, attraction.category, attraction.rating, attraction.hours, attraction.address, embedding_data))
      for review in attraction.reviews:
        cursor.execute("INSERT INTO review VALUES (?,?,?,?,?)", (unique_review_id, unique_key, review.review. review.rating, review.visited))
        unique_review_id += 1

connection.commit()
