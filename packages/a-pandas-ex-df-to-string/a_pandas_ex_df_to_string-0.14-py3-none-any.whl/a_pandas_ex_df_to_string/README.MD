## Installation

```python
pip install a-pandas-ex-df-to-string
```

## Usage

```python
from a_pandas_ex_df_to_string import pd_add_to_string
pd_add_to_string()
import pandas as pd
from random import choice
csvtests = [
    "https://github.com/pandas-dev/pandas/raw/main/doc/data/air_quality_long.csv",
    "https://github.com/pandas-dev/pandas/raw/main/doc/data/air_quality_no2.csv",
    "https://github.com/pandas-dev/pandas/raw/main/doc/data/air_quality_no2_long.csv",
    "https://github.com/pandas-dev/pandas/raw/main/doc/data/air_quality_parameters.csv",
    "https://github.com/pandas-dev/pandas/raw/main/doc/data/air_quality_pm25_long.csv",
    "https://github.com/pandas-dev/pandas/raw/main/doc/data/air_quality_stations.csv",
    "https://github.com/pandas-dev/pandas/raw/main/doc/data/baseball.csv",
    "https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv",
]
csvfile = choice(csvtests)
df = pd.read_csv(csvfile)
print(df)
print(df.dtypes)
df2=df.ds_to_string()
print(df2)
print(df2.dtypes)

     id                                        description   name
0    bc                                       Black Carbon     BC
1    co                                    Carbon Monoxide     CO
2   no2                                   Nitrogen Dioxide    NO2
3    o3                                              Ozone     O3
4  pm10  Particulate matter less than 10 micrometers in...   PM10
5  pm25  Particulate matter less than 2.5 micrometers i...  PM2.5
6   so2                                     Sulfur Dioxide    SO2
id             object
description    object
name           object
dtype: object
     id                                        description   name
0    bc                                       Black Carbon     BC
1    co                                    Carbon Monoxide     CO
2   no2                                   Nitrogen Dioxide    NO2
3    o3                                              Ozone     O3
4  pm10  Particulate matter less than 10 micrometers in...   PM10
5  pm25  Particulate matter less than 2.5 micrometers i...  PM2.5
6   so2                                     Sulfur Dioxide    SO2
id             string
description    string
name           string
dtype: object




```
