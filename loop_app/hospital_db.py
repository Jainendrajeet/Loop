

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

from google import genai


client = genai.Client (api_key = "GEMINI_API_KEY")

class HospitalDB:
    def __init__(self, df_path="hospitals.csv"):
        self.df = pd.read_csv(df_path)
        # Lowercase columns for easy search
        self.df['name_lower'] = self.df['Hospital'].str.lower()
        self.df['city_lower'] = self.df['City'].str.lower()

        # Build simple TF-IDF embeddings for RAG
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.embeddings = self.vectorizer.fit_transform(
            (self.df['Hospital'] + " " + self.df['City'] + " " + self.df['Address']).values
        )

    def find_hospitals_by_city(self, city: str, limit: int = 5):
        city_lower = city.lower()
        results = self.df[self.df['city_lower'] == city_lower]
        return results[['Hospital', 'Address']].head(limit).to_dict(orient='records')

    def check_hospital_in_network(self, hospital_name, city_name):
        name = hospital_name.lower()
        city = city_name.lower()
        match = self.df[(self.df['name_lower'] == name) & (self.df['city_lower'] == city)]
        return not match.empty

    def rag_search(self, query: str, top_k: int = 3):
        """Use TF-IDF vector similarity to retrieve top matching hospitals"""
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.embeddings).flatten()
        top_indices = similarities.argsort()[::-1][:top_k]
        results = self.df.iloc[top_indices]
        return results[['Hospital', 'Address', 'City']].to_dict(orient='records')

    def generate_gemini_response(self, user_query, context=None):
            """
            Fallback AI response using Gemini TextGeneration (v0.8.5)
            """
            context_text = ""
            if context:
                context_text = f"Previous conversation context: {context}\n"

            prompt = f"{context_text}, User asked: {user_query}\nPlease respond appropriately."
            
            try:
                response = client.models.generate_content(
                    model = "gemini-2.0-flash",
                    contents = prompt
                )
                return response.text
            except Exception as e:

                return f"Gemini API error: {str(e)}"
