import typing
from typing import List
import textblob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import pandas as pd



def find_percentage(part, whole):
    # Round to 2 decimal places
    return round(100 * float(part) / float(whole), 2)


def analyze_polarity(sentence_list: typing.List[str]):
    """Analyze polarity"""
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    len_of_sentence_list = len(sentence_list)

    # The stopwords are a list of words that are very very common but don’t provide 
    # useful information for most text analysis procedures.
    stop_words = set(stopwords.words("english"))

    for sentence in sentence_list:
        # word tokenize breaks down the sentence into a list of words
        word_tokens = nltk.word_tokenize(sentence)

        filtered_sentence = [w for w in word_tokens if not w in stop_words]

        analysis = textblob.TextBlob(" ".join(filtered_sentence))
        polarity += analysis.sentiment.polarity

        if analysis.sentiment.polarity == 0:
            neutral += 1
        elif analysis.sentiment.polarity < 0.00:
            negative += 1
        elif analysis.sentiment.polarity > 0.00:
            positive += 1

    positive = find_percentage(positive, len_of_sentence_list)
    negative = find_percentage(negative, len_of_sentence_list)
    neutral = find_percentage(neutral, len_of_sentence_list)
    polarity = find_percentage(polarity, len_of_sentence_list)
    
    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "polarity": polarity,
    }

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

def process_data(reviews:typing.List[dict]):
    # Fake review detection
    # There are various ways to detect fake reviews.
    # Here we are using some simple methods to detect fake reviews.
    # 1. Coherence - "evaluates whether the assigned rating is in accordance with the opinions expressed in the review's text."
    #     eg: If the review is 5 star, then the review should be positive. or if the review is 1 star, then the review should be negative.
    # 2. Filtering verified purchases 
    # 3. Filtering reviews that too short or too long - This is useful to filter reviews that posted by bots.
    # 4. Author - Check the author name. If the author name is not a real name, then it is a fake review.
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
    tokens = df['Full Sentence'].apply(lambda x: remove_stopwords(x))
    df['Word Tokens'] = tokens

    # Getting the sentiment of each review
    df['Sentiment Score'] = df["tokens"].apply(lambda x: get_sentiment(" ".join(x)))

    # Checking if the sentiment is in accordance with the rating
    df['Coherence'] = df.apply(lambda x: get_coherence(x['sentiment'], int(x['rating'][0])), axis=1)

    # Number of negative words in the review
    df['Neg Count'] = get_negative_count(df['Word Tokens'].to_list())

    # Unique words count
    unique_words = []

    for token in df['Word Tokens'].to_list():
        unique_words.append(len(set([t.lower() for t in token])))    

    df['Unique_Words'] = unique_words

  
