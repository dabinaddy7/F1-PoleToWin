#%%
import pandas as pd

pitstops = pd.read_csv('../data/pitstop/pitstops.csv')
driver_standings = pd.read_csv('../data/pitstop/driver_standings.csv')

print(pitstops.head(3))
print(pitstops.columns.tolist())

print(driver_standings.head(3))
print(driver_standings.columns.tolist())
# %%
# 2. 개별 피트스탑 시간(Time)을 수치형(초) 데이터로 변환 (누적시간 Total은 사용 X)
pitstops['Time_sec'] = pd.to_numeric(pitstops['Time'], errors='coerce')

# 3. 80km/h 피트레인 제한 규정 적용 시작년도인 2014년 이후 데이터 필터링
df_modern = pitstops[pitstops['Year'] >= 2014].copy()

# 4. (연도, 서킷)별 개별 스탑 중앙값 계산 및 지연 시간(pit_delta) 산출
race_medians = df_modern.groupby(['Year', 'Grand Prix'])['Time_sec'].transform('median')
df_modern['pit_delta'] = df_modern['Time_sec'] - race_medians

# 5. 이상치 제거 (해당 경기 평균 대비 +5초 초과 지연된 피트스탑 제외)
#    -> 장비 고장, 날개 교체, 패널티 수행 등의 이상치 스탑 필터링
df_valid = df_modern[df_modern['pit_delta'] <= 5.0].copy()

# 6. 팀(Car)별 그룹화하여 평균 피트스탑 시간 및 횟수 집계
team_pit_summary = df_valid.groupby('Car')['Time_sec'].agg(
    평균_피트스탑_시간='mean',
    총_피트스탑_횟수='count'
).reset_index()

# 7. 평균 피트스탑 시간 기준 내림차순 정렬 (느린 팀 -> 빠른 팀 순)
team_pit_summary = team_pit_summary.sort_values(by='평균_피트스탑_시간', ascending=True)

# 8. 소수점 3자리까지 정리 및 결과 출력
team_pit_summary['평균_피트스탑_시간'] = team_pit_summary['평균_피트스탑_시간'].round(3)

print("=== 2014년 이후 팀별 평균 피트스탑 시간 (오름차순) ===")
print(team_pit_summary.to_string(index=False))

# %%
# 1. 수치형 변환 & 2014년 이후 데이터 필터링
pitstops['Time_sec'] = pd.to_numeric(pitstops['Time'], errors='coerce')
df_modern = pitstops[pitstops['Year'] >= 2014].copy()

# 2. 서킷별 중앙값 기준 이상치(+5초 지연) 제거
race_medians = df_modern.groupby(['Year', 'Grand Prix'])['Time_sec'].transform('median')
df_modern['pit_delta'] = df_modern['Time_sec'] - race_medians
df_valid = df_modern[df_modern['pit_delta'] <= 5.0].copy()

# 3. 전체 F1 팀 계보 및 엔진 공급사 변경 통합 맵핑 딕셔너리
team_mapping_full = {
    # Red Bull Racing (엔진 변경: Renault -> TAG Heuer -> Honda -> RBPT)
    'Red Bull Racing Renault': 'Red Bull Racing',
    'Red Bull Racing TAG Heuer': 'Red Bull Racing',
    'Red Bull Racing Honda': 'Red Bull Racing',
    'Red Bull Racing RBPT': 'Red Bull Racing',

    # McLaren (엔진 변경: Mercedes -> Honda -> Renault)
    'McLaren Mercedes': 'McLaren',
    'McLaren Honda': 'McLaren',
    'McLaren Renault': 'McLaren',

    # Aston Martin 계보 (실버스톤 공장 팀)
    'Force India Mercedes': 'Aston Martin Group',
    'Racing Point BWT Mercedes': 'Aston Martin Group',
    'Aston Martin Mercedes': 'Aston Martin Group',
    'Aston Martin Aramco Mercedes': 'Aston Martin Group',

    # Alpine 계보 (엔스톤 공장 팀)
    'Lotus Mercedes': 'Alpine Group',
    'Lotus Renault': 'Alpine Group',
    'Renault': 'Alpine Group',
    'Alpine Renault': 'Alpine Group',

    # RB / AlphaTauri / Toro Rosso 계보 (파엔차 공장 팀)
    'STR Renault': 'RB Group',
    'Toro Rosso-Ferrari': 'RB Group',
    'Toro Rosso Ferrari': 'RB Group',
    'Toro Rosso': 'RB Group',
    'Scuderia Toro Rosso Honda': 'RB Group',
    'AlphaTauri Honda': 'RB Group',
    'AlphaTauri RBPT': 'RB Group',

    # Sauber 계보 (힌빌 공장 팀)
    'Sauber Ferrari': 'Sauber Group',
    'Alfa Romeo Racing Ferrari': 'Sauber Group',
    'Alfa Romeo Ferrari': 'Sauber Group',

    # Manor / Marussia 계보
    'Marussia Ferrari': 'Manor/Marussia',
    'MRT-Mercedes': 'Manor/Marussia',
    'MRT Mercedes': 'Manor/Marussia',

    # 단일/대표 팀
    'Mercedes': 'Mercedes',
    'Ferrari': 'Ferrari',
    'Williams Mercedes': 'Williams',
    'Haas Ferrari': 'Haas',
    'Caterham Renault': 'Caterham'
}

# 4. 모체 팀(Parent_Team) 컬럼 생성
df_valid['Parent_Team'] = df_valid['Car'].map(team_mapping_full).fillna(df_valid['Car'])

# 5. Parent_Team 기준 집계 (평균 시간 및 총 스탑 횟수)
team_group_summary = df_valid.groupby('Parent_Team')['Time_sec'].agg(
    평균_피트스탑_시간='mean',
    총_피트스탑_횟수='count'
).reset_index()

# 6. 소수점 정리 및 오름차순 정렬 (가장 빠른 팀이 맨 위로!)
team_group_summary['평균_피트스탑_시간'] = team_group_summary['평균_피트스탑_시간'].round(3)
team_group_summary = team_group_summary.sort_values(by='평균_피트스탑_시간', ascending=True)

print("=== [2014년 이후] F1 통합 팀별 평균 피트스탑 시간 (오름차순: 빠른 순) ===")
print(team_group_summary.to_string(index=False))
# %%
