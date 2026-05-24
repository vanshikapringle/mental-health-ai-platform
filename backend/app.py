from flask import Flask, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Get MongoDB URI from .env
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB Atlas
client = MongoClient(
    mongo_uri,
    tlsCAFile=certifi.where()
)

# Create/select database
db = client["mental_health_db"]

# Create/select collection
comments_collection = db["comments"]


# Home Route
@app.route("/")
def home():
    return {
        "message": "Backend + MongoDB Connected Successfully"
    }


# Add Comment Route
@app.route("/add_comment", methods=["POST"])
def add_comment():

    # Get JSON data from request
    data = request.json

    # Create comment document
    comment = {
        "text": data["text"],
        "sentiment": data["sentiment"]
    }

    # Insert into MongoDB
    comments_collection.insert_one(comment)

    # Return response
    return {
        "message": "Comment added successfully",
        "data": {
            "text": comment["text"],
            "sentiment": comment["sentiment"]
        }
    }


# Run Flask Server
if __name__ == "__main__":
    app.run(debug=True)