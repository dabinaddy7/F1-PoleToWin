# %%
import os

import fastf1

# 1. 캐시 폴더 경로 지정
cache_dir = "../f1_cache"

# 2. 폴더가 없으면 직접 생성
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# 3. 캐시 활성화
fastf1.Cache.enable_cache(cache_dir)
# %%
import fastf1

fastf1.Cache.enable_cache("../f1_cache")

session = fastf1.get_session(2023, "Hungary", "R")
session.load(telemetry=False)

laps_df = session.laps

print("--- Data Check ---")
print(f"데이터 타입: {type(laps_df)}")
print(f"전체 컬럼 목록:\n{laps_df.columns.to_list()}\n")


# %%
ver_laps = laps_df[laps_df["Driver"] == "VER"]
ver_laps.head()
# %%
fastest_lap = ver_laps.sort_values("LapTime").iloc[0]
# %%
print(fastest_lap["Compound"])
print(fastest_lap["LapTime"])
# %%
import pandas as pd


# ANSI 색상 코드 정의
class Colors:
    PURPLE = "\033[95m\033[1m"  # Session Best
    GREEN = "\033[92m\033[1m"  # Personal Best
    YELLOW = "\033[93m\033[1m"  # Slower
    GRAY = "\033[90m"  # In Progress / Sector 3 미통과
    RESET = "\033[0m"
    BOLD = "\033[1m"


