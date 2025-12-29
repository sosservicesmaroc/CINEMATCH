"""
Sentiment Analysis Module
Analyzes sentiment of movie reviews using VADER or TextBlob
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(str(Path(__file__).parent.parent))
import config
from src.data_loader import load_reviews_data

# Import sentiment analysis libraries
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    print("Warning: VADER not available")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("Warning: TextBlob not available")


class SentimentAnalyzer:
    """
    Sentiment analyzer for movie reviews
    Supports VADER and TextBlob
    """
    
    def __init__(self, analyzer_type='vader'):
        """
        Initialize sentiment analyzer
        
        Args:
            analyzer_type: 'vader' or 'textblob'
        """
        self.analyzer_type = analyzer_type.lower()
        
        if self.analyzer_type == 'vader':
            if not VADER_AVAILABLE:
                raise ImportError("VADER is not installed. Install with: pip install vaderSentiment")
            self.analyzer = SentimentIntensityAnalyzer()
        elif self.analyzer_type == 'textblob':
            if not TEXTBLOB_AVAILABLE:
                raise ImportError("TextBlob is not installed. Install with: pip install textblob")
            self.analyzer = None  # TextBlob doesn't need initialization
        else:
            raise ValueError(f"Unknown analyzer type: {analyzer_type}")
        
        print(f"Sentiment analyzer initialized: {self.analyzer_type.upper()}")
    
    def analyze_sentiment_vader(self, text):
        """
        Analyze sentiment using VADER
        
        Returns:
            Tuple of (sentiment_score, sentiment_label)
        """
        scores = self.analyzer.polarity_scores(text)
        compound_score = scores['compound']
        
        # Classify based on compound score
        if compound_score >= 0.05:
            label = 'positive'
        elif compound_score <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        
        return compound_score, label
    
    def analyze_sentiment_textblob(self, text):
        """
        Analyze sentiment using TextBlob
        
        Returns:
            Tuple of (sentiment_score, sentiment_label)
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # Range: -1 to 1
        
        # Classify based on polarity
        if polarity > 0.1:
            label = 'positive'
        elif polarity < -0.1:
            label = 'negative'
        else:
            label = 'neutral'
        
        return polarity, label
    
    def analyze_text(self, text):
        """
        Analyze sentiment of a single text
        
        Returns:
            Tuple of (sentiment_score, sentiment_label)
        """
        if not text or not isinstance(text, str):
            return 0.0, 'neutral'
        
        try:
            if self.analyzer_type == 'vader':
                return self.analyze_sentiment_vader(text)
            else:
                return self.analyze_sentiment_textblob(text)
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return 0.0, 'neutral'
    
    def analyze_dataframe(self, df, text_column='review'):
        """
        Analyze sentiment for all reviews in a DataFrame
        
        Args:
            df: DataFrame with reviews
            text_column: Name of column containing text
        
        Returns:
            DataFrame with added sentiment columns
        """
        print(f"Analyzing sentiment for {len(df)} reviews using {self.analyzer_type.upper()}...")
        
        results = []
        
        for idx, row in df.iterrows():
            text = row[text_column]
            score, label = self.analyze_text(text)
            results.append({'sentiment_score': score, 'sentiment_label': label})
            
            if (idx + 1) % 1000 == 0:
                print(f"Processed {idx + 1}/{len(df)} reviews...")
        
        # Add results to dataframe
        results_df = pd.DataFrame(results)
        df['sentiment_score'] = results_df['sentiment_score']
        df['sentiment_label'] = results_df['sentiment_label']
        
        print("Sentiment analysis complete!")
        return df


