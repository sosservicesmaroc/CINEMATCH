# Installation Guide

## Movie Recommendation System with Sentiment Analysis

This guide provides detailed instructions for installing and setting up the Movie Recommendation System on your local machine.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Verification](#verification)
4. [Troubleshooting](#troubleshooting)
5. [Configuration](#configuration)

---

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 500 MB free space
- **Display**: 1024x768 minimum resolution

### Software Prerequisites

- Python 3.8+ with pip
- Internet connection (for initial setup)
- Text editor (optional, for configuration)

---

## Installation Steps

### Step 1: Extract the Project

Extract the downloaded ZIP file to your desired location:

```bash
# On Linux/macOS
unzip movie_recommendation_project_final.zip
cd movie_recommendation_project

# On Windows
# Right-click the ZIP file and select "Extract All..."
# Navigate to the extracted folder
```

### Step 2: Verify Python Installation

Check that Python is installed and accessible:

```bash
python --version
# or
python3 --version
```

You should see output like: `Python 3.8.x` or higher.

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Install via Homebrew: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

### Step 3: Create Virtual Environment (Recommended)

Creating a virtual environment isolates the project dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- pandas, numpy (data processing)
- scikit-learn (machine learning)
- matplotlib, seaborn (visualization)
- nltk, textblob, vaderSentiment (NLP)
- fuzzywuzzy (fuzzy matching)
- python-dotenv (configuration)
- jupyter, notebook (notebooks)

**Installation time**: 2-5 minutes depending on your internet connection.

### Step 5: Download NLTK Data (Optional)

If using TextBlob for sentiment analysis:

```bash
python -m textblob.download_corpora
```

This downloads necessary language models for TextBlob.

### Step 6: Verify Installation

Run the configuration script to verify everything is set up correctly:

```bash
python config.py
```

Expected output:
```
Movie Recommendation System - Configuration
==================================================
project_root        : /path/to/movie_recommendation_project
data_dir            : /path/to/movie_recommendation_project/data
movies_file         : /path/to/movie_recommendation_project/data/movies_metadata.csv
reviews_file        : /path/to/movie_recommendation_project/data/reviews_data.csv
debug               : True
port                : 5000
n_recommendations   : 5
sentiment_analyzer  : vader
==================================================

All directories created/verified successfully!
```

---

## Verification

### Test Data Loading

```bash
python src/data_loader.py
```

Expected output:
```
Cleaning movies data...
Cleaned dataset: 34532 movies

Movies Dataset Info:
[Shows first 5 movies]

Cleaning reviews data...
Cleaned reviews: 10000 reviews

Reviews Dataset Info:
[Shows first 5 reviews]
```

### Test Recommendation Engine

```bash
python src/recommendation_engine.py
```

This will run tests on the recommendation engine and display sample recommendations.

### Test Sentiment Analyzer

```bash
python src/sentiment_analyzer.py
```

This will analyze all reviews and generate visualizations.

---

## Troubleshooting

### Issue: "Python not found"

**Solution**: Ensure Python is installed and added to your system PATH.

- **Windows**: Reinstall Python and check "Add Python to PATH" during installation
- **Linux/macOS**: Use `python3` instead of `python`

### Issue: "pip: command not found"

**Solution**: Install pip or use `python -m pip` instead:

```bash
python3 -m pip install -r requirements.txt
```

### Issue: "Permission denied" during installation

**Solution**: Use `--user` flag or run with appropriate permissions:

```bash
pip install --user -r requirements.txt
```

### Issue: "Module not found" when running scripts

**Solution**: Ensure you're in the project root directory and virtual environment is activated:

```bash
cd movie_recommendation_project
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

### Issue: "Dataset files not found"

**Solution**: Ensure the `data/` directory contains the CSV files:

```bash
ls data/
# Should show: movies_metadata.csv, reviews_data.csv, movies_raw.json
```

If files are missing, the dataset preparation script will need to be run (already done in this package).

### Issue: Tkinter not available

**Solution**: Install tkinter:

- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Tkinter is included with Python
- **Windows**: Tkinter is included with Python

### Issue: Slow performance

**Solution**: 
- Close other applications to free up RAM
- Reduce `N_RECOMMENDATIONS` in `.env` file
- Use a smaller subset of data for testing

---

## Configuration

### Environment Variables

The `.env` file contains all configuration settings. You can modify these values:

```env
# Application Settings
DEBUG=True              # Set to False for production
PORT=5000              # Port for web server (if applicable)

# Data Paths (relative to project root)
DATA_DIR=data
MOVIES_FILE=movies_metadata.csv
REVIEWS_FILE=reviews_data.csv

# Model Settings
N_RECOMMENDATIONS=5     # Number of recommendations to return
MIN_SIMILARITY_SCORE=0.1  # Minimum similarity threshold

# Sentiment Analysis
SENTIMENT_ANALYZER=vader  # Options: vader, textblob

# Interface Settings
WINDOW_WIDTH=900       # GUI window width
WINDOW_HEIGHT=700      # GUI window height
```

### Customizing Recommendations

To adjust recommendation behavior, edit `config.py`:

```python
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
```

---

## Next Steps

Once installation is complete:

1. **Run the application**: `python app.py`
2. **Explore the notebook**: `jupyter notebook notebook/project_report.ipynb`
3. **Read the documentation**: Check `docs/user_manual.md` and `docs/technical_documentation.md`
4. **Test different features**: Try searching for movies and emotion-based recommendations

---

## Getting Help

If you encounter issues not covered in this guide:

1. Check the main `README.md` file
2. Review the technical documentation in `docs/technical_documentation.md`
3. Verify all dependencies are correctly installed
4. Ensure you're using Python 3.8 or higher

---

**Installation Complete!** 🎉

You're now ready to use the Movie Recommendation System. Run `python app.py` to start the application.
