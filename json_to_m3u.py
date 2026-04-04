# -*- coding: utf-8 -*-

import json

INPUT_FILE = "channels.txt"
OUTPUT_FILE = "live.m3u"

# RTP代理
RTP_PROXY = "http://192.168.8.1:8888/rtp/"

# 台标配置
ICON_MAP_FILE = "icons_map.json"
ICON_BASE_URL = "https://raw.githubusercontent.com/yourrepo/logos/main/"

# ===================== 读取台标 ===================== #
try:
    with open(ICON_MAP_FILE, "r", encoding="utf-8") as f:
        icon_map = json.load(f)
except:
    icon_map = {}

# ===================== 工具函数 ===================== #
def parse_line(line):
    parts = line.strip().split("|")
    if len(parts) != 3:
        return None
    return parts[0].strip(), parts[1].strip(), parts[2].strip()


def convert_url(url):
    if url.startswith("rtp://"):
        return RTP_PROXY + url.replace("rtp://", "")
    return url


def get_logo(name, tvg_id):
    key = tvg_id if tvg_id else name

    if key in icon_map:
        return ICON_BASE_URL + icon_map[key]

    # 忽略大小写兜底
    for k in icon_map:
        if k.lower() == key.lower():
            return ICON_BASE_URL + icon_map[k]

    return ""


# ===================== 主逻辑 ===================== #
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

group = ""
output = []

# IPTV头
output.append('#EXTM3U x-tvg-url="http://epg.112114.xyz/pp.xml"\n')

for line in lines:
    line = line.strip()

    if not line:
        continue

    # ========= 分组 ========= #
    if line.startswith("#genre#"):
        group = line.replace("#genre#", "").strip()
        continue

    # ========= 频道 ========= #
    parsed = parse_line(line)
    if not parsed:
        continue

    name, url, tvg_id = parsed
    url = convert_url(url)

    logo = get_logo(name, tvg_id)

    # ========= EXTINF ========= #
    extinf = "#EXTINF:-1"

    if tvg_id:
        extinf += f' tvg-id="{tvg_id}"'

    if logo:
        extinf += f' tvg-logo="{logo}"'

    if group:
        extinf += f' group-title="{group}"'

    extinf += f",{name}"

    output.append(extinf)
    output.append(url)

# ===================== 写文件 ===================== #
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("✅ M3U生成完成 ->", OUTPUT_FILE)
