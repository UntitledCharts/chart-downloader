from main import AnsiColors

locale_keys = {
    "name": "unch",
    "chart_id_format": "unch_chart_id_format",
    "chart_id_prompt": "chart_id",
    "invalid_chart_id": "invalid_chart_id",
}
arguments = {
    "chart_id": {
        "required": True,
        "prompt": ["chart_id_prompt", "chart_id_format"],
        "invalid": "invalid_chart_id",
        "validate": [
            "arg.startswith('UnCh-')",
            "len(arg) > 37",
            "arg.removeprefix('UnCh-').isalnum()",
        ],
    },
}

from pathlib import Path


def exporter(locale, out_path: Path, chart_id: str):
    import json
    import requests
    from helpers.file_downloader import download_file
    from helpers.file_type import detect_image, detect_audio
    import shutil

    server_url = "https://untitledcharts.com"

    print(AnsiColors.apply_foreground(locale.fetching, AnsiColors.BLUE))
    url = f"{server_url}/sonolus/levels/{chart_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        if response.status_code == 404:
            return locale.invalid_chart_id
        response.raise_for_status()
        return locale.unknown_error  # in case it's something like 201
    item = data["item"]
    print(f"[{item['rating']}] {item['title']}")
    print(item["artists"])
    print(item["author"])
    del item["engine"]

    server_out_path = out_path / "untitled-charts"
    level_out_path = server_out_path / chart_id
    level_out_path.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(level_out_path)
    level_out_path.mkdir(parents=True, exist_ok=True)
    with open(level_out_path / "level.json", "w", encoding="utf8") as f:
        json.dump(item, f)

    print(AnsiColors.apply_foreground(locale.downloading, AnsiColors.BLUE))

    if "data" in item:
        print("Score...")
        data_url = item["data"]["url"]
        if data_url.startswith("/"):
            data_url = server_url + data_url
        download_file(data_url, level_out_path / "NSLevelData.json.gz")
    else:
        raise KeyError("Missing score file.")

    if "bgm" in item:
        print("Music...")
        bgm_url = item["bgm"]["url"]
        if bgm_url.startswith("/"):
            bgm_url = server_url + bgm_url

        music_path = level_out_path / "music"
        download_file(bgm_url, music_path)

        ext = detect_audio(music_path)
        if ext != "unknown":
            new_path = music_path.with_suffix(f".{ext}")
            music_path.rename(new_path)

    if "preview" in item:
        print("Preview...")
        preview_url = item["preview"]["url"]
        if preview_url.startswith("/"):
            preview_url = server_url + preview_url

        preview_path = level_out_path / "preview"
        download_file(preview_url, preview_path)
        ext = detect_audio(preview_path)
        if ext != "unknown":
            new_path = preview_path.with_suffix(f".{ext}")
            preview_path.rename(new_path)

    if "cover" in item:
        print("Jacket...")
        cover_url = item["cover"]["url"]
        if cover_url.startswith("/"):
            cover_url = server_url + cover_url

        jacket_path = level_out_path / "jacket"
        download_file(cover_url, jacket_path)

        ext = detect_image(jacket_path)
        if ext != "unknown":
            new_path = jacket_path.with_suffix(f".{ext}")
            jacket_path.rename(new_path)
    return True
