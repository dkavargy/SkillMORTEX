import matplotlib.pyplot as plt

# List of skills to plot (from your obsolescence detection)
skills_to_plot = df_rapid["Skill"].head(20).tolist()

for skill in skills_to_plot:
    if skill not in tag_series:
        continue

    s = tag_series[skill].fillna(0)
    peak_month = s.idxmax()
    peak_value = s.max()

    # 6-month drop
    peak_loc = s.index.get_loc(peak_month)
    drop_window = 6
    end_loc = min(peak_loc + drop_window, len(s) - 1)
    drop_month = s.index[end_loc]
    drop_value = s.iloc[end_loc]

    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(s.index, s.values, label=f"{skill}", color="blue", linewidth=2)
    plt.axvline(peak_month, color="red", linestyle="--", label="Peak")
    plt.axvline(drop_month, color="orange", linestyle="--", label=f"{drop_window}-Month Point")
    plt.scatter([peak_month], [peak_value], color="red")
    plt.scatter([drop_month], [drop_value], color="orange")

    plt.title(f"Rapid Obsolescence Curve for '{skill}'", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Monthly Frequency")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"rapid_obsolescence_{skill}.png")
    plt.close()

print("✅ Plots saved for top obsolescing skills.")

# -----------------


# === Define shock window ===
shock_start = pd.Timestamp("2023-01-01")
shock_end = pd.Timestamp("2023-06-30")

# Define comparison windows
pre_start = pd.Timestamp("2022-07-01")
pre_end = pd.Timestamp("2022-12-31")

# === Build shock detection results ===
shock_results = []

for tag, series in tag_series.items():
    series = series.fillna(0)

    # Pre- and post-shock means
    pre_period = series.loc[pre_start:pre_end]
    post_period = series.loc[shock_start:shock_end]

    if len(pre_period) == 0 or len(post_period) == 0:
        continue

    pre_avg = pre_period.mean()
    post_avg = post_period.mean()

    # Avoid dividing by zero
    if pre_avg == 0 and post_avg == 0:
        continue

    change_pct = 0
    if pre_avg == 0:
        change_pct = 999  # treat as infinite growth
    else:
        change_pct = 100 * (post_avg - pre_avg) / pre_avg

    shock_results.append({
        "Skill": tag,
        "Pre-Shock Avg": round(pre_avg, 2),
        "Post-Shock Avg": round(post_avg, 2),
        "Change (%)": round(change_pct, 2)
    })

# === Create DataFrame and sort ===
shock_df = pd.DataFrame(shock_results)
shock_df = shock_df.sort_values(by="Change (%)", ascending=False)

# === Save output ===
shock_df.to_csv("external_shock_skills_2023.csv", index=False)

print("✅ External shock detection complete. Saved to 'external_shock_skills_2023.csv'")

#-----------------

import matplotlib.pyplot as plt

# === Filter for medium/high-volume skills only ===
shock_df_filtered = shock_df.copy()
shock_df_filtered["Volume Flag"] = shock_df_filtered.apply(
    lambda row: "⚠️ Low" if max(row["Pre-Shock Avg"], row["Post-Shock Avg"]) < 0.5 else "✅ OK",
    axis=1
)

# Only keep OK-volume entries
shock_df_ok = shock_df_filtered[shock_df_filtered["Volume Flag"] == "✅ OK"]
shock_df_ok = shock_df_ok.sort_values(by="Change (%)", ascending=False)

# Select top 5 most-shocked, high-volume skills
top_skills = shock_df_ok.head(5)["Skill"].tolist()

# === Plot before/after bar chart for each ===
for skill in top_skills:
    pre_avg = shock_df_ok.loc[shock_df_ok["Skill"] == skill, "Pre-Shock Avg"].values[0]
    post_avg = shock_df_ok.loc[shock_df_ok["Skill"] == skill, "Post-Shock Avg"].values[0]
    change = shock_df_ok.loc[shock_df_ok["Skill"] == skill, "Change (%)"].values[0]

    # Bar plot
    plt.figure(figsize=(6, 4))
    plt.bar(["Pre-Shock", "Post-Shock"], [pre_avg, post_avg], color=["gray", "orange"])
    plt.title(f"{skill} — {change:.1f}% Change (External Shock)", fontsize=12)
    plt.ylabel("Avg Monthly Posts")
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig(f"external_shock_{skill}.png")
    plt.close()

print("✅ External Shock plots saved for top 5 high-volume skills.")

