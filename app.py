from flask import Flask, jsonify, request
import json

app = Flask(__name__)

with open("questions.json") as f:
    QUESTIONS = json.load(f)

@app.route("/")
def home():
    return "Interview Engine is running 🚀"

@app.route("/questions", methods=["GET"])
def get_questions():
    skill = request.args.get("skill")
    difficulty = request.args.get("difficulty")

    filtered = QUESTIONS

    if skill:
        filtered = [q for q in filtered if q["skill"].lower() == skill.lower()]

    if difficulty:
        filtered = [q for q in filtered if q["difficulty"].lower() == difficulty.lower()]

    return jsonify(filtered)

if __name__ == "__main__":
    app.run(debug=True)