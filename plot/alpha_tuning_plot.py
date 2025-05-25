import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv("alpha_tuning.csv")

# Clean and preprocess
df["data"] = df["data"].ffill()

# Identify and convert execution columns
exec_cols = [col for col in df.columns if "Exec" in col]
for col in exec_cols:
    df[col] = df[col].astype(str).str.replace(",", ".").astype(float)
df["CPLEX"] = df["CPLEX"].astype(str).str.replace(",", ".").astype(float)

# Calculate mean and std for GRASP
df["GRASP_avg"] = df[exec_cols].mean(axis=1)
df["GRASP_std"] = df[exec_cols].std(axis=1)

# Calculate optimality gap
df["Optimality Gap (%)"] = ((df["CPLEX"] - df["GRASP_avg"]) / df["CPLEX"]) * 100

# Group by instance and alpha, calculate mean and std for GRASP
summary = df.groupby(["data", "alpha"]).agg(
    GRASP_avg=("GRASP_avg", "mean"),
    GRASP_std=("GRASP_std", "std"),
    CPLEX=("CPLEX", "mean")  # CPLEX is usually constant, but just in case
).reset_index()

# Plot for each instance
for instance_name, group in df.groupby("data"):
    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.set_title(f"{instance_name} - Objective Value and Optimality Gap vs Alpha")
    ax1.set_xlabel("Alpha")
    ax1.set_ylabel("Objective Value", color="blue")
    ax1.errorbar(
        group["alpha"], group["GRASP_avg"],
        yerr=group["GRASP_std"],
        marker='o', label="GRASP (avg)", color="blue", capsize=4
    )
    ax1.plot(group["alpha"], group["CPLEX"], marker='x', label="CPLEX", color="cyan")
    ax1.tick_params(axis='y', labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Optimality Gap (%)", color="red")
    ax2.plot(group["alpha"], group["Optimality Gap (%)"], marker='s', linestyle='--', color="red", label="Optimality Gap")
    ax2.tick_params(axis='y', labelcolor="red")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    fig.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    plt.tight_layout()
    plt.savefig(f"img/{instance_name}.png")
