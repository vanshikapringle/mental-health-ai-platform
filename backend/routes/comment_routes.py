from flask import Blueprint, request
from services.sentiment_service import analyze_sentiment
from database.db import comments_collection

comment_bp = Blueprint("comment_bp", __name__)


@comment_bp.route("/analyze_comment", methods=["POST"])
def analyze_comment():

    data = request.json

    text = data["text"]

    sentiment = analyze_sentiment(text)

    comment = {
        "text": text,
        "sentiment": sentiment
    }

    comments_collection.insert_one(comment)

    return {
        "message": "Comment analyzed successfully",
        "data": {
            "text": text,
            "sentiment": sentiment
        }
    }


@comment_bp.route("/get_comments", methods=["GET"])
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