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

class ResultItem(BaseModel):
    sentence: str
    sentiment: str

class Result(BaseModel):
    results: list[ResultItem]

def get_sentiment(text: str):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.1:
        return "happy"
    elif polarity < -0.1:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment", response_model=Result)
def sentiment_analysis(data: Sentences):
    results = []

    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": get_sentiment(sentence)
        })

    return {"results": results}
