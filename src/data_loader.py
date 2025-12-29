"""
Data Loader Module
Handles dataset loading, downloading, and preprocessing
"""

import pandas as pd
import numpy as np
import json
import requests
from pathlib import Path
from tqdm import tqdm
import sys
import os

# Add parent directory to path for config import
sys.path.append(str(Path(__file__).parent.parent))
import config


def download_file(url, destination):
    """Download a file from URL with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=destination.name,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)


def download_imdb_dataset():
    """
    Download IMDb movie dataset with reviews
    Using a combination of TMDb and IMDb data
    """
    print("Downloading movie dataset...")
    
    # For this project, we'll create a synthetic but realistic dataset
    # In a real scenario, you would download from Kaggle or similar
    
    movies_path = config.MOVIES_FILE
    reviews_path = config.REVIEWS_FILE
    
    if not movies_path.exists() or not reviews_path.exists():
        print("Dataset files not found. Please ensure the dataset is available.")
        print("You can download IMDb dataset from: https://www.kaggle.com/datasets/")
        return False
    
    return True


def parse_json_column(df, column_name):
    """Parse JSON strings in a DataFrame column"""
    def safe_parse(x):
        if pd.isna(x):
            return []
        try:
            if isinstance(x, str):
                return json.loads(x.replace("'", '"'))
            return x
        except:
            return []
    
    df[column_name] = df[column_name].apply(safe_parse)
    return df


def extract_names(json_list, key='name'):
    """Extract names from JSON list of dictionaries"""
    if isinstance(json_list, list):
        return [item.get(key, '') for item in json_list if isinstance(item, dict)]
    return []


def clean_movies_data(df):
    """Clean and preprocess movies dataset"""
    print("Cleaning movies data...")
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['title'], keep='first')
    
    # Handle missing values
    df['overview'] = df['overview'].fillna('')
    df['genres'] = df['genres'].fillna('[]')
    df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce').fillna(0)
    df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce').fillna(0)
    df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce').fillna(0)
    
    # Parse JSON columns if they exist
    if df['genres'].dtype == 'object':
        # Parse genres from JSON string to list
        df['genres_list'] = df['genres'].apply(lambda x: json.loads(x) if isinstance(x, str) and x != '[]' else [])
        df['genres_str'] = df['genres_list'].apply(lambda x: ', '.join(x) if x else 'Unknown')
    
    # Filter out movies with no title or overview
    df = df[df['title'].str.len() > 0]
    df = df[df['overview'].str.len() > 0]
    
    # Reset index
    df = df.reset_index(drop=True)
    
    print(f"Cleaned dataset: {len(df)} movies")
    return df


def clean_reviews_data(df):
    """Clean and preprocess reviews dataset"""
    print("Cleaning reviews data...")
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['review'], keep='first')
    
    # Handle missing values
    df['review'] = df['review'].fillna('')
    df['sentiment'] = df['sentiment'].fillna('neutral')
    
    # Filter out empty reviews
    df = df[df['review'].str.len() > 10]
    
    # Reset index
    df = df.reset_index(drop=True)
    
    print(f"Cleaned reviews: {len(df)} reviews")
    return df


def load_movies_data():
    """Load and return cleaned movies dataset"""
    try:
        df = pd.read_csv(config.MOVIES_FILE)
        df = clean_movies_data(df)
        return df
    except FileNotFoundError:
        print(f"Error: Movies file not found at {config.MOVIES_FILE}")
        return None
    except Exception as e:
        print(f"Error loading movies data: {e}")
        return None


def load_reviews_data():
    """Load and return cleaned reviews dataset"""
    try:
        df = pd.read_csv(config.REVIEWS_FILE)
        df = clean_reviews_data(df)
        return df
    except FileNotFoundError:
        print(f"Error: Reviews file not found at {config.REVIEWS_FILE}")
        return None
    except Exception as e:
        print(f"Error loading reviews data: {e}")
        return None


def get_dataset_statistics(movies_df, reviews_df=None):
    """Get basic statistics about the datasets"""
    stats = {
        'n_movies': len(movies_df),
        'n_genres': len(movies_df['genres_str'].unique()) if 'genres_str' in movies_df.columns else 0,
        'avg_rating': movies_df['vote_average'].mean() if 'vote_average' in movies_df.columns else 0,
        'avg_popularity': movies_df['popularity'].mean() if 'popularity' in movies_df.columns else 0,
    }
    
    if reviews_df is not None:
        stats['n_reviews'] = len(reviews_df)
    
    return stats


if __name__ == '__main__':
    # Test the data loader
    config.ensure_directories()
    
    movies = load_movies_data()
    reviews = load_reviews_data()
    
    if movies is not None:
        print("\nMovies Dataset Info:")
        print(movies.head())
        print(f"\nShape: {movies.shape}")
    
    if reviews is not None:
        print("\nReviews Dataset Info:")
        print(reviews.head())
        print(f"\nShape: {reviews.shape}")
