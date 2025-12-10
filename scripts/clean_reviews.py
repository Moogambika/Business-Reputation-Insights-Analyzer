import pandas as pd
import json
import re
import emoji
import os

filename = input("Enter raw filename (without extension): ")

with open(f"data/raw/{filename}.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df["reviewer_name"] = df["user"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
df["review_text"] = df["snippet"]
df["review_date"] = df["date"]
df["rating"] = df["rating"]

def clean(text):
    if not text: return ""
    text = emoji.replace_emoji(text, '')
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["review_text"] = df["review_text"].astype(str).apply(clean)

df = df[["reviewer_name", "review_date", "rating", "review_text"]]
df = df[df["review_text"] != ""]

os.makedirs("data/cleaned", exist_ok=True)

output_path = f"data/cleaned/{filename}_cleaned.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"✨ Cleaning complete! Saved {len(df)} cleaned reviews to {output_path}")
