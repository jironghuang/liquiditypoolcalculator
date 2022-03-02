#https://lambert-guillaume.medium.com/how-to-deploy-delta-neutral-liquidity-in-uniswap-or-why-euler-finance-is-a-game-changer-for-lps-1d91efe1e8ac
import pandas as pd

def amt_assets_from_range(num_asset1, orig_price_denom_asset2, lower_price_denom_asset2, upper_price_denom_asset2, target_pool_value):
    
    """ Find amount of assets of both side of liqudiity pool with a provided asset and targeted liquidity pool size
    
    Attributes:
        num_asset1 (float) Number of asset 1 e.g. ETH
        orig_price_denom_asset2 (float) e.g. Current price of ETH in USDC
        lower_price_denom_asset2 (float) Lower bound price of ETH denominated in USDC
        upper_price_denom_asset2 (float) Lower bound price of ETH denominated in USDC    
        target_pool_value (float) Targeted pool size value denominated in USDC             
    """      
    
    L = num_asset1 * ((orig_price_denom_asset2 ** 0.5) * (upper_price_denom_asset2 ** 0.5)) / ((upper_price_denom_asset2  ** 0.5) - (orig_price_denom_asset2 ** 0.5))
    num_asset2 = L * ((orig_price_denom_asset2 ** 0.5) - (lower_price_denom_asset2 ** 0.5))
    
    orig_value_asset_in_asset2 = num_asset1 * orig_price_denom_asset2 + num_asset2    
    scale_up_ratio =  target_pool_value/orig_value_asset_in_asset2
    
    scaled_num_asset1 = num_asset1 * scale_up_ratio
    scaled_num_asset2 = num_asset2 * scale_up_ratio

    scaled_value_asset_in_asset2 = scaled_num_asset1 * orig_price_denom_asset2 + scaled_num_asset2    
    
    dict_val = {
    "num_asset1" : num_asset1,
    "num_asset2" : num_asset2,
    "scaled_num_asset1" : scaled_num_asset1,
    "scaled_num_asset2" : scaled_num_asset2,    
    "orig_value_asset_in_asset2": orig_value_asset_in_asset2,
    "scaled_value_asset_in_asset2": scaled_value_asset_in_asset2
    }            
    
    return dict_val

def uniswap_v3_hedging_ratio_amt(lower_price_denom_asset2, upper_price_denom_asset2, value_asset_in_asset2, orig_price_denom_asset2):
    
    """ Find amount of assets of both side of liqudiity pool with a provided asset and targeted liquidity pool size
    
    Attributes:
        lower_price_denom_asset2 (float) Lower bound price of ETH denominated in USDC
        upper_price_denom_asset2 (float) Lower bound price of ETH denominated in USDC    
        target_pool_value (float) Targeted pool size value denominated in USDC     
        value_asset_in_asset2 (float) Pool size value denominated in USDC           
        orig_price_denom_asset2 (float) e.g. Current price of ETH in USDC     
    """      
    
    a = (upper_price_denom_asset2 /lower_price_denom_asset2) ** 0.25 - 1
    b = (upper_price_denom_asset2/lower_price_denom_asset2) ** 0.5 - 1
    
    hedge_ratio = a/b        
    
    hedge_num_asset1 = value_asset_in_asset2 * hedge_ratio / orig_price_denom_asset2
    
    dict_val = {
    "hedge_ratio" : hedge_ratio,
    "hedge_num_asset1" : hedge_num_asset1
    }  
    
    return dict_val

if __name__ == "__main__":   
    
    num_asset1 = 5.44
    orig_price_denom_asset2 = 3027.46  #Take this as current price. Used as strike price. Analagous to middle price with 0 delta risk in a short straddle
    lower_price_denom_asset2 = orig_price_denom_asset2 * 0.73 #Use calculator to obtain 0.73 based on range factor, https://www.desmos.com/calculator/669zg1rmvb
    upper_price_denom_asset2 = orig_price_denom_asset2 * 1.3601785714285715 #Use calculator to obtain 1.36 based on range factor, https://www.desmos.com/calculator/669zg1rmvb
    target_pool_value = 37187 
    
    res = amt_assets_from_range(num_asset1, orig_price_denom_asset2, lower_price_denom_asset2, upper_price_denom_asset2, target_pool_value)    
    res

    uniswap_v3_hedging_ratio_amt(lower_price_denom_asset2, upper_price_denom_asset2, res['scaled_value_asset_in_asset2'], orig_price_denom_asset2)    
    
    
    