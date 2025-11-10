from flask import Flask, request, jsonify, make_response
import requests
import os

app = Flask(__name__)

TURNSTILE_SECRET = os.environ.get("TURNSTILE_SECRET")

@app.route("/verify", methods=["POST"])
def verify():
    token = request.form.get("response")
    if not token:
        return jsonify({"success": False, "message": "Missing token"}), 400

    resp = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": TURNSTILE_SECRET,
            "response": token
        },
        timeout=5
    )

    data = resp.json()

    if data.get("success"):
        response = make_response(jsonify({"success": True}))
        # Set cookie for 5 minutes
        response.set_cookie(
            "turnstile_verified",
            "true",
            max_age=300,
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        return response
    else:
        return jsonify({"success": False, "message": "Verification failed"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

