from flask import Flask, request, jsonify, make_response
import requests
import os

app = Flask(__name__)
TURNSTILE_SECRET = os.environ.get("TURNSTILE_SECRET")

@app.route("/verify", methods=["POST"])
def verify():
    # ← CORRECT FIELD NAME
    token = request.form.get("cf-turnstile-response")
    
    if not token:
        return jsonify({"success": False, "message": "Missing token"}), 400

    if not TURNSTILE_SECRET:
        return jsonify({"success": False, "message": "Server misconfigured"}), 500

    # Real Cloudflare verification
    resp = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": TURNSTILE_SECRET,
            "response": token,
            "remoteip": request.remote_addr
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
            secure=True,      # ← Only over HTTPS
            samesite="Lax"
        )
        return response
    else:
        return jsonify({
            "success": False,
            "message": "Verification failed",
            "error-codes": data.get("error-codes", [])
        }), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
