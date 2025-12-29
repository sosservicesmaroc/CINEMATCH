# Quick Start Guide

## Movie Recommendation System - Graduation Project

### Installation (3 steps)

1. **Extract the ZIP file**
   ```bash
   unzip movie_recommendation_project_final.zip
   cd movie_recommendation_project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

### Usage

**Search for movies:**
1. Type a movie title (e.g., "Matrix")
2. Click "Search & Recommend" or press Enter
3. View similar movie recommendations

**Get emotion-based recommendations:**
1. Select your emotion from dropdown (joy, anger, sadness, fear)
2. Click "Recommend"
3. Discover movies matching your mood

### Project Contents

- **app.py** - Main GUI application
- **config.py** - Configuration settings
- **requirements.txt** - Python dependencies
- **README.md** - Complete documentation
- **data/** - Movie and review datasets (34,532 movies, 10,000+ reviews)
- **src/** - Source code modules
- **docs/** - Technical documentation and guides
- **notebook/** - Project analysis report

### Features

✅ 34,532 movies from Wikipedia dataset  
✅ 10,000+ reviews with sentiment analysis  
✅ Hybrid recommendation algorithm (TF-IDF + Genre + Rating)  
✅ Emotion-based recommendations  
✅ Fuzzy search with typo tolerance  
✅ Interactive Tkinter GUI  
✅ Complete documentation  

### System Requirements

- Python 3.8 or higher
- 500 MB disk space
- 4 GB RAM (recommended)

### Troubleshooting

**Issue:** "Module not found"  
**Solution:** Run `pip install -r requirements.txt`

**Issue:** "Dataset not found"  
**Solution:** Ensure you're in the project directory

**Issue:** Tkinter not available  
**Solution:** Install python3-tk (Ubuntu: `sudo apt-get install python3-tk`)

### Documentation

- **Installation Guide:** `docs/installation_guide.md`
- **User Manual:** `docs/user_manual.md`
- **Technical Docs:** `docs/technical_documentation.md`
- **Project Report:** `notebook/project_report.md`

### Contact

For questions or issues, refer to the complete documentation in the `docs/` folder.

---

**Ready to use! Just run `python app.py` to start.**
