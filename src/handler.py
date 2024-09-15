import os
import json
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
from handlers.merge_request_handler import handle_merge_request
from handlers.push_handler import handle_push
import logging

load_dotenv()

app = Flask(__name__)

@app.route('/hook', methods=['POST'])
def webhook() -> tuple[Response, int]:
  payload = request.json
  if payload is None:
      print("payload is None")
      return jsonify({"error": "Payload inválido"}), 400

  # print(json.dumps(payload, indent=2))
  object_kind = payload.get("object_kind")
  not_comment = request.headers.get("comment") is not None and "false" in request.headers.get("comment").lower()
  print("not_comment:", not_comment)

  if object_kind == "merge_request":
      return handle_merge_request(payload, not_comment)
  elif object_kind == "push":
      return handle_push(payload, not_comment)

  return jsonify({"result": "object_kind não suportado"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
