import pandas as pd
from bertopic import BERTopic
import webbrowser
import os

# Load saved BERTopic model
model_path = "models/bertopic_model"
topic_model = BERTopic.load(model_path)

# Load dataset with assigned topics
df = pd.read_csv("data/final_topic_labeled_dataset.csv")

print(f"📌 Loaded {len(df)} reviews.")

# Generate visualization HTML
output_path = "visualizations"
os.makedirs(output_path, exist_ok=True)

html_file_path = os.path.join(output_path, "bertopic_visualization.html")

print("📊 Generating Topic Visualization... (This may take 10-30 seconds)")
fig = topic_model.visualize_topics()

# Save HTML file
fig.write_html(html_file_path)
print(f"✨ Visualization saved at: {html_file_path}")

# Auto-open the visualization in browser
abs_path = os.path.abspath(html_file_path)
webbrowser.open(f"file://{abs_path}")

print("\n🚀 Visualization launched in your browser!")
