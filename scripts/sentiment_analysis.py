import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load dataset
df = pd.read_csv("data/final_cleaned_dataset.csv")

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    if pd.isna(text) or text.strip() == "":
        return 0
    return analyzer.polarity_scores(text)["compound"]

def label_sentiment(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment rules
df["sentiment_score"] = df["review_text"].apply(get_sentiment)
df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)

# Save updated dataset
df.to_csv("data/final_sentiment_dataset.csv", index=False)

print("\n🎉 Sentiment Analysis Completed!")
print("📁 File Saved as: data/final_sentiment_dataset.csv")
print(f"🧾 Total Records: {len(df)}")
print(df["sentiment_label"].value_counts())
