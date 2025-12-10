import pandas as pd
import matplotlib.pyplot as plt

# Load dataset created during BERTopic modeling
df = pd.read_csv("data/final_topic_labeled_dataset.csv")

# Group by topic and count
topic_counts = df["topic"].value_counts().sort_index()

# Plot
plt.figure(figsize=(12, 6))
bars = plt.bar(topic_counts.index, topic_counts.values)
plt.xlabel("Topic Number")
plt.ylabel("Number of Reviews")
plt.title("Topic Distribution Across Reviews")

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 5, str(height), 
             ha='center', fontsize=10)

# Save chart
plt.savefig("visualizations/topic_distribution_barchart.png", dpi=300)
plt.show()

print("\n📊 Topic Distribution Bar Chart Created!")
print("📁 Saved to: visualizations/topic_distribution_barchart.png")
