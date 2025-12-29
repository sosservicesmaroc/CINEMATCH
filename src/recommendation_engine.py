"""
Recommendation Engine Module
Implements movie search and recommendation algorithms
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz, process
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import config
from .data_loader import load_movies_data


class MovieRecommendationEngine:
    """
    Movie Recommendation Engine using multiple similarity metrics:
    - Genre similarity
    - Rating similarity
    - Content similarity (TF-IDF on overview)
    """
    
    def __init__(self, movies_df=None):
        """Initialize the recommendation engine"""
        if movies_df is None:
            self.movies_df = load_movies_data()
        else:
            self.movies_df = movies_df
        
        if self.movies_df is None:
            raise ValueError("Could not load movies data")
        
        # Prepare TF-IDF vectorizer for content-based filtering
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Fit TF-IDF on movie overviews
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.movies_df['overview'].fillna('')
        )
        
        print(f"Recommendation engine initialized with {len(self.movies_df)} movies")
    
    def search_movie_by_title(self, title, threshold=70):
        """
        Search for a movie by title using fuzzy matching with priority for exact matches.
        
        Args:
            title: Movie title to search for
            threshold: Minimum similarity score (0-100)
        
        Returns:
            DataFrame with matching movies
        """
        if not title:
            return pd.DataFrame()
        
        title_lower = title.lower().strip()
        
        # First, try exact match (case-insensitive)
        exact_matches = self.movies_df[self.movies_df['title'].str.lower() == title_lower]
        if not exact_matches.empty:
            return exact_matches.copy()
        
        # Get all titles
        titles = self.movies_df['title'].tolist()
        
        # Fuzzy match with multiple scorers for better accuracy
        matches = process.extract(title, titles, scorer=fuzz.token_set_ratio, limit=5)
        
        # Filter by threshold and sort by score descending
        filtered_matches = [(match, score) for match, score in matches if score >= threshold]
        filtered_matches.sort(key=lambda x: x[1], reverse=True)
        
        if not filtered_matches:
            return pd.DataFrame()
        
        # Get matching indices
        matching_titles = [match[0] for match, score in filtered_matches]
        result_df = self.movies_df[self.movies_df['title'].isin(matching_titles)].copy()
        
        # Sort by similarity to input title
        result_df = result_df.sort_values('title', key=lambda x: x.apply(lambda t: fuzz.token_set_ratio(title_lower, t.lower())))
        
        return result_df
    
    def get_movie_info(self, movie_idx):
        """Get detailed information about a movie"""
        if movie_idx >= len(self.movies_df):
            return None
        
        movie = self.movies_df.iloc[movie_idx]
        
        info = {
            'title': movie['title'],
            'genres': movie['genres_str'],
            'overview': movie['overview'],
            'rating': movie['vote_average'],
            'popularity': movie['popularity'],
            'vote_count': movie['vote_count'],
        }
        
        if 'year' in movie:
            info['year'] = movie['year']
        
        return info
    
    def calculate_genre_similarity(self, idx1, idx2):
        """Calculate Jaccard similarity between two movies' genres"""
        genres1 = set(self.movies_df.iloc[idx1]['genres_list'])
        genres2 = set(self.movies_df.iloc[idx2]['genres_list'])
        
        if not genres1 or not genres2:
            return 0.0
        
        intersection = len(genres1.intersection(genres2))
        union = len(genres1.union(genres2))
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_rating_similarity(self, idx1, idx2):
        """Calculate similarity based on ratings (inverse of difference)"""
        rating1 = self.movies_df.iloc[idx1]['vote_average']
        rating2 = self.movies_df.iloc[idx2]['vote_average']
        
        # Normalize to 0-1 scale (max difference is 10)
        diff = abs(rating1 - rating2)
        similarity = 1 - (diff / 10.0)
        
        return max(0, similarity)
    
    def calculate_content_similarity(self, idx1, idx2):
        """Calculate cosine similarity between movie overviews using TF-IDF"""
        vec1 = self.tfidf_matrix[idx1]
        vec2 = self.tfidf_matrix[idx2]
        
        similarity = cosine_similarity(vec1, vec2)[0][0]
        return similarity
    
    def calculate_combined_similarity(self, idx1, idx2, weights=None):
        """
        Calculate combined similarity score
        
        Args:
            idx1, idx2: Movie indices
            weights: Dict with keys 'genre', 'rating', 'content'
        
        Returns:
            Combined similarity score (0-1)
        """
        if weights is None:
            weights = {'genre': 0.4, 'rating': 0.2, 'content': 0.4}
        
        genre_sim = self.calculate_genre_similarity(idx1, idx2)
        rating_sim = self.calculate_rating_similarity(idx1, idx2)
        content_sim = self.calculate_content_similarity(idx1, idx2)
        
        combined = (
            weights['genre'] * genre_sim +
            weights['rating'] * rating_sim +
            weights['content'] * content_sim
        )
        
        return combined
    
    def recommend_similar_movies(self, movie_title, n_recommendations=5, weights=None):
        """
        Recommend similar movies based on a given movie title
        
        Args:
            movie_title: Title of the movie to base recommendations on
            n_recommendations: Number of recommendations to return
            weights: Similarity weights
        
        Returns:
            DataFrame with recommended movies and similarity scores
        """
        # Search for the movie
        search_results = self.search_movie_by_title(movie_title, threshold=80)
        
        if search_results.empty:
            return pd.DataFrame()
        
        # Use the first match
        base_movie_idx = search_results.index[0]
        
        # Calculate similarities with all other movies
        similarities = []
        
        for idx in range(len(self.movies_df)):
            if idx == base_movie_idx:
                continue
            
            sim_score = self.calculate_combined_similarity(base_movie_idx, idx, weights)
            
            if sim_score >= config.MIN_SIMILARITY_SCORE:
                similarities.append((idx, sim_score))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top N recommendations
        top_indices = [idx for idx, score in similarities[:n_recommendations]]
        top_scores = [score for idx, score in similarities[:n_recommendations]]
        
        # Create result DataFrame
        recommendations = self.movies_df.iloc[top_indices].copy()
        recommendations['similarity_score'] = top_scores
        
        return recommendations
    
    def recommend_by_genre_and_rating(self, genres, min_rating=6.0, n_recommendations=5):
        """
        Recommend movies by genre and minimum rating
        
        Args:
            genres: List of genres to filter by
            min_rating: Minimum rating threshold
            n_recommendations: Number of recommendations
        
        Returns:
            DataFrame with recommended movies
        """
        if isinstance(genres, str):
            genres = [genres]
        
        # Filter movies by genre
        def has_genre(movie_genres):
            return any(genre in movie_genres for genre in genres)
        
        filtered_df = self.movies_df[
            self.movies_df['genres_list'].apply(has_genre) &
            (self.movies_df['vote_average'] >= min_rating)
        ].copy()
        
        # Sort by rating and popularity
        filtered_df['score'] = (
            filtered_df['vote_average'] * 0.7 +
            np.log1p(filtered_df['popularity']) * 0.3
        )
        
        filtered_df = filtered_df.sort_values('score', ascending=False)
        
        return filtered_df.head(n_recommendations)


