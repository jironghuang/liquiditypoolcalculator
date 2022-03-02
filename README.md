# liquiditypoolcalculator

1. The aim of this package is to provide a simple framework to compute expected changes in value of liquidity pool.
2. With the expected changes in liquidity pool, traders could estimate impermanent losses and expected profits. Arbitrageurs could apply appropriate hedge ratios through futures/ perpetuals to extract the yield.

## Note on current version 0

1. As of now, I only set up the class for uniswap v3. In future, I may expand to other platforms and generalize the code further. 
2. In addition, I'm using it mostly for my own purposes. Please include engineering safeguards if you use it for production purposes.
3. For uniswap v3, you have to include parameters such as defined lower bound and upper bound values for concentrated liquidity pool provision.

## Literature used as reference

I primarily referred to the following materials to develop this package,

- https://uniswap.org/blog/uniswap-v3
- Page 5: https://atiselsts.github.io/pdfs/uniswap-v3-liquidity-math.pdf
- https://lambert-guillaume.medium.com/how-to-deploy-delta-neutral-liquidity-in-uniswap-or-why-euler-finance-is-a-game-changer-for-lps-1d91efe1e8ac

## Set up

- pip install liquiditypoolcalculator
- required packages for package: pandas

## Project homepage

- https://github.com/jironghuang/liquiditypoolcalculator

## Examples

### Required hedge ratio based on price change

```
import pandas as pd
from liquiditypoolcalculator import uniswapv3_class

num_asset1 = 5.567  #Number of ETH
num_asset2 = 25560  #Number of USDC
orig_price_denom_asset2 = 2765.01  #Value of ETH per USDC
new_price_denom_asset2 = 2800.0
lower_price_denom_asset2 = 1813.50  #Lower bound of 
upper_price_denom_asset2 = 3526.30     

eg1 = uniswapv3_class(num_asset1, num_asset2, orig_price_denom_asset2, new_price_denom_asset2, lower_price_denom_asset2, upper_price_denom_asset2)
eg1_val = eg1.estimate_asset_composition()      
eg1_val

{'new_num_asset1': 5.2619612193407885,
 'new_num_asset2': 26407.889305387725,
 'orig_value_asset_in_asset2': 40952.810670000006,
 'new_value_asset_in_asset2': 41141.380719541936,
 'price_change_in_asset2': 0.012654565444609524,
 'price_change_in_lp': 0.004604569172588359,
 'hedge_ratio': 0.36386624200910594}
```

### Simulation on required hedge ratios based on expected price changes

```
import pandas as pd
from liquiditypoolcalculator import uniswapv3_class

num_asset1 = 5.567
num_asset2 = 25560
orig_price_denom_asset2 = 2765.01
new_price_denom_asset2 = 2800.0
lower_price_denom_asset2 = 1813.50
upper_price_denom_asset2 = 3526.30   

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
    
eg1_simulation = eg1.sensitivity_analysis(dict_param)

eg1_simulation
Out[158]: 
                               lb_1813.5  ...     ub_3526.3
new_num_asset1                 16.981105  ...      0.000000
new_num_asset2                  0.000000  ...  42942.207352
orig_value_asset_in_asset2  40952.810670  ...  40952.810670
new_value_asset_in_asset2   30795.234537  ...  42942.207352
price_change_in_asset2         -0.344125  ...      0.275330
price_change_in_lp             -0.248031  ...      0.048578
hedge_ratio                     0.720758  ...      0.176435

[7 rows x 8 columns]
      
```

### An alternative way of hedging based on price range and known pool value

- Please read following article for more info: https://lambert-guillaume.medium.com/how-to-deploy-delta-neutral-liquidity-in-uniswap-or-why-euler-finance-is-a-game-changer-for-lps-1d91efe1e8ac
- hedge_num_asset1, in this case eth can be borrowed amount against stablecoin collateral. Or short perpetual/future contracts.

```
import pandas as pd
from liquiditypoolcalculator.uniswapv3_hedging import *

num_asset1 = 5.44
orig_price_denom_asset2 = 2923.76  #Take this as current price. Used as strike price. Analagous to middle price with 0 delta risk in a short straddle
lower_price_denom_asset2 = orig_price_denom_asset2 * 0.73 #Use calculator to obtain 0.73 based on range factor, https://www.desmos.com/calculator/669zg1rmvb
upper_price_denom_asset2 = orig_price_denom_asset2 * 1.3601785714285715 #Use calculator to obtain 1.36 based on range factor, https://www.desmos.com/calculator/669zg1rmvb
target_pool_value = 36641.91 


res = amt_assets_from_range(num_asset1, orig_price_denom_asset2, lower_price_denom_asset2, upper_price_denom_asset2, target_pool_value)    
res

Out[103]: 
{'num_asset1': 5.44,
 'num_asset2': 16243.998561849383,
 'scaled_num_asset1': 6.200205977928685,
 'scaled_num_asset2': 18513.99576997123,
 'orig_value_asset_in_asset2': 32149.252961849386,
 'scaled_value_asset_in_asset2': 36641.91}


uniswap_v3_hedging_ratio_amt(lower_price_denom_asset2, upper_price_denom_asset2, res['scaled_value_asset_in_asset2'], orig_price_denom_asset2)    

Out[104]: {'hedge_ratio': 0.46118284684393274, 'hedge_num_asset1': 5.779756330067846}

```


