"""
Configuration settings for Customer Relationship AI Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# Supermemory Configuration
SUPERMEMORY_API_KEY = os.getenv("SUPERMEMORY_API_KEY", "")
SUPERMEMORY_BASE_URL = os.getenv("SUPERMEMORY_BASE_URL", "https://api.supermemory.ai")
USE_LOCAL_MEMORY = os.getenv("USE_LOCAL_MEMORY", "true").lower() == "true"

# Agent Configuration
MAX_MEMORY_RETRIEVAL = int(os.getenv("MAX_MEMORY_RETRIEVAL", "5"))
MAX_PROFILE_MEMORIES = int(os.getenv("MAX_PROFILE_MEMORIES", "20"))

# Streamlit Configuration
STREAMLIT_THEME = os.getenv("STREAMLIT_THEME", "light")
STREAMLIT_MAX_UPLOAD_SIZE = int(os.getenv("STREAMLIT_MAX_UPLOAD_SIZE", "200"))

# Application Settings
APP_NAME = "Customer Relationship AI Agent"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Sentiment Analysis Settings
SENTIMENT_LABELS = ["positive", "neutral", "negative"]

# Product Categories
PRODUCT_CATEGORIES = {
    "electronics": ["phone", "laptop", "computer", "tablet", "headphones", "camera"],
    "clothing": ["shirt", "pants", "dress", "shoes", "jacket", "sweater"],
    "home": ["home", "furniture", "decor", "kitchen", "appliances", "bedding"],
    "sports": ["sports", "gym", "fitness", "exercise", "yoga", "running"],
    "food": ["food", "snacks", "coffee", "tea", "beverage", "grocery"],
    "books": ["book", "ebook", "reading", "novel", "textbook"],
}

# Issue Categories
ISSUE_CATEGORIES = [
    "billing",
    "product_quality",
    "shipping",
    "customer_service",
    "technical",
    "other"
]

# Response Templates
RESPONSE_TEMPLATES = {
    "greeting": "Hello {name}! How can I assist you today?",
    "farewell": "Thank you for contacting us, {name}. Have a great day!",
    "help": "I'm here to help! How can I assist you?"
}

def validate_config():
    """Validate configuration"""
    errors = []

    if not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is not set")

    if not USE_LOCAL_MEMORY and not SUPERMEMORY_API_KEY:
        errors.append("SUPERMEMORY_API_KEY is required if not using local memory")

    return errors

def print_config():
    """Print current configuration"""
    print(f"""
    {'='*60}
    {APP_NAME} v{APP_VERSION}
    {'='*60}
    
    OpenAI Configuration:
      - Model: {OPENAI_MODEL}
      - Temperature: {OPENAI_TEMPERATURE}
      - API Key Set: {bool(OPENAI_API_KEY)}
    
    Memory Configuration:
      - Use Local Memory: {USE_LOCAL_MEMORY}
      - Supermemory API Key Set: {bool(SUPERMEMORY_API_KEY)}
      - Max Memories Retrieved: {MAX_MEMORY_RETRIEVAL}
    
    Debug Mode: {DEBUG}
    {'='*60}
    """)

if __name__ == "__main__":
    print_config()
    errors = validate_config()
    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  ❌ {error}")
