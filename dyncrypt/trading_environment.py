import random


DAYS_PER_EPISODE = 1
MINUTES_PER_EPISODE = 1440*DAYS_PER_EPISODE
NUM_EPISODES = 100
TRADING_FEE_MULTIPLIER = .99925 #this is the trading fee on binance VIP level 0 if using BNB to pay fees

class Env:
    def __init__(self, ratios, df):
        self.ratios = ratios
        self.main_df = df
        self.reset()
            
    def reset(self):
        self.balances = {'USD':1.0}
        for ratio in self.ratios:
            self.balances[ratio] = 0.0
        self.iloc = random.randint(0,len(self.main_df)-MINUTES_PER_EPISODE-1)
        self.episode_df = self.main_df[self.iloc:self.iloc+MINUTES_PER_EPISODE+2]
        self.money_in = 'USD'
        
        self.start_time = self.episode_df['time'].iloc[0]
        self.end_time = self.episode_df['time'].iloc[-1]
        
    def step(self):
        self.iloc+=1
        
        #-------IMPLEMENT STRATEGY HERE--------
        if self.money_in == 'USD':
            for ratio in self.ratios:
                
                #if low sma crosses above high sma
                if self.episode_df[f'{ratio}_{SMA_LOW}'][self.iloc] > self.episode_df[f'{ratio}_{SMA_HIGH}'][self.iloc] and self.episode_df[f'{ratio}_{SMA_LOW}'][self.iloc-1] > self.episode_df[f'{ratio}_{SMA_HIGH}'][self.iloc-1]:
                    self.to_buy = ratio
                    #buy that ratio (self.to_buy)
                    self.balances[self.to_buy] = (self.balances['USD']/self.episode_df[f'{self.to_buy}-USD_close'][self.iloc])*TRADING_FEE_MULTIPLIER
                    self.balances['USD'] = 0.0
                    self.buy_price = self.episode_df[f'{self.to_buy}-USD_close'][self.iloc]
                    memory.add_to_memory(f'Buy {self.to_buy}: {self.buy_price}')
                    self.money_in = self.to_buy
                    break
        
        if self.money_in != 'USD': #can't sell if money_in usd
            if self.episode_df[f'{self.money_in}_{SMA_LOW}'][self.iloc] < self.episode_df[f'{self.money_in}_{SMA_HIGH}'][self.iloc]:
                #if high sma crosses below low sma
                #sell money_in/USD
                self.balances['USD'] = (self.balances[self.money_in]*self.episode_df[f'{self.money_in}-USD_close'][self.iloc])*TRADING_FEE_MULTIPLIER
                self.balances[self.money_in] = 0.0
                self.sell_price = self.episode_df[f'{self.money_in}-USD_close'][self.iloc]
                memory.add_to_memory(f'Sell {self.money_in}: {self.sell_price}')
                self.money_in = 'USD'
        #-------IMPLEMENT STRATEGY HERE--------
        
        #-------CALCULATE PERFORMANCE METRICS HERE-------
        #Running net worth
        self.net_worth = self.balances['USD']
        for ratio in self.ratios: 
            self.net_worth += self.balances[ratio]*self.episode_df[f'{ratio}-USD_close'][self.iloc]
        
        #Net_worth had you owned all ratios over episode_df --> 'average_market_change'
        self.average_start_price = 0
        self.average_end_price = 0
        for ratio in self.ratios:
            self.average_start_price += self.episode_df[f'{ratio}-USD_close'].iloc[0]
            self.average_end_price += self.episode_df[f'{ratio}-USD_close'].iloc[-1]
        self.average_start_price /= len(ratios)
        self.average_end_price /= len(ratios)
        self.average_market_change = self.average_start_price / self.average_end_price
        #-------CALCULATE PERFORMANCE METRICS HERE-------
        
        return self.net_worth, self.average_market_change, self.start_time, self.end_time