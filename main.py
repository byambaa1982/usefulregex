"""usefulregex.main

Production-ready utilities to clean messy numeric-like strings in pandas DataFrames
without using complex regular expressions. Perfect for data exploration and prototyping.

✨ Features:
- Clean numeric columns with units, dashes, or other special characters
- Support for negative numbers and decimals
- Vectorized operations for better performance
- CLI and Python API for flexibility
- Type hints and comprehensive error handling

📖 Example CLI usage:

    python main.py input.csv --columns 2 Temperature Distance --output cleaned.csv

This will read `input.csv`, convert columns by index (2) and by name
(`Temperature`, `Distance`) and write the result to `cleaned.csv`.

🐍 Python API example:

    from main import anystring_to_float, change_df
    import pandas as pd
    
    # Clean individual values
    anystring_to_float("23.5 °C")  # → 23.5
    anystring_to_float("--")       # → NaN
    anystring_to_float("1200M")    # → 1200.0
    
    # Clean DataFrame columns
    df = pd.read_csv('messy_data.csv')
    clean_df = change_df(df, ['Temperature', 'Distance', 2])

The module is intentionally simple and only requires `pandas` and `numpy`.
For production use with complex patterns, consider using `pd.to_numeric()` with
proper preprocessing or dedicated parsing libraries.

Author: Byamba Enkhbat
License: MIT
"""

from typing import Iterable, List, Union, Optional
import argparse
import sys
import warnings

import pandas as pd
import numpy as np


def anystring_to_float(value: object) -> float:
    """Extract a float from a messy string without using regex.

    This function is intentionally simple and easy to understand. It extracts
    digits, decimal points, and leading minus signs while discarding everything
    else (units, dashes, letters, etc.).

    🎯 Behavior:
    - Non-string and `None` inputs → `np.nan`
    - Keeps: digits (0-9), single decimal point (.), leading minus sign (-)
    - Drops: letters, units, symbols, extra dashes, whitespace
    - Empty or invalid results → `np.nan`

    📊 Examples:
        >>> anystring_to_float("23.5 °C")
        23.5
        >>> anystring_to_float("--")
        nan
        >>> anystring_to_float("1200M")
        1200.0
        >>> anystring_to_float("-42.7")
        -42.7
        >>> anystring_to_float(None)
        nan

    Args:
        value: Any Python object (typically a string or number)

    Returns:
        float: Extracted number, or `np.nan` if parsing fails

    Notes:
        - Does NOT use regular expressions (by design)
        - Processes one character at a time for clarity
        - Only allows one decimal point
        - Only allows minus sign at the start
        
    Performance:
        ⚡ For large DataFrames (>100K rows), consider vectorized alternatives
        or use `pd.to_numeric(errors='coerce')` after preprocessing.
    """
    # Handle None and empty values early
    if value is None or pd.isna(value):
        return np.nan

    # Convert to string and strip whitespace
    s = str(value).strip()
    if not s:
        return np.nan

    result_chars: List[str] = []
    dot_seen = False
    allow_minus = True  # Only allow minus as first character

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
            # Drop everything else (units, letters, extra dashes, etc.)
            allow_minus = False

    cleaned = ''.join(result_chars)
    
    # Guard against edge cases: just '-' or '.' or '-.' or empty
    if cleaned in ('', '-', '.', '-.'):
        return np.nan

    # Attempt conversion
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return np.nan


