"""
MANTRA - Configuration
Centralized application settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


MANTRA_NAME = os.getenv("MANTRA_NAME", "MANTRA")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


def show_config() -> None:
    """Display safe configuration information."""
    print(f"Name: {MANTRA_NAME}")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Debug Mode: {DEBUG}")