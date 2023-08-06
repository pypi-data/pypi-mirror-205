import html
from typing import Union
from touchtouch import touch
from a_pandas_ex_df_to_string import pd_add_to_string
import re
import pandas as pd
from pandas.core.frame import DataFrame, Series


def series_to_dataframe(
    df: Union[pd.Series, pd.DataFrame]
) -> (Union[pd.Series, pd.DataFrame], bool):
    dataf = df
    isseries = False
    if isinstance(dataf, pd.Series):
        columnname = dataf.name
        dataf = dataf.to_frame()

        try:
            dataf.columns = [columnname]
        except Exception:
            dataf.index = [columnname]
            dataf = dataf.T
        isseries = True

    return dataf, isseries


def df2stringhtml(
    df: pd.DataFrame | pd.Series,
    outputfile=None,
    fontsize=12,
    fontcolor="black",
    repeat_columns_n_rows=70,
) -> str:
    r"""
    Converts a pandas DataFrame to an HTML string with customizable font size, font color, and repeated column headers.

    Args:
        df (pandas.DataFrame / pandas.Series): The DataFrame to be converted to an HTML string.
        outputfile (str, optional): The name of the output file to save the HTML string to. Defaults to None (won't be saved on HDD).
        fontsize (int, optional): The font size of the HTML string. Defaults to 12.
        fontcolor (str, optional): The font color of the HTML string. Defaults to "black".
        repeat_columns_n_rows (int, optional): The number of rows after which to repeat the column headers. Defaults to 70.

    Returns:
        str: The HTML string representation of the DataFrame.

    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> df2stringhtml(df, outputfile='output.html', fontsize=14, fontcolor='blue', repeat_columns_n_rows=50)
        '<html><head><body><p><font color="blue" face="Courier New" size="14" style="white-space: nowrap; font-weight: bold;">  A  B</font></p><p><font color="blue" face="Courier New" size="14" style="white-space: nowrap">0  1  4</font></p><p><font color="blue" face="Courier New" size="14" style="white-space: nowrap">1  2  5</font></p><p><font color="blue" face="Courier New" size="14" style="white-space: nowrap">2  3  6</font></p></body></head></html>'
    """
    df2 = df.ds_to_string()
    df2, isseries = series_to_dataframe(df2)
    aste = html.escape(df2.to_string()).replace(" ", "&nbsp;")
    allte = []
    repeatcols = repeat_columns_n_rows
    heading = ""
    for ini, q in enumerate(aste.splitlines()):
        if ini == 0:
            heading = f"""<p><font color="{fontcolor}" face="Courier New" size="{fontsize}" style="white-space: nowrap; font-weight: bold;">{q}</font></p>"""
            allte.append(heading)
            continue
        if ini % repeatcols == 0:
            allte.append(heading)
        allte.append(
            f"""<p><font color="{fontcolor}" face="Courier New" size="{fontsize}" style="white-space: nowrap">{q}</font></p>"""
        )

    wholetext = f"""<html><head><body>{''.join(allte)}</body></head></html>"""

    if outputfile:
        outputfile = re.sub(r"\.html?$", "", outputfile, flags=re.I)
        outputfile = outputfile + ".html"
        touch(outputfile)
        with open(outputfile, mode="w", encoding="utf-8") as f:
            f.write(wholetext)

    return wholetext


def pd_add_df2htmlstring():
    pd_add_to_string()

    DataFrame.ds_2htmlstring = df2stringhtml
    Series.ds_2htmlstring = df2stringhtml
