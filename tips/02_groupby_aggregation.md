# GroupBy & Aggregation Mastery

Unlock the power of split-apply-combine operations with these groupby techniques.

---

## 🎯 Quick Reference

| Operation | Example | Result |
|-----------|---------|--------|
| Simple aggregation | `df.groupby('dept')['salary'].mean()` | Mean salary per department |
| Multiple aggregations | `df.groupby('dept')['salary'].agg(['mean', 'max', 'min'])` | Multiple stats |
| Named aggregations | `df.groupby('dept').agg(avg_salary=('salary', 'mean'))` | Custom column names |
| Multiple columns | `df.groupby(['dept', 'city'])['salary'].mean()` | Group by 2+ columns |
| Transform | `df.groupby('dept')['salary'].transform('mean')` | Broadcast group stat to all rows |

---

## 💡 Pro Tips

### 1. Use Named Aggregations (pandas 0.25+)

```python
# ✅ Clean and explicit
result = df.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    total_employees=('employee_id', 'count'),
    salary_std=('salary', 'std')
)
```

### 2. Apply Different Functions to Different Columns

```python
agg_dict = {
    'salary': ['mean', 'median', 'std'],
    'age': ['min', 'max'],
    'employee_id': 'count'
}

df.groupby('department').agg(agg_dict)
```

### 3. Use `.transform()` to Keep Original Shape

```python
# Add group mean as a new column
df['dept_avg_salary'] = df.groupby('dept')['salary'].transform('mean')

# Calculate deviation from group mean
df['salary_vs_dept_avg'] = df['salary'] - df.groupby('dept')['salary'].transform('mean')

# Normalize within groups
df['normalized'] = df.groupby('dept')['salary'].transform(lambda x: (x - x.mean()) / x.std())
```

### 4. Filter Groups with `.filter()`

```python
# Keep only departments with more than 10 employees
df.groupby('dept').filter(lambda x: len(x) > 10)

# Keep groups where average salary > 75000
df.groupby('dept').filter(lambda x: x['salary'].mean() > 75000)
```

### 5. Custom Aggregation Functions

```python
def salary_range(x):
    return x.max() - x.min()

def top_quartile_mean(x):
    return x.quantile(0.75)

df.groupby('dept')['salary'].agg([
    'mean',
    ('range', salary_range),
    ('top_25%_avg', top_quartile_mean)
])
```

### 6. Multiple Group Keys with Different Levels

```python
# Group by multiple columns
result = df.groupby(['country', 'city', 'dept'])['salary'].mean()

# Access specific level
result.groupby(level='country').mean()  # Average by country only

# Unstack for pivot-table-like view
result.unstack('dept')
```

### 7. Use `.nth()` for Specific Rows Per Group

```python
# First row of each group
df.groupby('dept').nth(0)

# Last row of each group
df.groupby('dept').nth(-1)

# First 3 rows of each group
df.groupby('dept').head(3)

# Top 2 earners per department
df.sort_values('salary', ascending=False).groupby('dept').head(2)
```

### 8. Cumulative Operations Within Groups

```python
# Cumulative sum within each department
df['cumulative_sales'] = df.groupby('dept')['sales'].cumsum()

# Running average
df['running_avg'] = df.groupby('dept')['sales'].expanding().mean().reset_index(level=0, drop=True)

# Rank within group
df['salary_rank'] = df.groupby('dept')['salary'].rank(ascending=False)
```

### 9. Percentage of Total Within Groups

```python
# Each employee's percentage of department total
df['pct_of_dept'] = df.groupby('dept')['salary'].transform(lambda x: 100 * x / x.sum())
```

### 10. Rolling Windows Within Groups

```python
# 3-month rolling average per product
df.groupby('product')['sales'].rolling(window=3).mean()

# With explicit date index
df.set_index('date').groupby('product')['sales'].rolling('30D').mean()
```

---

## 🚀 Advanced Techniques

### Groupby with Multiple Aggregations and Flatten Columns

```python
result = df.groupby('dept').agg({
    'salary': ['mean', 'std'],
    'age': ['min', 'max']
})

# Flatten multi-level columns
result.columns = ['_'.join(col).strip() for col in result.columns.values]
result.reset_index(inplace=True)
```

### Use `groupby` with `.apply()` for Complex Logic

```python
def analyze_group(group):
    return pd.Series({
        'total': group['sales'].sum(),
        'avg': group['sales'].mean(),
        'growth': group['sales'].iloc[-1] / group['sales'].iloc[0] - 1,
        'top_product': group.loc[group['sales'].idxmax(), 'product']
    })

df.groupby('region').apply(analyze_group)
```

### GroupBy with Custom Binning

```python
# Group by age ranges
age_bins = [0, 25, 35, 50, 100]
age_labels = ['<25', '25-35', '35-50', '50+']

df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)
df.groupby('age_group')['salary'].mean()
```

### Weighted Averages

```python
def weighted_avg(values, weights):
    return (values * weights).sum() / weights.sum()

df.groupby('dept').apply(lambda x: weighted_avg(x['score'], x['weight']))
```

---

## ⚡ Performance Tips

| Tip | Speedup |
|-----|---------|
| Use built-in aggregations (`'mean'`, `'sum'`) instead of lambdas | 10-100x faster |
| Avoid `.apply()` when `.agg()` or `.transform()` works | 5-50x faster |
| Use categorical dtype for groupby columns | 2-5x faster |
| Use `observed=True` for categorical groupby | Avoids unused categories |

```python
# Convert to categorical for faster groupby
df['category'] = df['category'].astype('category')

# Only group by observed categories
df.groupby('category', observed=True)['value'].sum()
```

---

## 🎓 Common Patterns

### Calculate Group Statistics and Join Back

```python
# Method 1: Using transform
df['dept_avg'] = df.groupby('dept')['salary'].transform('mean')

# Method 2: Using merge
dept_stats = df.groupby('dept')['salary'].mean().reset_index(name='dept_avg')
df = df.merge(dept_stats, on='dept')
```

### Top N Per Group

```python
# Top 3 earners per department
(df.sort_values('salary', ascending=False)
   .groupby('dept')
   .head(3))
```

### Count Distinct Values Per Group

```python
df.groupby('city')['customer_id'].nunique()
```

### Percentage Change Within Groups

```python
df['pct_change'] = df.groupby('product')['sales'].pct_change()
```

---

**Next:** Explore [03_merge_join_concat.md](03_merge_join_concat.md) to master data combination!
