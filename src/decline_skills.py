import matplotlib.pyplot as plt
import pandas as pd
import json
import re
from collections import defaultdict
from datetime import datetime

# === Load JSON data ===
with open("/content/sample_data/Posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

posts = data['posts']['row']

# === Parse dates and tags ===
tag_dates = defaultdict(list)

for post in posts:
    try:
        date = datetime.strptime(post["@CreationDate"], "%Y-%m-%dT%H:%M:%S.%f")
        tags = re.findall(r'\|([^|]+)\|', post.get("@Tags", ""))
        for tag in tags:
            tag_dates[tag].append(date)
    except:
        continue

# === Build monthly time series for each tag ===
tag_series = {}
for tag, dates in tag_dates.items():
    s = pd.Series(1, index=pd.to_datetime(dates))
    s = s.resample("M").sum().fillna(0)
    tag_series[tag] = s

# === Pairs to plot (from your correlation results) ===
skill_pairs = [
    ("productivity", "design-patterns"),
    ("productivity", "c#"),
    ("productivity", "rest"),
    ("interview", "javascript"),
    ("learning", "algorithms"),
    ("open-source", "rest"),
]

# === Plot each pair ===
for skill_a, skill_b in skill_pairs:
    if skill_a not in tag_series or skill_b not in tag_series:
        print(f"Skipping pair: {skill_a} & {skill_b} (not found in data)")
        continue

    df = pd.DataFrame({
        skill_a: tag_series[skill_a],
        skill_b: tag_series[skill_b]
    }).fillna(0)

    # Normalize for better visual comparison
    df_norm = df / df.max()

    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(df_norm.index, df_norm[skill_a], label=skill_a, linewidth=2)
    plt.plot(df_norm.index, df_norm[skill_b], label=skill_b, linewidth=2)
    plt.title(f"Competing Skill Trends: {skill_a} vs {skill_b}", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Normalized Frequency")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(f"{skill_a}_vs_{skill_b}_trend.png")
    plt.close()

print("✅ Plots generated and saved as PNG files.")
