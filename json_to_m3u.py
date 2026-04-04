import json

INPUT_JSON = "channels.json"
OUTPUT_M3U = "live.m3u"
ICON_MAP = "icons_map.json"

BASE_PROXY = "http://192.168.8.1:8888/rtp/"
BASE_ICON_URL = "https://raw.githubusercontent.com/badboys88888/scmobilemulticast/main/"

# ===================== 读取 logo ===================== #
try:
    with open(ICON_MAP, "r", encoding="utf-8") as f:
        icons = json.load(f)
except:
    icons = {}

# ===================== 工具函数 ===================== #
def clean_name(name):
    return name.split("-")[0].replace(" ", "")

def get_logo(name):
    base = clean_name(name)
    file = icons.get(base, "")

    if not file:
        return ""   # ❌ 没有就返回空

    return BASE_ICON_URL + file

def get_tvg_id(name, manual=""):
    base = clean_name(name).lower()

    if manual:
        return manual

    if "cctv" in base:
        return base

    if "卫视" in name:
        return base.replace("卫视", "") + "hd"

    return ""

def convert_url(url):
    if url.startswith("rtp://"):
        return BASE_PROXY + url.replace("rtp://", "")
    return url

# ===================== 主程序 ===================== #
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
    f.write('#EXTM3U x-tvg-url="http://epg.112114.xyz/pp.xml"\n')

    for ch in data:
        name = ch.get("name", "")
        url = ch.get("url", "")
        group = ch.get("group", "")
        tvg_manual = ch.get("tvg_id", "")

        # ❌ 跳过空数据
        if not name or not url:
            continue

        play_url = convert_url(url)
        tvg_id = get_tvg_id(name, tvg_manual)
        logo = get_logo(name)

        # ===== 关键：动态拼 EXTINF ===== #
        extinf = f'#EXTINF:-1 tvg-id="{tvg_id}"'

        if logo:   # ✔ 只有有logo才写
            extinf += f' tvg-logo="{logo}"'

        if group:
            extinf += f' group-title="{group}"'

        extinf += f',{name}'

        f.write(extinf + "\n")
        f.write(play_url + "\n")

print("✅ live.m3u 生成完成")
