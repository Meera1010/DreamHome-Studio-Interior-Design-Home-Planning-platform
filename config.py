"""
DreamHome Studio — Configuration Management
Defines app configuration environments, security keys, database paths, and runtime settings.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dh_studio_sec_key_98374109823471098234")
    DATABASE_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "database" / "dreamhome.db"))
    SESSION_COOKIE_NAME = "dh_studio_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    
    # SaaS Business Logic Defaults
    DEFAULT_TAX_RATE = 0.085  # 8.5% default sales tax
    DEFAULT_LABOR_RATE_PER_SQM = 45.0  # $45 per sq meter installation labor
    DEFAULT_DESIGNER_MARGIN = 0.15  # 15% designer margin
    MAX_PROJECT_VERSIONS = 50  # Version history retention cap per project
    
    # Pagination & Limits
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Audit & Security Settings
    ENABLE_AUDIT_LOGGING = True
    PASSWORD_MIN_LENGTH = 8
    RATE_LIMIT_AUTH_ATTEMPTS = 5

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True
    DATABASE_PATH = str(BASE_DIR / "database" / "test_dreamhome.db")
    SECRET_KEY = "test_secret_key_only_for_automated_testing"

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
