import logging
from tmdbv3api import TMDb, Movie, Search
from tmdbv3api.exceptions import TMDbException
import config

logger = logging.getLogger(__name__)

# Initialize TMDB
tmdb = TMDb()
tmdb.api_key = config.TMDB_API_KEY
tmdb.language = 'en'
tmdb.debug = config.DEBUG

movie_api = Movie()
search_api = Search()

def get_movie_details(movie_id):
    """
    Fetches detailed information for a single movie by its TMDB ID.
    
    Args:
        movie_id (int): The TMDB ID of the movie.
        
    Returns:
        dict: A dictionary of movie details, or None if an error occurs.
    """
    try:
        details = movie_api.details(movie_id)
        
        # Extract relevant details
        movie_data = {
            'id': details.id,
            'title': details.title,
            'overview': details.overview,
            'release_date': details.release_date,
            'vote_average': details.vote_average,
            'poster_path': f"https://image.tmdb.org/t/p/w500{details.poster_path}" if details.poster_path else None,
            'backdrop_path': f"https://image.tmdb.org/t/p/original{details.backdrop_path}" if details.backdrop_path else None,
            'genres': [g['name'] for g in details.genres],
            'runtime': details.runtime,
            'tagline': details.tagline,
            'homepage': details.homepage,
            'imdb_id': details.imdb_id
        }
        
        return movie_data
        
    except TMDbException as e:
        logger.error(f"TMDB API Error fetching details for ID {movie_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching details for ID {movie_id}: {e}")
        return None

def search_movie_by_title(title):
    """
    Searches for a movie by title using the TMDB API.
    
    Args:
        title (str): The title of the movie to search for.
        
    Returns:
        list: A list of dictionaries, each containing basic movie info.
    """
    try:
        results = search_api.movies(title)
        
        # Filter and format results
        formatted_results = []
        for res in results:
            if res.release_date and res.poster_path: # Only include results with a release date and poster
                formatted_results.append({
                    'id': res.id,
                    'title': res.title,
                    'release_date': res.release_date,
                    'poster_path': f"https://image.tmdb.org/t/p/w500{res.poster_path}",
                    'vote_average': res.vote_average,
                    'overview': res.overview
                })
        
        return formatted_results
        
    except TMDbException as e:
        logger.error(f"TMDB API Error searching for title '{title}': {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error searching for title '{title}': {e}")
        return []

def get_movie_id_from_title(title):
    """
    Searches for a movie by title and returns the TMDB ID of the best match.
    
    Args:
        title (str): The title of the movie.
        
    Returns:
        int: The TMDB ID of the best match, or None.
    """
    results = search_movie_by_title(title)
    if results:
        # Assuming the first result is the best match
        return results[0]['id']
    return None

# Example usage (for testing)
if __name__ == '__main__':
    if not config.TMDB_API_KEY:
        print("TMDB_API_KEY is not set in config.py. Cannot run examples.")
    else:
        # 1. Search for a movie
        search_term = "Inception"
        print(f"--- Searching for '{search_term}' ---")
        search_results = search_movie_by_title(search_term)
        if search_results:
            print(f"Found {len(search_results)} results. Best match ID: {search_results[0]['id']}")
            
            # 2. Get details for the best match
            movie_id = search_results[0]['id']
            print(f"\n--- Fetching details for ID {movie_id} ---")
            details = get_movie_details(movie_id)
            if details:
                print(f"Title: {details['title']}")
                print(f"Tagline: {details['tagline']}")
                print(f"Genres: {', '.join(details['genres'])}")
                print(f"Poster: {details['poster_path']}")
            else:
                print("Failed to fetch details.")
        else:
            print("No search results found.")
