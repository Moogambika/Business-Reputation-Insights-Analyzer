import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/final_topic_labeled_dataset.csv")

# Check required columns
required_cols = {"topic", "sentiment_label"}
if not required_cols.issubset(df.columns):
    raise KeyError(f"❌ Missing required columns: {required_cols - set(df.columns)}")

# Calculate counts
sentiment_counts = df.groupby(["topic", "sentiment_label"]).size().unstack(fill_value=0)

# Plot stacked bar chart
plt.figure(figsize=(14, 6))
sentiment_counts.plot(kind="bar", stacked=True, figsize=(14, 6), colormap="tab20")

plt.title("Sentiment Distribution per Topic")
plt.xlabel("Topic ID")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=45)
plt.legend(title="Sentiment")
plt.tight_layout()

# Save visualization
plt.savefig("visualizations/sentiment_by_topic.png")

print("📊 Sentiment-by-Topic Graph Successfully Created!")
