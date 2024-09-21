

### deployed link 
https://smartrade.streamlit.app/

Here's a detailed explanation of the functionality of your Global Stock Market Sentiment Analysis app:

### Functionality Overview

1. **Load Company Data**:
   - The app starts by loading company data from a CSV file (`stock.csv`), which contains stock ticker symbols and their corresponding company names. This data is stored in a dictionary for easy access.

2. **User Interface**:
   - A user-friendly interface is created using Streamlit. Users can select a stock ticker from a dropdown menu populated with the symbols from the loaded data.

3. **Fetch News Articles**:
   - When the user clicks the "Fetch News" button, the app constructs a search query based on the selected stock ticker. This query is designed to retrieve relevant news articles from the News API.
   - The app fetches the latest articles related to the company, including titles and descriptions.

4. **Sentiment Analysis**:
   - The app uses the TextBlob library to perform sentiment analysis on the descriptions of the fetched news articles. It calculates a polarity score for each description, indicating whether the sentiment is positive, negative, or neutral.
   - A summary of the sentiments is generated, showing how many articles are positive, negative, or neutral.

5. **Determine Market Signal**:
   - Based on the sentiment analysis results, the app determines an overall market signal:
     - **Bullish**: More positive sentiments than negative.
     - **Bearish**: More negative sentiments than positive.
     - **Neutral**: An equal number of positive and negative sentiments.

6. **Display Results**:
   - The app displays the overall market signal prominently at the top of the interface.
   - Below the market signal, the app lists each article's title (clickable link to the original article), description, and its corresponding sentiment (positive, negative, or neutral) along with the polarity score.

### Summary of Key Functions

- **`load_company_data(file_path)`**: Reads company data from a CSV file and returns a dictionary mapping stock symbols to company names.
  
- **`fetch_news(query, language, num_articles)`**: Makes a request to the News API to retrieve news articles based on the constructed query, handling any request errors gracefully.
  
- **`initialize_sentiment_pipeline()`**: Prepares the TextBlob sentiment analysis tool for use.

- **`analyze_sentiments(sentiment_pipeline, texts)`**: Processes the fetched article descriptions through the sentiment analysis pipeline and returns the results.

- **`get_signal_from_sentiments(sentiments)`**: Analyzes the sentiment results and determines an overall market signal.

- **`get_company_description(company_data, ticker)`**: Constructs a descriptive query for fetching relevant news articles for the selected company.

### User Experience

- The user experience is streamlined, allowing users to easily select a stock ticker, fetch relevant news, and instantly view the sentiment analysis and overall market signal.
- The use of visual elements, such as headers and descriptions, makes the information clear and accessible, enhancing user engagement.

Overall, this app provides valuable insights into the sentiment surrounding stocks, helping users make more informed decisions based on current news trends.# Market-Signal-News
