from main import AnsiColors, apply_locale_keys, ask

locale_keys = {
    "name": "sb",
    "chart_id_format": "sb_chart_id_format",
    "chart_id_prompt": "chart_id",
    "invalid_chart_id": "invalid_chart_id",
    "auto": "auto",
    "ask_region": "ask_region",
    "global": "en_region",
    "japanese": "jp_region",
    "chinese": "chinese_region",
    "korean": "korean_region",
    "taiwanese": "taiwan_region",
    "ask_difficulty": "ask_difficulty",
    "cover": "sb_cover",
}
arguments = {
    "chart_id": {
        "required": True,
        "prompt": ["chart_id_prompt", "chart_id_format"],
        "invalid": "invalid_chart_id",
        "validate": [
            "arg.isdigit()",
        ],
    },
}

from pathlib import Path


def exporter(locale, out_path: Path, chart_id: str, region: str = "auto"):
    import json
    import requests
    from helpers.file_downloader import download_file
    from helpers.file_type import detect_image, detect_audio
    import shutil
    from helpers.backgrounds import generate_backgrounds

    if region is None:
        region = "auto"

    chart_id = int(chart_id)

    asset_paths = {
        "chart": "https://storage.sekai.best/sekai-{region}-assets/music/music_score/{id_4_zpad}_01/{diff}.txt",
        "music": "https://storage.sekai.best/sekai-{region}-assets/music/long/{cover_name}/{cover_name}.mp3",
        "preview": "https://storage.sekai.best/sekai-{region}-assets/music/short/{cover_name}/{cover_name}_short.mp3",
        "jacket": "https://storage.sekai.best/sekai-{region}-assets/music/jacket/{jacket_name}/{jacket_name}.png",
    }
    db_paths = {
        "jp": "https://raw.githubusercontent.com/Sekai-World/sekai-master-db-diff/refs/heads/main/{file}.json",
        "en": "https://raw.githubusercontent.com/Sekai-World/sekai-master-db-en-diff/refs/heads/main/{file}.json",
        "kr": "https://raw.githubusercontent.com/Sekai-World/sekai-master-db-kr-diff/refs/heads/main/{file}.json",
        "cn": "https://raw.githubusercontent.com/Sekai-World/sekai-master-db-cn-diff/refs/heads/main/{file}.json",
        "tw": "https://raw.githubusercontent.com/Sekai-World/sekai-master-db-tc-diff/refs/heads/main/{file}.json",
    }
    region_check_order = [
        "jp",
        "en",
        "cn",
        "kr",
        "tw",
    ]  # jp has most charts, en has most exclusives, cn has some exclusives, kr has least exclusives, tw has none
    # all of this is a fallback, we attempt to detect cn/kr exclusives first, then use this

    print(AnsiColors.apply_foreground(locale.fetching, AnsiColors.BLUE))
    chart_data = None
    if region == "auto":
        # check cn/kr if the id looks like exclusive, move the region forward in region_check_order
        if chart_id >= 10000 and chart_id < 20000:
            rg_id = region_check_order.index("kr")
            del region_check_order[rg_id]
            region_check_order.insert(0, "kr")
        if chart_id >= 20000 and chart_id < 30000:
            rg_id = region_check_order.index("cn")
            del region_check_order[rg_id]
            region_check_order.insert(0, "cn")
        for r in region_check_order:
            url = db_paths[r].format(file="musics")
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for chart in data:
                    if chart.get("id") == chart_id:
                        chart_data = chart
                        region = r
                        break
                if region != "auto":
                    break
                else:
                    continue
            elif response.status_code == 404:
                continue
            else:
                response.raise_for_status()
                return locale.unknown_error
        if region == "auto":
            return locale.invalid_chart_id
    else:
        url = db_paths[region].format(file="musics")
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for chart in data:
                if chart.get("id") == chart_id:
                    chart_data = chart
                    break
            else:
                return locale.invalid_chart_id
        elif response.status_code == 404:
            print("nt found")
            return locale.invalid_chart_id
        else:
            response.raise_for_status()
            return locale.unknown_error

    server_out_path = out_path / "pjsk"

    difficulties_url = db_paths[region].format(file="musicDifficulties")
    difficulties_data_resp = requests.get(difficulties_url)
    if difficulties_data_resp.status_code == 200:
        difficulties_data = difficulties_data_resp.json()
    else:
        difficulties_data_resp.raise_for_status()

    all_difficulties = [
        diff["musicDifficulty"]
        for diff in difficulties_data
        if diff.get("musicId") == chart_id
    ]

    covers_url = db_paths[region].format(file="musicVocals")
    covers_data_resp = requests.get(covers_url)
    if covers_data_resp.status_code == 200:
        covers_data = covers_data_resp.json()
    else:
        covers_data_resp.raise_for_status()
        return locale.unknown_error

    game_chars_url = db_paths[region].format(file="gameCharacters")
    game_chars_data_resp = requests.get(game_chars_url)
    if game_chars_data_resp.status_code == 200:
        game_chars_data = game_chars_data_resp.json()
    else:
        game_chars_data_resp.raise_for_status()
        return locale.unknown_error

    external_chars_url = db_paths[region].format(file="outsideCharacters")
    external_chars_data_resp = requests.get(external_chars_url)
    if external_chars_data_resp.status_code == 200:
        external_chars_data = external_chars_data_resp.json()
    else:
        external_chars_data_resp.raise_for_status()
        return locale.unknown_error

    if region != "en":
        en_game_chars_url = db_paths["en"].format(file="gameCharacters")
        en_game_chars_data_resp = requests.get(en_game_chars_url)
        if en_game_chars_data_resp.status_code == 200:
            en_game_chars_data = en_game_chars_data_resp.json()
        else:
            en_game_chars_data_resp.raise_for_status()
            return locale.unknown_error

        en_external_chars_url = db_paths["en"].format(file="outsideCharacters")
        en_external_chars_data_resp = requests.get(en_external_chars_url)
        if en_external_chars_data_resp.status_code == 200:
            en_external_chars_data = en_external_chars_data_resp.json()
        else:
            en_external_chars_data_resp.raise_for_status()
            return locale.unknown_error

    all_covers = [cover for cover in covers_data if cover.get("musicId") == chart_id]

    def handle_cover(cover: str) -> str:
        cover_caption = cover["caption"]
        en_cover_caption = None
        characters = cover["characters"]
        character_names = []
        en_character_names = [] if region != "en" else None
        for character in characters:
            charType = character["characterType"]
            charId = character["characterId"]
            # charType in ["game_character", "outside_character"]
            if charType == "game_character":
                char_data = next(
                    char for char in game_chars_data if char["id"] == charId
                )
                # only EN needs to add space (open an issue if wrong!)
                # Korean automatically adds the space in data.
                # JP/CN/TW don't need space.
                char_name = f"{char_data.get('firstName')}{' ' if region in ['en'] else ''}{char_data.get('givenName')}"
                if region != "en":
                    en_char_data = next(
                        (char for char in en_game_chars_data if char["id"] == charId),
                        None,
                    )
                    if en_char_data:
                        en_char_name = f"{en_char_data.get('firstName')} {en_char_data.get('givenName')}"
                        en_character_names.append(en_char_name)
                    else:
                        en_character_names.append(char_name)
                character_names.append(char_name)
            elif charType == "outside_character":
                char_data = next(
                    char for char in external_chars_data if char["id"] == charId
                )
                char_name = char_data["name"]
                if region != "en":
                    en_char_data = next(
                        (
                            char
                            for char in en_external_chars_data
                            if char["id"] == charId
                        ),
                        None,
                    )
                    if en_char_data:
                        en_char_name = en_char_data["name"]
                        en_character_names.append(en_char_name)
                    else:
                        en_character_names.append(char_name)
            else:
                print(f"WARN! character not game or external found: {character}")
        en_cover_map = {
            "vs_": "Virtual Singer ver.",
            "se_": "Sekai ver.",
            "an_": "Cover ver.",
        }
        for ab_key, en_cap in en_cover_map.items():
            if cover["assetbundleName"].startswith(ab_key):
                en_cover_caption = en_cap
                break
        if region == "en":
            caption = cover_caption
        else:
            if en_cover_caption:
                caption = f"{cover_caption} [{en_cover_caption}]"
            else:
                caption = cover_caption
        return (
            f"{caption}\n   - {', '.join(character_names).strip()}"
            + (
                f"\n   - {', '.join(en_character_names).strip()}"
                if en_character_names
                else ""
            )
            + "\n -->"
        )

    cover_index = ask(
        apply_locale_keys("cover", locale_keys),
        [str(i) for i in range(1, len(all_covers) + 1)],
        [handle_cover(cover) for cover in all_covers],
    )
    cover = all_covers[int(cover_index) - 1]

    possible_jacket_variants_url = db_paths[region].format(file="musicAssetVariants")
    possible_jacket_variants_resp = requests.get(possible_jacket_variants_url)
    if possible_jacket_variants_resp.status_code == 200:
        possible_jacket_variants_data = possible_jacket_variants_resp.json()
    else:
        possible_jacket_variants_resp.raise_for_status()
        return locale.unknown_error

    jacket_name = chart_data["assetbundleName"]
    asset_variant = next(
        (
            jacket_variant
            for jacket_variant in possible_jacket_variants_data
            if jacket_variant.get("musicVocalId") == cover["id"]
            and jacket_variant.get("musicAssetType") == "jacket"
        ),
        None,
    )
    if asset_variant:
        jacket_name = asset_variant["assetbundleName"]

    cover_name = cover["assetbundleName"]

    level_out_path = (
        server_out_path
        / region
        / f"{chart_id}_cover_{all_covers[int(cover_index)-1]['id']}"
    )
    level_out_path.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(level_out_path)
    level_out_path.mkdir(parents=True, exist_ok=True)

    with open(level_out_path / "level.json", "w", encoding="utf8") as f:
        json.dump(chart_data, f)

    print(AnsiColors.apply_foreground(locale.downloading, AnsiColors.BLUE))

    print("Score...")
    for diff in all_difficulties:
        data_url = asset_paths["chart"].format(
            region=region, id_4_zpad=str(chart_id).zfill(4), diff=diff
        )
        download_file(data_url, level_out_path / f"{diff}.sus")

    print("Music...")
    bgm_url = asset_paths["music"].format(region=region, cover_name=cover_name)
    music_path = level_out_path / "music.mp3"
    download_file(bgm_url, music_path)

    print("Preview...")
    preview_url = asset_paths["preview"].format(region=region, cover_name=cover_name)
    preview_path = level_out_path / "preview.mp3"
    download_file(preview_url, preview_path)

    print("Jacket...")
    cover_url = asset_paths["jacket"].format(region=region, jacket_name=jacket_name)
    jacket_path = level_out_path / "jacket.png"
    download_file(cover_url, jacket_path)
    generate_backgrounds(jacket_path)
    return True
