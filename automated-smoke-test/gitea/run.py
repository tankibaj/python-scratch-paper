import os
import requests
import random
import lorem
import base64

# -- Define Gitea API base URL and headers
api_base_url = f"{os.environ['GITEA_ENDPOINT']}/api/v1"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"token {os.environ['AUTH_TOKEN']}"
}

# -- Define repository parameters
repo_name = "test-repo"
repo_desc = "This is a test repository"
repo_visibility = "private"

# -- Get user information
username = ""
user_url = f"{api_base_url}/user"
user_response = requests.get(user_url, headers=headers)
user_response.raise_for_status()
username = user_response.json()["login"]
if user_response.status_code == 200:
    print(f"Successfully logged in as '{username}'")
else:
    print("There was an error logging in")

# -- Delete repository if it already exists
repo_url = f"{api_base_url}/repos/{username}/{repo_name}"
repo_response = requests.delete(repo_url, headers=headers, allow_redirects=True)
if repo_response.status_code == 204:
    print(f"Repository '{repo_name}' deleted successfully.")

# -- Create repository
repo_data = {
    "name": repo_name,
    "description": repo_desc,
    "private": (repo_visibility == "private"),
    "auto_init": True,
    "default_branch": "main"
}
repo_url = f"{api_base_url}/user/repos"
repo_response = requests.post(repo_url, headers=headers, json=repo_data)
repo_response.raise_for_status()
if repo_response.status_code == 201:
    print(f"Repository '{repo_name}' created successfully.")

# -- Create a new branch with random name
branch_name = f"branch-{random.randint(1, 1000)}"
branch_data = {
    "new_branch_name": branch_name,
    "old_branch_name": repo_response.json()["default_branch"]
}
branch_url = f"{api_base_url}/repos/{username}/{repo_name}/branches"
branch_response = requests.post(branch_url, headers=headers, json=branch_data)
branch_response.raise_for_status()
if branch_response.status_code == 201:
    print(f"New branch '{branch_name}' created successfully.")

# -- Create new markdown file
file_name = f"file-{random.randint(1, 1000)}.md"
file_content = lorem.paragraph()
# Encode file_content in base64 using a UTF-16 string
# https://github.com/go-gitea/gitea/issues/7844#issuecomment-524978197
base64_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
file_data = {
    "author": {"email": "thanos@avengers.movie", "name": "thanos"},
    "committer": {"email": "thanos@avengers.movie", "name": "thanos"},
    "message": f"Added {file_name} file",
    "content": base64_content,
    "branch": branch_name
}
file_url = f"{api_base_url}/repos/{username}/{repo_name}/contents/{file_name}"
file_response = requests.post(file_url, headers=headers, json=file_data)
file_response.raise_for_status()
if file_response.status_code == 201:
    print(f"File '{file_name}' created successfully.")

# Create a pull request based on changes
pr_title = f"Pull Request - {file_name}"
pr_data = {
    "title": pr_title,
    "head": branch_name,
    "base": "main",
    "body": f"This pull request adds the file '{file_name}' with the following content:\n\n{file_content}"
}
pr_url = f"{api_base_url}/repos/{username}/{repo_name}/pulls"
pr_response = requests.post(pr_url, headers=headers, json=pr_data)
pr_response.raise_for_status()
if pr_response.status_code == 201:
    print(f"Pull '{pr_title}' request created successfully.")
