import os
import time
import requests
from discord_webhook import DiscordWebhook
import logging
import sys

# Configure logging to write to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Time interval in seconds between release checks, it defaults to 2 hours (7200 seconds).
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 2 * 60 * 60))
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
REPOSITORIES = [tuple(repo.strip().split(', ')) for repo in os.getenv('REPOSITORIES', '').strip().split('\n') if repo]
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# The auth_log_printed flag, the log message will be printed only once for either authenticated or unauthenticated
# access. This will ensure that the logs are not too verbose while still providing the necessary information.
auth_log_printed = False


def get_latest_release(owner, repo):
    global auth_log_printed

    url = f'https://api.github.com/repos/{owner}/{repo}/releases'
    headers = {'Accept': 'application/vnd.github+json'}

    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
        if not auth_log_printed:
            logger.info("GitHub authenticated using token.")
            auth_log_printed = True
    else:
        if not auth_log_printed:
            logger.warning("Unauthenticated access. Please authentication to GitHub for higher rate limits.")
            auth_log_printed = True

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    releases = response.json()

    if releases:
        return releases[0]
    return None


def send_discord_notification(webhook_url, release, repo_info):
    owner, repo = repo_info
    release_name = release['name'] or release['tag_name']
    release_url = release['html_url']
    content = f"🚀 New release **{release_name}** in **{owner}/{repo}**\n{release_url}"
    webhook = DiscordWebhook(url=webhook_url, content=content)
    webhook.execute()


def main():
    logger.info("Starting GitHub release notifier...")

    last_release_ids = {}

    # Fetch and store the latest release ID for each repository initially
    for repo_info in REPOSITORIES:
        owner, repo = repo_info
        repo_key = f"{owner}/{repo}"

        try:
            latest_release = get_latest_release(owner, repo)
            if latest_release:
                last_release_ids[repo_key] = latest_release['id']
                logger.info(f"Initial release ID for {repo_key}: {latest_release['id']}")
        except Exception as e:
            logger.info(f"Error in {repo_key}: {e}")

    # Monitor for new releases
    while True:
        for repo_info in REPOSITORIES:
            owner, repo = repo_info
            repo_key = f"{owner}/{repo}"

            try:
                latest_release = get_latest_release(owner, repo)
                if latest_release and latest_release['id'] != last_release_ids.get(repo_key):
                    send_discord_notification(DISCORD_WEBHOOK_URL, latest_release, repo_info)
                    last_release_ids[repo_key] = latest_release['id']
                    logger.info(f"New release detected for {repo_key}: {latest_release['id']}")
            except Exception as e:
                logger.info(f"Error in {repo_key}: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
