import uuid, string, secrets, random


def random_string(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


# Locale
name = "English"

# Strings
invalid_choice = "Invalid choice. Please try again."
chart_id = "What is the chart ID to download? (eg. {0})"
what_server = "What server do you want to download charts from?"
done = "Done!"
required = "(REQUIRED)"
not_required = "(NOT REQUIRED, ENTER TO SKIP)"
invalid_chart_id = "Invalid chart id."
invalid_answer = "Invalid answer. Please try again."
fetching = "- Fetching..."
downloading = "- Downloading..."
converting = "- Converting..."
unknown_error = "Unknown error occurred."
auto = "Auto Detect"
ask_difficulty = "What difficulty?"

# regions
ask_region = "What server region would you like to use?"
en_region = "Global [HATSUNE MIKU: COLORFUL STAGE! feat. HATSUNE MIKU]"
jp_region = "Japanese [プロジェクトセカイ カラフルステージ! feat.初音ミク]"
chinese_region = "Chinese [初音未来：彩色舞台！feat. 初音未来]"
korean_region = "Korean [世界计划 彩色舞台 feat. 初音未来]"
taiwan_region = "Taiwan [世界計畫 繽紛舞台!feat. 初音未來]"

choose_instance = "Choose an instance"

# Chart Cyanvas
cc_all = "Chart Cyanvas (2 instances)"

# Chart Cyanvas Archive
cc = "Chart Cyanvas (Archive) by sevenc_nanashi"
cc_chart_id_format = f"chcy-{random_string(28-5)}"

# Chart Cyanvas Offshoot
cc_o = "Chart Cyanvas by chart-cyanvas.com"

# UntitledCharts
unch = "UntitledCharts by YumYummity"
unch_chart_id_format = f"UnCh-{uuid.uuid4().hex}"

# Next SEKAI
ns = "Next Sekai by Burrito & qwewqa"
ns_chart_id_format = f"coconut-next-sekai-{random.randint(1, 1000)}"

# sekai.best
sb = "Official Game Charts from sekai.best"
sb_chart_id_format = str(random.randint(1, 550))
# sb options
sb_cover = "What song cover?"
