import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
import re

# === Load your JSON file ===
with open("/content/sample_data/Posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === Parse the posts ===
posts = data['posts']['row']

# === Extract useful info ===
tag_data = defaultdict(list)

for post in posts:
    try:
        date = datetime.strptime(post["@CreationDate"], "%Y-%m-%dT%H:%M:%S.%f")
        score = int(post.get("@Score", 0))
        views = int(post.get("@ViewCount", 0))
        answers = int(post.get("@AnswerCount", 0))
        tags = re.findall(r'\|([^|]+)\|', post.get("@Tags", ""))

        for tag in tags:
            tag_data[tag].append({
                "date": date,
                "score": score,
                "views": views,
                "answers": answers
            })
    except Exception as e:
        continue

# === Create Skill Biology Summary ===
biology_summary = []

for tag, entries in tag_data.items():
    df = pd.DataFrame(entries)
    df['year_month'] = df['date'].dt.to_period('M')

    # Date of Birth
    birth = df['date'].min()

    # Peak Date
    peak = df['year_month'].value_counts().idxmax()

    # Vital Signs
    avg_views = df['views'].mean()
    avg_score = df['score'].mean()
    avg_answers = df['answers'].mean()
    post_count = len(df)

    # Immunity Proxy (basic heuristic)
    immunity = "High" if post_count > 1000 and df['date'].max().year > 2022 else "Low"

    biology_summary.append({
        "Skill": tag,
        "Date of Birth": birth,
        "Peak Activity Date": str(peak),
        "Avg Views": round(avg_views, 2),
        "Avg Score": round(avg_score, 2),
        "Avg Answers": round(avg_answers, 2),
        "Total Posts": post_count,
        "Immunity Score": immunity
    })

# === Save to CSV ===
bio_df = pd.DataFrame(biology_summary)
bio_df.to_csv("skill_biology_summary.csv", index=False)

print("✅ Skill biology summary saved to 'skill_biology_summary.csv'")
