from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

suggestions = [
    "Strengthen your online presence through social media.",
    "Offer limited-time discounts to attract new customers.",
    "Collect feedback and improve services.",
    "Use email or WhatsApp marketing for engagement.",
    "Collaborate with influencers to reach wider audience.",
    "Optimize website SEO to attract local customers.",
    "Run targeted ads on Instagram and Facebook.",
    "Host virtual events or webinars to educate clients.",
    "Implement loyalty programs to retain customers.",
    "Create engaging video content for brand awareness."
]

personas = {
    "Strategist": [
        "Focus on marketing & branding.",
        "Plan long-term growth strategies.",
        "Analyze competitors to stay ahead."
    ],
    "Creative": [
        "Use viral campaigns and trends.",
        "Design creative visuals for social media.",
        "Experiment with unique content styles."
    ],
    "Efficiency": [
        "Automate workflows to save time.",
        "Optimize cost-efficiency for operations.",
        "Prioritize high-impact tasks first."
    ]
}

@app.route("/")
def home():
    return "Yuktha Intelligence backend is running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    business = data.get("business", "").strip()
    task = data.get("task", "").strip()
    details = data.get("details", "").strip()

    if not business or not task or not details:
        return jsonify({"result": "⚠ Please provide business, task, and details."})

    persona_name, persona_suggestions = random.choice(list(personas.items()))
    combined = suggestions + persona_suggestions
    chosen = random.sample(combined, 3)

    output_with_scores = ""
    for i, s in enumerate(chosen, 1):
        score = random.randint(75, 95)
        output_with_scores += f"{i}. {s} (Priority: {score}%)\n"

    result = f"""
YUKTHA INTELLIGENCE — BUSINESS INSIGHT

AI Persona: {persona_name}
Business Type: {business}
Requested Task: {task}

Strategy Recommendations:
{output_with_scores}
Additional Notes:
{details}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""".strip()

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
