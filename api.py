from flask import Flask, request, jsonify
from brain.response_engine import ResponseEngine

app = Flask(__name__)

# MANTRA brain
brain = ResponseEngine()


@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "assistant": "MANTRA",
        "role": "College Admission Assistant"
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "assistant": "MANTRA"
    })


@app.post("/chat")
def chat():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must be JSON."
        }), 400

    user_input = data.get("message")

    if not user_input or not isinstance(user_input, str):
        return jsonify({
            "error": "Please provide a valid 'message'."
        }), 400

    user_input = user_input.strip()

    if not user_input:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    try:
        response = brain.respond(user_input)

        return jsonify({
            "assistant": "MANTRA",
            "message": user_input,
            "response": response
        })

    except Exception as error:
        return jsonify({
            "assistant": "MANTRA",
            "error": "MANTRA encountered an internal error.",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    print("\n================================")
    print("       MANTRA API SERVER")
    print("================================")
    print("Status : ONLINE")
    print("API    : http://127.0.0.1:5001")
    print("Chat   : POST /chat")
    print("Health : GET  /health")
    print("================================\n")

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )