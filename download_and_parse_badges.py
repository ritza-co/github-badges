import requests
import json

URL = "https://raw.githubusercontent.com/Ileriayo/markdown-badges/master/README.md"

raw = requests.get(URL).text.split("\n")

# Find the start of the data: # Badges
i = 0
while raw[i] != "# Badges":
    i += 1
print(i)

current_category = None
current_id = 0
database = {}
while i < len(raw) - 1:
    i += 1
    line = raw[i]
    if line.startswith("### "):
        current_category = ' '.join(line.split(" ")[2:])
    if "https://img.shields.io" in line:
        elements = line.split("|")
        if len(elements) == 5:
            _, name, url, _, _ = line.split("|")
        elif len(elements) == 4:
            _, name, url, _ = line.split("|")
        name = name.strip()
        url = url.strip()
        url = url.split("](")[1][:-1]
        entry = {"name": name, "badge": url, "id": current_id, "category": current_category}
        database[name] = entry
        current_id += 1

with open("badges.json", "w") as f:
    json.dump(database, f)



        






