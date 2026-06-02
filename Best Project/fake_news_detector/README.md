# Fake News Detector AI

A modern, attractive, AI-powered desktop application built entirely in Python to detect fake news. It uses `CustomTkinter` for a beautiful, dark-themed UI and supports loading trained machine learning models to classify news articles or headlines.

## Features
- **Modern UI**: Dark-themed, responsive dashboard built with CustomTkinter.
- **AI Chatbot Interface**: Conversational feedback during analysis.
- **ML Integration**: Automatically loads `.pkl` or `.joblib` models from the `models/` directory or current directory.
- **Fallback Mode**: Built-in heuristic mock-model if no ML model is provided.
- **History Tracking**: Keeps a session history of your analyses.
- **Antigravity Mode**: A fun easter egg!

## Installation

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your models:
   Place your trained model as `model.pkl` or `model.joblib` and vectorizer as `vectorizer.pkl` or `vectorizer.joblib` into the `models/` directory.

3. Run the app:
   ```bash
   python main.py
   ```