def visualize_sentiment_distribution(df, output_dir=None):
    """
    Create visualizations of sentiment distribution
    
    Args:
        df: DataFrame with sentiment analysis results
        output_dir: Directory to save plots (optional)
    """
    if output_dir is None:
        output_dir = config.DATA_DIR
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    
    # 1. Sentiment Label Distribution
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Pie chart of sentiment labels
    sentiment_counts = df['sentiment_label'].value_counts()
    axes[0, 0].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
                   colors=['#2ecc71', '#e74c3c', '#95a5a6'])
    axes[0, 0].set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
    
    # Bar chart of sentiment labels
    sns.countplot(data=df, x='sentiment_label', ax=axes[0, 1],
                  palette={'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'})
    axes[0, 1].set_title('Sentiment Count', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Sentiment')
    axes[0, 1].set_ylabel('Count')
    
    # Histogram of sentiment scores
    axes[1, 0].hist(df['sentiment_score'], bins=50, color='#3498db', edgecolor='black', alpha=0.7)
    axes[1, 0].set_title('Sentiment Score Distribution', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Sentiment Score')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Neutral')
    axes[1, 0].legend()
    
    # Box plot of sentiment scores by label
    sns.boxplot(data=df, x='sentiment_label', y='sentiment_score', ax=axes[1, 1],
                palette={'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'})
    axes[1, 1].set_title('Sentiment Score by Label', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Sentiment Label')
    axes[1, 1].set_ylabel('Sentiment Score')
    
    plt.tight_layout()
    
    # Save plot
    plot_path = output_dir / 'sentiment_distribution.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Sentiment distribution plot saved to {plot_path}")
    
    plt.close()
    
    # 2. Sentiment vs Rating Analysis
    if 'rating' in df.columns:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Scatter plot
        axes[0].scatter(df['rating'], df['sentiment_score'], alpha=0.3, c='#3498db')
        axes[0].set_title('Sentiment Score vs Rating', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Rating')
        axes[0].set_ylabel('Sentiment Score')
        axes[0].grid(True, alpha=0.3)
        
        # Average sentiment by rating
        avg_sentiment = df.groupby('rating')['sentiment_score'].mean()
        axes[1].bar(avg_sentiment.index, avg_sentiment.values, color='#9b59b6', edgecolor='black')
        axes[1].set_title('Average Sentiment by Rating', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Rating')
        axes[1].set_ylabel('Average Sentiment Score')
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        plot_path = output_dir / 'sentiment_vs_rating.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"Sentiment vs rating plot saved to {plot_path}")
        
        plt.close()


def process_and_save_reviews(analyzer_type='vader'):
    """
    Process reviews with sentiment analysis and save results
    
    Args:
        analyzer_type: Type of sentiment analyzer to use
    """
    print("="*50)
    print("Starting Sentiment Analysis Process")
    print("="*50)
    
    # Load reviews
    reviews_df = load_reviews_data()
    
    if reviews_df is None:
        print("Error: Could not load reviews data")
        return None
    
    print(f"\nLoaded {len(reviews_df)} reviews")
    
    # Initialize analyzer
    analyzer = SentimentAnalyzer(analyzer_type=analyzer_type)
    
    # Analyze sentiment
    reviews_df = analyzer.analyze_dataframe(reviews_df)
    
    # Display statistics
    print("\n" + "="*50)
    print("Sentiment Analysis Results")
    print("="*50)
    print(f"\nSentiment Label Distribution:")
    print(reviews_df['sentiment_label'].value_counts())
    print(f"\nSentiment Score Statistics:")
    print(reviews_df['sentiment_score'].describe())
    
    # Save updated dataset
    output_path = config.REVIEWS_FILE
    reviews_df.to_csv(output_path, index=False)
    print(f"\nUpdated reviews saved to {output_path}")
    
    # Create visualizations
    print("\nGenerating visualizations...")
    visualize_sentiment_distribution(reviews_df)
    
    print("\n" + "="*50)
    print("Sentiment Analysis Complete!")
    print("="*50)
    
    return reviews_df


if __name__ == '__main__':
    # Run sentiment analysis
    analyzer_type = config.SENTIMENT_ANALYZER
    process_and_save_reviews(analyzer_type=analyzer_type)
