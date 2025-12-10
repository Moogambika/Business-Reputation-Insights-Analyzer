import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import re

st.set_page_config(
    page_title="Business Reputation & Insights Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Reputation & Insights Analyzer")
st.write("Welcome! Use the left sidebar to navigate between analysis pages.")

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

# Load dataset
@st.cache_data
def load_data():
    """Load and preprocess the dataset"""
    df = pd.read_csv("../data/final_topic_labeled_dataset.csv")
    
    # Convert relative dates to actual datetime objects
    if 'review_date' in df.columns:
        df['review_date'] = df['review_date'].apply(convert_relative_date)
    
    return df

# Load the data
df = load_data()

# Display dataset overview
st.subheader("📁 Dataset Overview")

# Show key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Reviews", len(df))

with col2:
    if 'sentiment_score' in df.columns:
        avg_sentiment = df['sentiment_score'].mean()
        st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
    else:
        st.metric("Avg Sentiment", "N/A")

with col3:
    if 'rating' in df.columns:
        avg_rating = df['rating'].mean()
        st.metric("Avg Rating", f"{avg_rating:.1f} ⭐")
    else:
        st.metric("Avg Rating", "N/A")

with col4:
    if 'review_date' in df.columns:
        date_range = (df['review_date'].max() - df['review_date'].min()).days
        st.metric("Date Range", f"{date_range} days")
    else:
        st.metric("Date Range", "N/A")

# Show sample data
st.dataframe(df.head(10), use_container_width=True)

# Navigation guide
st.markdown("""
### 📌 Navigation Guide
- **Sentiment Trends:** Visualize customer sentiment over time  
- **Topic Analysis:** Explore positive & negative recurring themes  
- **AI Recommendations:** LLM-generated summary and business improvement tips  
""")

# Optional: Dataset statistics
with st.expander("📊 View Dataset Statistics"):
    st.write("**Dataset Shape:**", df.shape)
    st.write("**Column Names:**", df.columns.tolist())
    st.write("**Data Types:**")
    st.write(df.dtypes)
    
    if 'sentiment_score' in df.columns:
        st.write("**Sentiment Score Distribution:**")
        st.write(df['sentiment_score'].describe())

# Footer
st.markdown("---")
st.caption("💡 Tip: Use the sidebar to navigate to different analysis pages")