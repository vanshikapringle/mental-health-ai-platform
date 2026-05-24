from flask import Flask
from routes.comment_routes import comment_bp

app = Flask(__name__)

app.register_blueprint(comment_bp)


@app.route("/")
def home():
    return {
        "message": "Mental Health AI Backend Running"
    }


if __name__ == "__main__":
    app.run(debug=False)