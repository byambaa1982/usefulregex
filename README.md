## Data cleaning without using regex

All code is here:
https://github.com/byambaa1982/usefulregex/blob/master/main.py

If you want to fork the project on github and git clone your fork, e.g.:

    git clone https://github.com/<username>/usfulregex.git
    
As a data scientist, I wasted a lot of time cleaning data, especially for dirty data like the following one.  

### Raw data 

![Data](/images/data_pic.png)


Problem is that we cannot use following codes because of symbols like '--' or '-' 
```python
	df['DataFrame Column'] = pd.to_numeric(df['DataFrame Column'])

	or 

	df['DataFrame Column'] = df['DataFrame Column'].astype(int)
## usefulregex — clean numeric-looking strings without regex

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/)

A tiny utility to convert messy numeric-like strings (for example `"59.55 `, `1200M`, `--`) into floats so you can work with `pandas` without blowing up on bad cells.

This project shows a simple approach that avoids complex regular expressions and provides an executable script plus a Python API you can import.

Features
- Robust conversion of mixed strings to float (returns `NaN` for non-parsable values)
- Convert columns by name or by index in a CSV
- Small, easy-to-read implementation intended for data-cleaning quick tasks

Screenshot

![Raw data example](/images/data_pic.png)

Quick start

1. Install requirements (recommended in a venv):

```powershell
pip install -r requirements.txt
```

2. Run the CLI to clean columns (example):

```powershell
python main.py data/raw.csv -c 2 Temperature Distance -o data/cleaned.csv
```

This accepts column indices (0-based) and column names mixed together.

Python API

You can also use the functions from Python:

```python
from main import change_df, anystring_to_float
import pandas as pd

df = pd.read_csv('data/raw.csv')
clean = change_df(df, ['Temperature', 2])  # convert column named 'Temperature' and the 3rd column
```

Why this approach?

- Some datasets include characters like `-`, `--`, `M`, or letters inside numbers. `pandas.to_numeric` fails on those unless you pre-clean. This project provides a pragmatic cleaner.

Contributing

If you find the approach useful, please open an issue or a pull request. Small suggestions:

- Add unit tests for edge cases
- Add GitHub Actions for CI
- Add more parsing rules (thousands separators, currency, parentheses for negatives)

License

This project is MIT licensed — see the `LICENSE` file.

Contact

LinkedIn: https://www.linkedin.com/in/byamba-enkhbat-026722162/
