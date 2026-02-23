from datetime import datetime
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from emotion_engine.emotion_detector import detect_emotion
from storage.activity_db import insert_emotion

# Take user input
text = input("Enter how you feel: ")

# Detect emotion
emotion, score = detect_emotion(text)

# Generate timestamp
timestamp = datetime.now().isoformat()

# Store in database
insert_emotion(emotion, score, timestamp)

print("\nEmotion stored successfully!")
print("Emotion:", emotion)
print("Score:", score)
print("Timestamp:", timestamp)
