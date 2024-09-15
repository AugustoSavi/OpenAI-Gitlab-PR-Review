import openai
from typing import List, Dict

def load_system_content() -> str:
  with open('src/prompts/system-content.txt', 'r') as file:
    return file.read()

def load_pre_prompt() -> str:
  with open('src/prompts/pre-prompt.txt', 'r') as file:
    return file.read()

def load_questions() -> str:
  with open('src/prompts/questions.txt', 'r') as file:
    return file.read()

def load_assistant_content() -> str:
  with open('src/prompts/assistant-content.txt', 'r') as file:
    return file.read()


def create_review_message(diffs: str) -> List[Dict[str, str]]:
  return [
    {"role": "system", "content": load_system_content()},
    {"role": "user", "content": f"{load_pre_prompt()}\n\n{''.join(diffs)}\n\nPerguntas:\n{load_questions()}"},
    {"role": "assistant", "content": load_assistant_content()},
  ]