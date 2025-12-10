"""
Utility functions for Customer Relationship AI Agent
"""
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib


class TextProcessor:
    """Text processing utilities"""

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
        text = re.sub(r'[^\w\s\.\,\!\?\-\@]', '', text)  # Remove special chars
        return text

    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email from text"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number from text"""
        pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def extract_amount(text: str) -> Optional[float]:
        """Extract monetary amount from text"""
        pattern = r'\$\s?(\d+\.?\d*)|(\d+\.?\d*)\s?(?:dollars|bucks|USD)'
        match = re.search(pattern, text)
        if match:
            amount = match.group(1) or match.group(2)
            return float(amount)
        return None

    @staticmethod
    def keywords_in_text(text: str, keywords: List[str]) -> List[str]:
        """Find keywords in text"""
        text_lower = text.lower()
        found = [kw for kw in keywords if kw.lower() in text_lower]
        return found


class SentimentAnalyzer:
    """Sentiment analysis utilities"""

    POSITIVE_WORDS = {
        "great", "excellent", "amazing", "wonderful", "fantastic", "love",
        "happy", "satisfied", "good", "perfect", "awesome", "best", "thanks"
    }

    NEGATIVE_WORDS = {
        "bad", "terrible", "awful", "horrible", "worst", "hate", "angry",
        "disappointed", "poor", "problem", "issue", "complaint", "sad"
    }

    @classmethod
    def simple_sentiment(cls, text: str) -> str:
        """Simple sentiment analysis based on keyword matching"""
        text_lower = text.lower()

        positive_count = sum(1 for word in cls.POSITIVE_WORDS if word in text_lower)
        negative_count = sum(1 for word in cls.NEGATIVE_WORDS if word in text_lower)

        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        return "neutral"


class DataValidator:
    """Data validation utilities"""

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone format"""
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone.replace('-', '').replace(' ', '').replace('.', '')))

    @staticmethod
    def is_valid_customer_id(customer_id: str) -> bool:
        """Validate customer ID format"""
        return len(customer_id) > 0 and len(customer_id) <= 50

    @staticmethod
    def validate_profile_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate customer profile data"""
        errors = []

        if "customer_id" not in data:
            errors.append("customer_id is required")
        elif not DataValidator.is_valid_customer_id(data["customer_id"]):
            errors.append("Invalid customer_id format")

        if "name" not in data or not data["name"]:
            errors.append("name is required")

        if "email" in data and data["email"] and not DataValidator.is_valid_email(data["email"]):
            errors.append("Invalid email format")

        return len(errors) == 0, errors


class FileManager:
    """File management utilities"""

    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str) -> bool:
        """Save data to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False

    @staticmethod
    def load_json(filepath: str) -> Optional[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return None

    @staticmethod
    def backup_file(filepath: str) -> bool:
        """Create backup of file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{filepath}.backup_{timestamp}"
            with open(filepath, 'r') as src:
                with open(backup_path, 'w') as dst:
                    dst.write(src.read())
            return True
        except Exception as e:
            print(f"Error backing up file: {e}")
            return False


class IDGenerator:
    """ID generation utilities"""

    @staticmethod
    def generate_customer_id(name: str, email: str) -> str:
        """Generate unique customer ID"""
        combined = f"{name}_{email}_{datetime.now().isoformat()}"
        hash_obj = hashlib.md5(combined.encode())
        return f"cust_{hash_obj.hexdigest()[:8]}"

    @staticmethod
    def generate_memory_id() -> str:
        """Generate unique memory ID"""
        timestamp = datetime.now().isoformat()
        hash_obj = hashlib.md5(timestamp.encode())
        return f"mem_{hash_obj.hexdigest()[:8]}"


class DateTimeUtil:
    """DateTime utilities"""

    @staticmethod
    def format_datetime(dt: str, format_str: str = "%Y-%m-%d %H:%M") -> str:
        """Format datetime string"""
        try:
            dt_obj = datetime.fromisoformat(dt)
            return dt_obj.strftime(format_str)
        except Exception:
            return dt

    @staticmethod
    def get_relative_time(dt: str) -> str:
        """Get relative time (e.g., '2 hours ago')"""
        try:
            dt_obj = datetime.fromisoformat(dt)
            now = datetime.now(dt_obj.tzinfo) if dt_obj.tzinfo else datetime.now()
            diff = now - dt_obj

            if diff.days > 0:
                return f"{diff.days} day(s) ago"
            elif diff.seconds // 3600 > 0:
                return f"{diff.seconds // 3600} hour(s) ago"
            elif diff.seconds // 60 > 0:
                return f"{diff.seconds // 60} minute(s) ago"
            else:
                return "just now"
        except Exception:
            return "unknown time"


class Logger:
    """Simple logging utility"""

    @staticmethod
    def log(level: str, message: str, component: str = "Agent"):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] [{component}] {message}")

    @staticmethod
    def info(message: str, component: str = "Agent"):
        Logger.log("INFO", message, component)

    @staticmethod
    def warning(message: str, component: str = "Agent"):
        Logger.log("WARNING", message, component)

    @staticmethod
    def error(message: str, component: str = "Agent"):
        Logger.log("ERROR", message, component)

    @staticmethod
    def debug(message: str, component: str = "Agent"):
        Logger.log("DEBUG", message, component)
