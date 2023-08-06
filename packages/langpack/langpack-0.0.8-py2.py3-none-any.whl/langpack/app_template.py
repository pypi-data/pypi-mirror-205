""" Example
curl -H "Content-Type: application/json" \
    -X POST -d '{{input_key}: }' \
    http://127.0.0.1:5000/predict
"""
import json
import io
from flask import Flask, request, jsonify

from langpack import tools
from flask import send_from_directory

langchain_app = tools.unpack("app.json")

app = Flask(__name__, static_folder="static")


@app.route("/chat", methods=["GET"])
def chat():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if type(langchain_app).__name__ == "AgentExecutor":
        result = langchain_app(data["input"])
    else:
        result = langchain_app(data)

    print(result)

    return jsonify({{output_key}: result[{output_key}]})


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
