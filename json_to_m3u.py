# -*- coding: utf-8 -*-

import json
import re

INPUT_FILE = "channels.txt"
OUTPUT_FILE = "live.m3u"

RTP_PROXY = "http://192.168.8.1:8888/rtp/"

ICON_MAP_FILE = "icons_map.json"
ICON_BASE_URL = "https://raw.githubusercontent.com/badboys88888/scmobilemulticast/main/icons/"

# ===================== 读取台标 ===================== #
try:
    with open(ICON_MAP_FILE, "r", encoding="utf-8") as f:
        icon_map = json.load(f)
except:
    icon_map = {}

# ===================== 归一化（核心修复） ===================== #
def norm_name(name):
    # 去掉 -1 -2 -HD -备用 -数字后缀
    name = re.sub(r'[-_ ]?\d+$', '', name)
    return name.strip()

# ===================== 解析 ===================== #
def parse_line(line):
    parts = line.strip().split("|")
    if len(parts) != 3:
        return None
    return parts[0].strip(), parts[1].strip(), parts[2].strip()

# ===================== URL转换 ===================== #
def convert_url(url):
    if url.startswith("rtp://"):
        return RTP_PROXY + url.replace("rtp://", "")
    return url

# ===================== LOGO匹配 ===================== #
def get_logo(name, tvg_id):
    key = norm_name(name)

    # 1️⃣ 精确匹配
    if key in icon_map:
        return ICON_BASE_URL + icon_map[key]

    # 2️⃣ tvg_id匹配
    if tvg_id and tvg_id in icon_map:
        return ICON_BASE_URL + icon_map[tvg_id]

    # 3️⃣ 忽略大小写匹配
    for k in icon_map:
        if k.lower() == key.lower():
            return ICON_BASE_URL + icon_map[k]

    return ""

# ===================== 主逻辑 ===================== #
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

group = ""
output = []

# 🔥 标准EPG写法（建议保留）
output.append('#EXTM3U x-tvg-url="http://epg.51zmt.top:8000/e.xml"')

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

    # ========= 清洗名称 ========= #
    clean_name = norm_name(name)

    # ========= EXTINF ========= #
    extinf = "#EXTINF:-1"

    if tvg_id:
        extinf += f' tvg-id="{tvg_id}"'

    # 🔥 新增：tvg-name（标准关键）
    extinf += f' tvg-name="{clean_name}"'

    if logo:
        extinf += f' tvg-logo="{logo}"'

    if group:
        extinf += f' group-title="{group}"'

    # 显示名（保留原始，带-1 -2）
    extinf += f",{name}"

    output.append(extinf)
    output.append(url)

# ===================== 写文件 ===================== #
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("✅ M3U生成完成 ->", OUTPUT_FILE)