def change_df(
    df: pd.DataFrame,
    columns: Iterable[Union[int, str]],
    inplace: bool = False
) -> pd.DataFrame:
    """Convert specified DataFrame columns to float using `anystring_to_float`.

    This function accepts column names and/or 0-based integer indices, making it
    flexible for different use cases. It preserves the original DataFrame by default.

    📊 Usage Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A': ['23.5 °C', '--', '25.0'], 'B': [1, 2, 3]})
        >>> clean_df = change_df(df, ['A'])  # By name
        >>> clean_df = change_df(df, [0])    # By index
        >>> clean_df = change_df(df, ['A', 1])  # Mixed

    Args:
        df: pandas DataFrame to operate on
        columns: Iterable of column names (str) or 0-based indices (int)
        inplace: If True, modify the DataFrame in place. Default: False

    Returns:
        pd.DataFrame: DataFrame with specified columns converted to float.
                     If inplace=True, returns the same DataFrame object.

    Raises:
        IndexError: If a column index is out of range
        KeyError: If a column name is not found in the DataFrame

    Performance Tips:
        - For very large DataFrames, consider processing in chunks
        - Use categorical dtype for non-numeric columns before cleaning
        - Consider `pd.to_numeric(errors='coerce')` for simpler cases

    Notes:
        - Creates a copy by default to avoid unexpected mutations
        - Handles mixed types gracefully (converts to string first)
        - Preserves NaN values in the output
    """
    # Work on copy unless inplace=True
    if not inplace:
        df = df.copy()
    
    # Normalize mixed column references to column names
    col_names: List[str] = []
    for c in columns:
        if isinstance(c, int):
            try:
                col_names.append(df.columns[c])
            except IndexError:
                raise IndexError(
                    f"Column index {c} is out of range. "
                    f"DataFrame has {len(df.columns)} columns (0-{len(df.columns)-1})"
                )
        else:
            if c not in df.columns:
                available = ', '.join(f"'{col}'" for col in df.columns[:5])
                raise KeyError(
                    f"Column name '{c}' not found in DataFrame. "
                    f"Available columns: {available}..."
                )
            col_names.append(str(c))

    # Apply conversion to each specified column
    for name in col_names:
        # Vectorized apply is faster than iterating rows
        # For even better performance, consider using .map() with a dict
        df[name] = df[name].apply(anystring_to_float)

    return df


def _parse_columns_arg(values: List[str]) -> List[Union[int, str]]:
    """Parse command-line column arguments into integers or strings.
    
    Treats purely numeric arguments as column indices (int),
    everything else as column names (str).
    
    Args:
        values: List of string arguments from command line
        
    Returns:
        List of integers (for indices) or strings (for names)
    """
    parsed: List[Union[int, str]] = []
    for v in values:
        # Check if it's a valid integer (including negative indices)
        if v.lstrip('-').isdigit():
            parsed.append(int(v))
        else:
            parsed.append(v)
    return parsed


def main(argv: Optional[List[str]] = None) -> int:
    """Command-line interface for cleaning messy numeric columns in CSV files.
    
    Args:
        argv: Command-line arguments (defaults to sys.argv)
        
    Returns:
        int: Exit code (0 = success, >0 = error)
    """
    parser = argparse.ArgumentParser(
        description="Clean messy numeric columns in CSV files (removes units, dashes, etc.)",
        epilog="Example: python main.py data.csv -c Temperature Distance 2 -o clean.csv"
    )
    parser.add_argument(
        'input',
        help='Input CSV file path'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output CSV file path; if omitted, prints to stdout'
    )
    parser.add_argument(
        '-c', '--columns',
        nargs='+',
        required=True,
        help='Column names or 0-based indices to convert (space-separated)'
    )
    parser.add_argument(
        '--sep',
        default=',',
        help='CSV separator (default: comma)'
    )
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='File encoding (default: utf-8)'
    )
    
    args = parser.parse_args(argv)

    # Read input CSV
    try:
        df = pd.read_csv(args.input, sep=args.sep, encoding=args.encoding)
        print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns from '{args.input}'")
    except FileNotFoundError:
        print(f"✗ Error: File '{args.input}' not found", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"✗ Error reading '{args.input}': {exc}", file=sys.stderr)
        return 2

    # Parse and convert columns
    try:
        cols = _parse_columns_arg(args.columns)
        print(f"✓ Converting columns: {cols}")
        out_df = change_df(df, cols)
        print(f"✓ Conversion complete")
    except (KeyError, IndexError) as exc:
        print(f"✗ Error: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:
        print(f"✗ Error converting columns: {exc}", file=sys.stderr)
        return 3

    # Write output
    try:
        if args.output:
            out_df.to_csv(args.output, index=False, encoding=args.encoding)
            print(f"✓ Wrote cleaned data to '{args.output}'")
        else:
            # Print to stdout
            print("\n" + "="*50)
            print(out_df.to_csv(index=False))
    except Exception as exc:
        print(f"✗ Error writing output: {exc}", file=sys.stderr)
        return 4

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
