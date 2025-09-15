import json
import os

import google.genai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory

# Get your Gemini API key from an environment variable
API_KEY = os.environ.get("API_KEY")

# Check if the API key is set
if not API_KEY:
    raise ValueError("API_KEY environment variable not set. Please get an API key at https://g.co/ai/idxGetGeminiKey and set it as an environment variable.")

genai.configure(api_key=API_KEY)
app = Flask(__name__)


@app.route("/")
def index():
    return send_file('web/index.html')


@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            contents = req_body.get("contents")
            model = genai.GenerativeModel(req_body.get("model"))
            response = model.generate_content(contents, stream=True)

            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.text })

            return stream(), {'Content-Type': 'text/event-stream'}

        except Exception as e:
            return jsonify({ "error": str(e) })


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))
