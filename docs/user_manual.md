# User Manual

## Movie Recommendation System with Sentiment Analysis

Welcome to the Movie Recommendation System! This manual will guide you through using all features of the application.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Main Interface](#main-interface)
3. [Searching for Movies](#searching-for-movies)
4. [Emotion-Based Recommendations](#emotion-based-recommendations)
5. [Understanding Results](#understanding-results)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [Frequently Asked Questions](#frequently-asked-questions)

---

## Getting Started

### Launching the Application

1. Open a terminal or command prompt
2. Navigate to the project directory:
   ```bash
   cd movie_recommendation_project
   ```
3. Activate the virtual environment (if using one):
   ```bash
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
4. Run the application:
   ```bash
   python app.py
   ```

The application window will open automatically.

### First Launch

On first launch, the application will:
- Load the movie dataset (34,532 movies)
- Load the reviews dataset (10,000+ reviews)
- Initialize the recommendation engines
- Display the main interface

**Loading time**: 5-10 seconds

---

## Main Interface

The application window is divided into several sections:

### 1. Title Bar
- Displays: "🎬 Movie Recommendation System"

### 2. Search by Title Section
- **Movie Title field**: Enter the name of a movie
- **Search & Recommend button**: Click to search and get recommendations

### 3. Recommend by Emotion Section
- **Emotion dropdown**: Select your current emotional state
- **Recommend button**: Click to get emotion-based recommendations

### 4. Results Section
- Large scrollable text area displaying:
  - Search results
  - Movie details
  - Recommendations

### 5. Status Bar
- Shows current status and dataset statistics
- Example: "Ready | Movies: 34532 | Reviews: 10000"

---

## Searching for Movies

### How to Search

1. **Enter a movie title** in the "Movie Title" field
   - You don't need to type the exact title
   - The system uses fuzzy matching to find close matches
   
2. **Click "Search & Recommend"** or press Enter

3. **View the results**:
   - The matching movie appears first
   - Followed by 5 similar movie recommendations

### Search Examples

**Example 1: Exact Match**
```
Input: The Matrix
Result: Finds "The Matrix" (1999) and recommends similar sci-fi action movies
```

**Example 2: Partial Match**
```
Input: dark knight
Result: Finds "The Dark Knight" and recommends superhero/action movies
```

**Example 3: Misspelled**
```
Input: inceptoin
Result: Still finds "Inception" using fuzzy matching
```

### Understanding Search Results

Each movie result displays:

```
================================================================================
Title: The Matrix
Year: 1999
Genres: Action, Science Fiction
Rating: 8.7/10 (15234 votes)
Match Score: 95.5%

Overview:
Set in the 22nd century, The Matrix tells the story of a computer hacker...
================================================================================
```

**Fields explained**:
- **Title**: Movie name
- **Year**: Release year
- **Genres**: Movie categories
- **Rating**: Average user rating out of 10
- **Match Score**: How similar this movie is to your search (for recommendations)
- **Overview**: Brief plot summary

---

## Emotion-Based Recommendations

### How It Works

The system maps your emotional state to appropriate movie genres:

| Emotion | Genres |
|---------|--------|
| **Joie / Joy** | Comedy, Adventure, Family, Animation |
| **Colère / Anger** | Action, Thriller, Crime |
| **Tristesse / Sadness** | Drama, Romance |
| **Peur / Fear** | Horror, Thriller, Mystery |

### How to Get Emotion-Based Recommendations

1. **Select your emotion** from the dropdown menu
   - Choose from: joie/joy, colère/anger, tristesse/sadness, peur/fear

2. **Click "Recommend"**

3. **Browse the results**:
   - Top 5 movies matching your emotional state
   - All movies have a minimum rating of 6.0/10

### Example Usage

**Scenario**: You're feeling happy and want something uplifting

1. Select "joie / joy" from the dropdown
2. Click "Recommend"
3. Receive recommendations like:
   - Comedies
   - Adventure films
   - Family-friendly movies
   - Animated features

**Scenario**: You're in the mood for something intense

1. Select "colère / anger" from the dropdown
2. Click "Recommend"
3. Receive recommendations like:
   - Action-packed thrillers
   - Crime dramas
   - Intense action movies

---

## Understanding Results

### Recommendation Scores

**Match Score (for title-based search)**:
- Ranges from 0% to 100%
- Higher scores indicate greater similarity
- Based on:
  - Genre overlap (40%)
  - Content similarity using TF-IDF (40%)
  - Rating similarity (20%)

**Emotion Score (for emotion-based recommendations)**:
- Ranges from 0% to 100%
- Higher scores indicate better match to your emotion
- Based on:
  - Genre match (50%)
  - Movie rating (30%)
  - Popularity (20%)

### Movie Ratings

- **8.0-10.0**: Excellent movies, highly rated
- **6.0-7.9**: Good movies, generally well-received
- **4.0-5.9**: Average movies, mixed reviews
- **Below 4.0**: Poor ratings, proceed with caution

### Vote Count

- Higher vote counts indicate more reliable ratings
- Movies with 1000+ votes are generally trustworthy
- Movies with <100 votes may have unreliable ratings

---

## Tips and Best Practices

### For Better Search Results

1. **Use common movie titles**: Search for well-known movies for better recommendations
2. **Try variations**: If you don't find a movie, try alternative titles or spellings
3. **Be specific**: Include year or distinctive words if the title is common
4. **Use English titles**: The dataset primarily contains English movie titles

### For Better Recommendations

1. **Explore different emotions**: Try all emotion categories to discover new movies
2. **Check multiple results**: Don't just look at the first recommendation
3. **Read the overview**: The plot summary helps you decide if you'll enjoy the movie
4. **Consider the rating**: Balance between high ratings and interesting plots

### Navigation Tips

1. **Scroll through results**: Use the scrollbar to see all recommendations
2. **Clear results**: New searches automatically clear previous results
3. **Try both methods**: Use title search AND emotion recommendations for variety

---

## Frequently Asked Questions

### Q: Why can't I find a specific movie?

**A**: The dataset contains 34,532 movies, primarily from Wikipedia. Some very recent or obscure movies may not be included. Try:
- Checking the spelling
- Using the original title
- Searching for similar movies instead

### Q: How accurate are the recommendations?

**A**: The system uses industry-standard algorithms (TF-IDF, cosine similarity) combined with multiple factors. Recommendations are based on:
- Content similarity
- Genre matching
- Rating patterns
- User sentiment from 10,000+ reviews

### Q: Can I get more than 5 recommendations?

**A**: The default is 5 recommendations for optimal user experience. To change this:
1. Edit the `.env` file
2. Change `N_RECOMMENDATIONS=5` to your desired number
3. Restart the application

### Q: What's the difference between the two recommendation methods?

**A**: 
- **Title Search**: Finds movies similar to a specific movie you already know
- **Emotion-Based**: Suggests movies matching your current mood, regardless of specific titles

### Q: Why do some movies have low vote counts?

**A**: The dataset includes both popular blockbusters and lesser-known films. Low vote counts may indicate:
- Older movies with fewer reviews
- Independent or foreign films
- Recently added movies

### Q: How is sentiment analysis used?

**A**: The system analyzes 10,000+ movie reviews to:
- Understand audience reception
- Validate rating accuracy
- Provide additional context for recommendations
- Generate insights about movie reception

### Q: Can I use this offline?

**A**: Yes! Once installed, the application works completely offline. All data is stored locally.

### Q: How do I close the application?

**A**: Simply close the window or press Alt+F4 (Windows/Linux) or Cmd+Q (macOS).

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Search (when in title field) |
| **Tab** | Navigate between fields |
| **Alt+F4** | Close application (Windows/Linux) |
| **Cmd+Q** | Close application (macOS) |

---

## Getting More Information

### Additional Resources

- **Technical Documentation**: `docs/technical_documentation.md`
- **Installation Guide**: `docs/installation_guide.md`
- **Project Notebook**: `notebook/project_report.ipynb`
- **Main README**: `README.md`

### Exploring the Data

To explore the dataset directly:

```bash
# View movies
python -c "import pandas as pd; print(pd.read_csv('data/movies_metadata.csv').head())"

# View reviews
python -c "import pandas as pd; print(pd.read_csv('data/reviews_data.csv').head())"
```

---

## Troubleshooting

### Application won't start

1. Verify Python is installed: `python --version`
2. Check dependencies: `pip install -r requirements.txt`
3. Ensure you're in the correct directory
4. Check for error messages in the terminal

### No results found

1. Try a different search term
2. Check spelling
3. Try searching for a more popular movie
4. Verify the dataset files exist in `data/` folder

### Application is slow

1. Close other applications to free RAM
2. Reduce the number of recommendations in `.env`
3. Restart the application

---

## Enjoy Your Movie Discovery! 🎬

We hope you enjoy using the Movie Recommendation System. Happy watching!

For technical support or questions, refer to the documentation in the `docs/` folder.