def test_recommendation_engine():
    """Test the recommendation engine"""
    print("Testing Recommendation Engine...")
    print("="*50)
    
    engine = MovieRecommendationEngine()
    
    # Test search
    print("\n1. Testing search functionality:")
    results = engine.search_movie_by_title("The Matrix")
    if not results.empty:
        print(f"Found {len(results)} matches for 'The Matrix':")
        print(results[['title', 'genres_str', 'vote_average']].head())
    
    # Test recommendations
    print("\n2. Testing recommendation functionality:")
    recommendations = engine.recommend_similar_movies("The Matrix", n_recommendations=5)
    if not recommendations.empty:
        print(f"\nTop 5 recommendations for 'The Matrix':")
        print(recommendations[['title', 'genres_str', 'vote_average', 'similarity_score']])
    
    # Test genre-based recommendations
    print("\n3. Testing genre-based recommendations:")
    genre_recs = engine.recommend_by_genre_and_rating(['Action', 'Sci-Fi'], min_rating=7.0, n_recommendations=5)
    if not genre_recs.empty:
        print(f"\nTop 5 Action/Sci-Fi movies (rating >= 7.0):")
        print(genre_recs[['title', 'genres_str', 'vote_average']].head())
    
    print("\n" + "="*50)
    print("Testing complete!")


if __name__ == '__main__':
    test_recommendation_engine()
