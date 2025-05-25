import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV
df = pd.read_csv("main_results.csv")

# Preprocess numbers: convert comma to dot for decimals
df["Elapsed time (sec)"] = df["Elapsed time (sec)"].str.replace(",", ".").astype(float)
df["Objective Value"] = pd.to_numeric(df["Objective Value"], errors="coerce")

# Group by N and Algorithm, average over both instances
summary = df.groupby(["N", "Algorithm"]).agg({
    "Objective Value": ["mean", "std"],
    "Elapsed time (sec)": ["mean", "std"]
}).reset_index()

# Pivot for plotting
pivot_obj_mean = summary.pivot(index="N", columns="Algorithm", values=("Objective Value", "mean"))
pivot_obj_std = summary.pivot(index="N", columns="Algorithm", values=("Objective Value", "std"))
pivot_time_mean = summary.pivot(index="N", columns="Algorithm", values=("Elapsed time (sec)", "mean"))
pivot_time_std = summary.pivot(index="N", columns="Algorithm", values=("Elapsed time (sec)", "std"))

# Define consistent colors for each algorithm
color_map = {
    "Greedy": "blue",        # blue
    "Greedy + LS": "green",   # green
    "GRASP": "orange",         # orange
    "GRASP + LS": "red",    # red
    "CPLEX": "purple"          # purple
}


# ----- PLOT 1: Objective Value vs N -----
plt.figure(figsize=(8, 5))
for algo in pivot_obj_mean.columns:
    plt.errorbar(
        pivot_obj_mean.index, pivot_obj_mean[algo],
        yerr=pivot_obj_std[algo],
        marker='o',
        label=algo,
        color=color_map.get(algo, None),
        capsize=4
    )
plt.title("Average Objective Value vs N (with Variance)")
plt.xlabel("N")
plt.ylabel("Objective Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("img/objective_value_vs_n.png")

# ----- PLOT 2: Elapsed Time vs N (with CPLEX) -----
plt.figure(figsize=(8, 5))
for algo in pivot_time_mean.columns:
    plt.errorbar(
        pivot_time_mean.index, pivot_time_mean[algo],
        yerr=pivot_time_std[algo],
        marker='o',
        label=algo,
        color=color_map.get(algo, None),
        capsize=4
    )
plt.title("Average Elapsed Time vs N (with CPLEX)")
plt.xlabel("N")
plt.ylabel("Elapsed Time (sec)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("img/elapsed_time_vs_n_with_cplex.png")

# ----- PLOT 3: Elapsed Time vs N (without CPLEX) -----
pivot_time_no_cplex = pivot_time_mean.drop(columns=["CPLEX"], errors="ignore")

plt.figure(figsize=(8, 5))
for algo in pivot_time_no_cplex.columns:
    plt.errorbar(
        pivot_time_no_cplex.index, pivot_time_no_cplex[algo],
        yerr=pivot_time_std[algo],
        marker='o',
        label=algo,
        color=color_map.get(algo, None),
        capsize=4
    )
plt.title("Average Elapsed Time vs N (excluding CPLEX)")
plt.xlabel("N")
plt.ylabel("Elapsed Time (sec)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("img/elapsed_time_vs_n_without_cplex.png")


# ----- PLOT 4: Optimality Gap vs N (excluding CPLEX) -----
# Compute optimality gap for each algorithm (except CPLEX)
gap_df = pivot_obj_mean.copy()
for algo in gap_df.columns:
    if algo != "CPLEX":
        gap_df[algo] = ((pivot_obj_mean["CPLEX"] - pivot_obj_mean[algo]) / pivot_obj_mean["CPLEX"]) * 100
gap_df = gap_df.drop(columns=["CPLEX"], errors="ignore")

plt.figure(figsize=(8, 5))
for algo in gap_df.columns:
    plt.plot(
        gap_df.index, gap_df[algo],
        marker='o',
        label=algo,
        color=color_map.get(algo, None)
    )
plt.title("Optimality Gap vs N (excluding CPLEX)")
plt.xlabel("N")
plt.ylabel("Optimality Gap (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("img/optimality_gap_vs_n.png")