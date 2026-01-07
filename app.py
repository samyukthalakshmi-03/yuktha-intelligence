from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# 🔐 Set API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    business = data.get("business", "")
    task = data.get("task", "")
    details = data.get("details", "")

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
        return jsonify({"result": f"⚠ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
