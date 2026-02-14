import os
from dotenv import load_dotenv

load_dotenv()

URL = "http://localhost:8000/api/admin/analytics"
KEY = os.getenv("ADMIN_API_KEY", "secure_admin_key_123")


def test_admin_view():
    print(f"Testing Local Admin View at {URL}...")
    try:
        response = requests.get(f"{URL}?key={KEY}")
        if response.status_code == 200:
            print("✅ SUCCESS: Admin view accessible!")
            data = response.json()
            # print(data)
            print(f"Status: {data.get('status')}")
            print(f"Visits Count: {data['data']['visits_count']}")
            print(f"Contacts Count: {data['data']['contacts_count']}")
        else:
            print(f"❌ FAILED: Status code {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Could not connect to server. Is it running?")

if __name__ == "__main__":
    test_admin_view()
