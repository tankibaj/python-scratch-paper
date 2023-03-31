# GitHub Release Notifier

A Python script that watches specified GitHub repositories for new releases and sends notifications to a Discord channel via webhook.

## Features

- Monitors multiple GitHub repositories for new releases.
- Sends notifications to a Discord channel using webhooks.
- Can be deployed as a Docker container or in a Kubernetes cluster.
- Optional GitHub authentication for higher rate limits.
- Configurable check interval.

## Requirements

- Python 3.6 or higher.
- Docker (for image build).
- Helm and Kubernetes (for Kubernetes deployment).

## Quick Start

### Local Deployment

- Clone the repository

    ```bash
    git clone https://github.com/tankibaj/python-scratch-paper.git
    ```

- Navigate to the project directory

    ```bash
    cd github-release-notifier
    ```

- Install the required Python packages.

    ```bash
    pip install -r requirements.txt
    ```

- Run the script

    ```bash
    python3 github_release_notifier.py
    ```

### Build container image

- Build the Docker image

    ```bash
    docker build -t thenaim/github-release-notifier:latest .
    ```

### Kubernetes Deployment
- Create a Helm chart using the provided instructions in the previous answers.

- Deploy the Helm chart to your Kubernetes cluster.

    ```bash
     helm upgrade --install github-release-notifier ./helm-chart \
      --namespace github-release-notifier  \
      --create-namespace
    ```

## Configuration
The following environment variables can be set for configuration:

- `DISCORD_WEBHOOK_URL`: The Discord webhook URL for sending notifications (required).
- `GITHUB_TOKEN`: A GitHub personal access token for authenticated requests (optional).
- `CHECK_INTERVAL`: The check interval in seconds (default: 7200, which is 2 hours).
- `REPOSITORIES`: A list of repositories to monitor, formatted as OWNER,REPO (required).


## Contributing
Contributions are welcome! Please submit a pull request or open an issue if you have any improvements or bug fixes.