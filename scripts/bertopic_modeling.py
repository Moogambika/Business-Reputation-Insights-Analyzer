import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import nltk
import re
from nltk.corpus import stopwords

# ---------- Step 1: Load Dataset ----------
file_path = "data/final_sentiment_dataset.csv"
df = pd.read_csv(file_path)

print("📌 Loaded dataset with", len(df), "reviews")

# ---------- Step 2: Text Cleaning ----------
nltk.download('stopwords')
stop_words = set(stopwords.words("english"))

def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # remove special characters
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

df["cleaned_text"] = df["review_text"].apply(clean_text)

# Remove empty rows after cleaning
df = df[df["cleaned_text"].str.strip() != ""]

print("🧹 Cleaning done. Remaining rows:", len(df))

# ---------- Step 3: Topic Modeling ----------
print("⚙️ Running BERTopic... (This may take 1-5 minutes)")

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df["cleaned_text"].tolist(), show_progress_bar=True)

topic_model = BERTopic(verbose=True)
topics, probabilities = topic_model.fit_transform(df["cleaned_text"], embeddings)

df["topic"] = topics

# ---------- Step 4: Save Output ----------
print("\n🎉 BERTopic Modeling Completed!")

# Create folder if missing
import os
os.makedirs("models", exist_ok=True)

df.to_csv("data/final_topic_labeled_dataset.csv", index=False)
topic_model.save("models/bertopic_model")

print("\n🎉 BERTopic Modeling Completed!")
print("📁 Saved:")
print("  - data/final_topic_labeled_dataset.csv")
print("  - models/bertopic_model")

# ---------- Step 5: Topic Overview ----------
print("\n🔍 Top 10 Topics:")
print(topic_model.get_topic_info().head(10))
