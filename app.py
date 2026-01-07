from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import re

app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")

def looks_like_gibberish(text: str) -> bool:
    if not text:
        return True

    text = text.strip()

    # Too short
    if len(text) < 3:
        return True

    # If more than 50% characters are non letters
    letters = sum(c.isalpha() for c in text)
    if letters / max(len(text), 1) < 0.5:
        return True

    # Repeated same character like "aaaaaa" or "!!!!!"
    if len(set(text)) <= 2:
        return True

    # Random consonant soup (very rough heuristic)
    if re.fullmatch(r"[bcdfghjklmnpqrstvwxyz]{6,}", text.lower()):
        return True

    return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}

    business = data.get("business", "").strip()
    task = data.get("task", "").strip()
    details = data.get("details", "").strip()

    combined = f"{business} {task} {details}"

    if looks_like_gibberish(combined):
        return jsonify({
            "result": "🤖 Hmm… that doesn’t look like a real request. Please enter something meaningful so I can help you 😊"
        })

    prompt = f"""
You are an AI assistant for a business platform called Yuktha Intelligence.

Business type: {business}
Task: {task}
Details: {details}

Generate a professional, structured response.
"""

    try:
        response = model.generate_content(prompt)
        return jsonify({"result": response.text})

    except Exception as e:
        return jsonify({"result": "⚠ Server error. Please try again in a moment."})


if __name__ == "__main__":
    app.run(debug=True)
