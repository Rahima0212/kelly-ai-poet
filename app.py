import os
from flask import Flask, request, jsonify, render_template
from groq import Groq

# Load Kelly prompt
with open("kelly_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

app = Flask(__name__)

# Groq client (key will be loaded from environment)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = (data.get("message") or "").strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ Free model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/keycheck")
def keycheck():
    return "KEY LOADED ✅" if os.environ.get("GROQ_API_KEY") else "KEY MISSING ❌"

@app.route("/models")
def models():
    try:
        models = client.models.list().data
        return "<br>".join([m.id for m in models])
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run()
