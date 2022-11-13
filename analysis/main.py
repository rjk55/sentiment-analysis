import typing
import textblob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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
