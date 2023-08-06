```sh
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 91486 entries, 0 to 91485
Data columns (total 3 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   x       91486 non-null  float64
 1   y       91486 non-null  float64
 2   label   91486 non-null  category
dtypes: category(1), float64(2)
memory usage: 1.6 MB

confusion (rust) took 0.5796697490150109 seconds
confusion (python) took 195.24605548300315 seconds
```
