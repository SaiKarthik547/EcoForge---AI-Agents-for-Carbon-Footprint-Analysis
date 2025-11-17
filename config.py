import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for EcoForge application"""
    
    # Application Settings
    APP_TITLE = os.getenv("APP_TITLE", "EcoForge - AI Agents for Carbon Footprint Analysis")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Transform your lifestyle with AI-powered environmental insights")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    # API Keys (Optional - app works with mock data if not provided)
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "ecoforge-agents")
    
    CLIMATIQ_API_KEY = os.getenv("CLIMATIQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Demo Mode Settings
    USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
    ENABLE_ANIMATIONS = os.getenv("ENABLE_ANIMATIONS", "true").lower() == "true"
    SHOW_AGENT_COMMUNICATION = os.getenv("SHOW_AGENT_COMMUNICATION", "true").lower() == "true"
    
    @classmethod
    def get_api_status(cls):
        """Get status of API integrations"""
        return {
            "langsmith": bool(cls.LANGSMITH_API_KEY),
            "climatiq": bool(cls.CLIMATIQ_API_KEY),
            "tavily": bool(cls.TAVILY_API_KEY),
            "google": bool(cls.GOOGLE_API_KEY),
            "openai": bool(cls.OPENAI_API_KEY),
            "mock_mode": cls.USE_MOCK_DATA
        }
    
    @classmethod
    def is_production_ready(cls):
        """Check if app has all required API keys for production"""
        required_keys = [cls.GOOGLE_API_KEY or cls.OPENAI_API_KEY]  # At least one LLM API
        return all(required_keys) and not cls.USE_MOCK_DATA