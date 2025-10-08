import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model Configuration
    MODEL_NAME = "gemini-2.0-flash"
    MODEL_TEMPERATURE = 0.1
    
    # Database Configuration
    DATABASE_PATH = Path(__file__).parent.parent.parent / "data" / "sample_business.db"
    
    # UI Configuration
    MAX_RESULTS_DISPLAY = 100
    MAX_RESULTS_FOR_LLM = 10
    
    # Workflow Configuration
    ENABLE_CHECKPOINTING = True
    CHECKPOINT_PATH = Path(__file__).parent.parent.parent / "data" / "checkpoints"
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Create necessary directories
        cls.DATABASE_PATH.parent.mkdir(exist_ok=True)
        if cls.ENABLE_CHECKPOINTING:
            cls.CHECKPOINT_PATH.mkdir(exist_ok=True)
        
        return True

# Global settings instance
settings = Settings()
