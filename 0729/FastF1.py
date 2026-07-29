# %%
%pip install fastf1 matplotlib pandas
#%%
import os
import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt

os.makedirs('f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('f1_cache') 

# FastF1 그래프 스타일 및 캐시 설정 (캐시 디렉토리를 생성하면 데이터 로딩이 빨라집니다)
fastf1.plotting.setup_mpl(misc_mpl_mods=False)
fastf1.Cache.enable_cache('f1_cache') 

# 1. 경기 세션 데이터 로드 (2023년 라운드 1 바레인 GP 예선 'Q')
session = fastf1.get_session(2023, 1, 'Q')
session.load()

# 2. 두 드라이버의 가장 빠른 랩 추출
ver_lap = session.laps.pick_driver('VER').pick_fastest()
lec_lap = session.laps.pick_driver('LEC').pick_fastest()

# 3. 각 드라이버의 텔레메트리(속도, 브레이크, 스티어링 등 초단위 센서 데이터) 가져오기
ver_tel = ver_lap.get_telemetry()
lec_tel = lec_lap.get_telemetry()

# 4. 엔지니어링 차트 그리기 (속도 & 브레이크 비교)
fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

# (1) 속도 비교 (Speed Trace)
ax[0].plot(ver_tel['Distance'], ver_tel['Speed'], color='blue', label='VER (Red Bull)')
ax[0].plot(lec_tel['Distance'], lec_tel['Speed'], color='red', label='LEC (Ferrari)')
ax[0].set_ylabel('Speed (km/h)')
ax[0].set_title('Telemetry Comparison: VER vs LEC (2023 Bahrain GP Q3)')
ax[0].legend()
ax[0].grid(True, linestyle='--', alpha=0.6)

# (2) 브레이크 온/오프 비교 (Brake Pressure Trace)
ax[1].plot(ver_tel['Distance'], ver_tel['Brake'], color='blue', label='VER')
ax[1].plot(lec_tel['Distance'], lec_tel['Brake'], color='red', label='LEC')
ax[1].set_xlabel('Distance on Track (m)')
ax[1].set_ylabel('Brake (On/Off)')
ax[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

# %%
fastf1.plotting.setup_mpl()

session = fastf1.get_session(2026,'Hungary', 'R')
session.load()

ver_lap = session.laps.pick_driver('VER').pick_fastest()
ham_lap = session.laps.pick_driver('HAM').pick_fastest()

ver_tel = ver_lap.get_telemetry().add_distance()
ham_tel = ham_lap.get_telemetry().add_distance()

ver_tel['Distance'] = ver_tel['Distance'] - ver_tel['Distance'].iloc[0]
ham_tel['Distance'] = ham_tel['Distance'] - ham_tel['Distance'].iloc[0]

fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

ax[0].plot(ver_tel['Distance'], ver_tel['Speed'], color='blue', label='VER')
ax[0].plot(ham_tel['Distance'], ham_tel['Speed'], color='red', label='HAM')
ax[0].set_ylabel('Speed (km/h)')
ax[0].set_title('Telemetry Comparison: VER vs HAM (2026 Hungary GP R)')
ax[0].legend()
ax[0].grid(True, linestyle='--', alpha=0.6)

ax[1].plot(ver_tel['Distance'], ver_tel['Throttle'], color='blue', label='VER')
ax[1].plot(ham_tel['Distance'], ham_tel['Throttle'], color='red', label='HAM')
ax[1].set_xlabel('Distance on Track (m)')
ax[1].set_ylabel('Throttle (%)')
ax[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

# %%
fastf1.plotting.setup_mpl()

session = fastf1.get_session(2025,'Hungary', 'R')
session.load()

ver_lap = session.laps.pick_driver('VER').pick_fastest()
ant_lap = session.laps.pick_driver('ANT').pick_fastest()

ver_tel = ver_lap.get_telemetry().add_distance()
ant_tel = ant_lap.get_telemetry().add_distance()

fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

ax[0].plot(ver_tel['Distance'], ver_tel['Speed'], color='blue', label='VER')
ax[0].plot(ant_tel['Distance'], ant_tel['Speed'], color='red', label='ANT')
ax[0].set_ylabel('Speed (km/h)')
ax[0].set_title('Telemetry Comparison: VER vs ANT (2025 Hungary GP R)')
ax[0].legend()
ax[0].grid(True, linestyle='--', alpha=0.6)

ax[1].plot(ver_tel['Distance'], ver_tel['Throttle'], color='blue', label='VER')
ax[1].plot(ant_tel['Distance'], ant_tel['Throttle'], color='red', label='ANT')
ax[1].set_xlabel('Distance on Track (m)')
ax[1].set_ylabel('Throttle (%)')
ax[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()