import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download once
nltk.download('vader_lexicon')

analyzer = SentimentIntensityAnalyzer()

def detect_emotion(text):
    score = analyzer.polarity_scores(text)['compound']

    if score >= 0.3:
        emotion = "positive"
    elif score <= -0.3:
        emotion = "negative"
    else:
        emotion = "neutral"

    return emotion, score


if __name__ == "__main__":
    sample_text = "I felt low after watching negative content for a long time"
    emotion, score = detect_emotion(sample_text)
    print("Emotion:", emotion)
    print("Score:", score)
