"""usefulregex.main

Small utilities to coerce messy numeric-like strings into floats without
relying on full regular expressions. Provides a safe `anystring_to_float`
converter and a helper to convert columns of a pandas DataFrame.

Example CLI usage:

    python main.py input.csv --columns 2 Temperature Distance --output cleaned.csv

This will read `input.csv`, convert columns by index (2) and by name
(`Temperature`, `Distance`) and write the result to `cleaned.csv`.

The module is intentionally small and dependency-light: it only needs
`pandas` and `numpy` to operate on tabular data.
"""

from typing import Iterable, List, Union
import argparse
import sys

import pandas as pd
import numpy as np


def anystring_to_float(value: object) -> float:
    """Attempt to extract a float from a messy string.

    Behavior:
    - Non-string and `None` inputs return `np.nan`.
    - Keeps digits, a single leading minus sign, and at most one decimal
      point. All other characters are dropped.
    - Empty or invalid results return `np.nan`.

    This deliberately avoids using regular expressions so it's easy to
    understand and modify.

    Args:
        value: Any python object (typically a str or numeric).

    Returns:
        A float when a numeric value can be parsed, otherwise `np.nan`.
    """
    if value is None:
        return np.nan

    s = str(value).strip()
    if s == "":
        return np.nan

    result_chars: List[str] = []
    dot_seen = False
    # allow a single leading minus sign
    allow_minus = True

    for ch in s:
        if ch.isdigit():
            result_chars.append(ch)
            allow_minus = False
        elif ch == '.' and not dot_seen:
            result_chars.append(ch)
            dot_seen = True
            allow_minus = False
        elif ch == '-' and allow_minus:
            result_chars.append(ch)
            allow_minus = False
        else:
            # drop everything else
            allow_minus = False

    cleaned = ''.join(result_chars)
    # guard against values that are just '-' or '.' etc.
    if cleaned in ('', '-', '.', '-.'):
        return np.nan

    try:
        return float(cleaned)
    except Exception:
        return np.nan


def change_df(df: pd.DataFrame, columns: Iterable[Union[int, str]]) -> pd.DataFrame:
    """Convert specified columns of `df` to float using `anystring_to_float`.

    Args:
        df: pandas DataFrame to operate on (in-place changes are applied to a copy).
        columns: Iterable of column names or 0-based integer indices.

    Returns:
        A new DataFrame with the requested columns converted to floats.
    """
    df = df.copy()
    # Normalize to column names
    col_names: List[str] = []
    for c in columns:
        if isinstance(c, int):
            try:
                col_names.append(df.columns[c])
            except Exception:
                raise IndexError(f"Column index {c} is out of range for DataFrame")
        else:
            if c not in df.columns:
                raise KeyError(f"Column name '{c}' not found in DataFrame")
            col_names.append(c)

    for name in col_names:
        # Use apply to keep NaN handling and avoid problems with mixed types
        df[name] = df[name].apply(anystring_to_float)

    return df


def _parse_columns_arg(values: List[str]) -> List[Union[int, str]]:
    parsed: List[Union[int, str]] = []
    for v in values:
        # treat purely numeric tokens as indices
        if v.lstrip('-').isdigit():
            parsed.append(int(v))
        else:
            parsed.append(v)
    return parsed


def main(argv: List[str] = None) -> int:
    parser = argparse.ArgumentParser(description="Convert messy numeric-looking columns to floats")
    parser.add_argument('input', help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output CSV file path; if omitted prints to stdout')
    parser.add_argument('-c', '--columns', nargs='+', required=True, help='List of column names or 0-based indices to convert')
    parser.add_argument('--sep', default=',', help='CSV separator (default: ,)')
    args = parser.parse_args(argv)

    try:
        df = pd.read_csv(args.input, sep=args.sep)
    except Exception as exc:
        print(f"Error reading '{args.input}': {exc}", file=sys.stderr)
        return 2

    try:
        cols = _parse_columns_arg(args.columns)
        out_df = change_df(df, cols)
    except Exception as exc:
        print(f"Error converting columns: {exc}", file=sys.stderr)
        return 3

    if args.output:
        out_df.to_csv(args.output, index=False)
        print(f"Wrote cleaned data to {args.output}")
    else:
        out = out_df.to_csv(index=False)
        print(out)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
import pandas as pd 
import numpy as np 




#--------------no regex version---------------
# ---------------turn any string into foat-------------
def anystring_to_float(string):
  newstring ="" 
  my_float=""
  count=0
  try:
    for a in string: 
        if a=='.' or (a.isnumeric()) == True: 
            count+= 1
            my_float+=a
        else: 
            newstring+= a 
    # print(count) 
    # print(newstring) 
    # print('data type of {} is now {}'.format(num, type(num)))
    return float(my_float)
  except:
    return np.nan


# anystring_to_float(string)


def change_df(df):
  for i in indice_of_columns:
    print(df.columns[i])
    df[df.columns[i]]=df[df.columns[i]].map(lambda row:anystring_to_float(row))
  return df


#--------You should change indice list here: ---------


indice_of_columns=[5,7,8,9]
change_df(df)
