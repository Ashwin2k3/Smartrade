
import yfinance as yf
import requests
import csv
import streamlit as st
from textblob import TextBlob

# Load company data from CSV (global dataset)
def load_company_data(file_path='stock.csv'):
    company_data = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticker = row['Symbol'].strip().upper()  # 'Symbol' instead of 'Ticker'
                company_data[ticker] = {
                    'name': row['Name'],  # 'Name' instead of 'name'
                }
    except Exception as e:
        st.error(f"Error loading company data: {e}")
    return company_data

# Fetch news articles using a search query
def fetch_news(query, language='en', num_articles=10):
    api_key = "7c9628099fbd4d63be8c502113ad9ec7"  # Your News API key
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}&pageSize={num_articles}"
    try:
        response = requests.get(url, timeout=10)  # Add timeout to prevent hanging
        response.raise_for_status()  # Check for request errors
        news_data = response.json()
        return news_data.get('articles', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return []

# Initialize the sentiment analysis pipeline
def initialize_sentiment_pipeline():
    return TextBlob

# Analyze sentiments of fetched texts
def analyze_sentiments(sentiment_pipeline, texts):
    if sentiment_pipeline:
        st.write("Analyzing sentiments...")
        try:
            return [sentiment_pipeline(text) for text in texts]
        except Exception as e:
            st.error(f"Error during sentiment analysis: {e}")
            return []
    else:
        return []

# Determine market signal based on sentiment analysis results
def get_signal_from_sentiments(sentiments):
    positive_count = sum(1 for sentiment in sentiments if sentiment.polarity > 0)
    negative_count = sum(1 for sentiment in sentiments if sentiment.polarity < 0)
    
    if positive_count > negative_count:
        return "Bullish"
    elif negative_count > positive_count:
        return "Bearish"
    else:
        return "Neutral"

# Get the company-specific query for all companies
def get_company_description(company_data, ticker):
    company_info = company_data.get(ticker.upper(), None)
    if company_info:
        company_name = company_info.get('name', ticker)
        
        # Build the query using name, sector, industry, and avoid similar-sounding names
        description = f'"{company_name}" OR "{company_name} stock" OR "{company_name} shares"'
        description += f' OR "{company_name} " OR "{company_name}"'
        
        return description
    else:
        st.error(f"No information found for ticker {ticker}")
        return ticker  # Return the ticker if company info is unavailable

# Main function to show sentiment analysis
def show_sentiment_analysis():
    st.title("Global Stock Market Sentiment Analysis")
    
    # Load company data from CSV
    company_data = load_company_data()

    # Create a dropdown for selecting a stock ticker
    ticker_options = list(company_data.keys())
    stock_ticker = st.selectbox("Select the stock ticker to analyze:", ticker_options)

    if st.button("Fetch News"):
        with st.spinner("Fetching news articles..."):
            # Get the specific description for the company
            query = get_company_description(company_data, stock_ticker)
            articles = fetch_news(query, num_articles=10)
        
        if articles:
            st.write(f"Found {len(articles)} articles related to {stock_ticker}.")
            
            max_articles = min(len(articles), 10)
            with st.spinner("Analyzing sentiments..."):
                texts = [article['description'] for article in articles[:max_articles] if article['description']]
                if texts:
                    sentiment_pipeline = initialize_sentiment_pipeline()
                    sentiments = analyze_sentiments(sentiment_pipeline, texts)
                    
                    # Determine the overall market signal
                    overall_signal = get_signal_from_sentiments(sentiments)
                    
                    # Display the overall market signal at the top
                    st.subheader("Overall Market Signal")
                    st.write(f"The overall market signal based on the latest news is: **{overall_signal}**")
                    
                    st.subheader("Sentiment Analysis Results")
                    for i, article in enumerate(articles[:max_articles]):
                        # st.write(f"**Title**: {article['title']}")
                        # st.write(f"**Title**: [{article['title']}]({article['url']})")
                        st.header(f"[{article['title']}]({article['url']})")  # Make the title a header

                        st.write(f"**Description**: {article['description']}")

                        if i < len(sentiments):
                            sentiment = sentiments[i]
                            polarity = sentiment.polarity
                            sentiment_label = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
                            st.write(f"**Sentiment**: {sentiment_label} (Polarity: {polarity:.2f})")
                        else:
                            st.write("**Sentiment**: Not available")
                        st.write("---")
                else:
                    st.write("No descriptions found in the articles to analyze.")
        else:
            st.write("No articles found.")


# Run the Streamlit app
show_sentiment_analysis()
