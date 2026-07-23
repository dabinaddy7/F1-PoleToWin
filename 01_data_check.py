#%%
import pandas as pd
races = pd.read_csv('races.csv')
results = pd.read_csv('results.csv')
qualifying = pd.read_csv('qualifying.csv')

races.describe()
races.count()
# %%
results[results['grid']==1].count()
# %%
results[(results['grid'] == 1) & (results['position_order'] == 1)].count()
# %%
pole_to_win = len(results[(results['grid'] == 1) & (results['position_order'] == 1)])
print(pole_to_win)
# %%
df = pd.merge(results, races[['race_id', 'season']], on = 'race_id', how = 'left')

df.head()
# %%
df['decade'] = (df['season'] //10) *10
df['decade'].head
# %%

pole_df = df[df['grid']==1]

pole_starts = pole_df.groupby('decade')['race_id'].count()

ptw_df = df[(df['grid'] ==1) & (df['position_order'] ==1)]

ptw_wins = ptw_df.groupby('decade')['race_id'].count()

win_rate  = (ptw_wins/pole_starts)*100
print(win_rate)
# %%
import re
def is_finished(status):
    if status == 'Finished':
        return True
    if re.match(r'^\+\d+\s+Laps?$', str(status)):
        return True
    return False

df['is_completed'] = df['status'].apply(is_finished)
print(df['is_completed'].sum())
# %%
# race_name 컬럼을 추가하여 머지
df = pd.merge(results, races[['race_id', 'season', 'race_name']], on = 'race_id', how = 'left')
win_df = df[df['position_order'] ==1]
result = win_df[['season', 'race_name', 'driver_id', 'grid']].sort_values(by='grid', ascending=False).head(5)
print(result.reset_index(drop=True))
# %%
