import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Create an instance of the sentiment analyzer
sia = SentimentIntensityAnalyzer()

def analyze_report(text):
    # Analyze sentiment of the text
    sentiment = sia.polarity_scores(text)

    # Print sentiment analysis results
    print("Report Analysis Results:")
    print("Negative result: ", sentiment['neg']*100, "%")
    print("Neutral result: ", sentiment['neu']*100, "%")
    print("Positive result: ", sentiment['pos']*100, "%")
    print("Compound result: ", sentiment['compound']*100, "%")
    neg = sentiment['neg']
    pos = sentiment['pos']
    neu = sentiment['neu']

    if neg > 0.5:
        print("This report seems like negative. Think twice about it. ")
    elif pos >= 0.5:
        print("This report is positive. You are safe on it. ")
    elif neu > 0.5:
        print("This report is average. You can think it averagely. ")
