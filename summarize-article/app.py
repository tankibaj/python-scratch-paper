import argparse
import requests
from bs4 import BeautifulSoup
import os
import json


def split_text(text, token_limit):
    words = text.split()
    chunks = []
    current_chunk = []
    current_token_count = 0

    for word in words:
        tokens = len(word) + 1
        if current_token_count + tokens > token_limit:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_token_count = tokens
        else:
            current_chunk.append(word)
            current_token_count += tokens

    chunks.append(" ".join(current_chunk))
    return chunks


def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    text = " ".join([para.text for para in paragraphs])
    return text


def generate_summary(chunk, summary_size):
    api_endpoint = "https://api.openai.com/v1/completions"
    api_key = os.getenv("OPENAI_API_KEY")

    request_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    request_data = {
        "model": "text-davinci-003",
        "prompt": f"Summarize the following text in {summary_size} words:\n{chunk}",
        "max_tokens": summary_size * 5,
        "n": 1,
        "stop": None,
        "temperature": 0.5
    }

    response = requests.post(api_endpoint, headers=request_headers, json=request_data)
    response_text = response.json()["choices"][0]["text"]
    return response_text


def summarize_article(url, token_limit, summary_size):
    article_content = fetch_article_content(url)
    chunks = split_text(article_content, token_limit)
    summaries = [generate_summary(chunk, summary_size) for chunk in chunks]
    return " ".join(summaries)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate summaries of articles using the OpenAI API")
    parser.add_argument("url", help="The URL of the article to summarize")
    parser.add_argument("--token_limit", type=int, default=2048, help="The token limit for GPT models (default: 2048)")
    parser.add_argument("--summary_size", type=int, default=10,
                        help="The desired summary size in words (default: 100)")
    args = parser.parse_args()

    summary = summarize_article(args.url, args.token_limit, args.summary_size)
    print(summary)
