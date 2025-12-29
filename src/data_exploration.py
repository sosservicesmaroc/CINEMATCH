"""
Data Exploration Module
Provides functions for exploratory data analysis and visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import json

sys.path.append(str(Path(__file__).parent.parent))
import config
from data_loader import load_movies_data, load_reviews_data

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def get_descriptive_statistics(movies_df, reviews_df):
    """Generate descriptive statistics for the datasets"""
    stats = {}
    
    # Movies statistics
    stats['movies'] = {
        'total_movies': len(movies_df),
        'avg_rating': movies_df['vote_average'].mean(),
        'median_rating': movies_df['vote_average'].median(),
        'std_rating': movies_df['vote_average'].std(),
        'avg_popularity': movies_df['popularity'].mean(),
        'total_votes': movies_df['vote_count'].sum(),
        'year_range': (movies_df['year'].min(), movies_df['year'].max()) if 'year' in movies_df.columns else (0, 0),
    }
    
    # Reviews statistics
    if reviews_df is not None:
        stats['reviews'] = {
            'total_reviews': len(reviews_df),
            'avg_review_rating': reviews_df['rating'].mean() if 'rating' in reviews_df.columns else 0,
            'sentiment_distribution': reviews_df['sentiment'].value_counts().to_dict() if 'sentiment' in reviews_df.columns else {},
        }
    
    # Genre statistics
    all_genres = []
    for genres_list in movies_df['genres_list']:
        all_genres.extend(genres_list)
    
    genre_counts = pd.Series(all_genres).value_counts()
    stats['genres'] = {
        'total_genres': len(genre_counts),
        'top_genres': genre_counts.head(10).to_dict(),
    }
    
    return stats


def plot_genre_distribution(movies_df, save_path=None):
    """Plot distribution of movie genres"""
    # Extract all genres
    all_genres = []
    for genres_list in movies_df['genres_list']:
        all_genres.extend(genres_list)
    
    genre_counts = pd.Series(all_genres).value_counts().head(15)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(len(genre_counts)), genre_counts.values, color='steelblue')
    ax.set_title('Distribution of Movie Genres (Top 15)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Genre', fontsize=12)
    ax.set_ylabel('Number of Movies', fontsize=12)
    ax.set_xticks(range(len(genre_counts)))
    ax.set_xticklabels(genre_counts.index, rotation=45, ha='right')
    plt.tight_layout()
    
    # Add value labels on bars
    for i, v in enumerate(genre_counts.values):
        ax.text(i, v + 50, str(v), ha='center', va='bottom')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved genre distribution plot to {save_path}")
    
    plt.close()


def plot_rating_distribution(movies_df, save_path=None):
    """Plot distribution of movie ratings"""
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.hist(movies_df['vote_average'], bins=30, color='coral', edgecolor='black', alpha=0.7)
    plt.title('Distribution of Movie Ratings', fontsize=12, fontweight='bold')
    plt.xlabel('Rating', fontsize=10)
    plt.ylabel('Frequency', fontsize=10)
    plt.axvline(movies_df['vote_average'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {movies_df["vote_average"].mean():.2f}')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.boxplot(movies_df['vote_average'], vert=True)
    plt.title('Box Plot of Movie Ratings', fontsize=12, fontweight='bold')
    plt.ylabel('Rating', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved rating distribution plot to {save_path}")
    
    plt.close()


def plot_rating_by_genre(movies_df, save_path=None):
    """Plot average rating by genre"""
    # Calculate average rating per genre
    genre_ratings = {}
    
    for idx, row in movies_df.iterrows():
        rating = row['vote_average']
        for genre in row['genres_list']:
            if genre not in genre_ratings:
                genre_ratings[genre] = []
            genre_ratings[genre].append(rating)
    
    # Calculate means
    genre_means = {genre: np.mean(ratings) for genre, ratings in genre_ratings.items()}
    genre_means_sorted = dict(sorted(genre_means.items(), key=lambda x: x[1], reverse=True)[:15])
    
    plt.figure(figsize=(12, 6))
    genres = list(genre_means_sorted.keys())
    means = list(genre_means_sorted.values())
    
    ax = plt.bar(range(len(genres)), means, color='teal', alpha=0.7)
    plt.title('Average Rating by Genre (Top 15)', fontsize=14, fontweight='bold')
    plt.xlabel('Genre', fontsize=12)
    plt.ylabel('Average Rating', fontsize=12)
    plt.xticks(range(len(genres)), genres, rotation=45, ha='right')
    plt.ylim(0, 10)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved rating by genre plot to {save_path}")
    
    plt.close()


def plot_popularity_vs_rating(movies_df, save_path=None):
    """Plot popularity vs rating scatter plot"""
    plt.figure(figsize=(12, 6))
    
    # Sample data for better visualization if too many points
    if len(movies_df) > 5000:
        sample_df = movies_df.sample(5000)
    else:
        sample_df = movies_df
    
    plt.scatter(sample_df['vote_average'], sample_df['popularity'], 
                alpha=0.5, c='purple', s=20)
    plt.title('Popularity vs Rating', fontsize=14, fontweight='bold')
    plt.xlabel('Rating', fontsize=12)
    plt.ylabel('Popularity', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(sample_df['vote_average'], sample_df['popularity'], 1)
    p = np.poly1d(z)
    plt.plot(sample_df['vote_average'].sort_values(), 
             p(sample_df['vote_average'].sort_values()), 
             "r--", alpha=0.8, linewidth=2, label='Trend')
    plt.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved popularity vs rating plot to {save_path}")
    
    plt.close()


def plot_sentiment_distribution(reviews_df, save_path=None):
    """Plot sentiment distribution of reviews"""
    if reviews_df is None or 'sentiment' not in reviews_df.columns:
        print("No sentiment data available")
        return
    
    plt.figure(figsize=(10, 6))
    
    sentiment_counts = reviews_df['sentiment'].value_counts()
    colors = {'positive': 'green', 'negative': 'red', 'neutral': 'gray'}
    plot_colors = [colors.get(s, 'blue') for s in sentiment_counts.index]
    
    ax = sentiment_counts.plot(kind='bar', color=plot_colors, alpha=0.7)
    plt.title('Distribution of Review Sentiments', fontsize=14, fontweight='bold')
    plt.xlabel('Sentiment', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    plt.xticks(rotation=0)
    
    # Add value labels
    for i, v in enumerate(sentiment_counts):
        ax.text(i, v + 50, str(v), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved sentiment distribution plot to {save_path}")
    
    plt.close()


def generate_all_plots(output_dir=None):
    """Generate all exploratory plots"""
    if output_dir is None:
        output_dir = config.BASE_DIR / 'docs' / 'figures'
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Loading datasets...")
    movies_df = load_movies_data()
    reviews_df = load_reviews_data()
    
    if movies_df is None:
        print("Error: Could not load movies data")
        return
    
    print("\nGenerating plots...")
    
    plot_genre_distribution(movies_df, output_dir / 'genre_distribution.png')
    plot_rating_distribution(movies_df, output_dir / 'rating_distribution.png')
    plot_rating_by_genre(movies_df, output_dir / 'rating_by_genre.png')
    plot_popularity_vs_rating(movies_df, output_dir / 'popularity_vs_rating.png')
    
    if reviews_df is not None:
        plot_sentiment_distribution(reviews_df, output_dir / 'sentiment_distribution.png')
    
    print(f"\nAll plots saved to {output_dir}")
    
    # Print statistics
    print("\n" + "="*50)
    print("DATASET STATISTICS")
    print("="*50)
    
    stats = get_descriptive_statistics(movies_df, reviews_df)
    
    print("\nMovies:")
    for key, value in stats['movies'].items():
        print(f"  {key}: {value}")
    
    if 'reviews' in stats:
        print("\nReviews:")
        for key, value in stats['reviews'].items():
            print(f"  {key}: {value}")
    
    print("\nTop Genres:")
    for genre, count in list(stats['genres']['top_genres'].items())[:10]:
        print(f"  {genre}: {count}")


if __name__ == '__main__':
    generate_all_plots()
