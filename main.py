from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Sentences(BaseModel):
    sentences: list[str]

HAPPY_WORDS = {
    "love", "loved", "loving", "great", "excellent", "amazing", "awesome",
    "fantastic", "wonderful", "happy", "joy", "joyful", "excited", "best",
    "beautiful", "perfect", "brilliant", "superb", "delightful", "glad",
    "enjoy", "enjoyed", "fun", "incredible", "grateful", "thankful",
    "pleased", "cheerful", "outstanding", "terrific", "yay", "hooray",
    "smile", "laugh", "positive", "nice", "good", "like", "liked",
    "success", "successful", "win", "winning"
}

SAD_WORDS = {
    "hate", "hated", "terrible", "awful", "horrible", "bad", "worst",
    "sad", "disappointed", "disappointing", "upset", "angry",
    "frustrated", "annoyed", "miserable", "depressed", "cry", "crying",
    "dreadful", "disgusting", "dislike", "failed", "fail", "failure",
    "poor", "useless", "broken", "hurt", "pain", "problem", "issue",
    "suffering", "regret", "sorry", "waste", "pathetic", "disaster",
    "ugly", "boring", "dull", "tired", "exhausted", "tragic",
    "devastated", "hopeless", "helpless", "furious", "negative",
    "sucks", "cannot", "can't", "never", "nothing", "wrong"
}

def get_sentiment(text: str) -> str:
    text = text.lower()

    happy_score = sum(word in text for word in HAPPY_WORDS)
    sad_score = sum(word in text for word in SAD_WORDS)

    if sad_score > happy_score:
        return "sad"

    if happy_score > sad_score:
        return "happy"

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.45:
        return "happy"
    elif polarity < -0.30:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment")
def sentiment_analysis(data: Sentences):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": get_sentiment(sentence)
            }
            for sentence in data.sentences
        ]
    }
