from flask import Flask, jsonify, request
import random
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

@app.route("/question/random", methods=["GET"])
def random_question():
    skill = request.args.get("skill")

    pool = QUESTIONS
    if skill:
        pool = [q for q in QUESTIONS if q["skill"].lower() == skill.lower()]

    if not pool:
        return jsonify({"error": "No questions found"}), 404

    q = random.choice(pool)
    q_safe = q.copy()
    q_safe.pop("answer")

    return jsonify(q_safe)

@app.route("/answer", methods=["POST"])
def check_answer():
    data = request.json
    question_id = data.get("id")
    user_answer = data.get("answer")

    question = next((q for q in QUESTIONS if q["id"] == question_id), None)

    if not question:
        return jsonify({"error": "Invalid question ID"}), 404

    correct = question["answer"] == user_answer

    return jsonify({
        "correct": correct,
        "correct_answer": question["answer"]
    })

if __name__ == "__main__":
    app.run(debug=True)