import re

def preprocess_text(text: str) -> str:
    """
    Cleans and preprocesses the input text for fake news detection.
    """
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove punctuation and special characters
    # Keeping only alphanumeric and whitespaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
