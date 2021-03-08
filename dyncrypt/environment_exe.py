from readdata_binance import *
from trading_environment import *

df = pd.read_csv('12-coins-Jan21_Jan21')

env = Env(ratios, df)
memory = Memory()

net_worth_collect = []
average_market_change_collect = []

for i_episode in range(NUM_EPISODES):
    for i in range(len(env.episode_df)-1):
        net_worth, average_market_change, start_time, end_time = env.step()
    
    net_worth_collect.append(net_worth)
    average_market_change_collect.append(average_market_change)
    
    #log after each episode
    print(f'episode: {i_episode}')
    print(memory.actions)
    print('\n')
    print(f'interval: {start_time} - {end_time}')
    print(f'net worth after {DAYS_PER_EPISODE} day(s): {net_worth}')
    print(f'average market change: {average_market_change}')
    print('\n')

    memory.clear()
    env.reset()

#log overall
print(f'net worth average after {NUM_EPISODES} backtest episodes: {np.mean(net_worth_collect)}')
#Yes, average of the average market changes
print(f'average, average market change over {NUM_EPISODES} episodes: {np.mean(average_market_change_collect)}')