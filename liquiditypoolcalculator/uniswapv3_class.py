import pandas as pd

class uniswapv3_class(object):
    
    def __init__(self, num_asset1, num_asset2, orig_price_denom_asset2, new_price_denom_asset2, lower_price_denom_asset2, upper_price_denom_asset2):
        
        """ Constructor for bootstrap_index class
        
        Attributes:
            num_asset1 (float) Number of asset 1 e.g. ETH
            num_asset2 (float) Number of asset 2 e.g. USDC
            orig_price_denom_asset2 (float) e.g. Current price of ETH in USDC
            new_price_denom_asset2 (float) e.g. New price of ETH in USDC
            lower_price_denom_asset2 (float) Lower bound price of ETH denominated in USDC
            upper_price_denom_asset2 (float) Lower bound price of ETH denominated in USDC             
        """               
        
        self.num_asset1 = num_asset1
        self.num_asset2 = num_asset2
        self.orig_price_denom_asset2 = orig_price_denom_asset2
        self.new_price_denom_asset2 = new_price_denom_asset2
        self.lower_price_denom_asset2 = lower_price_denom_asset2
        self.upper_price_denom_asset2 = upper_price_denom_asset2
        
    def estimate_asset_composition(self):
        
        """ Returns dictionary of param including change in liqudity pool value, hedge ratio based on expected price change, etc.    
        """          
        
        new_ref_price = self.new_price_denom_asset2
        
        if self.new_price_denom_asset2 > self.upper_price_denom_asset2:
            
            new_ref_price = self.upper_price_denom_asset2
            
        elif self.new_price_denom_asset2 < self.lower_price_denom_asset2:

            new_ref_price = self.lower_price_denom_asset2            
            
        
        L1 = (self.num_asset1 * (self.orig_price_denom_asset2**0.5) * (self.upper_price_denom_asset2**0.5)) / ((self.upper_price_denom_asset2**0.5) - (self.orig_price_denom_asset2**0.5))
        L2 = self.num_asset2 / (self.orig_price_denom_asset2**0.5 - self.lower_price_denom_asset2**0.5)
        
        L = min(L1, L2)
        
        new_num_asset1 = L * ((self.upper_price_denom_asset2**0.5) - (new_ref_price**0.5) ) / ((new_ref_price**0.5) * (self.upper_price_denom_asset2**0.5))
        new_num_asset2 = L  * ((new_ref_price**0.5) - (self.lower_price_denom_asset2**0.5))
        
        new_value_asset_in_asset2 = new_num_asset2 + new_num_asset1 * self.new_price_denom_asset2
        orig_value_asset_in_asset2 = self.num_asset2 + self.num_asset1 * self.orig_price_denom_asset2  
        
        price_change_in_asset2 = (self.new_price_denom_asset2 - self.orig_price_denom_asset2) / self.orig_price_denom_asset2
        price_change_in_lp = (new_value_asset_in_asset2 - orig_value_asset_in_asset2) / orig_value_asset_in_asset2
        
        prop_of_change = price_change_in_lp / price_change_in_asset2
        
        dict_val = {
        "new_num_asset1" : new_num_asset1,
        "new_num_asset2" : new_num_asset2,
        "orig_value_asset_in_asset2": orig_value_asset_in_asset2,
        "new_value_asset_in_asset2": new_value_asset_in_asset2,
        "price_change_in_asset2": price_change_in_asset2,
        "price_change_in_lp": price_change_in_lp,
        "hedge_ratio": prop_of_change
        }
        
        return dict_val    
    
    def sensitivity_analysis(self,dict_param):
        
        """ Dictionary of parameters based on different new prices
        
        Attributes:
            dict_param (dict) e.g.
            dict_param = {
                "lb": 1813.50,
                'sd_minus_3': 2358,
                'sd_minus_2': 2497,
                'sd_minus_1': 2636,
                'sd_plus_1': 2914,
                'sd_plus_2': 3052,       
                'sd_plus_3': 3191,       
                "ub": 3526.30        
                }            
        """          
        
        df = None
        
        for i in dict_param:

            self.new_price_denom_asset2 = dict_param[i]            
            print(dict_param[i])
            dict_res = self.estimate_asset_composition()

            if df is None:
                
                df = pd.DataFrame.from_dict(dict_res, orient='index')
                df.columns = [i + '_' + str(dict_param[i])]
                
            else:

                df_single = pd.DataFrame.from_dict(dict_res, orient='index')
                df_single.columns = [i + '_' + str(dict_param[i])]

                df = pd.concat([df, df_single], axis=1)
                
        return df
                
    
