# Copyright (c) 2025 haogu2025@gmail.com
# download data list for NDL( National Diet Library)
# https://lab.ndl.go.jp/service/tsugidigi/apiinfo/
import zipfile

import requests


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def main() -> None:
    for i in range(1, 6):
        fname = f"dataset_202506_t_internet_{i:02}.zip"
        url = f"https://dl.ndl.go.jp/static/files/dataset/{fname}"
        download_file(url, fname)
        with zipfile.ZipFile(fname) as f:
            f.extractall()


if __name__ == "__main__":
    main()
