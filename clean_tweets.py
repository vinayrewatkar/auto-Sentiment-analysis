import csv
import re
from urllib.parse import urlparse

def clean_tweet(tweet):
    # Remove hashtags
    tweet = re.sub(r'#\w+', '', tweet)

    # Remove mentions
    tweet = re.sub(r'@\w+', '', tweet)

    # Remove retweets
    tweet = re.sub(r'RT : ', '', tweet)

    # Remove usernames
    tweet = re.sub(r': ', '', tweet)

    # Remove duplicate links
    tweet = re.sub(r'http\S+|www\S+', lambda match: remove_duplicate_links(match.group()), tweet)

    return tweet

def remove_duplicate_links(link):
    parsed_link = urlparse(link)
    if parsed_link.netloc not in unique_links:
        unique_links.add(parsed_link.netloc)
        return link
    return ''

# Input and output file paths
input_file = 'hashtag-ssr1.csv'
output_file = 'cleaned-hashtag-ssr1.csv'

# Open input and output files
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    # Keep only 'tweets' column and create a new fieldnames list
    fieldnames = ['tweets']

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    unique_tweets = set()
    unique_links = set()

    # Read and process each row
    for row in reader:
        tweet_text = row['rawContent']  # Assuming the 'tweets' column contains the tweet text
        cleaned_tweet = clean_tweet(tweet_text)

        # Remove duplicate tweets
        if cleaned_tweet not in unique_tweets:
            unique_tweets.add(cleaned_tweet)

            # Write only the cleaned tweet to the output file
            writer.writerow({'tweets': cleaned_tweet})

print("Cleaning complete. Cleaned data saved to", output_file)
