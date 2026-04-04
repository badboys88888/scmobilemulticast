import json
import re

INPUT_FILE = "channels.txt"
OUTPUT_FILE = "channels.json"

def parse_line(line):
    line = line.strip()
    if not line or line.startswith("#genre#"):
        return None
    
    # 支持两种格式：逗号 或 |
    if "|" in line:
        parts = line.split("|")
    else:
        parts = line.split(",")

    if len(parts) < 2:
        return None

    name = parts[0].strip()
    url = parts[1].strip()

    return {
        "name": name,
        "url": url
    }

channels = []
group = ""

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if line.startswith("#genre#"):
            group = line.replace("#genre#", "").strip()
            continue

        data = parse_line(line)
        if data:
            data["group"] = group
            channels.append(data)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(channels, f, ensure_ascii=False, indent=2)

print("✅ 已生成 channels.json")
