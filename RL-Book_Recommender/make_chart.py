import matplotlib.pyplot as plt
import numpy as np
import csv
import os

csv_path = "outputs/results_log.csv"
runs, dqn, popularity, random_policy = [], [], [], []

with open(csv_path, newline="") as f:
    for row in csv.DictReader(f):
        runs.append(row["run_label"])
        dqn.append(float(row["dqn"]))
        popularity.append(float(row["popularity"]))
        random_policy.append(float(row["random"]))

x = np.arange(len(runs))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 4.5))
bars1 = ax.bar(x - width, dqn, width, label="DQN Agent", color="#4C72B0")
bars2 = ax.bar(x, popularity, width, label="Popularity Baseline", color="#DD8452")
bars3 = ax.bar(x + width, random_policy, width, label="Random Baseline", color="#C44E52")

ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("Average Reward per Recommendation")
ax.set_title("DQN Agent vs. Baseline Policies (Goodbooks-10k)")
ax.set_xticks(x)
ax.set_xticklabels(runs)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.4)

for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4 if height >= 0 else -14),
                    textcoords="offset points",
                    ha="center", fontsize=9)

plt.tight_layout()
plt.savefig("outputs/results_chart.png", dpi=200)
print("Saved outputs/results_chart.png")