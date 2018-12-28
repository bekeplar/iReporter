import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Common configurations"""
    CSRF_ENABLED = True
    SECRET_KEY: secrets.token_hex(16)
    JWT_SECRET_KEY = os.environ.get("Kimberley")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]


class DevelopmentConfig(Config):
    """Development configurations"""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Testing configurations"""
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Production configurations"""
    DEBUG = False


app_settings = {
    "development": "config.config.DevelopmentConfig",
    "testing": "config.config.TestingConfig",
    "production": "config.config.ProductionConfig"
}