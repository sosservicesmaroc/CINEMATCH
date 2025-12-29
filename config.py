"""
Configuration Module
Centralized configuration for the Movie Recommendation System
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Application Settings
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
PORT = int(os.getenv('PORT', 5000))

# Data Paths
DATA_DIR = PROJECT_ROOT / os.getenv('DATA_DIR', 'data')
MOVIES_FILE = DATA_DIR / os.getenv('MOVIES_FILE', 'movies_metadata.csv')
REVIEWS_FILE = DATA_DIR / os.getenv('REVIEWS_FILE', 'reviews_data.csv')

# Model Settings
N_RECOMMENDATIONS = int(os.getenv('N_RECOMMENDATIONS', 5))
MIN_SIMILARITY_SCORE = float(os.getenv('MIN_SIMILARITY_SCORE', 0.1))

# Sentiment Analysis
SENTIMENT_ANALYZER = os.getenv('SENTIMENT_ANALYZER', 'vader')  # Options: vader, textblob

# Interface Settings
WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', 900))
WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', 700))

# TMDB API Settings
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# Emotion to Genre Mapping
EMOTION_GENRE_MAP = {
    'joie': ['Comedy', 'Adventure', 'Family', 'Animation'],
    'joy': ['Comedy', 'Adventure', 'Family', 'Animation'],
    'colère': ['Action', 'Thriller', 'Crime'],
    'anger': ['Action', 'Thriller', 'Crime'],
    'tristesse': ['Drama', 'Romance'],
    'sadness': ['Drama', 'Romance'],
    'peur': ['Horror', 'Thriller', 'Mystery'],
    'fear': ['Horror', 'Thriller', 'Mystery'],
}


def ensure_directories():
    """Ensure all required directories exist"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / 'notebook').mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / 'docs').mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / 'src').mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / 'config').mkdir(parents=True, exist_ok=True)


def get_config_info():
    """Return configuration information as a dictionary"""
    return {
        'project_root': str(PROJECT_ROOT),
        'data_dir': str(DATA_DIR),
        'movies_file': str(MOVIES_FILE),
        'reviews_file': str(REVIEWS_FILE),
        'debug': DEBUG,
        'port': PORT,
        'n_recommendations': N_RECOMMENDATIONS,
        'sentiment_analyzer': SENTIMENT_ANALYZER,
        'tmdb_api_key_set': bool(TMDB_API_KEY)
    }


if __name__ == '__main__':
    # Display configuration
    print("Movie Recommendation System - Configuration")
    print("=" * 50)
    
    config_info = get_config_info()
    for key, value in config_info.items():
        print(f"{key:20s}: {value}")
    
    print("=" * 50)
    
    # Ensure directories exist
    ensure_directories()
    print("\nAll directories created/verified successfully!")
