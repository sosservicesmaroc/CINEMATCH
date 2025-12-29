"""
Movie Recommendation System - Main Application
Tkinter GUI for movie search and emotion-based recommendations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

import config
from src.data_loader import load_movies_data, load_reviews_data
from src.recommendation_engine import MovieRecommendationEngine
from src.emotion_recommender import EmotionRecommender


class MovieRecommendationApp:
    """Main application window for movie recommendations"""
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("Movie Recommendation System with Sentiment Analysis")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        
        # Load data and initialize engines
        self.load_data()
        
        # Create UI
        self.create_ui()
        
        # Center window
        self.center_window()
    
    def load_data(self):
        """Load datasets and initialize recommendation engines"""
        try:
            print("Loading data...")
            self.movies_df = load_movies_data()
            self.reviews_df = load_reviews_data()
            
            if self.movies_df is None:
                messagebox.showerror("Error", "Could not load movies dataset")
                sys.exit(1)
            
            print("Initializing recommendation engines...")
            self.recommendation_engine = MovieRecommendationEngine(self.movies_df)
            self.emotion_recommender = EmotionRecommender(self.movies_df)
            
            print("Application ready!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize application: {e}")
            sys.exit(1)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🎬 Movie Recommendation System",
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Search Section
        search_frame = ttk.LabelFrame(main_frame, text="Search by Title", padding="10")
        search_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Movie Title:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.title_entry = ttk.Entry(search_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.search_button = ttk.Button(
            search_frame,
            text="Search & Recommend",
            command=self.search_and_recommend
        )
        self.search_button.grid(row=0, column=2)
        
        # Emotion Section
        emotion_frame = ttk.LabelFrame(main_frame, text="Recommend by Emotion", padding="10")
        emotion_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        emotion_frame.columnconfigure(1, weight=1)
        
        ttk.Label(emotion_frame, text="Your Emotion:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.emotion_var = tk.StringVar()
        self.emotion_combo = ttk.Combobox(
            emotion_frame,
            textvariable=self.emotion_var,
            values=['joie / joy', 'colère / anger', 'tristesse / sadness', 'peur / fear'],
            state='readonly',
            width=37
        )
        self.emotion_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.emotion_combo.set('joie / joy')
        
        self.emotion_button = ttk.Button(
            emotion_frame,
            text="Recommend",
            command=self.recommend_by_emotion
        )
        self.emotion_button.grid(row=0, column=2)
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Scrolled text for results
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Courier", 10)
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(f"Ready | Movies: {len(self.movies_df)} | Reviews: {len(self.reviews_df)}")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Bind Enter key
        self.title_entry.bind('<Return>', lambda e: self.search_and_recommend())
    
    def clear_results(self):
        """Clear the results text area"""
        self.results_text.delete(1.0, tk.END)
    
    def display_results(self, text):
        """Display results in the text area"""
        self.results_text.insert(tk.END, text)
    
    def format_movie_info(self, movie, index=None, score=None):
        """Format movie information for display"""
        output = ""
        
        if index is not None:
            output += f"\n{'='*80}\n"
            output += f"#{index}\n"
        else:
            output += f"\n{'='*80}\n"
        
        output += f"Title: {movie['title']}\n"
        
        if 'year' in movie and movie['year']:
            output += f"Year: {movie['year']}\n"
        
        output += f"Genres: {movie['genres_str']}\n"
        output += f"Rating: {movie['vote_average']:.1f}/10 ({movie['vote_count']} votes)\n"
        
        if score is not None:
            output += f"Match Score: {score:.2%}\n"
        
        output += f"\nOverview:\n{movie['overview'][:300]}"
        if len(movie['overview']) > 300:
            output += "..."
        output += "\n"
        
        return output
    
    def search_and_recommend(self):
        """Search for a movie and provide recommendations"""
        title = self.title_entry.get().strip()
        
        if not title:
            messagebox.showwarning("Input Required", "Please enter a movie title")
            return
        
        self.clear_results()
        self.status_var.set("Searching...")
        self.root.update()
        
        try:
            # Search for the movie
            search_results = self.recommendation_engine.search_movie_by_title(title)
            
            if search_results.empty:
                self.display_results(f"No movies found matching '{title}'\n\n")
                self.display_results("Try a different title or check the spelling.")
                self.status_var.set("No results found")
                return
            
            # Display search result
            self.display_results(f"SEARCH RESULT FOR: '{title}'\n")
            movie = search_results.iloc[0]
            self.display_results(self.format_movie_info(movie))
            
            # Get recommendations
            recommendations = self.recommendation_engine.recommend_similar_movies(
                title,
                n_recommendations=5
            )
            
            if not recommendations.empty:
                self.display_results(f"\n\n{'='*80}\n")
                self.display_results(f"RECOMMENDED MOVIES (Similar to '{movie['title']}')\n")
                self.display_results(f"{'='*80}\n")
                
                for idx, (_, rec_movie) in enumerate(recommendations.iterrows(), 1):
                    score = rec_movie['similarity_score']
                    self.display_results(self.format_movie_info(rec_movie, index=idx, score=score))
            
            self.status_var.set(f"Found {len(recommendations)} recommendations")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_var.set("Error occurred")
    
    def recommend_by_emotion(self):
        """Recommend movies based on emotion"""
        emotion_full = self.emotion_var.get()
        
        if not emotion_full:
            messagebox.showwarning("Input Required", "Please select an emotion")
            return
        
        # Extract emotion (take first word)
        emotion = emotion_full.split('/')[0].strip()
        
        self.clear_results()
        self.status_var.set(f"Finding movies for emotion: {emotion}...")
        self.root.update()
        
        try:
            # Get emotion-based recommendations
            recommendations = self.emotion_recommender.recommend_by_emotion(
                emotion,
                n_recommendations=5,
                min_rating=6.0
            )
            
            if recommendations.empty:
                self.display_results(f"No movies found for emotion '{emotion}'\n\n")
                self.display_results("Try a different emotion.")
                self.status_var.set("No results found")
                return
            
            # Display recommendations
            self.display_results(f"EMOTION-BASED RECOMMENDATIONS\n")
            self.display_results(f"Emotion: {emotion_full}\n")
            
            # Show mapped genres
            genres = self.emotion_recommender.get_genres_for_emotion(emotion)
            self.display_results(f"Genres: {', '.join(genres)}\n")
            
            self.display_results(f"\n{'='*80}\n")
            self.display_results(f"TOP MOVIES FOR YOUR MOOD\n")
            self.display_results(f"{'='*80}\n")
            
            for idx, (_, movie) in enumerate(recommendations.iterrows(), 1):
                score = movie.get('emotion_score', 0)
                self.display_results(self.format_movie_info(movie, index=idx, score=score))
            
            self.status_var.set(f"Found {len(recommendations)} movies for {emotion}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_var.set("Error occurred")


def main():
    """Main entry point"""
    print("Starting Movie Recommendation System...")
    print("="*50)
    
    # Ensure directories exist
    config.ensure_directories()
    
    # Create and run application
    root = tk.Tk()
    app = MovieRecommendationApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