def render_broadcast_graphic(driver, lap_num, laps_df):
    clean_laps = laps_df.dropna(subset=["Sector1Time", "Sector2Time", "Sector3Time"])

    # 1. 세션 / 개인 최속 구하기
    s1_purple = clean_laps["Sector1Time"].min()
    s2_purple = clean_laps["Sector2Time"].min()
    s3_purple = clean_laps["Sector3Time"].min()

    driver_laps = clean_laps[clean_laps["Driver"] == driver]
    s1_green = driver_laps["Sector1Time"].min()
    s2_green = driver_laps["Sector2Time"].min()
    s3_green = driver_laps["Sector3Time"].min()

    # 타겟 랩 추출
    target_lap = laps_df[
        (laps_df["Driver"] == driver) & (laps_df["LapNumber"] == lap_num)
    ]
    if target_lap.empty:
        print("해당 랩 데이터를 찾을 수 없습니다.")
        return

    lap = target_lap.iloc[0]

    # 2. 섹터별 색상 지정 함수
    def get_color_info(time_val, green_val, purple_val):
        if pd.isna(time_val):
            return Colors.GRAY, "Gray"
        if time_val == purple_val:
            return Colors.PURPLE, "Purple"
        elif time_val == green_val:
            return Colors.GREEN, "Green"
        else:
            return Colors.YELLOW, "Yellow"

    c1, _ = get_color_info(lap["Sector1Time"], s1_green, s1_purple)
    c2, _ = get_color_info(lap["Sector2Time"], s2_green, s2_purple)
    c3, _ = get_color_info(lap["Sector3Time"], s3_green, s3_purple)

    # 랩 타임 포맷팅 (예: 1:17.725)
    lap_time_str = "---"
    if not pd.isna(lap["LapTime"]):
        total_sec = lap["LapTime"].total_seconds()
        minutes = int(total_sec // 60)
        seconds = total_sec % 60
        lap_time_str = f"{minutes}:{seconds:06.3f}"

    # 3. 중계 UI 그리드 출력
    print("\n" + "=" * 45)
    print(
        f" {Colors.BOLD}{lap['Position'] if 'Position' in lap else 1} | {driver}{Colors.RESET}   Compound: {lap['Compound']}"
    )
    print(f" {Colors.BOLD}{lap_time_str:>15}{Colors.RESET}")
    print("-" * 45)

    # 하단 섹터 컬러 바 (S1, S2, S3 막대그래프 형태)
    s1_bar = f"{c1}  S1  ██████████{Colors.RESET}"
    s2_bar = f"{c2}  S2  ██████████{Colors.RESET}"
    s3_bar = f"{c3}  S3  ██████████{Colors.RESET}"

    print(f"{s1_bar} {s2_bar} {s3_bar}")
    print("=" * 45 + "\n")


# 실행 예시 (VER의 5번째 랩 출력)
render_broadcast_graphic("VER", 17, laps_df)
# %%
import numpy as np

clean_race_laps = laps_df[
    (laps_df["TrackStatus"] == "1")
    & (laps_df["PitOutTime"].isna())
    & (laps_df["PitInTime"].isna())
].copy()

clean_race_laps["LapTimeSeconds"] = clean_race_laps["LapTime"].dt.total_seconds()


def filter_normal_pace(group):
    median_time = group["LapTimeSeconds"].median()
    return group[group["LapTimeSeconds"] <= median_time * 1.07]


valid_laps = clean_race_laps.groupby(
    ["Driver", "Compound", "Stint"], group_keys=False
).apply(filter_normal_pace)


def get_deg_rate(df):
    df_clean = df.dropna(subset=["LapTimeSeconds"])
    if len(df_clean) < 3:
        return pd.Series({"Deg_Rate_Sec": np.nan, "Lap_Count": len(df_clean)})

    slope, _ = np.polyfit(df_clean["TyreLife"], df_clean["LapTimeSeconds"], 1)
    return pd.Series({"Deg_Rate_Sec": slope, "Lap_Count": len(df_clean)})


deg_analysis = (
    valid_laps.groupby(["Driver", "Compound", "Stint"])
    .apply(get_deg_rate)
    .reset_index()
)

print("=== Tire Degradation Analysis (Sec / Lap)===")
print(deg_analysis.sort_values("Lap_Count", ascending=False).to_string(index=False))
# %%
print(len(laps_df))
print(len(clean_race_laps))
# %%
# 1. 107% 필터링까지 마친 데이터의 총 개수 및 상위 행 확인
print("valid_laps 총 개수:", len(valid_laps))
print(
    valid_laps[["Driver", "Compound", "Stint", "TyreLife", "LapTimeSeconds"]].head(10)
)

# 2. 그룹별 랩 수가 몇 개씩 할당되었는지 확인
print(valid_laps.groupby(["Driver", "Compound", "Stint"]).size())
# %%
import matplotlib.pyplot as plt

hard_deg = deg_analysis[
    (deg_analysis["Compound"] == "HARD") & (deg_analysis["Lap_Count"] > 15)
].sort_values("Deg_Rate_Sec", ascending=True)

top3_drivers = hard_deg.head(3)

plt.figure(figsize=(12, 6))

colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

for idx, (_, row) in enumerate(top3_drivers.iterrows()):
    driver = row["Driver"]
    stint = row["Stint"]
    deg = row["Deg_Rate_Sec"]

    driver_laps = valid_laps[
        (valid_laps["Driver"] == driver) & (valid_laps["Stint"] == stint)
    ].sort_values("TyreLife")

    plt.scatter(
        driver_laps["TyreLife"],
        driver_laps["LapTimeSeconds"],
        label=f"{driver} (Stint {int(stint)}) : {deg:.4f}s/lap",
        color=colors[idx],
        alpha=0.5,
        s=30,
    )
    m, b = np.polyfit(driver_laps["TyreLife"], driver_laps["LapTimeSeconds"], 1)
    x_range = np.array([driver_laps["TyreLife"].min(), driver_laps["TyreLife"].max()])

    plt.plot(x_range, m * x_range + b, color=colors[idx], linewidth=2.5, linestyle="--")


# 4. 그래프 스타일링
plt.title("Top 3 Tire Managers - HARD Compound Degradation Curve", fontsize=14, pad=15)
plt.xlabel("Tyre Life (Laps)", fontsize=12)
plt.ylabel("Lap Time (Seconds)", fontsize=12)
plt.legend(title="Driver & Deg Rate", fontsize=10, loc="upper left")
plt.grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()
plt.show()
# %%
print(top3_drivers)
# %%
