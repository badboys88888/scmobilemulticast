import json

INPUT_JSON = "channels.json"
OUTPUT_M3U = "output.m3u"
ICON_MAP = "icons_map.json"

# 读取 logo
try:
    with open(ICON_MAP, "r", encoding="utf-8") as f:
        icons = json.load(f)
except:
    icons = {}

def get_logo(name):
    base = name.split("-")[0]
    return icons.get(base, "")

def get_tvg_id(name):
    base = name.split("-")[0].lower()

    if "cctv" in base:
        return base.replace("+", "plus")
    if "卫视" in base:
        return base.replace("卫视", "") + "hd"

    return ""

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
    f.write('#EXTM3U x-tvg-url="http://epg.112114.xyz/pp.xml"\n')

    for ch in data:
        name = ch["name"]
        url = ch["url"]
        group = ch.get("group", "")

        logo = get_logo(name)
        tvg_id = get_tvg_id(name)

        f.write(
            f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-logo="{logo}" group-title="{group}",{name}\n{url}\n'
        )

print("✅ M3U生成完成")
