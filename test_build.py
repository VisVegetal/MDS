import json
from build import build

def test_titles_appear_in_output():
    build()
    with open("site/index.html") as f:
        html = f.read()
    with open("data.json") as f:
        items = json.load(f)
    for item in items:
        assert item["title"] in html
