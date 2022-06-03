import pandas as pd
import numpy as np

# make the example reproducible by setting a seed
np.random.seed(10)

# dependent variable, if a sale occurs
if_sale = np.random.binomial(n=1,
                             p=0.1,
                             size=100)

# numerical feature such clicks
clicks = np.floor(
    np.random.exponential(scale=10,
                          size=100)).astype(int)

# float feature like costs
costs = np.round(np.random.normal(loc=120, scale=10, size=100), 2)

# float feature like views
views = np.round(np.random.normal(loc=1000, scale=50, size=100),0).astype(int)

# categorical feature
import string
platform = np.random.choice(
    list(string.ascii_lowercase[:4]),
    size=100)

dict_arrays = {'if_sale': if_sale,
               'clicks': clicks,
               'platform': platform,
               'costs': costs,
               'views': views}

df = pd.DataFrame(dict_arrays)

print(df.head())
