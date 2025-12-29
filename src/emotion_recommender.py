"""
Emotion-Based Recommendation Module
Recommends movies based on user's emotional state
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import config
from .data_loader import load_movies_data


class EmotionRecommender:
    """
    Recommend movies based on user emotion
    Maps emotions to appropriate genres
    """
    
    def __init__(self, movies_df=None):
        """Initialize the emotion recommender"""
        if movies_df is None:
            self.movies_df = load_movies_data()
        else:
            self.movies_df = movies_df
        
        if self.movies_df is None:
            raise ValueError("Could not load movies data")
        
        self.emotion_map = config.EMOTION_GENRE_MAP
        
        print(f"Emotion recommender initialized with {len(self.movies_df)} movies")
    
    def normalize_emotion(self, emotion):
        """Normalize emotion input to lowercase"""
        return emotion.lower().strip()
    
    def get_genres_for_emotion(self, emotion):
        """Get list of genres associated with an emotion"""
        normalized = self.normalize_emotion(emotion)
        
        genres = self.emotion_map.get(normalized, [])
        
        if not genres:
            # Try to find partial match
            for key in self.emotion_map.keys():
                if normalized in key or key in normalized:
                    genres = self.emotion_map[key]
                    break
        
        return genres
    
    def recommend_by_emotion(self, emotion, n_recommendations=5, min_rating=6.0):
        """
        Recommend movies based on user emotion
        
        Args:
            emotion: User's emotional state (joie, colère, tristesse, peur)
            n_recommendations: Number of movies to recommend
            min_rating: Minimum rating threshold
        
        Returns:
            DataFrame with recommended movies
        """
        # Get genres for this emotion
        genres = self.get_genres_for_emotion(emotion)
        
        if not genres:
            print(f"Warning: No genres found for emotion '{emotion}'")
            print(f"Available emotions: {', '.join(set(self.emotion_map.keys()))}")
            return pd.DataFrame()
        
        print(f"Emotion '{emotion}' mapped to genres: {', '.join(genres)}")
        
        # Filter movies by genre
        def has_emotion_genre(movie_genres):
            """Check if movie has any of the emotion-related genres"""
            if not isinstance(movie_genres, list):
                return False
            return any(genre in movie_genres for genre in genres)
        
        filtered_df = self.movies_df[
            self.movies_df['genres_list'].apply(has_emotion_genre) &
            (self.movies_df['vote_average'] >= min_rating)
        ].copy()
        
        if filtered_df.empty:
            print(f"No movies found for emotion '{emotion}' with rating >= {min_rating}")
            return pd.DataFrame()
        
        # Calculate emotion score based on genre match count and rating
        def calculate_emotion_score(row):
            """Calculate how well movie matches the emotion"""
            genre_matches = sum(1 for genre in genres if genre in row['genres_list'])
            genre_score = genre_matches / len(genres)
            
            # Normalize rating to 0-1
            rating_score = row['vote_average'] / 10.0
            
            # Popularity boost (log scale)
            popularity_score = np.log1p(row['popularity']) / 10.0
            
            # Combined score
            score = (
                genre_score * 0.5 +
                rating_score * 0.3 +
                popularity_score * 0.2
            )
            
            return score
        
        filtered_df['emotion_score'] = filtered_df.apply(calculate_emotion_score, axis=1)
        
        # Sort by emotion score
        filtered_df = filtered_df.sort_values('emotion_score', ascending=False)
        
        # Return top N recommendations
        return filtered_df.head(n_recommendations)
    
    def get_available_emotions(self):
        """Return list of available emotions"""
        return sorted(set(self.emotion_map.keys()))


def test_emotion_recommender():
    """Test the emotion recommender"""
    print("Testing Emotion Recommender...")
    print("=" * 50)
    
    recommender = EmotionRecommender()
    
    # Test each emotion
    emotions = ['joie', 'colère', 'tristesse', 'peur']
    
    for emotion in emotions:
        print(f"\n{'='*50}")
        print(f"Testing emotion: {emotion}")
        print(f"{'='*50}")
        
        recommendations = recommender.recommend_by_emotion(emotion, n_recommendations=5)
        
        if not recommendations.empty:
            print(f"\nTop 5 recommendations for '{emotion}':")
            print(recommendations[['title', 'genres_str', 'vote_average', 'emotion_score']].to_string())
        else:
            print(f"No recommendations found for '{emotion}'")
    
    print("\n" + "=" * 50)
    print("Testing complete!")


if __name__ == '__main__':
    test_emotion_recommender()
