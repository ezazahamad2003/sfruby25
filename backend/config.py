import os
from dotenv import load_dotenv

# Get the directory where this config.py file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')

# Try loading with dotenv first
load_dotenv(env_path)

# If that doesn't work, manually read the file
if not os.getenv('PERPLEXITY_API_KEY'):
    try:
        with open(env_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
                    print(f"🔧 Manually set {key} from .env file")
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")

# Perplexity API Configuration
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

# You can also set the API key directly here for testing
# PERPLEXITY_API_KEY = "your_actual_api_key_here"

def check_api_key():
    """Check if the API key is properly configured"""
    if not PERPLEXITY_API_KEY or PERPLEXITY_API_KEY == "your_api_key_here":
        print("❌ Error: PERPLEXITY_API_KEY not set")
        print("Please do one of the following:")
        print("1. Create a .env file with: PERPLEXITY_API_KEY=your_actual_key")
        print("2. Set the environment variable: set PERPLEXITY_API_KEY=your_actual_key")
        print("3. Edit config.py and set the key directly")
        return False
    return True 