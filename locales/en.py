import uuid, string, secrets


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
