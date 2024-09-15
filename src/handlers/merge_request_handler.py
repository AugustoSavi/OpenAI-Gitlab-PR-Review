import os
import requests
from flask import Flask, request, jsonify, Response
from utils.utils import create_review_message, load_questions
import openai

gitlab_token = os.environ.get("GITLAB_TOKEN")
gitlab_url = os.environ.get("GITLAB_URL")

def handle_merge_request(payload, not_comment) -> tuple[Response, int]:
  if payload["object_attributes"]["action"] != "open":
      print("object_attributes.action != open")
      return jsonify({"error": "Não abriu um mr"}), 200

  project_id = payload["project"]["id"]
  mr_id = payload["object_attributes"]["iid"]
  changes_url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_id}/changes"

  headers = {"Private-Token": gitlab_token}
  response = requests.get(changes_url, headers=headers)
  if response.status_code != 200:
      print("Erro ao buscar changes")
      return jsonify({"error": "Erro ao buscar changes"}), 502

  try:
      mr_changes = response.json()
  except ValueError:
      print("Erro ao decodificar JSON das changes")
      return jsonify({"error": "Erro ao decodificar JSON"}), 502

  diffs = [change["diff"] for change in mr_changes["changes"]]
  messages = create_review_message(diffs)

  try:
      completions = openai.ChatCompletion.create(
          deployment_id=os.environ.get("OPENAI_API_MODEL"),
          model=os.environ.get("OPENAI_API_MODEL") or "gpt-3.5-turbo",
          temperature=0.2,
          stream=False,
          messages=messages
      )
      answer = completions.choices[0].message["content"].strip()
  except Exception as e:
      answer = f"I'm sorry, I'm not feeling well today. Error: {e}"

  comment_url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_id}/notes"
  comment_payload = {"body": answer}

  if not_comment:
    return comment_payload

  comment_response = requests.post(comment_url, headers=headers, json=comment_payload)

  if comment_response.status_code != 201:
      print("Erro ao comentar no merge request")
      return jsonify({"error": "Erro ao comentar no merge request"}), 502

  return jsonify({"sucess": "comentado no merge request"}), 200
