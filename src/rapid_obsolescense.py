import pandas as pd
import numpy as np

# === PARAMETERS ===
drop_threshold = 0.5        # 50% drop
drop_window = 6             # months
min_peak_value = 10         # peak usage must be at least this to be considered real
min_total_months = 24       # avoid short-lived tags

# === Detect Rapid Obsolescence ===
rapid_drops = []

for tag, series in tag_series.items():
    series = series.fillna(0)
    if series.sum() == 0:
        continue

    # Ensure series is long enough
    non_zero_months = (series > 0).sum()
    if non_zero_months < min_total_months:
        continue

    # Find peak month
    peak_value = series.max()
    if peak_value < min_peak_value:
        continue

    peak_index = series.idxmax()
    peak_loc = series.index.get_loc(peak_index)

    # Check drop in following 6 months
    end_loc = peak_loc + drop_window
    if end_loc >= len(series):
        continue

    post_peak_values = series.iloc[peak_loc:end_loc+1]
    min_val_after_peak = post_peak_values.min()

    drop_ratio = (peak_value - min_val_after_peak) / peak_value

    if drop_ratio >= drop_threshold:
        rapid_drops.append({
            "Skill": tag,
            "Peak Month": peak_index.strftime("%Y-%m"),
            "Peak Value": int(peak_value),
            "Min Value After Peak": int(min_val_after_peak),
            "Drop Window (Months)": drop_window,
            "Drop %": round(drop_ratio * 100, 2)
        })

# === Save results ===
df_rapid = pd.DataFrame(rapid_drops)
df_rapid = df_rapid.sort_values(by="Drop %", ascending=False)

df_rapid.to_csv("rapid_obsolescence_skills.csv", index=False)

print(f"✅ Found {len(df_rapid)} skills with >{int(drop_threshold*100)}% drop in {drop_window} months.")
print("📄 Results saved to: rapid_obsolescence_skills.csv")
