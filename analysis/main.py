import typing
import textblob


def find_percentage(part, whole):
    # Round to 2 decimal places
    return round(100 * float(part) / float(whole), 2)


def analyze_polarity(text: typing.List[str]):
    """Analyze polarity"""
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    for sentence in text:
        analysis = textblob.TextBlob(sentence)
        polarity += analysis.sentiment.polarity

        if analysis.sentiment.polarity == 0:
            neutral += 1
        elif analysis.sentiment.polarity < 0.00:
            negative += 1
        elif analysis.sentiment.polarity > 0.00:
            positive += 1

    # print(f"Positive: {positive}")
    # print(f"Negative: {negative}")
    # print(f"Neutral: {neutral}")
    # print(f"Polarity: {polarity}")
    # print("\n------------------\n")

    positive = find_percentage(positive, len(text))
    negative = find_percentage(negative, len(text))
    neutral = find_percentage(neutral, len(text))
    polarity = polarity / len(text)

    print(f"Positive: {positive}%")
    print(f"Negative: {negative}%")
    print(f"Neutral: {neutral}%")
    print(f"Polarity: {polarity}%")
