import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")

STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
LOCKED_USER = os.getenv("LOCKED_USER", "locked_out_user")
PERFORMANCE_USER = os.getenv("PERFORMANCE_USER", "performance_glitch_user")
PASSWORD = os.getenv("PASSWORD", "secret_sauce")

HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))
TIMEOUT = int(os.getenv("TIMEOUT", "10000"))
