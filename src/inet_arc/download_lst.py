# Copyright (c) 2025 haogu2025@gmail.com
from argparse import ArgumentParser
import urllib.parse

import requests

def escape(url):
    parsed = urllib.parse.urlsplit(url)
    escaped_path = urllib.parse.quote(parsed.path)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, escaped_path, parsed.query, parsed.fragment))


def id2pdf(identifier):
    meta_url = f"https://archive.org/metadata/{identifier}"
    res = requests.get(meta_url)
    data = res.json()
    return [
        f["name"] for f in data["files"] if f["name"].lower().endswith(".pdf")
    ]


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--subject", default="Loeb Classical Library")
    args = parser.parse_args()
    base_api = "https://archive.org/advancedsearch.php"
    query = f'subject:"{args.subject}" AND format:pdf'
    # query = 'language:"japanese" AND format:pdf AND mediatype:texts AND date:[* TO 1930]'
    # query = 'language:"japanese" AND format:pdf AND date:[* TO 1930]'
    fields = ["identifier", "title", "language"]
    print(query)
    rows = 50
    page = 1
    cnt = 0

    while True:
        params = {
            "q": query,
            "fl[]": fields,
            "output": "json",
            "rows": rows,
            "page": page
        }
        response = requests.get(base_api, params=params)
        data = response.json()
        docs = data["response"]["docs"]
        if not docs:
            break

        for doc in docs:
            identifier = doc["identifier"]
            lang = doc["language"]
            title = doc.get("title", "No title")
            pdf_files = id2pdf(identifier)
            url = None
            if pdf_files:
                url = f"https://archive.org/download/{identifier}/{pdf_files[0]}"
                url = escape(url)
            cnt += 1
            print(f"{cnt} {title} [{lang}]\nurl: {url}\n")
        page += 1


if __name__ == "__main__":
    main()
