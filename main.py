import json
import os

import google.genai as genai
from adk_agent.agent import BenchmarkAgent
agent = BenchmarkAgent()
from flask import Flask, jsonify, request, send_file, send_from_directory
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv() 

# Get your Gemini API key from an environment variable
API_KEY = os.environ.get("API_KEY")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
client = genai.Client(api_key=os.environ.get("API_KEY"))  # Initialize once

@app.route("/api/generate", methods=["POST"])
def generate_api():
    try:
        req_body = request.get_json()
        contents = req_body.get("contents")
        model_name = req_body.get("model")

        response = client.models.generate_content(
            model=model_name,
            contents=contents
        )
        print("Full response object:", response)
        # Extract generated text from Gemini response
        try:
            text = response.candidates[0].content.parts[0].text
        except Exception as extract_err:
            print("Error extracting text:", extract_err)
            text = str(response)
        print("Extracted text:", text)
        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/benchmark", methods=["POST"])
def benchmark_api():
    try:
        req_body = request.get_json()
        startup_name = req_body.get("startup")
        sector = req_body.get("sector")
        result = agent.benchmark(startup_name, sector)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

if __name__ == "__main__":
    app.run(
        port=int(os.environ.get('PORT', 80)),
        debug=True  # Enables debug mode for development
    )

