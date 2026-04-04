import json

INPUT_JSON = "channels.json"
OUTPUT_M3U = "output.m3u"
ICON_MAP = "icons_map.json"

# 读取 logo 映射
try:
    with open(ICON_MAP, "r", encoding="utf-8") as f:
        icons = json.load(f)
except:
    icons = {}

def get_logo(name):
    return icons.get(name, "")

def get_tvg_id(name):
    name = name.lower()

    if "cctv" in name:
        return name.replace("+", "plus").replace("-", "").lower()
    if "卫视" in name:
        return name.replace("卫视", "").lower() + "hd"

    return ""

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    for ch in data:
        name = ch["name"]
        url = ch["url"]
        group = ch.get("group", "")
        logo = get_logo(name)
        tvg_id = get_tvg_id(name)

        line = f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-logo="{logo}" group-title="{group}",{name}\n{url}\n'
        f.write(line)

print("✅ 已生成 output.m3u")
