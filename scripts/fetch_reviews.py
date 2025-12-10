import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")
BASE_URL = "https://serpapi.com/search.json"

def fetch_reviews(place_id):
    reviews = []
    page = 0
    Max_page = 100  # Limit to avoid timeout & API overuse

    while True:
        if page >= Max_page:
            print("\n⚠️ Reached max page limit (100). Stopping to avoid API overload.")
            break

        params = {
            "engine": "google_maps_reviews",
            "place_id": place_id,
            "api_key": API_KEY,
            "hl": "en",
            "start": page * 10
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "reviews" not in data or len(data["reviews"]) == 0:
            print("\n🚫 No more reviews found.")
            break

        reviews.extend(data["reviews"])
        page += 1
        print(f"📄 Fetched page {page}... Total reviews so far: {len(reviews)}")

        time.sleep(2)  # delay to prevent API blocking t

    return reviews


if __name__ == "__main__":
    place_id = input("Enter Place ID: ")
    filename = input("Enter filename (without extension): ")

    reviews = fetch_reviews(place_id)

    os.makedirs("data/raw", exist_ok=True)

    path = f"data/raw/{filename}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=4, ensure_ascii=False)

    print(f"\n🎉 Saved {len(reviews)} reviews to {path}")
