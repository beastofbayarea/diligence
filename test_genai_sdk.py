"""Test Google Generative AI SDK with service account"""
import os
import sys

# Try the google-generativeai library
try:
    import google.generativeai as genai
    print("google.generativeai is installed")
except ImportError:
    print("google.generativeai NOT installed; installing...")
    os.system("pip install google-generativeai -q")
    import google.generativeai as genai

# Load service account key file
sa_path = r"C:\Users\Nagarro\Downloads\Job App Automation\config\cent-capital-472820-f55ada69e99b.json"

# Method 1: Try with API key from environment (won't work, but checking)
if os.environ.get('GEMINI_API_KEY'):
    print(f"Using GEMINI_API_KEY from environment")
    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
else:
    print("No GEMINI_API_KEY in environment")
    print("Service account at:", sa_path)
    print("Service accounts don't work with genai.configure() directly")
    print("Need API key from Google AI Studio instead")
    sys.exit(1)

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Extract claims: Revenue grew 50%.")
    print("SUCCESS!")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
