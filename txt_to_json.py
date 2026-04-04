import json

INPUT_FILE = "channels.txt"
OUTPUT_FILE = "channels.json"

channels = []
group = ""
name_count = {}

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        if line.startswith("#genre#"):
            group = line.replace("#genre#", "").strip()
            continue

        if "|" in line:
            parts = line.split("|")
        else:
            parts = line.split(",")

        if len(parts) < 2:
            continue

        name = parts[0].strip()
        url = parts[1].strip()

        # 自动去重
        count = name_count.get(name, 0) + 1
        name_count[name] = count

        if count > 1:
            name = f"{name}-{count}"

        channels.append({
            "name": name,
            "url": url,
            "group": group
        })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(channels, f, ensure_ascii=False, indent=2)

print("✅ JSON生成完成")
