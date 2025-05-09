import pandas as pd
from datetime import datetime

# Assuming tag_series is already constructed (monthly time series per skill)

# === Set time windows ===
recent_window = pd.date_range(start="2023-01-01", end="2023-12-31", freq="M")
older_window = pd.date_range(start="2022-01-01", end="2022-12-31", freq="M")

epi_metrics = []

for tag, series in tag_series.items():
    series = series.fillna(0)
    total_posts = series.sum()
    if total_posts == 0:
        continue

    # --- Incidence calculation ---
    incidence = series[recent_window].sum()
    old_incidence = series[older_window].sum()

    # --- Change in incidence ---
    if old_incidence > 0:
        pct_change = 100 * (incidence - old_incidence) / old_incidence
    elif incidence > 0:
        pct_change = 999  # emerging
    else:
        pct_change = 0

    # --- Freshness ratio ---
    incidence_prevalence_ratio = incidence / total_posts

    # --- Mortality (dead if no posts in last 6 months) ---
    recent_activity = series[series.index >= datetime(2023, 7, 1)].sum()
    is_dead = recent_activity == 0

    # --- Revival check ---
    revival = "Yes" if old_incidence < incidence and old_incidence > 0 else "No"

    # --- Mortality ratio ---
    mortality_ratio = incidence / (total_posts - incidence) if (total_posts - incidence) > 0 else 999

    # --- Case Fatality Rate (CFR) ---
    was_active = old_incidence > 0 or incidence > 0
    cfr = 1.0 if (was_active and is_dead) else 0.0

    # --- Attack Rate ---
    active_months = (series > 0).sum()
    total_months = len(series)
    attack_rate = active_months / total_months if total_months > 0 else 0.0

    # --- Append metrics ---
    epi_metrics.append({
        "Skill": tag,
        "Total Posts": int(total_posts),
        "Incidence (2023)": int(incidence),
        "Incidence (2022)": int(old_incidence),
        "% Change in Incidence": round(pct_change, 2),
        "Incidence : Prevalence": round(incidence_prevalence_ratio, 4),
        "Mortality Risk": "☠️" if is_dead else "🟢",
        "Revived?": revival,
        "Incidence : Mortality Ratio": round(mortality_ratio, 2),
        "CFR": round(cfr, 2),
        "Attack Rate": round(attack_rate, 4)
    })

# === Export to CSV ===
epi_df = pd.DataFrame(epi_metrics)
epi_df = epi_df.sort_values(by="Incidence (2023)", ascending=False)
epi_df.to_csv("epidemiological_skill_metrics.csv", index=False)

print("✅ Epidemiological layer (with CFR and Attack Rate) saved to 'epidemiological_skill_metrics.csv'")
