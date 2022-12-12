from typing import List, Tuple
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import pandas as pd



def find_percentage(part, whole):
    # Round to 2 decimal places
    return round(100 * float(part) / float(whole), 2)


def tokenize(sentence:str) -> str:
    return word_tokenize(sentence)

def remove_stopwords(sentence:str) -> list:
    stop_words = set(stopwords.words('english'))
    word_tokens = tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence

def get_sentiment(sentence:str) -> float:
    analysis = TextBlob(sentence)
    return analysis.sentiment.polarity

def get_coherence(sentiment:float, rating:int) -> bool:
    if sentiment > 0 and rating >= 4:
        return True
    elif sentiment < 0 and rating <= 2:
        return True

    elif sentiment == 0:
        return True
    else:
        return False

def get_negative_count(tokens:List[List[str]]) -> List[int]:
    """
    Get the number of negative words in the review
    Args: accepts a list of list of words
    Returns: a list of number of negative words in each review
    """
    negative_count = []
    for token in tokens:
        neg = 0
        for word in token:
            testimonial = TextBlob(word)
            if testimonial.sentiment.polarity < 0:
                neg += 1
        negative_count.append(neg)
    return negative_count

def process_reviews(reviews:List[dict]):
    # Fake review detection
    # There are various ways to detect fake reviews.
    # Here we are using some simple methods to detect fake reviews.
    # 1. Coherence - "evaluates whether the assigned rating is in accordance with the opinions expressed in the review's text."
    #     eg: If the review is 5 star, then the review should be positive. or if the review is 1 star, then the review should be negative.
    # 2. Filtering verified purchases 
    # 3. Filtering reviews that too short or too long - This is useful to filter reviews that posted by bots.
    # 4. Author TODO: - Check the author name. If the author name is not a real name, then it is a fake review.
    #    eg: It's very common to see fake reviews with names like "Amazon Customer", "Anonymous", or false names like a single letter or a number.

    df = pd.DataFrame(reviews)

    # TODO: clean the dataset
    # Joining review title and review content and adding it to a new column
    df["Full Sentence"] = df[["title", "content"]].agg(". ".join, axis=1)

    # Removing emojis from the review
    df["Full Sentence"] = df["Full Sentence"].apply(lambda x: x.encode("ascii", "ignore").decode())

    # Formatting the rating (eg: 5.0 out of 5 stars to 5.0)
    df["rating"].apply(lambda x: x.split(" ")[0]).astype(float)

    # Remove special characters
    # \W represents any non-word character
    df["Full Sentence"] = df["Full Sentence"].str.replace("\W", " ")

    # \d represents Numeric digits
    df["Full Sentence"] = df["Full Sentence"].str.replace("\d", " ")

    # Upper case to lower case
    df["Full Sentence"] = df["Full Sentence"].str.lower()

    # Removing stopwords and converting the sentence to a list of token words
    df['Word Tokens'] = df['Full Sentence'].apply(lambda x: remove_stopwords(x))

    # Getting the sentiment of each review
    df['Sentiment Score'] = df["Word Tokens"].apply(lambda x: get_sentiment(" ".join(x)))

    # Checking if the sentiment is in accordance with the rating
    df['Coherence'] = df.apply(lambda x: get_coherence(x['Sentiment Score'], int(x['rating'][0])), axis=1)

    # Number of negative words in the review
    df['Neg Count'] = get_negative_count(df['Word Tokens'].to_list())

    # Unique words count
    unique_words = []

    for token in df['Word Tokens'].to_list():
        unique_words.append(len(set([t.lower() for t in token])))    

    df['Unique_Words'] = unique_words

    df["Authenticity"] = df.apply(lambda x: x['Coherence'] and x['verified_purchase'] and x['Unique_Words'] > 3, axis=1)

    return df


def analyze_polarity(reviews:List[dict]) -> Tuple[float, float, float, float]:
    """Analyze polarity on the basis of positive, negative and neutral reviews"""
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    
    df = process_reviews(reviews)
    # total number of reviews
    total = len(df["Full Sentence"])

    # Get sentiment score where authenticity is True
    sentiment_score = df[df["Authenticity"] == True]["Sentiment Score"].to_list()

    for score in sentiment_score:
        # adding up polarities by adding positive, negative and neutral reviews
        if score > 0:
            positive += 1
        elif score < 0:
            negative += 1
        else:
            neutral += 1
        polarity += score
    
    # percentage of positive reviews
    positive = round(positive/total * 100, 2)

    # percentage of negative reviews
    negative = round(negative/total * 100, 2)

    # percentage of neutral reviews
    neutral = round(neutral/total * 100, 2)

    # average polarity
    polarity = round(polarity/total, 2)

    return positive, negative, neutral, polarity