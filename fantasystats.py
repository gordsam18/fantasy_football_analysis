import pandas as pd
import matplotlib.pyplot as plt 


data = pd.read_csv("2024_nfl_fantasy_football_stats.csv")
df = pd.DataFrame(data)


# 1. Which position provides the most value to a fantasy football team? 
avg_ppr_pos = df.groupby('FantPos').apply(lambda group: group.nlargest(40, 'PPR')['PPR'].mean())


# graph the top 40 fantasy player average points by position
avg_ppr_pos.plot(kind='bar')
plt.title('Average of the top 40 PPR Fantasy Points by Position')
plt.xlabel('Position')
plt.ylabel('Average of PPR Fantasy Points')



# 2. Which team scores the most fantasy points and how does it vary by position?

#group the fantasy teams by position 
team_position_points = (df.groupby(['Tm', 'FantPos'])['PPR'].sum().reset_index(name='Total_PPR'))

#Sum teams by position 
team_points = team_position_points.groupby('Tm')['Total_PPR'].sum().reset_index()
team_points = team_points.sort_values(by='Total_PPR', ascending=False)

avg_ppr_pos.head()
print("Top positions by fantasy points: ")
print(avg_ppr_pos.head())

plt.show()

print("Top teams by fantasy points: ")
print(team_points.head(32))

# 3. Which player is most efficient with fantasy point per touch? 

# Calculate touches and FPPT
df['Touches'] = df['Att'] + df['Rec']
df['FPPT'] = df['PPR'] / df['Touches']  

# Filter out players with very few touches to avoid outliers
df_filtered = df[df['Touches'] > 20]

# Find the top 10 most efficient players
top_efficient_players = df_filtered[['Player', 'FantPos', 'Tm', 'Touches', 'PPR', 'FPPT']].sort_values(by='FPPT', ascending=False).head(10)

print("Top 10 Most Efficient Players (FPPT):")
print(top_efficient_players)

# 4. Which play contributes the most total  receiving and rushing touchdowns?

# Calculate total touchdowns (rushing + receiving)
df['Total_TDs'] = df['TD']  # Assuming 'TD' includes rushing and receiving touchdowns

# Group by position and calculate the total touchdowns
position_td_totals = df.groupby('FantPos')['Total_TDs'].sum().reset_index()
position_td_totals = position_td_totals.sort_values(by='Total_TDs', ascending=False)

print("Total Touchdowns by Position:")
print(position_td_totals)

# Visualization
import matplotlib.pyplot as plt

plt.bar(position_td_totals['FantPos'], position_td_totals['Total_TDs'], color=['blue', 'green', 'orange', 'red'])
plt.title('Total Touchdowns by Fantasy Position')
plt.xlabel('Fantasy Position')
plt.ylabel('Total Touchdowns')
plt.show()

