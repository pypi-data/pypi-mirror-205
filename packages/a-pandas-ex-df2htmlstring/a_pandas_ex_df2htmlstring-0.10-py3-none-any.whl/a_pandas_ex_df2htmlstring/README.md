# exports pandas DataFrames/Series as HTML (formatted string that looks like a table!)

### pip install a-pandas-ex-df2htmlstring

#### Tested against Windows 10 / Python 3.10 / Anaconda


![](https://github.com/hansalemaos/screenshots/raw/main/pandasstringhtml.png)



### How to use it

```python
from a_pandas_ex_df2htmlstring import pd_add_df2htmlstring

pd_add_df2htmlstring()
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
outfile = "e:\\outputhtml.html"
df.ds_2htmlstring(
    outputfile=outfile, fontsize=12, fontcolor="black", repeat_columns_n_rows=70
)
os.startfile(outfile)
df.Name.ds_2htmlstring(
    outputfile=outfile, fontsize=12, fontcolor="black", repeat_columns_n_rows=70
)


Converts a pandas DataFrame to an HTML string with customizable font size, font color, and repeated column headers.

Args:
	df (pandas.DataFrame / pandas.Series): The DataFrame to be converted to an HTML string. (automatically passed)
	outputfile (str, optional): The name of the output file to save the HTML string to. Defaults to None (won't be saved on HDD).
	fontsize (int, optional): The font size of the HTML string. Defaults to 12.
	fontcolor (str, optional): The font color of the HTML string. Defaults to "black".
	repeat_columns_n_rows (int, optional): The number of rows after which to repeat the column headers. Defaults to 70.

Returns:
	str: The HTML string representation of the DataFrame.

```