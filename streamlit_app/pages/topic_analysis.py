import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import re

st.title("🧠 Topic Analysis")
st.write("Explore the top recurring themes extracted using BERTopic.")

def convert_relative_date(text):
    """Convert relative date strings to datetime objects"""
    try:
        text = str(text).lower().strip()
        
        if text.startswith("a "):
            text = "1 " + text[2:]
        
        match = re.search(r"(\d+)", text)
        if not match:
            return datetime.today()
        
        num = int(match.group(1))
        
        if "year" in text:
            return datetime.today() - timedelta(days=num * 365)
        elif "month" in text:
            return datetime.today() - timedelta(days=num * 30)
        elif "week" in text:
            return datetime.today() - timedelta(weeks=num)
        elif "day" in text:
            return datetime.today() - timedelta(days=num)
        elif "hour" in text:
            return datetime.today() - timedelta(hours=num)
        else:
            return datetime.today()
            
    except Exception as e:
        print(f"Error parsing date '{text}': {e}")
        return datetime.today()

@st.cache_data
def load_data():
    df = pd.read_csv("../data/final_topic_labeled_dataset.csv")
    
    # Convert dates if review_date column exists
    if 'review_date' in df.columns:
        df['review_date'] = df['review_date'].apply(convert_relative_date)
    
    return df

df = load_data()

# ------- Topic Distribution -------
st.subheader("📊 Topic Distribution")

topic_counts = df["topic"].value_counts().reset_index()
topic_counts.columns = ["Topic", "Count"]

fig = px.bar(
    topic_counts.head(10),
    x="Topic",
    y="Count",
    title="Top 10 Most Frequent Topics",
    text="Count",
    color="Count",
    color_continuous_scale="Blues"
)
fig.update_traces(textposition='outside')
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# ------- Sentiment Overview -------
st.subheader("🎭 Sentiment Distribution")
col1, col2, col3 = st.columns(3)

total_reviews = len(df)
positive_count = len(df[df["sentiment_label"] == "Positive"])
negative_count = len(df[df["sentiment_label"] == "Negative"])
neutral_count = total_reviews - positive_count - negative_count

with col1:
    st.metric("Positive Reviews", f"{positive_count} ({positive_count/total_reviews*100:.1f}%)")

with col2:
    st.metric("Negative Reviews", f"{negative_count} ({negative_count/total_reviews*100:.1f}%)")

with col3:
    st.metric("Other/Neutral", f"{neutral_count} ({neutral_count/total_reviews*100:.1f}%)")

# ------- Top Positive Topics -------
st.subheader("💚 Top 5 Positive Topics")

positive = df[df["sentiment_label"] == "Positive"]

if len(positive) > 0:
    positive_topics = positive["topic"].value_counts().head(5).reset_index()
    positive_topics.columns = ["Topic", "Count"]
    
    fig_pos = px.bar(
        positive_topics,
        x="Topic",
        y="Count",
        title="Most Common Topics in Positive Reviews",
        text="Count",
        color="Count",
        color_continuous_scale="Greens"
    )
    fig_pos.update_traces(textposition='outside')
    fig_pos.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_pos, use_container_width=True)
    
    # Show detailed breakdown
    with st.expander("View Detailed Positive Topics"):
        st.dataframe(positive_topics, use_container_width=True)
else:
    st.warning("No positive reviews found in the dataset.")

# ------- Top Negative Topics -------
st.subheader("❤️‍🩹 Top 5 Negative Topics")

negative = df[df["sentiment_label"] == "Negative"]

if len(negative) > 0:
    negative_topics = negative["topic"].value_counts().head(5).reset_index()
    negative_topics.columns = ["Topic", "Count"]
    
    fig_neg = px.bar(
        negative_topics,
        x="Topic",
        y="Count",
        title="Most Common Topics in Negative Reviews",
        text="Count",
        color="Count",
        color_continuous_scale="Reds"
    )
    fig_neg.update_traces(textposition='outside')
    fig_neg.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_neg, use_container_width=True)
    
    # Show detailed breakdown
    with st.expander("View Detailed Negative Topics"):
        st.dataframe(negative_topics, use_container_width=True)
