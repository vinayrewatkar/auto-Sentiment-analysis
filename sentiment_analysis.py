import csv
from textblob import TextBlob
from prettytable import PrettyTable

# Open the CSV file
with open('cleaned_data2.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)

    # Create a table for displaying the results
    table = PrettyTable(['Tweet', 'Sentiment'])

    # Initialize counters for sentiment analysis
    total_tweets = 0
    positive_tweets = 0
    negative_tweets = 0
    neutral_tweets = 0

    # Iterate through each row in the CSV file
    for row in reader:
        if len(row) > 0:
            tweet_text = row[0]  # Assuming the tweet text is in the first column

            # Perform sentiment analysis using TextBlob
            blob = TextBlob(tweet_text)
            sentiment = blob.sentiment.polarity

            # Classify the sentiment as positive, negative, or neutral
            if sentiment > 0:
                sentiment_label = 'Positive'
                positive_tweets += 1
            elif sentiment < 0:
                sentiment_label = 'Negative'
                negative_tweets += 1
            else:
                sentiment_label = 'Neutral'
                neutral_tweets += 1

            # Add the tweet and sentiment to the table
            table.add_row([tweet_text, sentiment_label])

            total_tweets += 1

    # Print the sentiment analysis results
    print(table)
    print('---')
    print('Sentiment Analysis Results:')
    print('Total Tweets:', total_tweets)
    print('Positive Tweets:', positive_tweets, '({:.2%})'.format(positive_tweets / total_tweets))
    print('Negative Tweets:', negative_tweets, '({:.2%})'.format(negative_tweets / total_tweets))
    print('Neutral Tweets:', neutral_tweets, '({:.2%})'.format(neutral_tweets / total_tweets))
