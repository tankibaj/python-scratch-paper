# Gitea Smoke Test

This is a Python script that automates the process of creating a new private repository, adding a new branch, creating a new markdown file, and submitting a pull request based on the changes.

## Requirements
- Python 3.6 or higher
- Requests library

## Prerequisite
- Clone the repository or download the script.
- Install the Requests library by running the following command:
  ```
  pip3 install requests
  ```
- Set the following environment variables with your Gitea API endpoint and authorization token:
  ```
  export GITEA_ENDPOINT="https://git.example.com"
  export AUTH_TOKEN="your_gitea_api_token"
  ```
  
## Usage
- Open the terminal and navigate to the directory where the script is located.
- Run the script using the following command:
  ```
  python3 run.py
  ```
  
## Notes
- If the repository with the given name already exists, the script will delete it and create a new one.
- The script assumes that the default branch of the repository is "main". If your repository has a different default branch, you can change it in the script.
- The script uses lorem ipsum text as the content of the new markdown file. You can replace this with your own content by changing the file_content variable in the script.
- he script uses a UTF-16 string to encode the file content in base64, as this is the format that Gitea requires. If you change the content of the file, make sure to encode it using a UTF-16 string.