import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import re

# Download VADER lexicon (run once)
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

def preprocess_text(text):
    """Clean the news text for better sentiment analysis."""
    text = re.sub(r'\W', ' ', str(text))  # Remove non-word characters
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)  # Remove single letters
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)  # Remove single letters at start
    text = re.sub(r'\s+', ' ', text, flags=re.I)  # Replace multiple spaces
    return text.lower().strip()

def hawk_function():
    st.title("News Sentiment Analysis (Hawk)")
    st.write("Paste the news article or headline below to analyze sentiment and get a BUY/SELL/HOLD signal.")

    # Initialize session state for news text and results
    if 'news_text' not in st.session_state:
        st.session_state.news_text = ""
    if 'sentiment_result' not in st.session_state:
        st.session_state.sentiment_result = None

    # Text area with persisted input
    news_input = st.text_area("Enter News Text", value=st.session_state.news_text, height=200, 
                              placeholder="Paste your news here, e.g., 'Tesla reports record profits amid EV boom...'")

    # Update session state with the latest input
    st.session_state.news_text = news_input

    if st.button("Analyze Sentiment"):
        if news_input:
            # Preprocess the text
            cleaned_text = preprocess_text(news_input)
            st.write("Cleaned Text Preview:", cleaned_text[:200] + "..." if len(cleaned_text) > 200 else cleaned_text)

            # Initialize VADER
            sia = SentimentIntensityAnalyzer()
            sentiment = sia.polarity_scores(cleaned_text)
            compound_score = sentiment['compound']

            # Display sentiment scores
            st.write("**Sentiment Breakdown:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Positive", f"{sentiment['pos']:.2%}")
            with col2:
                st.metric("Negative", f"{sentiment['neg']:.2%}")
            with col3:
                st.metric("Neutral", f"{sentiment['neu']:.2%}")
            with col4:
                st.metric("Compound Score", f"{compound_score:.3f}")

            # Determine BUY/SELL/HOLD
            if compound_score > 0.05:
                signal = "🟢 BUY"
                explanation = "Positive sentiment detected – favorable news for potential price increase."
            elif compound_score < -0.05:
                signal = "🔴 SELL"
                explanation = "Negative sentiment detected – unfavorable news suggesting price decline."
            else:
                signal = "🟡 HOLD"
                explanation = "Neutral sentiment – no clear directional signal from the news."

            # Store result in session state
            st.session_state.sentiment_result = {
                "signal": signal,
                "explanation": explanation,
                "sentiment": sentiment
            }
        else:
            st.session_state.sentiment_result = None
            st.write("Please paste some news text to analyze.")

    # Display persisted result if available
    if st.session_state.sentiment_result:
        st.write(f"**Recommendation: {st.session_state.sentiment_result['signal']}**")
        st.write(st.session_state.sentiment_result['explanation'])

    if st.button("Back"):
        st.session_state.page = 'main'
        st.experimental_rerun()  # Force app rerun to return to main page