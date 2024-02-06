# microsearch

`microsearch` is a minimal Python search engine designed for simplicity and efficiency. The project allows users to perform searches using Python, and it also provides an option to deploy a FastAPI app with an endpoint and a website for a user-friendly experience. It has been designed to provide users with a straightforward way to deploy their own search engine and search documents from their favorite blogs. The project includes a script for asynchronously downloading all the posts from a series of RSS feeds. 

## Features:
- **Python Implementation**: `microsearch` is entirely implemented in Python, making it accessible and easy to understand for developers with varying levels of experience.

- **FastAPI App Deployment**: The project provides an option to deploy a FastAPI app, allowing users to interact with the search engine through a dedicated endpoint and a user-friendly website.

- **RSS Feed Crawling Script**: To populate the search engine with data, `microsearch` offers a script for asynchronously downloading posts from a series of RSS feeds. This feature ensures that users can conveniently aggregate content from their chosen blogs.


## Getting started

The first step is to download this repo

```bash
git clone https://github.com/alexmolas/microsearch.git
```

Then, I recommend you install everything in a virtual environment. I usually use `virtualenv` but any other environment manager should work.

```bash
virtualenv -p python3.10 venv
```

activate the environment

```bash
source venv/bin/activate
```

and install the package and the dependencies

```bash
pip install .
```

## Crawl data

Now we need to download the content of the blogs. I'm sharing [here](https://github.com/alexmolas/microsearch/blob/main/feeds.txt) a list of feed examples, but please feel free to use your own. To download the content do

```bash
python download_content.py --feed-path feeds.txt
```

## Launch app

Finally, once the content is crawled and stored you can run the app as


```bash
python -m app.app --data-path output.parquet
```

and if you navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) you'll be able to query the engine.

