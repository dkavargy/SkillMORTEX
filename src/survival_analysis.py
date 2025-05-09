import pandas as pd
import matplotlib.pyplot as plt
!pip install lifelines
from lifelines import KaplanMeierFitter
from datetime import datetime

# === PARAMETERS ===
cutoff_date = pd.Timestamp("2024-01-01")  # observation end
death_gap_months = 12  # months of inactivity = death

# === COMPUTE SURVIVAL DATA ===
survival_data = []

for skill, series in tag_series.items():
    series = series.sort_index()

    # Skip tags with very low activity
    if series.sum() < 100:
        continue

    # Get first and last active month
    active_months = series[series > 0]
    if active_months.empty:
        continue

    birth_date = active_months.index.min()
    last_active = active_months.index.max()
    duration = (last_active - birth_date).days // 30

    # Is the skill dead?
    months_inactive = (cutoff_date - last_active).days // 30
    is_dead = 1 if months_inactive >= death_gap_months else 0

    survival_data.append({
        "Skill": skill,
        "Duration": duration,
        "Event": is_dead
    })

# === BUILD DATAFRAME ===
surv_df = pd.DataFrame(survival_data)

# === FIT AND PLOT KAPLAN-MEIER ===
kmf = KaplanMeierFitter()
kmf.fit(durations=surv_df["Duration"], event_observed=surv_df["Event"])

plt.figure(figsize=(10, 6))
kmf.plot(ci_show=False)
plt.title("Kaplan-Meier Survival Curve for Stack Overflow Skills")
plt.xlabel("Months Since First Appearance")
plt.ylabel("Survival Probability (Skill Still Active)")
plt.grid(True)
plt.tight_layout()
plt.savefig("skill_survival_kmf.png")
plt.show()

#-----------

# === PARAMETERS ===
cutoff_date = pd.Timestamp("2024-01-01")
death_gap_months = 12

# === Find dead skills (no posts in last 12 months) ===
dead_skills = []

for tag, series in tag_series.items():
    series = series.sort_index()
    if series.sum() < 30:
        continue  # skip low-activity tags

    last_active = series[series > 0].index.max()
    months_inactive = (cutoff_date - last_active).days // 30
    if months_inactive >= death_gap_months:
        dead_skills.append(tag)

print(f"✅ Found {len(dead_skills)} dead skills.")

# === Compute Survival Data for DEAD skills only ===
survival_data = []

for skill in dead_skills:
    series = tag_series[skill].sort_index()
    active_months = series[series > 0]

    if active_months.empty:
        continue

    birth = active_months.index.min()
    last_active = active_months.index.max()
    duration = (last_active - birth).days // 30
    survival_data.append({
        'Skill': skill,
        'Duration': duration,
        'Event': 1  # All are dead
    })

# === Plot Kaplan-Meier for all DEAD skills ===
surv_df = pd.DataFrame(survival_data)

plt.figure(figsize=(12, 7))
kmf = KaplanMeierFitter()

for _, row in surv_df.head(10).iterrows():
    kmf.fit(durations=[row["Duration"]], event_observed=[row["Event"]], label=row["Skill"])
    kmf.plot_survival_function(ci_show=False)

plt.title("Kaplan-Meier Survival Curves for DEAD Skills (No Posts in Last 12 Months)")
plt.xlabel("Months From First Use")
plt.ylabel("Survival Probability")
plt.grid(True)
plt.tight_layout()
plt.savefig("dead_skills_kmf.png")
plt.show()


#-----------

import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, NelsonAalenFitter
from datetime import datetime

# === PARAMETERS ===
cutoff_date = pd.Timestamp("2024-01-01")  # observation end
death_gap_months = 12  # months of inactivity = death

# === COMPUTE SURVIVAL DATA ===
survival_data = []

for skill, series in tag_series.items():
    series = series.sort_index()

    # Skip tags with very low activity
    if series.sum() < 100:
        continue

    active_months = series[series > 0]
    if active_months.empty:
        continue

    birth_date = active_months.index.min()
    last_active = active_months.index.max()
    duration = (last_active - birth_date).days // 30

    months_inactive = (cutoff_date - last_active).days // 30
    is_dead = 1 if months_inactive >= death_gap_months else 0

    survival_data.append({
        "Skill": skill,
        "Duration": duration,
        "Event": is_dead
    })

# === BUILD DATAFRAME ===
surv_df = pd.DataFrame(survival_data)

# === FIT ESTIMATORS ===
kmf = KaplanMeierFitter()
naf = NelsonAalenFitter()

kmf.fit(surv_df["Duration"], event_observed=surv_df["Event"])
naf.fit(surv_df["Duration"], event_observed=surv_df["Event"])

# === PLOT ===
plt.figure(figsize=(10, 6))

# Survival Curve
kmf.plot_survival_function(label="Kaplan-Meier Survival", ci_show=True)

# Hazard Curve
naf.plot_cumulative_hazard(label="Nelson-Aalen Hazard", ci_show=True)

plt.title("Stack Overflow Skills: Survival vs Hazard")
plt.xlabel("Months Since First Appearance")
plt.ylabel("Survival Probability / Cumulative Hazard")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("skill_survival_vs_hazard.png")
plt.show()
