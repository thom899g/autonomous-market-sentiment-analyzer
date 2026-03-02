"""
Configuration module for Autonomous Market Sentiment Analyzer.
Centralized configuration management with environment variable support.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation"""
    service_account_path: str
    database_url: str
    
    def validate(self) -> bool:
        """Validate Firebase configuration exists"""
        if not os.path.exists(self.service_account_path):
            raise FileNotFoundError(f"Firebase service account file not found: {self.service_account_path}")
        if not self.database_url:
            raise ValueError("Firebase database URL is required")
        return True

@dataclass
class TradingConfig:
    """Trading platform configuration"""
    # Alpaca Trading API (preferred for realistic trading simulation)
    alpaca_api_key: str
    alpaca_secret_key: str
    alpaca_base_url: str = "https://paper-api.alpaca.markets"
    
    # CCXT exchange configurations (backup/alternative)
    exchange_id: str = "binance"
    testnet: bool = True
    
    # Risk management
    max_position_size: float = 0.1  # 10% of portfolio per trade
    stop_loss_pct: float = 0.02  # 2% stop loss
    take_profit_pct: float = 0.05  # 5% take profit

@dataclass
class SentimentConfig:
    """Sentiment analysis configuration"""
    # Data sources
    news_api_key: Optional[str] = None
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    twitter_access_token: Optional[str] = None
    twitter_access_secret: Optional[str] = None
    
    # Analysis parameters
    sentiment_update_interval: int = 300  # 5 minutes
    historical_window_days: int = 30
    min_confidence_threshold: float = 0.6
    
    # Market symbols to monitor
    default_symbols: list = None
    
    def __post_init__(self):
        if self.default_symbols is None:
            self.default_symbols = ["BTC/USDT", "ETH/USDT", "AAPL", "GOOGL", "MSFT"]

@dataclass
class MLConfig:
    """Machine learning model configuration"""
    model_retrain_interval_hours: int = 24
    feature_window_size: int = 50  # Number of periods for feature calculation
    prediction_horizon: int = 10   # Predict 10 periods ahead
    test_size: float = 0.2
    
    # Model hyperparameters
    random_state: int = 42
    n_estimators: int = 100

class Config:
    """Main configuration class"""
    def __init__(self):
        self.firebase = FirebaseConfig(
            service_account_path=os.getenv("FIREBASE_SERVICE_ACCOUNT", "firebase-service-account.json"),
            database_url=os.getenv("FIREBASE_DATABASE_URL", "")
        )
        
        self.trading = TradingConfig(
            alpaca_api_key=os.getenv("ALPACA_API_KEY", ""),
            alpaca_secret_key=os.getenv("ALPACA_SECRET_KEY", ""),
            alpaca_base_url=os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
        )
        
        self.sentiment = SentimentConfig(
            news_api_key=os.getenv("NEWS_API_KEY"),
            twitter_api_key=os.getenv("TWITTER_API_KEY"),
            twitter_api_secret=os.getenv("TWITTER_API_SECRET"),
            twitter_access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            twitter_access_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        
        self.ml = MLConfig()
        
        # Validate critical configurations
        self._validate()
    
    def _validate(self) -> None:
        """Validate all configurations"""
        try:
            self.firebase.validate()
            if not self.trading.alpaca_api_key or not self.trading.alpaca_secret_key:
                print("⚠️  Warning: Trading API keys not configured. Using simulation mode.")
        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            raise

# Global configuration instance
config = Config()