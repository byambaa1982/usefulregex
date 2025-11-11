# DateTime & Time Series Pro Tips

Master temporal data manipulation with pandas datetime magic.

---

## 🎯 Quick Reference

| Operation | Example | Result |
|-----------|---------|--------|
| Parse strings to datetime | `pd.to_datetime(df['date'])` | Convert to datetime64 |
| Extract components | `df['date'].dt.year` | Year, month, day, etc. |
| Date range | `pd.date_range('2024-01-01', periods=10, freq='D')` | 10 days |
| Resample | `df.resample('M').sum()` | Monthly aggregation |
| Rolling window | `df.rolling(window=7).mean()` | 7-day moving average |
| Time delta | `df['date2'] - df['date1']` | Duration between dates |

---

## 💡 Pro Tips

### 1. Parse Dates Efficiently

```python
# Parse on read (fastest)
df = pd.read_csv('data.csv', parse_dates=['date_column'])

# Parse existing column
df['date'] = pd.to_datetime(df['date'])

# Handle different formats
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# Infer format (slower but flexible)
df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

# Handle errors gracefully
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Invalid → NaT
```

### 2. Extract Date Components

```python
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek  # Monday=0, Sunday=6
df['quarter'] = df['date'].dt.quarter
df['week'] = df['date'].dt.isocalendar().week

# Get month/day names
df['month_name'] = df['date'].dt.month_name()
df['day_name'] = df['date'].dt.day_name()

# Business vs weekend
df['is_weekend'] = df['date'].dt.dayofweek >= 5
```

### 3. Set DateTime Index for Time Series

```python
# Convert to datetime index
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Now you can use powerful time-based indexing
df['2024']              # All data from 2024
df['2024-01']           # January 2024
df['2024-01-15':]       # From Jan 15 onwards
df['2024-01':'2024-03'] # Q1 2024
```

### 4. Date Ranges and Frequencies

```python
# Daily
pd.date_range('2024-01-01', '2024-01-31', freq='D')

# Business days only
pd.date_range('2024-01-01', '2024-01-31', freq='B')

# Weekly on Mondays
pd.date_range('2024-01-01', periods=10, freq='W-MON')

# Month end
pd.date_range('2024-01-01', periods=12, freq='M')

# Quarterly
pd.date_range('2024-01-01', periods=4, freq='Q')

# Hourly
pd.date_range('2024-01-01', periods=24, freq='H')

# Custom: every 3 hours
pd.date_range('2024-01-01', periods=8, freq='3H')
```

### 5. Resample Time Series

```python
# Downsample to monthly
monthly = df.resample('M').sum()

# Multiple aggregations
monthly = df.resample('M').agg({
    'sales': 'sum',
    'customers': 'mean',
    'transactions': 'count'
})

# Upsample to daily (forward fill)
daily = df.resample('D').ffill()

# Week starting on Monday
weekly = df.resample('W-MON').sum()
```

### 6. Rolling Windows

```python
# 7-day moving average
df['rolling_avg'] = df['sales'].rolling(window=7).mean()

# 30-day moving sum
df['rolling_sum'] = df['sales'].rolling(window=30).sum()

# With minimum periods
df['rolling_avg'] = df['sales'].rolling(window=7, min_periods=3).mean()

# Centered window (useful for smoothing)
df['centered_avg'] = df['sales'].rolling(window=7, center=True).mean()

# Custom window function
df['rolling_range'] = df['sales'].rolling(window=7).apply(lambda x: x.max() - x.min())
```

### 7. Time-Based Rolling Windows

```python
# 7-day window based on dates (not just 7 rows)
df['7d_avg'] = df['sales'].rolling('7D').mean()

# 30-day window
df['30d_sum'] = df['sales'].rolling('30D').sum()

# Requires datetime index!
```

### 8. Expanding Windows (Cumulative)

```python
# Cumulative sum
df['cumsum'] = df['sales'].expanding().sum()

# Expanding mean (all previous values)
df['expanding_avg'] = df['sales'].expanding().mean()

# Year-to-date sum
df.groupby(df.index.year)['sales'].expanding().sum()
```

### 9. Shift and Lag

```python
# Previous day's value
df['prev_day'] = df['sales'].shift(1)

# Next day's value
df['next_day'] = df['sales'].shift(-1)

# Calculate daily change
df['daily_change'] = df['sales'] - df['sales'].shift(1)

# Percentage change
df['pct_change'] = df['sales'].pct_change()

# Shift by time period (with datetime index)
df['last_week'] = df['sales'].shift(freq='7D')
```

