# 🎬 Movie Recommendation System with Sentiment Analysis

A comprehensive Python-based movie recommendation system featuring content-based filtering, emotion-based recommendations, and sentiment analysis of user reviews. This project was developed as an end-of-studies graduation project.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [Dataset](#dataset)
- [Documentation](#documentation)
- [Screenshots](#screenshots)

## 🎯 Overview

This project implements a complete movie recommendation system that combines multiple approaches:

1. **Content-Based Filtering**: Recommends movies based on similarity in genres, ratings, and plot descriptions using TF-IDF
2. **Emotion-Based Recommendations**: Suggests movies matching the user's current emotional state
3. **Sentiment Analysis**: Analyzes 10,000+ movie reviews using VADER sentiment analysis
4. **Interactive GUI**: User-friendly Tkinter interface for searching and discovering movies

## ✨ Features

### Core Functionality

- **Fuzzy Movie Search**: Find movies even with approximate title matches
- **Hybrid Recommendation Engine**: Combines genre similarity, rating similarity, and content similarity (TF-IDF)
- **Emotion Mapping**: Maps emotions (joy, anger, sadness, fear) to appropriate movie genres
- **Sentiment Analysis**: Processes reviews with VADER to extract sentiment scores and labels
- **Rich Dataset**: 34,000+ movies and 10,000+ reviews with sentiment scores

### User Interface

- Clean and intuitive Tkinter GUI
- Search movies by title with instant recommendations
- Recommend movies based on current emotion
- Scrollable results display with detailed movie information
- Real-time status updates

### Visualizations

- Sentiment distribution charts (pie chart, bar chart, histogram)
- Sentiment score analysis by rating
- Genre distribution analysis
- Rating vs popularity correlations

## 📁 Project Structure

```
movie_recommendation_project/
│
├── app.py                      # Main Tkinter application
├── config.py                   # Configuration and settings
├── prepare_dataset.py          # Dataset preparation script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── README.md                   # This file
│
├── data/                       # Data directory
│   ├── movies_metadata.csv     # Movies dataset (34,532 movies)
│   ├── reviews_data.csv        # Reviews with sentiment (10,000+ reviews)
│   ├── movies_raw.json         # Raw movie data from Wikipedia
│   └── *.png                   # Visualization outputs
│
├── src/                        # Source code modules
│   ├── data_loader.py          # Data loading and preprocessing
│   ├── data_exploration.py     # Exploratory data analysis
│   ├── recommendation_engine.py # Content-based recommendation
│   ├── emotion_recommender.py  # Emotion-based recommendation
│   └── sentiment_analyzer.py   # Sentiment analysis module
│
├── notebook/                   # Jupyter notebooks
│   └── project_report.ipynb    # Complete project analysis
│
├── docs/                       # Documentation
│   ├── technical_documentation.md
│   ├── user_manual.md
│   └── installation_guide.md
│
└── config/                     # Configuration files
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 500 MB free disk space

### Step-by-Step Installation

1. **Extract the project archive**
   ```bash
   unzip movie_recommendation_project_final.zip
   cd movie_recommendation_project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data (for TextBlob, if needed)**
   ```bash
   python -m textblob.download_corpora
   ```

5. **Verify installation**
   ```bash
   python config.py
   ```

## 💻 Usage

### Running the Application Locally

1. **Launch the GUI application**
   ```bash
   python app.py
   ```

2. **Search for movies**
   - Enter a movie title in the search field
   - Click "Search & Recommend" or press Enter
   - View the movie details and similar recommendations

3. **Get emotion-based recommendations**
   - Select your current emotion from the dropdown
   - Click "Recommend"
   - Discover movies matching your mood

### Running Individual Modules

**Data Exploration**
```bash
python src/data_exploration.py
```

**Sentiment Analysis**
```bash
python src/sentiment_analyzer.py
```

**Test Recommendation Engine**
```bash
python src/recommendation_engine.py
```

**Test Emotion Recommender**
```bash
python src/emotion_recommender.py
```

### Configuration

Edit the `.env` file to customize settings:

```env
# Application Settings
DEBUG=True
PORT=5000

# Data Paths
DATA_DIR=data
MOVIES_FILE=movies_metadata.csv
REVIEWS_FILE=reviews_data.csv

# Model Settings
N_RECOMMENDATIONS=5
MIN_SIMILARITY_SCORE=0.1

# Sentiment Analysis
SENTIMENT_ANALYZER=vader  # Options: vader, textblob

# Interface Settings
WINDOW_WIDTH=900
WINDOW_HEIGHT=700
```

## 🛠️ Technologies

### Core Libraries

- **pandas** (2.0.3): Data manipulation and analysis
- **numpy** (1.24.3): Numerical computing
- **scikit-learn** (1.3.0): Machine learning algorithms (TF-IDF, cosine similarity)

### Natural Language Processing

- **nltk** (3.8.1): Natural language toolkit
- **textblob** (0.17.1): Text processing and sentiment analysis
- **vaderSentiment** (3.3.2): Sentiment analysis optimized for social media text

### Visualization

- **matplotlib** (3.7.2): Plotting and visualization
- **seaborn** (0.12.2): Statistical data visualization

### User Interface

- **tkinter**: Built-in Python GUI framework

### Utilities

- **fuzzywuzzy** (0.18.0): Fuzzy string matching
- **python-dotenv** (1.0.0): Environment variable management
- **requests** (2.31.0): HTTP library for data download

## 📊 Dataset

### Movies Dataset

- **Source**: Wikipedia Movie Data
- **Size**: 34,532 movies
- **Features**:
  - Title, year, genres
  - Overview/plot description
  - Cast information
  - Vote average, vote count
  - Popularity score

### Reviews Dataset

- **Size**: 10,000+ reviews
- **Features**:
  - Movie ID and title
  - Review text
  - Rating (1-10)
  - Original sentiment label
  - **Sentiment score** (calculated by VADER)
  - **Sentiment label** (positive/negative/neutral)

### Data Sources

- Movies: [Wikipedia Movie Data](https://github.com/prust/wikipedia-movie-data)
- Reviews: Synthetically generated based on movie ratings with realistic templates

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- **Installation Guide**: Step-by-step setup instructions
- **User Manual**: How to use the application
- **Technical Documentation**: Algorithm explanations and architecture
- **API Reference**: Module and function documentation

## 📸 Screenshots

### Main Application Interface

The application features a clean, user-friendly interface with:
- Movie title search with fuzzy matching
- Emotion-based recommendation selector
- Scrollable results display
- Real-time status updates

### Sentiment Analysis Visualizations

Generated visualizations include:
- Sentiment distribution (pie chart and bar chart)
- Sentiment score histogram
- Sentiment vs rating correlation
- Box plots by sentiment category

## 🎓 Project Implementation

This project fulfills all requirements for the graduation project:

### Stage 1: Data Preparation and Exploration (20 points)
✅ Dataset loading and cleaning  
✅ Handling missing values and JSON parsing  
✅ Descriptive statistics  
✅ Visualizations (genre distribution, ratings, popularity)

### Stage 2: Search and Recommendation Engine (20 points)
✅ Fuzzy title search  
✅ Movie information display  
✅ Multi-factor recommendations (genre, rating, TF-IDF)

### Stage 3: Emotion-Based Recommendations (15 points)
✅ Emotion to genre mapping  
✅ Recommendations based on user emotion

### Stage 4: Tkinter Interface (15 points)
✅ Title search field  
✅ Emotion selector  
✅ Search and recommend buttons  
✅ Scrollable results display

### Stage 5: Sentiment Analysis (20 points)
✅ VADER sentiment analyzer  
✅ 10,000+ reviews processed  
✅ Sentiment score and label columns  
✅ Distribution visualizations

### Stage 6: Final Report (10 points)
✅ Complete Jupyter notebook  
✅ Pedagogical explanations  
✅ Graph interpretations  
✅ Clear conclusions

## 🚀 Deployment

### Local Deployment

Simply run:
```bash
python app.py
```

### Server Deployment (Optional)

For web server deployment with Flask:

1. Uncomment Flask routes in `app.py` (if added)
2. Configure environment variables:
   ```env
   DEBUG=False
   PORT=8080
   ```
3. Run with:
   ```bash
   python app.py
   ```

## 🤝 Contributing

This is a graduation project, but suggestions and improvements are welcome:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is developed for educational purposes as part of an end-of-studies graduation project.

## 👨‍💻 Author

Developed as a graduation project demonstrating:
- Data science and machine learning skills
- Natural language processing
- Software engineering best practices
- User interface design

## 🙏 Acknowledgments

- Wikipedia Movie Data for the comprehensive movie dataset
- VADER Sentiment Analysis for robust sentiment detection
- The Python community for excellent libraries and tools

---

**Note**: This project is fully functional and ready for demonstration. All requirements have been implemented and tested.

For questions or issues, please refer to the documentation in the `docs/` folder.