else:
    st.warning("No negative reviews found in the dataset.")

# ------- Topic-Sentiment Heatmap -------
st.subheader("🔥 Topic-Sentiment Distribution")

sentiment_topic = df.groupby(["topic", "sentiment_label"]).size().reset_index(name='Count')
sentiment_topic_pivot = sentiment_topic.pivot(index="topic", columns="sentiment_label", values='Count').fillna(0)

# Get top 15 topics by total count
top_topics = df["topic"].value_counts().head(15).index
sentiment_topic_pivot_top = sentiment_topic_pivot.loc[sentiment_topic_pivot.index.isin(top_topics)]

fig_heatmap = px.imshow(
    sentiment_topic_pivot_top,
    title="Top 15 Topics by Sentiment",
    labels=dict(x="Sentiment", y="Topic", color="Count"),
    color_continuous_scale="RdYlGn",
    aspect="auto",
    text_auto=True
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ------- Sample Reviews by Topic -------
st.subheader("📝 Sample Reviews by Topic")

# Find the review text column
text_col = None
for col in ['review_text', 'text', 'review', 'Review', 'Review_Text']:
    if col in df.columns:
        text_col = col
        break

if text_col:
    # Create a better display for topic selection
    topic_counts_map = df["topic"].value_counts().to_dict()
    topic_options = sorted(df["topic"].unique())
    
    # Format the display as "Topic X (Y reviews)"
    topic_display = [f"Topic {topic} ({topic_counts_map[topic]} reviews)" for topic in topic_options]
    topic_dict = dict(zip(topic_display, topic_options))
    
    selected_display = st.selectbox("Select a topic to view sample reviews:", topic_display)
    selected_topic = topic_dict[selected_display]
    
    topic_df = df[df["topic"] == selected_topic]
    
    # Show statistics for this topic
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reviews", len(topic_df))
    with col2:
        pos_pct = len(topic_df[topic_df["sentiment_label"] == "Positive"]) / len(topic_df) * 100
        st.metric("Positive %", f"{pos_pct:.1f}%")
    with col3:
        neg_pct = len(topic_df[topic_df["sentiment_label"] == "Negative"]) / len(topic_df) * 100
        st.metric("Negative %", f"{neg_pct:.1f}%")
    
    # Try to show common keywords for this topic
    st.write(f"**Topic {selected_topic} - Most Common Words:**")
    # Get all reviews for this topic and find most common words
    all_text = " ".join(topic_df[text_col].astype(str).tolist()).lower()
    words = all_text.split()
    # Remove common stop words
    stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'was', 'are', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its', 'our', 'their']
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    from collections import Counter
    word_counts = Counter(filtered_words).most_common(10)
    
    keywords = ", ".join([f"**{word}** ({count})" for word, count in word_counts])
    st.info(f"🔑 {keywords}")
    
    # Show sample reviews
    st.write("**Sample Reviews:**")
    sample_reviews = topic_df.head(5)
    
    for i, (idx, row) in enumerate(sample_reviews.iterrows(), 1):
        sentiment = row["sentiment_label"]
        sentiment_emoji = "💚" if sentiment == "Positive" else "💔" if sentiment == "Negative" else "😐"
        
        with st.container():
            st.write(f"{sentiment_emoji} **Review {i}** ({sentiment})")
            st.write(row[text_col])
            st.divider()
else:
    st.info("No review text column found to display samples.")

# ------- Dataset Statistics -------
with st.expander("📊 View Full Dataset Statistics"):
    st.write(f"**Total Reviews:** {len(df)}")
    st.write(f"**Total Unique Topics:** {df['topic'].nunique()}")
    st.write(f"**Date Range:** {df['review_date'].min().strftime('%Y-%m-%d')} to {df['review_date'].max().strftime('%Y-%m-%d')}" if 'review_date' in df.columns else "Date information not available")
    
    st.write("\n**All Topics Distribution:**")
    all_topics = df["topic"].value_counts().reset_index()
    all_topics.columns = ["Topic", "Count"]
    st.dataframe(all_topics, use_container_width=True, height=400)