### 10. Business Day Arithmetic

```python
from pandas.tseries.offsets import BDay

# Add 5 business days
df['delivery_date'] = df['order_date'] + BDay(5)

# Subtract 1 business day
df['previous_bday'] = df['date'] - BDay(1)

# Number of business days between dates
(df['end_date'] - df['start_date']).dt.days
```

---

## 🚀 Advanced Techniques

### Custom Business Day Calendar

```python
from pandas.tseries.holiday import USFederalHolidayCalendar, AbstractHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

cal = USFederalHolidayCalendar()
bday_us = CustomBusinessDay(calendar=cal)

# Date range excluding US federal holidays
pd.date_range('2024-01-01', '2024-12-31', freq=bday_us)
```

### Time Zone Handling

```python
# Localize naive datetime to timezone
df['date'] = df['date'].dt.tz_localize('UTC')

# Convert timezone
df['date_eastern'] = df['date'].dt.tz_convert('America/New_York')

# Remove timezone (make naive again)
df['date_naive'] = df['date'].dt.tz_localize(None)
```

### Period Data (Fixed Frequency)

```python
# Convert to period
df['month_period'] = df['date'].dt.to_period('M')

# Period range
periods = pd.period_range('2024-01', '2024-12', freq='M')

# Convert back to timestamp
df['date'] = df['month_period'].dt.to_timestamp()
```

### Time Deltas

```python
# Calculate duration
df['duration'] = df['end_time'] - df['start_time']

# Extract days, seconds
df['days'] = df['duration'].dt.days
df['seconds'] = df['duration'].dt.seconds

# Create timedelta
df['deadline'] = df['start'] + pd.Timedelta(days=7)
df['cutoff'] = df['timestamp'] + pd.Timedelta(hours=2, minutes=30)
```

---

## ⚡ Performance Tips

| Tip | Speedup |
|-----|---------|
| Parse dates on read (`parse_dates` in `read_csv`) | 2-5x |
| Use `.dt` accessor instead of `.apply()` | 10-100x |
| Set datetime index for time-based operations | 2-10x |
| Use `pd.to_datetime()` once, not in loop | 100x+ |

```python
# ❌ Slow
df['year'] = df['date'].apply(lambda x: x.year)

# ✅ Fast
df['year'] = df['date'].dt.year
```

---

## 🎓 Common Patterns

### Filter by Date Range

```python
# With datetime index
df['2024-01-01':'2024-03-31']

# Without index
mask = (df['date'] >= '2024-01-01') & (df['date'] <= '2024-03-31')
df[mask]

# Last N days
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=30)
df[df['date'] >= cutoff]
```

### Group by Time Period

```python
# Group by month
df.groupby(df['date'].dt.to_period('M'))['sales'].sum()

# Group by year and quarter
df.groupby([df['date'].dt.year, df['date'].dt.quarter])['sales'].sum()

# Group by day of week
df.groupby(df['date'].dt.day_name())['sales'].mean()
```

### Fill Missing Dates

```python
# Ensure continuous date range
df = df.set_index('date')
df = df.reindex(pd.date_range(df.index.min(), df.index.max(), freq='D'))

# Fill missing values
df['sales'] = df['sales'].fillna(0)
```

### Compare to Same Period Last Year

```python
# Add last year's data
df['sales_last_year'] = df['sales'].shift(365)

# Year-over-year growth
df['yoy_growth'] = (df['sales'] / df['sales_last_year'] - 1) * 100
```

---

## 📊 Real-World Example: Daily Sales Analysis

```python
# Setup
df = pd.read_csv('sales.csv', parse_dates=['date'])
df = df.set_index('date').sort_index()

# Add time features
df['dayofweek'] = df.index.dayofweek
df['month'] = df.index.month
df['is_weekend'] = df.index.dayofweek >= 5

# 7-day moving average
df['ma_7'] = df['sales'].rolling(7).mean()

# Month-over-month change
monthly = df.resample('M').sum()
monthly['mom_change'] = monthly['sales'].pct_change() * 100

# Compare weekday vs weekend average
df.groupby('is_weekend')['sales'].mean()

# Best/worst day of week
df.groupby(df.index.day_name())['sales'].mean().sort_values(ascending=False)
```

---

**Next:** Boost performance with [06_performance_optimization.md](06_performance_optimization.md)!
