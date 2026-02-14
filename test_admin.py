import requests
import sys

URL = "https://view-portfolio-be.onrender.com/api/admin/analytics"  # Update this if you deploy
KEY = "secure_admin_key_123"

def test_admin_view():
    print(f"Testing Admin View at {URL}...")
    try:
        response = requests.get(f"{URL}?key={KEY}")
        if response.status_code == 200:
            print("✅ SUCCESS: Admin view accessible!")
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Visits Count: {data['data']['visits_count']}")
            print(f"Contacts Count: {data['data']['contacts_count']}")
            print("-" * 20)
            print("To see full data in browser, visit:")
            print(f"{URL}?key={KEY}")
        elif response.status_code == 403:
            print("❌ FAILED: Invalid API Key (403 Forbidden)")
        else:
            print(f"❌ FAILED: Status code {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Could not connect to server. Is it running?")
        print("Run: uvicorn main:app --reload")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        URL = sys.argv[1]
    test_admin_view()
