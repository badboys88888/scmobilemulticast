import json

INPUT_JSON = "channels.json"
OUTPUT_M3U = "output.m3u"
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
    # CCTV1-1 → CCTV1
    return name.split("-")[0].replace(" ", "")

def get_logo(name):
    base = clean_name(name)
    return BASE_ICON_URL + icons.get(base, "")

def get_tvg_id(name, manual_id=""):
    base = clean_name(name).lower()

    # 如果 JSON 里有手动 tvg_id 优先用
    if manual_id:
        return manual_id

    # CCTV
    if "cctv" in base:
        return base

    # 卫视
    if "卫视" in name:
        return base.replace("卫视", "") + "hd"

    return ""

def convert_url(url):
    # rtp://239.x.x.x → http代理播放
    if url.startswith("rtp://"):
        return BASE_PROXY + url.replace("rtp://", "")
    return url

# ===================== 主程序 ===================== #
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
    f.write(f'#EXTM3U x-tvg-url="http://epg.112114.xyz/pp.xml"\n')

    for ch in data:
        name = ch["name"]
        url = ch["url"]
        group = ch.get("group", "")
        tvg_manual = ch.get("tvg_id", "")

        logo = get_logo(name)
        tvg_id = get_tvg_id(name, tvg_manual)

        play_url = convert_url(url)

        f.write(
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-logo="{logo}" group-title="{group}",{name}\n{play_url}\n'
        )

print("✅ M3U生成完成")
