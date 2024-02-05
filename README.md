microsearch
---

## Install environment

I recommend you to install everything in a virtual environment. I usually use `virtualenv` but any other environment manager should work.

```bash
virtualenv -p python3.10 venv
```

activate the environment

```bash
sourve venv/bin/activate
```

and install dependencies

```bash
pip install -r requirements.txt
```

## Crawl data

Now we need to download the content of the blogs. Here I provide a list of feeds examples, but feel free to use your own. To download the content do

```bash
python scripts/download_content.py --feed-path feeds.txt
```

## Launch app

Finally, once the content is crawled and stored you can run the app as


```bash
python -m microsearch.app --data-path output.parquet
```
