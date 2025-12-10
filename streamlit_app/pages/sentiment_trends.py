import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import re

st.title("📈 Sentiment Trend Analysis")

def convert_relative_date(text):
    """
    Convert relative date strings like '4 weeks ago', '2 months ago' 
    to actual datetime objects
    """
    try:
        text = str(text).lower().strip()
        
        # Handle "a week ago", "a month ago" (no number)
        if text.startswith("a "):
            text = "1 " + text[2:]
        
        # Extract number from the string
        match = re.search(r"(\d+)", text)
        if not match:
            # If no number found, return today
            return datetime.today()
        
        num = int(match.group(1))
        
        # Check what time unit is mentioned
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
            # Default to today if format not recognized
            return datetime.today()
            
    except Exception as e:
        print(f"Error parsing date '{text}': {e}")
        return datetime.today()

@st.cache_data
def load_data():
    """Load the CSV file with reviews"""
    df = pd.read_csv("../data/final_topic_labeled_dataset.csv")
    return df

# Load the data
df = load_data()

# Convert all relative dates to actual datetime objects
# DO NOT USE pd.to_datetime() - it cannot parse "4 weeks ago"
df["review_date"] = df["review_date"].apply(convert_relative_date)

# Sort by date for better visualization
df = df.sort_values("review_date")

# Create the line chart
fig = px.line(
    df,
    x="review_date",
    y="sentiment_score",
    title="Sentiment Score Over Time",
    markers=True,
    labels={
        "review_date": "Review Date",
        "sentiment_score": "Sentiment Score"
    }
)

# Customize the layout
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sentiment Score",
    hovermode="x unified",
    showlegend=False
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Show summary statistics
st.subheader("📊 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Reviews", len(df))

with col2:
    st.metric("Average Sentiment", f"{df['sentiment_score'].mean():.2f}")

with col3:
    st.metric("Highest Sentiment", f"{df['sentiment_score'].max():.2f}")

with col4:
    st.metric("Lowest Sentiment", f"{df['sentiment_score'].min():.2f}")

# Optional: Show sentiment distribution
st.subheader("📉 Sentiment Distribution")
fig2 = px.histogram(
    df,
    x="sentiment_score",
    nbins=30,
    title="Distribution of Sentiment Scores",
    labels={"sentiment_score": "Sentiment Score", "count": "Number of Reviews"}
)
st.plotly_chart(fig2, use_container_width=True)

# Optional: Show raw data
with st.expander("📋 View Raw Data"):
    st.dataframe(
        df[["review_date", "sentiment_score"]].head(50),
        use_container_width=True
    )