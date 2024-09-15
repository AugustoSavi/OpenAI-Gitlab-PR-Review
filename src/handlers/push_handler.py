import os
import requests
from flask import jsonify
from utils.utils import create_review_message
import openai

gitlab_token = os.environ.get("GITLAB_TOKEN")
gitlab_url = os.environ.get("GITLAB_URL")

def handle_push(payload, not_comment):
    ref = payload["ref"]
    if "main" in ref or "master" in ref:
        return jsonify({"ok": "commit master/main"}), 200

    project_id = payload["project_id"]
    commit_id = payload["after"]
    commit_url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/commits/{commit_id}/diff"

    headers = {"Private-Token": gitlab_token}
    response = requests.get(commit_url, headers=headers)
    if response.status_code != 200:
        print("Erro na requisição da busca do commit")
        return jsonify({"error": "Erro na requisição"}), 502

    changes = response.json()
    changes_string = ''.join([str(change) for change in changes])
    messages = create_review_message(changes_string)

    try:
        completions = openai.ChatCompletion.create(
            deployment_id=os.environ.get("OPENAI_API_MODEL"),
            model=os.environ.get("OPENAI_API_MODEL") or "gpt-3.5-turbo",
            temperature=0.7,
            stream=False,
            messages=messages
        )
        answer = completions.choices[0].message["content"].strip()
    except Exception as e:
        print("Erro ao buscar completions", e)
        answer = f"I'm sorry, I'm not feeling well today. Error: {e}"

    comment_url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/commits/{commit_id}/comments"
    comment_payload = {"note": answer}
    
    if not_comment:
      return comment_payload
    
    comment_response = requests.post(comment_url, headers=headers, json=comment_payload)

    if comment_response.status_code != 201:
        print("Erro ao comentar no commit")
        return jsonify({"error": "Erro ao comentar no commit"}), 502

    return jsonify({"sucess": "comentado no commit"}), 200
