import argparse
import aiohttp
import asyncio
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_feed(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        return [entry.link for entry in feed.entries]
    except Exception as e:
        print(f"Error parsing feed {feed_url}: {e}")
        return []


async def fetch_content(session, url):
    async with session.get(url) as response:
        return await response.text()


async def process_feed(feed_url, session, loop):
    try:
        post_urls = await loop.run_in_executor(None, parse_feed, feed_url)
        tasks = [fetch_content(session, post_url) for post_url in post_urls]
        post_contents = await asyncio.gather(*tasks)
        cleaned_contents = [clean_content(content) for content in post_contents]
        return list(zip(post_urls, cleaned_contents))
    except Exception as e:
        print(f"Error processing feed {feed_url}: {e}")
        return []


def clean_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    cleaned_text = " ".join(chunk for chunk in chunks if chunk)
    return cleaned_text


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed-path")
    return parser.parse_args()


async def main(feed_file):
    async with aiohttp.ClientSession() as session:
        loop = asyncio.get_event_loop()
        with open(feed_file, "r") as file:
            feed_urls = [line.strip() for line in file]

        tasks = [process_feed(feed_url, session, loop) for feed_url in feed_urls]
        results = await asyncio.gather(*tasks)

    flattened_results = [item for sublist in results for item in sublist]
    df = pd.DataFrame(flattened_results, columns=["URL", "content"])
    df.to_parquet("output.parquet", index=False)


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.feed_path))
