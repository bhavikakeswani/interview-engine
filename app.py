from flask import Flask, jsonify, request
import random
import json

sessions = {}

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

    safe_questions = []
    for q in filtered:
        q_safe = q.copy()
        q_safe.pop("answer")
        safe_questions.append(q_safe)

    return jsonify(safe_questions)

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

    correct = question["answer"].strip().lower() == user_answer.strip().lower()

    return jsonify({
        "correct": correct
    })

@app.route("/start-interview", methods=["POST"])
def start_interview():
    data = request.json
    skill = data.get("skill")

    pool = QUESTIONS
    if skill:
        pool = [q for q in QUESTIONS if q["skill"].lower() == skill.lower()]

    if not pool:
        return jsonify({"error": "No questions found"}), 404

    session_id = str(random.randint(1000, 9999))

    sessions[session_id] = {
        "questions": random.sample(pool, min(5, len(pool))),
        "current": 0,
        "score": 0
    }

    return jsonify({
        "session_id": session_id,
        "total_questions": len(sessions[session_id]["questions"])
    })

@app.route("/interview/answer", methods=["POST"])
def interview_answer():
    data = request.json
    session_id = data.get("session_id")
    user_answer = data.get("answer")

    session = sessions.get(session_id)
    if not session:
        return jsonify({"error": "Invalid session"}), 404

    if session["current"] >= len(session["questions"]):
        return jsonify({
            "message": "Interview already finished",
            "score": session["score"],
            "total": len(session["questions"])
        }), 400

    q = session["questions"][session["current"]]

    if q["answer"].lower().strip() == user_answer.lower().strip():
        session["score"] += 1
        correct = True
    else:
        correct = False

    session["current"] += 1
    remaining = len(session["questions"]) - session["current"]

    return jsonify({
        "correct": correct,
        "score": session["score"],
        "remaining": remaining
    })

@app.route("/interview/question", methods=["GET"])
def interview_question():
    session_id = request.args.get("session_id")

    session = sessions.get(session_id)
    if not session:
        return jsonify({"error": "Invalid session"}), 404

    if session["current"] >= len(session["questions"]):
        return jsonify({"message": "Interview finished"}), 200

    q = session["questions"][session["current"]]
    q_safe = q.copy()
    q_safe.pop("answer")

    return jsonify(q_safe)

if __name__ == "__main__":
    app.run(debug=True)