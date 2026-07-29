# %%
import pandas as pd

start = pd.read_csv("../data/pitstop/starting_grids.csv")
result = pd.read_csv("../data/pitstop/race_details.csv")

start.head()

# %%
result.head()
# %%
start["Grid_Pos"] = pd.to_numeric(start["Pos"], errors="coerce")
result["Race_Pos"] = pd.to_numeric(result["Pos"], errors="coerce")

start["Grid_Pos"].info()
# %%
result["Race_Pos"].info()
# %%
start = start[start["Year"] >= 2014]
start.head()
# %%
result = result[result["Year"] >= 2014]
result.head()

# %%
start = start[["Year", "Grand Prix", "DriverCode", "Driver", "Car", "Grid_Pos"]]
result = result[["Year", "Grand Prix", "DriverCode", "Race_Pos"]]

# %%
start_and_result = pd.merge(
    start, result, on=["Year", "Grand Prix", "DriverCode"], how="inner"
)
start_and_result.head()

# %%
start_and_result = start_and_result.dropna(subset=["Race_Pos"])
# %%
start_and_result["changes"] = (
    start_and_result["Grid_Pos"] - start_and_result["Race_Pos"]
)
start_and_result.head(10)
# %%

avg_result_changes = start_and_result.groupby(["DriverCode", "Driver"])["changes"].agg(
    ["mean", "count"]
)

# %%
avg_result_changes = avg_result_changes[avg_result_changes["count"] >= 20]
avg_result_changes.sort_values(by="mean", ascending=False).head(10)

# %%
team_result_changes = start_and_result.groupby(["Car"])["changes"].agg(
    ["mean", "count"]
)
team_result_changes = team_result_changes[team_result_changes["count"] >= 20]
team_result_changes.sort_values(by="mean", ascending=False).head(10)

# %%
import matplotlib.pyplot as plt
import seaborn as sns

# 팀별 평균 순위 상승 상위 10개 시각화
top10_cars = (
    team_result_changes.sort_values(by="mean", ascending=False).head(10).reset_index()
)

plt.figure(figsize=(10, 6))
sns.barplot(data=top10_cars, x="mean", y="Car", palette="viridis")
plt.title("Top 10 F1 Teams by Avg Position Change (2014-Present)", fontsize=14)
plt.xlabel("Avg Position Change (Grid vs Race)", fontsize=12)
plt.ylabel("Team (Car)", fontsize=12)
plt.tight_layout()
plt.show()
# %%
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.barplot(data=avg_result_changes, x="mean", y="Driver", palette="viridis")
plt.title("Top 10 F1 Drivers by Avg Position Change (2014-Present)", fontsize=14)
plt.xlabel("Avg Position Change (Grid vs Race)", fontsize=12)
plt.ylabel("Driver", fontsize=12)
plt.tight_layout()
