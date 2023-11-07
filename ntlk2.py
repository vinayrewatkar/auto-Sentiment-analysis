import csv
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
import matplotlib.pyplot as plt

nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('sentiwordnet')


def get_emotion(emotion_scores):
    max_score = max(emotion_scores.values())
    for emotion, score in emotion_scores.items():
        if score == max_score:
            return emotion


def analyze_sentiments(csv_file):
    # Read the CSV file
    tweets = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            tweets.append(row[0])

    # Perform sentiment analysis and emotion detection
    sid = SentimentIntensityAnalyzer()
    emotion_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0, 'Anger': 0, 'Sadness': 0, 'Anxiety': 0, 'Disturbance': 0}
    for tweet in tweets:
        sentiment_scores = sid.polarity_scores(tweet)
        if sentiment_scores['compound'] >= 0.05:
            emotion_counts['Positive'] += 1
        elif sentiment_scores['compound'] <= -0.05:
            emotion_counts['Negative'] += 1
        else:
            emotion_counts['Neutral'] += 1

        emotion_scores = {'Anger': 0, 'Sadness': 0, 'Anxiety': 0, 'Disturbance': 0}
        tokenized_words = word_tokenize(tweet)
        for word in tokenized_words:
            word = word.lower()
            if word in stopwords.words('english'):
                continue

            synsets = list(swn.senti_synsets(word))
            if synsets:
                synset = synsets[0]
                emotion_scores['Anger'] += synset.pos_score() - synset.neg_score()
                emotion_scores['Sadness'] += synset.neg_score() - synset.pos_score()
                emotion_scores['Anxiety'] += synset.obj_score() - synset.neg_score()
                emotion_scores['Disturbance'] += synset.neg_score() - synset.obj_score()

        dominant_emotion = get_emotion(emotion_scores)
        emotion_counts[dominant_emotion] += 1

    # Generate pie chart
    labels = emotion_counts.keys()
    sizes = emotion_counts.values()
    colors = ['#66b3ff', '#ff9999', '#99ff99', '#ffcc99', '#ccccff', '#ffccff', '#ccff99']
    explode = (0.1, 0, 0, 0, 0, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Emotion Sentiment Analysis')
    plt.show()

    # Generate bar graph
    plt.bar(labels, sizes, color=colors)
    plt.title('Emotion Sentiment Analysis')
    plt.xlabel('Emotions')
    plt.ylabel('Count')
    plt.show()

    # Display emotion counts
    print('Emotion Counts:')
    for emotion, count in emotion_counts.items():
        print(f'{emotion}: {count}')


# Provide the path to your CSV file
csv_file_path = 'cleaned_data1(1).csv'

# Perform sentiment analysis and generate visualizations
analyze_sentiments(csv_file_path)
