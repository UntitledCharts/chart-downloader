import uuid, string, secrets, random


def random_string(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


# Locale
name = "日本語"

# Strings
invalid_choice = "選択肢が違うよ。もう一度試してみてね。"
# 譜面 (Chart)
chart_id = "ダウンロードしたい譜面のIDは何？ (例: {0})"
what_server = "どこから譜面をダウンロードしたい？"
done = "完了！"
required = "（必須）"
not_required = "（任意、スキップするにはエンター）"
invalid_chart_id = "譜面IDが間違ってるよ。"
invalid_answer = "回答が違うよ。もう一度試してみてね。"
fetching = "- 取得中..."
# ダウンロード中 (Downloading)
downloading = "- ダウンロード中..."
converting = "- 変換中..."
unknown_error = "原因不明のエラーが発生したよ。"

ask_difficulty = "What difficulty?"

auto = "自動検出"
# regions
ask_region = "どのサーバーリージョンを選択しますか？"
en_region = "グローバル [HATSUNE MIKU: COLORFUL STAGE! feat. HATSUNE MIKU]"
jp_region = "日本 [プロジェクトセカイ カラフルステージ! feat.初音ミク]"
chinese_region = "中国 [初音未来：彩色舞台！feat. 初音未来]"
korean_region = "韓国 [世界计划 彩色舞台 feat. 初音未来]"
taiwan_region = "台湾 [世界計畫 繽紛舞台!feat. 初音未來]"

choose_instance = "インスタンスを選んでね"

# Chart Cyanvas
cc_all = "Chart Cyanvas (2つのインスタンス)"

# Chart Cyanvas Archive
cc = "sevenc_nanashi の Chart Cyanvas (アーカイブ)"
cc_chart_id_format = f"chcy-{random_string(28-5)}"

# Chart Cyanvas Offshoot
cc_o = "chart-cyanvas.com の Chart Cyanvas"

# UntitledCharts
unch = "YumYummity の UntitledCharts"
unch_chart_id_format = f"UnCh-{uuid.uuid4().hex}"

# Next SEKAI
ns = "Burrito & qwewqa の Next Sekai"
ns_chart_id_format = f"coconut-next-sekai-{random.randint(1, 1000)}"

# sekai.best
sb = "sekai.best からの公式ゲーム譜面"
sb_chart_id_format = str(random.randint(1, 550))
# sb options
sb_cover = "どの曲のカバーがいい？"
