"""Test public Gemini API (generativelanguage) with service account credentials"""
from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import json
import os

sa_path = r"C:\Users\Nagarro\Downloads\Job App Automation\config\cent-capital-472820-f55ada69e99b.json"

if not os.path.exists(sa_path):
    raise SystemExit(f'Service account not found at {sa_path}')

# Load service account
scopes = ['https://www.googleapis.com/auth/cloud-platform']
creds = service_account.Credentials.from_service_account_file(sa_path, scopes=scopes)
request_obj = google.auth.transport.requests.Request()
creds.refresh(request_obj)
token = creds.token

# Test public Gemini API endpoint
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "contents": [{
        "role": "user",
        "parts": [{"text": "Extract falsifiable claims from: Revenue grew 50% YoY. Customers doubled. Return a JSON array with claim and type."}]
    }],
    "generationConfig": {
        "temperature": 0.1,
        "maxOutputTokens": 1024,
    }
}

print(f"Testing public Gemini API endpoint")
print(f"URL: {url}")
print(f"Using Bearer token from service account: {creds.service_account_email}")

try:
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    print(f"\nStatus: {r.status_code}")
    
    if r.status_code in [200, 202]:
        print("SUCCESS! Gemini API is accessible")
        try:
            result = r.json()
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Parse error: {e}")
            print(r.text[:500])
    else:
        print("ERROR response:")
        try:
            error = r.json()
            print(json.dumps(error, indent=2))
        except:
            print(r.text[:500])
            
except Exception as e:
    print(f"Request error: {e}")