if __name__ == "__main__":   

    #Ethereum    
    num_asset1 = 6.333
    num_asset2 = 18200
    orig_price_denom_asset2 = 2801.06
    new_price_denom_asset2 = 3808.5/1.365    #2520.5861329521085
    lower_price_denom_asset2 = 2044.7
    upper_price_denom_asset2 = 3808.5   
    
    eg1 = uniswapv3_class(num_asset1, num_asset2, orig_price_denom_asset2, new_price_denom_asset2, lower_price_denom_asset2, upper_price_denom_asset2)
    eg1_val = eg1.estimate_asset_composition()
       
    volatility = 0.8/15.8
    
    # dict_param = {
    #     "lb": lower_price_denom_asset2,
    #     'sd_minus_3': orig_price_denom_asset2 * (1-3 * volatility),
    #     'sd_minus_2': orig_price_denom_asset2 * (1-2 * volatility),
    #     'sd_minus_1': orig_price_denom_asset2 * (1-1 * volatility),
    #     '99pc': orig_price_denom_asset2 * 0.99,        
    #     '101pc': orig_price_denom_asset2 * 1.01,           
    #     'sd_plus_1': orig_price_denom_asset2 * (1+1 * volatility),   
    #     'sd_plus_2': orig_price_denom_asset2 * (1+2 * volatility),     #Use as benchmark for hedging (never change)  
    #     'sd_plus_3': orig_price_denom_asset2 * (1+3 * volatility),       
    #     "ub": upper_price_denom_asset2        
    #     }
    
    dict_param = {
        'sd_minus_2': orig_price_denom_asset2 * (1-2 * volatility),
        'sd_plus_2': orig_price_denom_asset2 * (1+2 * volatility),     #Use as benchmark for hedging (never change)  
        }    
        
    eg1_simulation = eg1.sensitivity_analysis(dict_param)
    
    #Amount to unhedge
    9.339-(41978 * eg1_simulation[eg1_simulation.columns[1]][-1])/orig_price_denom_asset2  
    
    #Matic
    num_asset1 = 1514  #Matic
    num_asset2 = 7317  #USDC
    orig_price_denom_asset2 = 1.69046
    new_price_denom_asset2 = 1.7
    lower_price_denom_asset2 = 1.004
    upper_price_denom_asset2 = 2.004     
    
    eg1 = uniswapv3_class(num_asset1, num_asset2, orig_price_denom_asset2, new_price_denom_asset2, lower_price_denom_asset2, upper_price_denom_asset2)
    eg1_val = eg1.estimate_asset_composition()
    
    volatility = 0.887/15.8
    
    dict_param = {
        "lb": lower_price_denom_asset2,
        'sd_minus_3': orig_price_denom_asset2 * (1-3 * volatility),
        'sd_minus_2': orig_price_denom_asset2 * (1-2 * volatility),
        'sd_minus_1': orig_price_denom_asset2 * (1-1 * volatility),         
        'sd_plus_1': orig_price_denom_asset2 * (1+1 * volatility),
        'sd_plus_2': orig_price_denom_asset2 * (1+2 * volatility),       
        'sd_plus_3': orig_price_denom_asset2 * (1+3 * volatility),       
        "ub": upper_price_denom_asset2        
        }
        
    eg1_simulation = eg1.sensitivity_analysis(dict_param)