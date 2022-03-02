import pandas as pd

class uniswapv2_class(object):
    
    def __init__(self, lp_asset1, lp_asset2, share_in_lp, orig_price_denom_asset2, new_price_denom_asset2):
        
        self.lp_asset1 = lp_asset1
        self.lp_asset2 = lp_asset2
        self.share_in_lp = share_in_lp
        self.orig_price_denom_asset2 = orig_price_denom_asset2
        self.new_price_denom_asset2 = new_price_denom_asset2
        self.constant = self.lp_asset1 * self.lp_asset2   #Each trade increases k by 0.03% of trade value. Yield value tied to k
        self.new_lp_asset1 = None
        self.new_lp_asset2 = None
        

    def estimate_asset_composition(self):
        
        self.new_lp_asset1= (self.constant / self.new_price_denom_asset2) ** 0.5
        self.new_lp_asset2= (self.constant * self.new_price_denom_asset2) ** 0.5
        
        orig_value_asset_in_asset2 = self.lp_asset1 * orig_price_denom_asset2 + self.lp_asset2
        new_value_asset_in_asset2 = self.new_lp_asset1 * new_price_denom_asset2 + self.new_lp_asset2
        
        price_change_in_asset2 = (self.new_price_denom_asset2 - self.orig_price_denom_asset2) / self.orig_price_denom_asset2
        price_change_in_lp = (new_value_asset_in_asset2 - orig_value_asset_in_asset2) / orig_value_asset_in_asset2
        
        prop_of_change = price_change_in_lp / price_change_in_asset2

        dict_val = {
        "new_num_asset1" : self.new_lp_asset1,
        "new_num_asset2" : self.new_lp_asset2,
        "orig_value_asset_in_asset2": orig_value_asset_in_asset2,
        "new_value_asset_in_asset2": new_value_asset_in_asset2,
        "price_change_in_asset2": price_change_in_asset2,
        "price_change_in_lp": price_change_in_lp,
        "hedge_ratio": prop_of_change
        }
        
        return dict_val         
    
    #Some bug rendering weird results for now
    def sensitivity_analysis(self,dict_param):
        
        """ Dictionary of parameters based on different new prices
        
        Attributes:
            dict_param (dict) e.g.
            volatility = 0.8/15.8            
            dict_param = {
                'sd_minus_3': orig_price_denom_asset2 * (1-3 * volatility),
                'sd_minus_2': orig_price_denom_asset2 * (1-2 * volatility),
                'sd_minus_1': orig_price_denom_asset2 * (1-1 * volatility),
                'sd_minus_0_5': orig_price_denom_asset2 * (1-0.5 * volatility),               
                'sd_plus_0_5': orig_price_denom_asset2 * (1+0.5 * volatility),                
                'sd_plus_1': orig_price_denom_asset2 * (1+1 * volatility),
                'sd_plus_2': orig_price_denom_asset2 * (1+2 * volatility),       
                'sd_plus_3': orig_price_denom_asset2 * (1+3 * volatility),       
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

    #https://www.theancientbabylonians.com/what-is-liquidity-pool-lp-in-defi/
    #https://docs.uniswap.org/protocol/V2/concepts/protocol-overview/how-uniswap-works
    #Eth   
    lp_asset1 = 8295
    lp_asset2 = 25199886
    share_in_lp = 0.01
    orig_price_denom_asset2 = 3038 
    new_price_denom_asset2 = 2689.9113924050635
        
    eg1 = uniswapv2_class(lp_asset1, lp_asset2, share_in_lp, orig_price_denom_asset2, new_price_denom_asset2)
    eg1.estimate_asset_composition()
    
    volatility = 0.8/15.8
    
    dict_param = {
        'sd_minus_3': orig_price_denom_asset2 * (1-3 * volatility),
        'sd_minus_2': orig_price_denom_asset2 * (1-2 * volatility),
        'sd_minus_1': orig_price_denom_asset2 * (1-1 * volatility),
        'sd_minus_0_5': orig_price_denom_asset2 * (1-0.5 * volatility),               
        'sd_plus_0_5': orig_price_denom_asset2 * (1+0.5 * volatility),                
        'sd_plus_1': orig_price_denom_asset2 * (1+1 * volatility),
        'sd_plus_2': orig_price_denom_asset2 * (1+2 * volatility),       
        'sd_plus_3': orig_price_denom_asset2 * (1+3 * volatility)        
        }
                 
    for i in dict_param:
        
        print(i)
        lp_asset1 = 8354
        lp_asset2 = 25001651
        share_in_lp = 0.01
        orig_price_denom_asset2 = 2993 
        new_price_denom_asset2 = dict_param[i] 
            
        eg1 = uniswapv2_class(lp_asset1, lp_asset2, share_in_lp, orig_price_denom_asset2, new_price_denom_asset2)
        print(eg1.estimate_asset_composition())  
        
    df = eg1.sensitivity_analysis(dict_param)
    
    #If you borrow asset and deposit into LP. In extreme scenario, you only lose 0.6% but you earn 0.1% every day
    # ((8295-7725.570222497361) * 3499.4683544303793)
    # Out[17]: 1992701.486440817
    
    # 27035388.51355918 - 1992701.486440817
    # Out[18]: 25042687.027118362
    
    # (25199886 - 25042687.027118362)/25199886
    # Out[19]: 0.006238082699327986    
    
    