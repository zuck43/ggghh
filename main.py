from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ StarX GitHub Dispatch Proxy is Live"

@app.route('/trigger')
def trigger_dispatch():
    secret = request.args.get("secret")
    if secret != os.environ.get("SECRET_KEY"):
        return "⛔ Unauthorized", 403

    url = os.environ['GITHUB_API_URL']  # full URL like https://api.github.com/repos/OWNER/REPO/dispatches
    headers = {
        "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "StarX-CronProxy"
    }
    data = {
  "event_type": "external-triggered"
    }
    res = requests.post(url, headers=headers, json=data)
    return jsonify({
        "status": res.status_code,
        "response": res.text
    })
