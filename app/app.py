import argparse
from fastapi import FastAPI, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from uvicorn import run
import pathlib

from microsearch.engine import SearchEngine

script_dir = pathlib.Path(__file__).resolve().parent
templates_path = script_dir / "templates"
static_path = script_dir / "static"


app = FastAPI()
engine = SearchEngine()
templates = Jinja2Templates(directory=str(templates_path))
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


def get_top_urls(scores_dict: dict, n: int):
    sorted_urls = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
    top_n_urls = sorted_urls[:n]
    top_n_dict = dict(top_n_urls)
    return top_n_dict


@app.get("/", response_class=HTMLResponse)
async def search(request: Request):
    posts = engine.posts
    return templates.TemplateResponse(
        "search.html", {"request": request, "posts": posts}
    )


@app.get("/results/{query}", response_class=HTMLResponse)
async def search_results(request: Request, query: str = Path(...)):
    results = engine.search(query)
    results = get_top_urls(results, n=5)
    return templates.TemplateResponse(
        "results.html", {"request": request, "results": results, "query": query}
    )


@app.get("/about")
def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    data = pd.read_parquet(args.data_path)
    content = list(zip(data["URL"].values, data["content"].values))
    engine.bulk_index(content)
    run(app, host="127.0.0.1", port=8000)
