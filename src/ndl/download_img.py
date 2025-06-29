# Copyright (c) 2025 haogu2025@gmail.com
# download data list for NDL( National Diet Library)
# https://lab.ndl.go.jp/service/tsugidigi/apiinfo/
from argparse import ArgumentParser
from pathlib import Path

import requests


def get_canvases(pid):
    presentation_url = f"https://www.dl.ndl.go.jp/api/iiif/{pid}/manifest.json"
    res = requests.get(presentation_url)
    res.raise_for_status()
    manifest = res.json()
    return manifest["sequences"][0]["canvases"]


def download_images_from_canvases(canvases, save_dir):
    Path(save_dir).makedirs(exist_ok=True)
    for i, canvas in enumerate(canvases):
        image_url = canvas["images"][0]["resource"]["@id"]
        print(f"downloading {image_url} ...")
        img_res = requests.get(image_url)
        img_res.raise_for_status()
        with open(f"{save_dir}/page_{i}.jpg", "wb") as f:
            f.write(img_res.content)
    print("download complete")


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--pid", default="1912739")
    parser.add_argument("--save_dir", default="downloaded_pages")
    args = parser.parse_args()
    # https://dl.ndl.go.jp/pid/1912739
    canvases = get_canvases(args.pid)
    download_images_from_canvases(canvases, args.save_dir)


if __name__ == "__main__":
    main()
