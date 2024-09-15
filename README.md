# AI Code Reviewer

AI Code Reviewer is a Python script that leverages OpenAI's GPT-3.5-turbo to automatically review code changes in GitLab repositories. It listens for merge request and push events, fetches the associated code changes, and provides feedback on the changes in a Markdown format.

## Features

- Automatically reviews code changes in GitLab repositories
- Provides feedback on code clarity, simplicity, bugs, and security issues
- Generates Markdown-formatted responses for easy readability in GitLab

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker (optional)
- An OpenAI API key
- A GitLab API token

### Installation

1. Clone o repo :
```
https://github.com/AugustoSavi/OpenAI-Gitlab-PR-Review
cd OpenAI-Gitlab-PR-Review
```

1. Crie um virtual env  

```bash
python3 -m venv venv
```

2. Ative o virtual env criado 

```bash
source ./venv/bin/activate
```

3. Instale as dependencias  

```bash
pip install --requirement requirements.txt
```

3. Create a `.env` file and set the required environment variables:

```
OPENAI_API_KEY=<your OpenAI API key>
GITLAB_TOKEN=<your GitLab API token>
GITLAB_URL=https://gitlab.com/api/v4
```

4. Run the application:

```
python src/handler.py
```

## Usage

1. Gere o access token no seu profile gitlab

2. Configure your GitLab repository to send webhook events to the AI Code Reviewer application by following [GitLab's webhook documentation](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html).

3. The AI Code Reviewer application will automatically review code changes in your GitLab repository and provide feedback as comments on merge requests and commit diffs.

## Testar local:

- https://dashboard.ngrok.com/get-started/setup/linux
