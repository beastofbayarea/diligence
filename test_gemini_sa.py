"""Test Gemini access using the correct Gemini service account"""
from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import json
import os

sa_path = r"C:\Users\Nagarro\Downloads\Job App Automation\config\cent-capital-472820-f55ada69e99b.json"

if not os.path.exists(sa_path):
    raise SystemExit(f'Service account not found at {sa_path}')

scopes = ['https://www.googleapis.com/auth/cloud-platform']
creds = service_account.Credentials.from_service_account_file(sa_path, scopes=scopes)
request = google.auth.transport.requests.Request()
creds.refresh(request)
token = creds.token

# Test 1: REST predict on Vertex Gemini model
project = "cent-capital-472820"
location = "us-central1"

models = [
    "publishers/google/models/gemini-1.5-flash-001",
    "publishers/google/models/gemini-1.5-pro-001",
    "publishers/google/models/gemini-2.0-flash",
]

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

for model in models:
    url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/{model}:generateContent"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": "Extract claims from: Revenue grew 50% in 2025. Say 'OK' if you understand."}]
        }]
    }
    
    print(f"\nTesting {model}")
    print(f"URL: {url}")
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        try:
            result = r.json()
            print("SUCCESS!")
            print(json.dumps(result, indent=2)[:500])
        except Exception as e:
            print(f"Response parse error: {e}")
            print(r.text[:300])
    else:
        try:
            error = r.json()
            print(f"Error: {error.get('error', {}).get('message', r.text[:200])}")
        except:
            print(f"Error: {r.text[:200]}")
