import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import time
import glob

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found! Add it to your .env file.")

client = Groq(api_key=api_key)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/final_topic_labeled_dataset.csv")
df = df.dropna(subset=["cleaned_text"])  # remove empty reviews

# -----------------------------
# Helper: chunk reviews safely
# -----------------------------
def chunk_reviews_safe(reviews, chunk_size=25):
    return [reviews[i:i+chunk_size] for i in range(0, len(reviews), chunk_size)]

# -----------------------------
# Helper: function to call Groq model with fallback
# -----------------------------
def call_model(prompt, timeout=120):
    primary_model = "meta-llama/llama-4-maverick-17b-128e-instruct"
    fallback_model = "moonshotai/kimi-k2-instruct"

    try:
        response = client.chat.completions.create(
            model=primary_model,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        return response.choices[0].message.content, primary_model
    except Exception as e:
        # If primary fails (rate limit or size), use fallback
        print(f"⚠️ Primary model hit an issue: {str(e)}\nSwitching to fallback model {fallback_model}...")
        response = client.chat.completions.create(
            model=fallback_model,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        return response.choices[0].message.content, fallback_model

# -----------------------------
# Create reports folder
# -----------------------------
os.makedirs("reports", exist_ok=True)

# -----------------------------
# EXECUTIVE SUMMARY (per chunk)
# -----------------------------
review_chunks = chunk_reviews_safe(df["cleaned_text"].tolist(), chunk_size=25)

print(f"🔹 Generating executive summary in {len(review_chunks)} chunks...")
for idx, chunk in enumerate(review_chunks):
    chunk_file = f"reports/executive_chunk_{idx+1}.txt"
    if os.path.exists(chunk_file):
        print(f"✅ Skipping executive summary chunk {idx+1} (already done)")
        continue

    print(f"Processing executive summary chunk {idx+1}/{len(review_chunks)}...")
    chunk_text = " ".join(chunk)
    exec_prompt = f"""
You are an expert business analyst. Summarize the following customer feedback reviews into a clear executive summary. Focus on:

- Main customer feelings (positive/negative)
- Overall satisfaction level
- Key recurring themes

Reviews:
{chunk_text}
"""
    summary, used_model = call_model(exec_prompt)
    print(f"✔️ Chunk {idx+1} generated using {used_model}")
    with open(chunk_file, "w", encoding="utf-8") as f:
        f.write(summary)
    time.sleep(1)

# -----------------------------
# TOPIC INSIGHTS (per topic, chunked)
# -----------------------------
grouped_reviews = df.groupby("topic")["cleaned_text"].apply(list)

print(f"\n🔹 Generating topic insights for {len(grouped_reviews)} topics...")
for idx, (topic, reviews_list) in enumerate(grouped_reviews.items()):
    if pd.isna(topic):
        continue
    safe_topic = str(topic).replace(" ", "_").replace("/", "_")
    topic_file = f"reports/topic_{idx+1}_{safe_topic}.txt"
    if os.path.exists(topic_file):
        print(f"✅ Skipping topic {idx+1} ({topic}) (already done)")
        continue

    print(f"Processing topic {idx+1}/{len(grouped_reviews)}: {topic}")

    # Chunk the reviews per topic to avoid token limit
    review_chunks_topic = chunk_reviews_safe(reviews_list, chunk_size=20)
    insights = []

    for cidx, chunk in enumerate(review_chunks_topic):
        reviews_text = " ".join(chunk)
        topic_prompt = f"""
Based on the customer reviews below, explain clearly what this topic represents in bullet points:

Topic: {topic}
Reviews: {reviews_text}
"""
        try:
            insight, used_model = call_model(topic_prompt)
            insights.append(insight)
            print(f"✔️ Topic {idx+1} chunk {cidx+1} generated using {used_model}")
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Topic {idx+1} chunk {cidx+1} failed: {e}")
            continue

    # Merge insights from chunks into a single topic file
    with open(topic_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(insights))

# -----------------------------
# RECOMMENDATIONS (per chunk)
# -----------------------------
print(f"\n🔹 Generating recommendations in {len(review_chunks)} chunks...")
for idx, chunk in enumerate(review_chunks):
    chunk_file = f"reports/reco_chunk_{idx+1}.txt"
    if os.path.exists(chunk_file):
        print(f"✅ Skipping recommendation chunk {idx+1} (already done)")
        continue

    print(f"Processing recommendation chunk {idx+1}/{len(review_chunks)}...")
    chunk_text = " ".join(chunk)
    recommend_prompt = f"""
Based on the customer feedback trends, generate practical business improvement recommendations.

Focus on:
- Service quality
- Staff behavior
- Facilities
- Wait time
- Value for money
- Digital experience

Reviews:
{chunk_text}
"""
    reco, used_model = call_model(recommend_prompt)
    print(f"✔️ Recommendation chunk {idx+1} generated using {used_model}")
    with open(chunk_file, "w", encoding="utf-8") as f:
        f.write(reco)
    time.sleep(1)

# -----------------------------
# MERGE CHUNKS INTO FINAL FILES
# -----------------------------
def merge_files(pattern, output_file):
    files = sorted(glob.glob(pattern))
    with open(output_file, "w", encoding="utf-8") as outfile:
        for fname in files:
            with open(fname, "r", encoding="utf-8") as infile:
                outfile.write(infile.read() + "\n\n")

print("\n🔹 Merging executive summary chunks...")
merge_files("reports/executive_chunk_*.txt", "reports/executive_summary.txt")

print("🔹 Merging topic insights...")
merge_files("reports/topic_*.txt", "reports/topic_insights.txt")

print("🔹 Merging recommendation chunks...")
merge_files("reports/reco_chunk_*.txt", "reports/recommendations.txt")

print("\n🎉 All AI Analysis Reports are Ready in the `reports/` folder!")
