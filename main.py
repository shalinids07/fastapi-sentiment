from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
    "smile", "laugh", "positive", "nice", "good", "like", "liked"
}

SAD_WORDS = {
    "hate", "hated", "terrible", "awful", "horrible", "bad", "worst",
    "sad", "disappointed", "disappointing", "upset", "angry",
    "frustrated", "annoyed", "miserable", "depressed", "cry", "crying",
    "dreadful", "disgusting", "dislike", "failed", "fail", "failure",
    "poor", "useless", "broken", "hurt", "pain", "problem", "issue",
    "suffering", "regret", "sorry", "waste", "pathetic", "disaster",
    "ugly", "boring", "dull", "tired", "exhausted", "tragic",
    "devastated", "hopeless", "helpless", "furious", "negative", "sucks"
}

def get_sentiment(text: str) -> str:
    lower = text.lower()

    words = set(
        lower.replace(".", "")
             .replace(",", "")
             .replace("!", "")
             .replace("?", "")
             .split()
    )

    happy_score = len(words & HAPPY_WORDS)
    sad_score = len(words & SAD_WORDS)

    if happy_score > sad_score:
        return "happy"

    if sad_score > happy_score:
        return "sad"

    polarity = TextBlob(text).sentiment.polarity

    if polarity >= 0.35:
        return "happy"
    elif polarity <= -0.15:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment")
def sentiment_analysis(data: Sentences):
    results = []

    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": get_sentiment(sentence)
        })

    return {"results": results}
