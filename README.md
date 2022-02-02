# liquiditypoolcalculator

1. The aim of this package is to provide a simple framework to compute expected changes in value of liqudity pool.
2. With the expected changes in liquidity pool, traders could estimate impermanent losses and expected profits. Arbitrageurs could apply appropiate hedge ratios through futures/ perpetuals to extract the yield.

## Note on current version 0

1. As of now, I only set up the class for uniswap v3. In future, I may expand to other platforms and generalize the code further. 
2. In addition, I'm using it mostly for my own purposes. Please include engineering safeguards if you use it for production purposes.
3. For uniswap v3, you have to include parameters such as defined lower bound and upper bound values for concentrated liquidity pool provision.

## Literature used as reference

I primarily referred to the following materials to develop this package,

- https://uniswap.org/blog/uniswap-v3
- Page 5: https://atiselsts.github.io/pdfs/uniswap-v3-liquidity-math.pdf

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