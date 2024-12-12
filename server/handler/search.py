import sqlite3
import pandas as pd
import numpy as np
import pickle

from sentence_transformers import SentenceTransformer, util
import faiss

from collections import Counter
import math

# BM25 Implementation
class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_lengths = [len(doc) for doc in corpus]
        self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)
        self.doc_freqs = self._calculate_doc_frequencies()
        self.N = len(corpus)

    def _calculate_doc_frequencies(self):
        doc_freqs = Counter()
        for doc in self.corpus:
            unique_terms = set(doc)
            for term in unique_terms:
                doc_freqs[term] += 1
        return doc_freqs

    def _idf(self, term):
        n_t = self.doc_freqs.get(term, 0)
        return math.log((self.N - n_t + 0.5) / (n_t + 0.5) + 1)

    def score(self, query, doc):
        score = 0.0
        doc_counter = Counter(doc)
        for term in query:
            tf = doc_counter[term]
            idf = self._idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * len(doc) / self.avg_doc_length)
            score += idf * (numerator / denominator)
        return score

    def get_scores(self, query):
        return [self.score(query, doc) for doc in self.corpus]

# Modified search_attractions
def search_attractions(city: str, interests: str):
    connection = sqlite3.connect("data/attractions.db")
    cursor = connection.cursor()
    print(city, interests)
    # Get attractions from the database for the specified city
    ids = []
    descriptions = []
    rows = cursor.execute("""
        SELECT attraction.id, attraction.description 
        FROM city, attraction 
        WHERE city.id = attraction.city_id AND city.name = ?
    """, (city,))
    for id, description in rows:
        ids.append(id)
        descriptions.append(description.split())  # Tokenize descriptions for BM25

    # Initialize BM25
    bm25 = BM25(descriptions)

    # Tokenize the interests query
    query_tokens = interests.split()

    # Rank attractions using BM25
    scores = bm25.get_scores(query_tokens)
    ranked_results = sorted(
        zip(ids, scores, descriptions), 
        key=lambda x: x[1], 
        reverse=True
    )

    # Format the results
    results = []
    for id, score, description in ranked_results:
        row = cursor.execute("SELECT name FROM attraction WHERE id = ?", (id,))
        name = row.fetchone()[0]
        results.append({
            "id": id,
            "name": name,
            "description": " ".join(description),  # Reconstruct the description
            "score": score,
        })

    cursor.close()
    connection.close()

    return results
