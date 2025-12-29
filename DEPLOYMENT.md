# Deployment Guide for Movie Recommender Web Service

This guide provides instructions for deploying the Flask-based Movie Recommender application to cloud platforms like Render, Heroku, or AWS Elastic Beanstalk.

## Prerequisites

1.  A Git repository containing the project files.
2.  An account on your chosen cloud platform (e.g., Render, Heroku, AWS).

## Project Structure for Deployment

Ensure your project directory contains the following files and folders:

```
movie_recommendation_project/
├── web_app.py              # The main Flask application file
├── requirements.txt        # Python dependencies
├── Procfile                # Specifies the web server command
├── DEPLOYMENT.md           # This guide
├── templates/              # HTML templates (e.g., index.html)
├── static/                 # Static assets (CSS, JS, images)
├── data/                   # Data files (movies.csv, similarity_matrix.npy, etc.)
└── src/                    # Source code modules
```

## 1. Local Setup (Verification)

Before deploying, ensure the application runs correctly locally:

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the application**:
    ```bash
    gunicorn web_app:app
    ```
    Gunicorn is the production-ready WSGI server specified in the `Procfile`.

## 2. Deployment on Cloud Platforms (e.g., Render)

The application is configured to use **Gunicorn** as the production web server, which is standard for Python web apps.

### Render Deployment Steps

1.  **Connect to Git**: Link your Render account to your Git repository (GitHub, GitLab, etc.).
2.  **Create a New Web Service**: Select the repository and choose "Web Service".
3.  **Configuration**:
    *   **Name**: `movie-recommender-service` (or your preferred name)
    *   **Environment**: Python
    *   **Branch**: `main` (or your deployment branch)
    *   **Root Directory**: `movie_recommendation_project` (or the path to your project folder)
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn web_app:app` (This command is read from the `Procfile`)
4.  **Deploy**: Click "Create Web Service". Render will automatically build and deploy your application.

### Heroku Deployment Steps

1.  **Install Heroku CLI** and log in.
2.  **Create a Heroku App**:
    ```bash
    heroku create your-app-name
    ```
3.  **Set Buildpack**: Ensure the Python buildpack is used.
    ```bash
    heroku buildpacks:set heroku/python
    ```
4.  **Push to Heroku**:
    ```bash
    git push heroku main
    ```
    Heroku will detect the `requirements.txt` and `Procfile` and deploy the application.

## 3. Important Notes

*   **Data Files**: The application relies on the data files in the `data/` directory. Ensure these files are included in your repository and pushed to the cloud platform.
*   **Performance**: The initial loading of the data and model (TF-IDF matrix) is a heavy operation. This happens once when the application starts. Cloud platforms may have limits on memory and startup time. If you encounter issues, consider upgrading your service plan or pre-calculating and storing the model artifacts more efficiently.
*   **Static Files**: The application serves static files (CSS, JS) directly via Flask's built-in static file handler. For high-traffic production environments, consider using a CDN or configuring your web server (Gunicorn/Nginx) to serve static files directly.
