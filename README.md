#  Pandas Pro Tips & Data Cleaning Utilities

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/)

**Your one-stop repository for pandas mastery and practical data cleaning utilities.**

Master pandas with battle-tested tips, tricks, and real-world examples. Plus a lightweight utility to clean messy numeric data without wrestling with regex.

---

##  What''s Inside

###  Pandas Tips & Tricks

8 comprehensive guides covering everything from basics to advanced techniques:

| Guide | Topics Covered | Skill Level |
|-------|----------------|-------------|
| [**01. Selection & Filtering**](tips/01_selection_filtering.md) | `.loc`, `.iloc`, `.query()`, `.isin()`, boolean indexing |  |
| [**02. GroupBy & Aggregation**](tips/02_groupby_aggregation.md) | Split-apply-combine, `.transform()`, `.agg()`, custom functions |  |
| [**03. Merge, Join & Concat**](tips/03_merge_join_concat.md) | Inner/outer joins, `merge_asof`, handling duplicates, validation |  |
| [**04. Reshape & Pivot**](tips/04_reshape_pivot.md) | WideLong, `pivot_table()`, `melt()`, `stack()`/`unstack()` |  |
| [**05. DateTime & Time Series**](tips/05_datetime_timeseries.md) | Date parsing, resampling, rolling windows, time zones |  |
| [**06. Performance Optimization**](tips/06_performance_optimization.md) | Vectorization, categorical dtype, memory profiling, `eval()` |  |
| [**07. String & Regex Operations**](tips/07_string_operations.md) | `.str` accessor, regex patterns, text cleaning, extraction |  |
| [**08. Data I/O Operations**](tips/08_io_operations.md) | CSV, Excel, Parquet, SQL, JSON, performance tips |  |

 **Each guide includes:**
- Quick reference tables
- Real-world examples
- Performance comparisons
- Common pitfalls to avoid
- Advanced techniques

---

###  Data Cleaning Utility

A practical tool for cleaning messy numeric columns in pandas DataFrames.

#### The Problem

You''ve got data like this:

| Temperature | Distance | Pressure |
|-------------|----------|----------|
| 23.5        | 120      | 101.3    |
| 25.3        | --       | 99.8     |
| --          | 135      | -        |
| 22.1 C     | 142M     | 100.2    |

Standard pandas methods fail:

``````python
#  Throws ValueError
df[''Temperature''] = pd.to_numeric(df[''Temperature''])
df[''Distance''] = df[''Distance''].astype(int)
``````

#### The Solution

``````python
from main import anystring_to_float, change_df

# Clean individual values
anystring_to_float("23.5 C")  #  23.5
anystring_to_float("--")       #  NaN
anystring_to_float("1200M")    #  1200.0

# Clean entire columns
clean_df = change_df(df, [''Temperature'', ''Distance'', ''Pressure''])
``````

#### CLI Usage

``````powershell
# Clean specific columns by name or index
python main.py data.csv -c Temperature Distance 2 -o cleaned.csv

# Accepts mix of column names and 0-based indices
python main.py sales.csv -c 0 1 "Sales Amount" "Units Sold" -o clean_sales.csv
``````

---

##  Quick Start

### Installation

``````powershell
# Clone the repo
git clone https://github.com/byambaa1982/usefulregex.git
cd usefulregex

# Install dependencies (optional, only pandas needed)
pip install -r requirements.txt
``````

### Browse the Tips

Start with any guide in the [`tips/`](tips/) folder. Each is self-contained with copy-paste examples.

**Recommended learning path:**
1. Selection & Filtering (basics)
2. GroupBy & Aggregation (intermediate)
3. Merge, Join & Concat (intermediate)
4. Performance Optimization (advanced)

### Use the Cleaner

``````python
import pandas as pd
from main import change_df

# Load messy data
df = pd.read_csv(''messy_data.csv'')

# Specify columns to clean (by name or index)
clean_df = change_df(df, [''Temperature'', 2, ''Pressure''])

# Now you can do numeric operations!
clean_df[''avg_temp''] = clean_df[''Temperature''].mean()
``````

---

##  Why This Approach?

### For the Tips

- **Practical over theoretical**: Real examples you''ll use daily
- **Performance-focused**: Includes timing comparisons and optimization tricks
- **Pitfall warnings**: Learn from common mistakes
- **Copy-paste ready**: All code examples are tested and runnable

### For the Cleaner

| Feature | This Tool | `pd.to_numeric()` | Regex Solutions |
|---------|-----------|-------------------|-----------------|
| Handles `--` / `-` |  |  |  (complex) |
| Handles units (`M`, `K`) |  |  |  (complex) |
| No regex needed |  |  |  |
| Simple code |  |  |  |
| Production-ready |  (basic) |  |  |

**When to use this cleaner:**
- Quick data exploration and prototyping
- Small to medium datasets
- Learning/teaching data cleaning concepts
- When you don''t want to write regex

**When to use alternatives:**
- Production pipelines  Use `pd.to_numeric()` with `errors=''coerce''` after proper preprocessing
- Complex patterns  Write targeted regex or use dedicated parsing libraries

---

##  Learning Resources

### Quick Wins (Start Here!)

- **Never iterate with `for` loops**  See [Performance Optimization](tips/06_performance_optimization.md)
- **Use categorical dtype** for repeated values  Saves 50-90% memory
- **Use `.query()` for complex filters**  2-5x faster and more readable

### Common Questions

**Q: How do I combine multiple DataFrames?**  
A: See [Merge, Join & Concat guide](tips/03_merge_join_concat.md) for all joining strategies.

**Q: My code is too slow. How do I speed it up?**  
A: Check [Performance Optimization](tips/06_performance_optimization.md) for vectorization and profiling techniques.

**Q: How do I work with dates and time series?**  
A: See [DateTime & Time Series guide](tips/05_datetime_timeseries.md) for parsing, resampling, and rolling windows.

**Q: How do I reshape data from wide to long (or vice versa)?**  
A: Check [Reshape & Pivot guide](tips/04_reshape_pivot.md) for `pivot()`, `melt()`, and friends.

---

##  Contributing

Contributions welcome! Here are some ideas:

**For the tips:**
- Add more real-world examples
- Cover additional pandas topics (plotting, styling, etc.)
- Create Jupyter notebook versions
- Add interactive quiz/exercises

**For the cleaner:**
- Unit tests for edge cases
- Support for currency symbols (`$`, ``)
- Handle thousands separators (`,`)
- Support for scientific notation
- GitHub Actions for CI/CD

Open an issue or submit a PR  all skill levels welcome!

---

##  License

This project is MIT licensed. See the [`LICENSE`](LICENSE) file for details.

Free to use, modify, and distribute. Attribution appreciated but not required.

---

##  Contact & Support

**Author:** Byamba Enkhbat  
**LinkedIn:** [linkedin.com/in/byamba-enkhbat-026722162](https://www.linkedin.com/in/byamba-enkhbat-026722162/)  
**GitHub:** [github.com/byambaa1982](https://github.com/byambaa1982)

Found this helpful?  Star the repo to show support!

---

##  Quick Links

- [Browse All Tips](tips/)
- [View Source Code](main.py)
- [Report an Issue](https://github.com/byambaa1982/usefulregex/issues)
- [Fork This Repo](https://github.com/byambaa1982/usefulregex/fork)

---

**Happy pandas-ing! **
