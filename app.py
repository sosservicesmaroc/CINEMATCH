"""
Flask Web Application for Movie Recommendation System
Exposes the core recommendation logic via a modern web interface with AJAX support.
Now integrated with TMDB API for rich movie data and dedicated detail pages.
Optimized with caching and async processing for better performance.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
from pathlib import Path
import os
import logging
from dotenv import load_dotenv
import threading
from functools import lru_cache

# Load environment variables from .env file
load_dotenv()

# Add project root to path for module imports
sys.path.append(str(Path(__file__).parent))

import config
from src.data_loader import load_movies_data
from src.recommendation_engine import MovieRecommendationEngine
from src.emotion_recommender import EmotionRecommender
from src import tmdb_api # New TMDB API module

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Cache for TMDB API calls to reduce latency
tmdb_cache = {}
cache_lock = threading.Lock()

# --- Initialization ---
# Load data and initialize engines once
recommendation_engine = None
emotion_recommender = None
available_emotions = []
init_error = None

try:
    logger.info("Loading data and initializing engines for web app...")
    config.ensure_directories()
    
    # Load movies data
    movies_df = load_movies_data()
    if movies_df is None:
        raise ValueError("Could not load movies dataset.")
        
    # Initialize engines
    recommendation_engine = MovieRecommendationEngine(movies_df)
    emotion_recommender = EmotionRecommender(movies_df)
    
    # Get available emotions for the dropdown
    emotion_map = emotion_recommender.emotion_map
    available_emotions = sorted([f"{k} / {emotion_map[k][0].lower()}" if k in ['joie', 'colère', 'tristesse', 'peur'] else k for k in emotion_map.keys()])
    
    logger.info("Web app initialization complete.")

except Exception as e:
    logger.error(f"FATAL ERROR during web app initialization: {e}")
    init_error = f"Application failed to initialize: {e}"


def get_cached_tmdb_details(movie_id):
    """Get TMDB details with caching to reduce API calls."""
    if movie_id in tmdb_cache:
        return tmdb_cache[movie_id]
    
    details = tmdb_api.get_movie_details(movie_id)
    if details:
        with cache_lock:
            tmdb_cache[movie_id] = details
    return details


def get_tmdb_id_for_movie(title):
    """Get TMDB ID for a movie title with caching."""
    # Create a cache key from the title
    cache_key = f"title_{title.lower()}"
    if cache_key in tmdb_cache:
        return tmdb_cache[cache_key]
    
    tmdb_id = tmdb_api.get_movie_id_from_title(title)
    if tmdb_id:
        with cache_lock:
            tmdb_cache[cache_key] = tmdb_id
    return tmdb_id


def format_recommendations(df):
    """Format DataFrame results into a list of dictionaries for the template"""
    if df.empty:
        return []
    
    results = []
    for _, row in df.iterrows():
        # Use cached TMDB API to get rich data for the recommended movie
        tmdb_id = get_tmdb_id_for_movie(row['title'])
        
        # Fallback to local data if TMDB ID is not found
        if tmdb_id:
            tmdb_details = get_cached_tmdb_details(tmdb_id)
        else:
            tmdb_details = None

        result = {
            'id': tmdb_id, # TMDB ID for detail page link
            'title': row['title'],
            'genres': row['genres_str'],
            'rating': f"{row['vote_average']:.1f}/10",
            'vote_count': int(row['vote_count']),
            'overview': row['overview'][:300] + '...' if len(row['overview']) > 300 else row['overview'],
            'score': f"{row.get('similarity_score', row.get('emotion_score', 0)):.2%}",
            'poster_path': tmdb_details.get('poster_path') if tmdb_details else None,
            'release_date': tmdb_details.get('release_date') if tmdb_details else None,
        }
        results.append(result)
    return results


@app.route('/', methods=['GET'])
def index():
    """Main page"""
    if init_error:
        return render_template('index.html', error=init_error, emotions=available_emotions)
    return render_template('index.html', emotions=available_emotions)


@app.route('/movie/<int:tmdb_id>', methods=['GET'])
def movie_detail(tmdb_id):
    """Dedicated movie detail page using TMDB ID"""
    if init_error:
        return render_template('index.html', error=init_error, emotions=available_emotions)
    
    movie_details = get_cached_tmdb_details(tmdb_id)
    
    if not movie_details:
        return render_template('404.html', message="Movie not found or TMDB API error."), 404

    # Find the movie in the local dataset to get the recommendation base
    local_movie = recommendation_engine.search_movie_by_title(movie_details['title'], threshold=95)
    
    recommendations = []
    if not local_movie.empty:
        base_movie_title = local_movie.iloc[0]['title']
        
        # Get recommendations from the local engine
        recs_df = recommendation_engine.recommend_similar_movies(
            base_movie_title,
            n_recommendations=config.N_RECOMMENDATIONS
        )
        
        # Format recommendations, using TMDB for rich data
        recommendations = format_recommendations(recs_df)

    return render_template('movie_detail.html', movie=movie_details, recommendations=recommendations)


@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for title search and recommendation"""
    if init_error:
        return jsonify({'error': init_error}), 500
    
    try:
        title = request.json.get('title', '').strip()
        
        if not title:
            return jsonify({'error': 'Please enter a movie title.'}), 400
        
        logger.info(f"Searching for movie: {title}")
        
        # 1. Search local dataset for the best match
        search_results = recommendation_engine.search_movie_by_title(title, threshold=80)
        
        if search_results.empty:
            return jsonify({'error': f"No movie found matching '{title}' in local data. Try a different title or check the spelling."}), 404
        
        # 2. Use the best local match for recommendation
        base_movie_title = search_results.iloc[0]['title']
        logger.info(f"Found local movie: {base_movie_title}")
        
        recommendations = recommendation_engine.recommend_similar_movies(
            base_movie_title,
            n_recommendations=config.N_RECOMMENDATIONS
        )
        
        if recommendations.empty:
            return jsonify({'error': f"Found '{base_movie_title}' but no similar recommendations were generated."}), 404
        
        # 3. Format recommendations, enriching with TMDB data
        results = format_recommendations(recommendations)
        
        # 4. Get TMDB ID for the base movie to link to its detail page
        base_movie_tmdb_id = get_tmdb_id_for_movie(base_movie_title)
        
        logger.info(f"Returning {len(results)} recommendations, base TMDB ID: {base_movie_tmdb_id}")
        
        return jsonify({
            'success': True,
            'search_type': 'title',
            'base_movie': base_movie_title,
            'base_movie_id': base_movie_tmdb_id,
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in title search: {e}")
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/api/emotion-search', methods=['POST'])
def api_emotion_search():
    """API endpoint for emotion-based search"""
    if init_error:
        return jsonify({'error': init_error}), 500
    
    try:
        emotion_full = request.json.get('emotion', '').strip()
        
        if not emotion_full:
            return jsonify({'error': 'Please select an emotion.'}), 400
        
        # Extract the actual emotion key (e.g., 'joie / joy' -> 'joie')
        emotion = emotion_full.split('/')[0].strip()
        logger.info(f"Searching for emotion: {emotion}")
        
        # Get emotion-based recommendations
        recommendations = emotion_recommender.recommend_by_emotion(
            emotion,
            n_recommendations=config.N_RECOMMENDATIONS,
            min_rating=6.0
        )
        
        if recommendations.empty:
            return jsonify({'error': f"No movies found for emotion '{emotion_full}' with a rating above 6.0."}), 404
        
        # Format recommendations, enriching with TMDB data
        results = format_recommendations(recommendations)
        logger.info(f"Returning {len(results)} recommendations for emotion")
        
        return jsonify({
            'success': True,
            'search_type': 'emotion',
            'emotion': emotion_full,
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Error in emotion search: {e}")
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/api/emotions', methods=['GET'])
def api_emotions():
    """API endpoint to get available emotions"""
    return jsonify({'emotions': available_emotions}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html', message="Resource not found."), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html', message="Internal server error."), 500


if __name__ == '__main__':
    # Use environment variables for host and port for deployment flexibility
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', config.PORT))
    debug = os.getenv('FLASK_DEBUG', str(config.DEBUG)).lower() == 'true'
    
    # Only run if initialization was successful
    if recommendation_engine is not None:
        logger.info(f"Starting Flask app on {host}:{port}")
        app.run(host=host, port=port, debug=debug)
    else:
        logger.error("Web application failed to start due to initialization error.")
