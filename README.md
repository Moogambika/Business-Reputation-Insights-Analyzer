📊 Business Reputation & Insights Analyzer
Using Google Maps Reviews + NLP + LLMs + Streamlit Dashboard

This project analyzes Google Maps customer reviews and converts them into meaningful business insights, using modern NLP techniques, sentiment analysis, topic modeling and LLM-generated summaries.
It helps organizations understand customer satisfaction, identify recurring issues and improve service quality through data-driven decisions.

⭐ Features
🔍 1. Data Collection

Scraped reviews from Google Maps for selected businesses.

Captured fields such as:

Reviewer Name

Review Text

Rating

Review Date (relative dates like "2 weeks ago")

Source Location

🧹 2. Data Cleaning & Preprocessing

Removed emojis, HTML tags, and noise.

Converted relative dates (e.g., “3 weeks ago”) into actual date objects.

Normalized text:

Lowercasing

Stopword removal

Lemmatization

Created a clean, machine-readable dataset.

🤖 3. Sentiment Analysis

Used a fine-tuned Transformer model to assign:

sentiment_score

sentiment_label (Positive / Neutral / Negative)

🧠 4. Topic Modeling

Used LDA / BERTopic to identify hidden themes in reviews.

Each review was assigned a topic number.

✨ 5. LLM-Generated Interpretations

Used OpenAI/LLM pipeline to generate:

Business-level summary (executive summary of all reviews)

Areas of Excellence

Areas That Need Improvement

Actionable Recommendations for improving customer satisfaction

Topic-wise insights in natural language

🖥️ Streamlit Dashboard (Deployment)

The entire analysis is deployed through a Streamlit multi-page app, with the following pages:

📁 1. Overview Dashboard (Home Page)

Dataset preview

Total number of reviews

Average Rating

Sentiment distribution pie chart

Top keywords from reviews

Summary insights

📈 2. Sentiment Trend Analysis

Time-series visualization using Plotly

Shows how customer sentiment improves or drops over time

Helps businesses track performance month-to-month

🧩 3. Topic Analysis

Bar chart of topic frequency

Topic-wise average sentiment score

Table of reviews under each topic

🧠 4. LLM Summary Page

Auto-generated business insights

Top 5 positive themes

Top 5 negative themes

Improvement suggestions

Downloadable PDF summary (if implemented)

📁 Project Structure
root/
│
├── data/
│   ├── raw_reviews.csv
│   ├── cleaned_reviews.csv
│   └── final_topic_labeled_dataset.csv
│
├── notebooks/
│   ├── 1_data_cleaning.ipynb
│   ├── 2_sentiment_analysis.ipynb
│   ├── 3_topic_modeling.ipynb
│   └── 4_llm_summary.ipynb
│
├── streamlit_app/
│   ├── app.py               # Main dashboard
│   ├── pages/
│   │   ├── sentiment_trends.py
│   │   ├── topic_analysis.py
│   │   └── LLM_summary.py
│
├── models/
│   ├── sentiment_model.pkl
│   └── topic_model.pkl
│
├── requirements.txt
├── README.md
└── .venv/

📘 How to Run Locally
1. Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

2. Create Virtual Environment
python -m venv .venv


Activate:

#Windows

.venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Create .env file with your API keys
echo GROQ_API_KEY=your_api_key_here > .env

5. Run Streamlit App

#Navigate to project folder

cd "Business Reputation & Insights Analyzer using Google Maps Reviews + LLMs"

streamlit run app.py

📊 Evaluation Metrics
1. Sentiment Classification Accuracy

Measured using validation dataset.

2. Coherence of Topic Modeling

Topic coherence score

Manual interpretability assessment

3. Quality of LLM Summaries

Human evaluation of clarity & usefulness

4. Actionability of Recommendations

Do the LLM insights help businesses improve?

5. Dashboard Usability

Page loading speed

User satisfaction

Navigation smoothness

🎯 Expected Outcomes

Meaningful summaries of customer feedback

Identification of positive & negative themes

Ratings and sentiment trends over time

Clear improvement recommendations

Easy-to-use dashboard interface

💡 Impact

Helps businesses adapt quickly to customer needs

Improves customer satisfaction and loyalty

Enables data-driven decision making

Saves time by automating review analysis

Provides competitive advantage with actionable insights

🙏 Acknowledgments

I am deeply grateful to the internal mentors at GUVI for their unwavering support and guidance throughout the development of this project. Their mentorship has been crucial in helping me navigate challenges and successfully complete this Business Reputation & Insights Analyzer.

Special thanks to the GUVI team for providing an excellent learning environment and for their continuous encouragement.
