import os
import numpy as np
import pandas as pd
import sqlite3
import pickle
from sentence_transformers import SentenceTransformer

connection = sqlite3.connect("data/attractions.db")
cursor = connection.cursor()

base_dir = os.path.join(os.getcwd(), "data", "sources", "us_news_world_report")

encoder = SentenceTransformer("all-MiniLM-L6-v2")

city_df = pd.read_csv(os.path.join(base_dir, "city_names.csv"))
for row in city_df.itertuples():
    cursor.execute("INSERT INTO city VALUES (?,?,?)", (row[1], row[2], row[3]))
connection.commit()

attractions_df = pd.read_csv(os.path.join(base_dir, "attraction_information.csv"))
attractions_df = attractions_df.fillna("")

for row in attractions_df.itertuples():
    embedding = encoder.encode(f"{row[3]}\n{row[5]}\n{row[4]}").tolist()
    embedding_data = pickle.dumps(embedding)
    cursor.execute("INSERT INTO attraction VALUES (?,?,?,?,?,?,?,?,?,?)", (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], embedding_data))
    if row[0] % 100 == 99:
        connection.commit()
connection.commit()

images_df = pd.read_csv(os.path.join(base_dir, "attraction_images.csv"))
for row in images_df.itertuples():
    cursor.execute("INSERT INTO image VALUES (?,?,?)", (row[1], row[2], row[3]))
connection.commit()

reviews_df = pd.read_csv(os.path.join(base_dir, "attraction_reviews.csv"))
reviews_df = reviews_df.fillna("")
for row in reviews_df.itertuples():
    cursor.execute("INSERT INTO review VALUES (?,?,?,?,?,?)", (row[1], row[2], row[3], row[4], row[5], row[6]))
connection.commit()
