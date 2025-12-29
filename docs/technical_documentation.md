# Technical Documentation

## Movie Recommendation System with Sentiment Analysis

This document provides detailed technical information about the system architecture, algorithms, and implementation details.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Data Pipeline](#data-pipeline)
3. [Recommendation Algorithms](#recommendation-algorithms)
4. [Sentiment Analysis](#sentiment-analysis)
5. [Module Documentation](#module-documentation)
6. [Performance Considerations](#performance-considerations)
7. [Future Enhancements](#future-enhancements)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface (Tkinter)              │
│  - Title Search Input                                    │
│  - Emotion Selector                                      │
│  - Results Display                                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Application Layer (app.py)                  │
│  - Event Handling                                        │
│  - Result Formatting                                     │
│  - UI Updates                                            │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴──────────┐
         ▼                      ▼
┌──────────────────┐   ┌──────────────────┐
│ Recommendation   │   │    Emotion       │
│    Engine        │   │  Recommender     │
│ - TF-IDF         │   │ - Genre Mapping  │
│ - Similarity     │   │ - Emotion Score  │
└────────┬─────────┘   └────────┬─────────┘
         │                      │
         └───────────┬──────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Data Layer (data_loader.py)                 │
│  - CSV Loading                                           │
│  - Data Cleaning                                         │
│  - Preprocessing                                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Data Storage                            │
│  - movies_metadata.csv (34,532 movies)                   │
│  - reviews_data.csv (10,000+ reviews)                    │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **UI** | Tkinter | Cross-platform GUI |
| **ML** | scikit-learn | TF-IDF, cosine similarity |
| **NLP** | VADER, TextBlob | Sentiment analysis |
| **Data** | pandas, numpy | Data manipulation |
| **Viz** | matplotlib, seaborn | Data visualization |
| **Config** | python-dotenv | Configuration management |

---

## Data Pipeline

### 1. Data Acquisition

**Source**: Wikipedia Movie Data (JSON format)

```python
# Download from GitHub repository
url = 'https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json'
```

**Raw Data Structure**:
```json
{
  "title": "The Matrix",
  "year": 1999,
  "cast": ["Keanu Reeves", "Laurence Fishburne"],
  "genres": ["Action", "Science Fiction"],
  "extract": "Plot summary text..."
}
```

### 2. Data Transformation

**Movies Dataset Creation** (`prepare_dataset.py`):

1. **Parse JSON**: Extract relevant fields
2. **Generate ratings**: Assign realistic ratings using normal distribution
   - Mean: 6.5
   - Standard deviation: 1.5
   - Range: 1.0 - 10.0

3. **Generate metadata**:
   - Vote count: Log-normal distribution (10 - 10,000)
   - Popularity: Log-normal distribution (0.1 - 1,000)

4. **Create genre lists**: Convert JSON arrays to Python lists

**Reviews Dataset Creation**:

1. **Generate synthetic reviews**: Based on movie ratings
   - Rating ≥ 7.0 → Positive review
   - Rating ≤ 4.0 → Negative review
   - 4.0 < Rating < 7.0 → Neutral review

2. **Review templates**: 30 templates (10 positive, 10 negative, 10 neutral)

3. **Distribution**: Reviews per movie based on vote count
   - Formula: `n_reviews = min(vote_count / 100, 50)`

### 3. Data Cleaning

**Movies Cleaning** (`data_loader.py`):
- Remove duplicates by title
- Fill missing overviews with empty strings
- Parse JSON genre strings
- Filter movies without title or overview
- Convert ratings to numeric type

**Reviews Cleaning**:
- Remove duplicate reviews
- Fill missing sentiment labels
- Filter reviews shorter than 10 characters
- Reset indices

### 4. Sentiment Analysis

**Process** (`sentiment_analyzer.py`):

1. **Load reviews**: Read from CSV
2. **Initialize analyzer**: VADER or TextBlob
3. **Analyze each review**:
   ```python
   score, label = analyzer.analyze_text(review_text)
   ```
4. **Add columns**: `sentiment_score`, `sentiment_label`
5. **Save updated dataset**: Overwrite CSV with new columns

---

## Recommendation Algorithms

### 1. Content-Based Filtering

**Algorithm**: Hybrid similarity combining multiple factors

#### Genre Similarity

**Method**: Jaccard similarity

```python
def calculate_genre_similarity(genres1, genres2):
    intersection = len(set(genres1) & set(genres2))
    union = len(set(genres1) | set(genres2))
    return intersection / union if union > 0 else 0.0
```

**Example**:
- Movie A: [Action, Sci-Fi, Thriller]
- Movie B: [Action, Sci-Fi]
- Intersection: 2 (Action, Sci-Fi)
- Union: 3 (Action, Sci-Fi, Thriller)
- Similarity: 2/3 = 0.667

#### Rating Similarity

**Method**: Inverse of normalized difference

```python
def calculate_rating_similarity(rating1, rating2):
    diff = abs(rating1 - rating2)
    similarity = 1 - (diff / 10.0)
    return max(0, similarity)
```

**Example**:
- Movie A: 8.5/10
- Movie B: 7.5/10
- Difference: 1.0
- Similarity: 1 - (1.0/10) = 0.90

#### Content Similarity (TF-IDF)

**Method**: TF-IDF vectorization + cosine similarity

**TF-IDF (Term Frequency-Inverse Document Frequency)**:
- Converts text to numerical vectors
- Emphasizes unique words
- Reduces weight of common words

```python
vectorizer = TfidfVectorizer(
    max_features=5000,      # Top 5000 words
    stop_words='english',   # Remove common words
    ngram_range=(1, 2)      # Unigrams and bigrams
)
```

**Cosine Similarity**:
```
similarity = (A · B) / (||A|| × ||B||)
```

Where:
- A, B are TF-IDF vectors
- · is dot product
- ||·|| is vector magnitude

**Range**: 0 (completely different) to 1 (identical)

#### Combined Similarity

**Formula**:
```python
combined_score = (
    0.4 × genre_similarity +
    0.2 × rating_similarity +
    0.4 × content_similarity
)
```

**Weights rationale**:
- **Genre (40%)**: Strong indicator of movie type
- **Content (40%)**: Captures plot and theme similarity
- **Rating (20%)**: Ensures quality consistency

### 2. Fuzzy Title Matching

**Algorithm**: Levenshtein distance with token sorting

**Library**: fuzzywuzzy

```python
from fuzzywuzzy import fuzz, process

matches = process.extract(
    query,
    all_titles,
    scorer=fuzz.token_sort_ratio,
    limit=10
)
```

**Token Sort Ratio**:
1. Tokenize strings
2. Sort tokens alphabetically
3. Calculate Levenshtein distance
4. Return similarity score (0-100)

**Example**:
- Query: "dark knight"
- Match: "The Dark Knight" → 95% similarity
- Match: "Dark Knight Rises" → 85% similarity

**Threshold**: 70% minimum for matches

### 3. Emotion-Based Recommendation

**Algorithm**: Genre filtering + weighted scoring

#### Emotion-Genre Mapping

```python
EMOTION_GENRE_MAP = {
    'joy': ['Comedy', 'Adventure', 'Family', 'Animation'],
    'anger': ['Action', 'Thriller', 'Crime'],
    'sadness': ['Drama', 'Romance'],
    'fear': ['Horror', 'Thriller', 'Mystery']
}
```

**Psychological basis**:
- **Joy**: Uplifting, positive content
- **Anger**: Intense, cathartic action
- **Sadness**: Emotional, reflective stories
- **Fear**: Suspenseful, thrilling experiences

#### Emotion Score Calculation

```python
def calculate_emotion_score(movie, target_genres):
    # Genre match score
    genre_matches = sum(1 for g in target_genres if g in movie.genres)
    genre_score = genre_matches / len(target_genres)
    
    # Rating score (normalized)
    rating_score = movie.rating / 10.0
    
    # Popularity score (log scale)
    popularity_score = log(1 + movie.popularity) / 10.0
    
    # Combined score
    return (
        0.5 × genre_score +
        0.3 × rating_score +
        0.2 × popularity_score
    )
```

**Weights rationale**:
- **Genre match (50%)**: Primary factor for emotion alignment
- **Rating (30%)**: Ensures quality recommendations
- **Popularity (20%)**: Favors well-known, accessible movies

---

## Sentiment Analysis

### VADER (Valence Aware Dictionary and sEntiment Reasoner)

**Advantages**:
- Optimized for social media and short texts
- Handles emoticons, slang, and intensifiers
- Pre-trained, no training required
- Fast processing

**Output**:
```python
{
    'neg': 0.0,      # Negative score
    'neu': 0.5,      # Neutral score
    'pos': 0.5,      # Positive score
    'compound': 0.6  # Overall score (-1 to 1)
}
```

**Classification**:
- Compound ≥ 0.05 → Positive
- Compound ≤ -0.05 → Negative
- -0.05 < Compound < 0.05 → Neutral

### TextBlob (Alternative)

**Advantages**:
- Simple API
- Returns polarity and subjectivity
- Good for general text

**Output**:
```python
{
    'polarity': 0.5,      # -1 (negative) to 1 (positive)
    'subjectivity': 0.6   # 0 (objective) to 1 (subjective)
}
```

**Classification**:
- Polarity > 0.1 → Positive
- Polarity < -0.1 → Negative
- -0.1 ≤ Polarity ≤ 0.1 → Neutral

### Performance Comparison

| Metric | VADER | TextBlob |
|--------|-------|----------|
| **Speed** | Fast (1000 reviews/sec) | Moderate (500 reviews/sec) |
| **Accuracy** | High for informal text | High for formal text |
| **Training** | None required | None required |
| **Dependencies** | vaderSentiment | textblob, nltk |

**Recommendation**: VADER for this project (better for diverse review styles)

---

## Module Documentation

### config.py

**Purpose**: Centralized configuration management

**Key Functions**:
- `ensure_directories()`: Create required directories
- `get_config_info()`: Return configuration dictionary

**Environment Variables**:
- Loaded from `.env` file using python-dotenv
- Provides defaults for all settings

### src/data_loader.py

**Purpose**: Data loading and preprocessing

**Key Functions**:

```python
def load_movies_data() -> pd.DataFrame
    """Load and clean movies dataset"""
    
def load_reviews_data() -> pd.DataFrame
    """Load and clean reviews dataset"""
    
def clean_movies_data(df: pd.DataFrame) -> pd.DataFrame
    """Clean movies: remove duplicates, handle missing values"""
    
def clean_reviews_data(df: pd.DataFrame) -> pd.DataFrame
    """Clean reviews: remove duplicates, filter short reviews"""
```

### src/recommendation_engine.py

**Purpose**: Content-based movie recommendations

**Class**: `MovieRecommendationEngine`

**Key Methods**:

```python
def search_movie_by_title(title: str, threshold: int = 70) -> pd.DataFrame
    """Fuzzy search for movies by title"""
    
def recommend_similar_movies(movie_title: str, n_recommendations: int = 5) -> pd.DataFrame
    """Recommend movies similar to given title"""
    
def calculate_combined_similarity(idx1: int, idx2: int) -> float
    """Calculate hybrid similarity score"""
```

**Initialization**:
- Loads movie dataset
- Fits TF-IDF vectorizer on overviews
- Creates TF-IDF matrix for all movies

**Time Complexity**:
- Initialization: O(n × m) where n = movies, m = avg words per overview
- Search: O(n × log n) for fuzzy matching
- Recommendation: O(n) for similarity calculation

### src/emotion_recommender.py

**Purpose**: Emotion-based recommendations

**Class**: `EmotionRecommender`

**Key Methods**:

```python
def recommend_by_emotion(emotion: str, n_recommendations: int = 5, min_rating: float = 6.0) -> pd.DataFrame
    """Recommend movies based on user emotion"""
    
def get_genres_for_emotion(emotion: str) -> List[str]
    """Map emotion to appropriate genres"""
```

**Supported Emotions**:
- English: joy, anger, sadness, fear
- French: joie, colère, tristesse, peur

### src/sentiment_analyzer.py

**Purpose**: Sentiment analysis of reviews

**Class**: `SentimentAnalyzer`

**Key Methods**:

```python
def analyze_text(text: str) -> Tuple[float, str]
    """Analyze sentiment of single text"""
    
def analyze_dataframe(df: pd.DataFrame) -> pd.DataFrame
    """Analyze sentiment for all reviews in DataFrame"""
```

**Functions**:

```python
def visualize_sentiment_distribution(df: pd.DataFrame, output_dir: Path)
    """Create sentiment visualization plots"""
    
def process_and_save_reviews(analyzer_type: str = 'vader') -> pd.DataFrame
    """Complete sentiment analysis pipeline"""
```

### app.py

**Purpose**: Main GUI application

**Class**: `MovieRecommendationApp`

**Key Methods**:

```python
def search_and_recommend()
    """Handle title search and display recommendations"""
    
def recommend_by_emotion()
    """Handle emotion-based recommendations"""
    
def format_movie_info(movie, index, score) -> str
    """Format movie information for display"""
```

---

## Performance Considerations

### Memory Usage

**Estimated Memory Requirements**:
- Movies dataset: ~50 MB
- Reviews dataset: ~5 MB
- TF-IDF matrix: ~100 MB
- Application overhead: ~50 MB
- **Total**: ~200-300 MB

### Processing Time

**Initialization** (one-time):
- Load movies: 1-2 seconds
- Load reviews: 0.5-1 second
- Fit TF-IDF: 2-3 seconds
- **Total**: 4-6 seconds

**Per-Query**:
- Fuzzy search: 0.1-0.2 seconds
- Similarity calculation: 0.5-1 second (for 34k movies)
- **Total**: 0.6-1.2 seconds per search

### Optimization Strategies

1. **TF-IDF Caching**: Matrix computed once at initialization
2. **Vectorized Operations**: Use numpy/pandas for batch processing
3. **Lazy Loading**: Load data only when needed
4. **Threshold Filtering**: Skip low-similarity comparisons

### Scalability

**Current Limits**:
- Movies: 34,532 (can handle 100k+)
- Reviews: 10,000 (can handle 1M+)
- Recommendations: 5 (configurable)

**Bottlenecks**:
- TF-IDF matrix size grows with vocabulary
- Similarity calculation is O(n) per query
- GUI responsiveness with large result sets

**Solutions for Larger Datasets**:
- Use approximate nearest neighbors (ANN)
- Implement caching for popular queries
- Add pagination for results
- Use database instead of CSV files

---

## Future Enhancements

### Algorithmic Improvements

1. **Collaborative Filtering**:
   - Add user-based recommendations
   - Implement matrix factorization (SVD)
   - Combine with content-based (hybrid approach)

2. **Deep Learning**:
   - Use BERT for semantic similarity
   - Implement neural collaborative filtering
   - Add image-based recommendations (movie posters)

3. **Advanced NLP**:
   - Extract themes and topics from reviews
   - Identify spoilers automatically
   - Sentiment analysis by aspect (acting, plot, etc.)

### Feature Additions

1. **User Profiles**:
   - Save favorite movies
   - Track watch history
   - Personalized recommendations

2. **Social Features**:
   - Share recommendations
   - User reviews and ratings
   - Friend recommendations

3. **Enhanced UI**:
   - Movie posters and images
   - Trailers and clips
   - Interactive filters (year, genre, rating)

### Technical Improvements

1. **Backend**:
   - RESTful API with Flask/FastAPI
   - Database integration (PostgreSQL)
   - Caching layer (Redis)

2. **Frontend**:
   - Web interface (React/Vue)
   - Mobile app
   - Progressive Web App (PWA)

3. **Deployment**:
   - Docker containerization
   - Cloud deployment (AWS/Azure)
   - CI/CD pipeline

---

## References

### Algorithms

- **TF-IDF**: Salton, G., & Buckley, C. (1988). "Term-weighting approaches in automatic text retrieval"
- **Cosine Similarity**: Singhal, A. (2001). "Modern Information Retrieval: A Brief Overview"
- **VADER**: Hutto, C.J. & Gilbert, E.E. (2014). "VADER: A Parsimonious Rule-based Model for Sentiment Analysis"

### Libraries

- **scikit-learn**: Pedregosa et al. (2011). "Scikit-learn: Machine Learning in Python"
- **pandas**: McKinney, W. (2010). "Data Structures for Statistical Computing in Python"
- **NLTK**: Bird, S., Klein, E., & Loper, E. (2009). "Natural Language Processing with Python"

---

## Conclusion

This technical documentation provides a comprehensive overview of the Movie Recommendation System architecture, algorithms, and implementation. The system combines multiple recommendation approaches with sentiment analysis to provide accurate and relevant movie suggestions.

For questions or clarifications, refer to the code comments and docstrings in each module.
