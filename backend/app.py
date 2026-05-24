from flask import Flask, request
from pymongo import MongoClient
from dotenv import load_dotenv
from transformers import pipeline
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Load AI Sentiment Model
sentiment_pipeline = pipeline("sentiment-analysis")

# Get MongoDB URI
mongo_uri = os.getenv("MONGO_URI")

# Connect MongoDB Atlas
client = MongoClient(mongo_uri)

# Database and Collection
db = client["mental_health_db"]
comments_collection = db["comments"]


# Home Route
@app.route("/")
def home():
    return {
        "message": "Mental Health AI Backend Running"
    }


# Analyze Comment with AI
@app.route("/analyze_comment", methods=["POST"])
def analyze_comment():

    data = request.json

    text = data["text"]

    # AI Prediction
    result = sentiment_pipeline(text)

    sentiment = result[0]["label"]

    # Create document
    comment = {
        "text": text,
        "sentiment": sentiment
    }

    # Save into MongoDB
    comments_collection.insert_one(comment)

    return {
        "message": "Comment analyzed successfully",
        "data": {
            "text": text,
            "sentiment": sentiment
        }
    }


# Get All Comments
@app.route("/get_comments", methods=["GET"])
def get_comments():

    comments = []

    for comment in comments_collection.find():

        comments.append({
            "id": str(comment["_id"]),
            "text": comment["text"],
            "sentiment": comment["sentiment"]
        })

    return {
        "comments": comments
    }


# Run Flask App
if __name__ == "__main__":
    app.run(debug=False)