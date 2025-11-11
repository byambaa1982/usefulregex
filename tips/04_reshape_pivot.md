# Reshape & Pivot Mastery

Transform your data between wide and long formats like a pro.

---

## 🎯 Quick Reference

| Operation | Use Case | Example |
|-----------|----------|---------|
| **Pivot** | Wide format (unique index) | `df.pivot(index='date', columns='product', values='sales')` |
| **Pivot Table** | Wide format (with aggregation) | `df.pivot_table(index='date', columns='product', values='sales', aggfunc='sum')` |
| **Melt** | Long format | `df.melt(id_vars=['id'], value_vars=['Q1', 'Q2', 'Q3'])` |
| **Stack** | Columns → Rows | `df.stack()` |
| **Unstack** | Rows → Columns | `df.unstack()` |

---

## 💡 Pro Tips

### 1. Pivot: From Long to Wide

```python
# Long format
# date       | product | sales
# 2024-01-01 | A       | 100
# 2024-01-01 | B       | 150
# 2024-01-02 | A       | 120

# Wide format
result = df.pivot(index='date', columns='product', values='sales')

# Result:
# product    | A   | B
# 2024-01-01 | 100 | 150
# 2024-01-02 | 120 | NaN
```

### 2. Pivot Table: With Aggregation

```python
# When there are duplicate index/column combinations, use pivot_table
result = df.pivot_table(
    index='date',
    columns='product',
    values='sales',
    aggfunc='sum',      # 'mean', 'count', 'max', etc.
    fill_value=0,       # Replace NaN with 0
    margins=True        # Add row/column totals
)
```

### 3. Multiple Aggregations in Pivot Table

```python
result = df.pivot_table(
    index='region',
    columns='product',
    values='sales',
    aggfunc=['sum', 'mean', 'count']
)
```

### 4. Melt: From Wide to Long

```python
# Wide format
# id | Q1  | Q2  | Q3
# 1  | 100 | 150 | 200
# 2  | 80  | 120 | 160

# Long format
result = df.melt(
    id_vars=['id'],
    value_vars=['Q1', 'Q2', 'Q3'],
    var_name='quarter',
    value_name='sales'
)

# Result:
# id | quarter | sales
# 1  | Q1      | 100
# 1  | Q2      | 150
# 1  | Q3      | 200
```

### 5. Melt All Columns Except ID Columns

```python
# Melt everything except 'id' and 'name'
result = df.melt(id_vars=['id', 'name'], var_name='metric', value_name='value')
```

### 6. Stack and Unstack with MultiIndex

```python
# Stack: move innermost column level to innermost row level
stacked = df.stack()

# Unstack: move innermost row level to innermost column level
unstacked = df.unstack()

# Specify level by name or position
df.unstack(level='product')
df.unstack(level=-1)
```

### 7. CrossTab: Quick Frequency Table

```python
# Count occurrences of combinations
pd.crosstab(df['department'], df['gender'])

# With values and aggregation
pd.crosstab(
    df['department'],
    df['gender'],
    values=df['salary'],
    aggfunc='mean'
)

# With margins (totals)
pd.crosstab(df['department'], df['gender'], margins=True)
```

### 8. Pivot with Multiple Value Columns

```python
result = df.pivot_table(
    index='date',
    columns='product',
    values=['sales', 'quantity'],  # Multiple metrics
    aggfunc='sum'
)

# Result has MultiIndex columns: (sales, A), (sales, B), (quantity, A), (quantity, B)
```

### 9. Normalize Pivot Table (Percentages)

```python
result = df.pivot_table(
    index='region',
    columns='product',
    values='sales',
    aggfunc='sum',
    normalize='all'  # or 'index', 'columns'
)
# Shows proportion of total
```

### 10. Explode Lists in Cells

```python
# DataFrame with lists
# id | tags
# 1  | ['python', 'data', 'ml']
# 2  | ['sql', 'data']

# Explode into separate rows
result = df.explode('tags')

# Result:
# id | tags
# 1  | python
# 1  | data
# 1  | ml
# 2  | sql
# 2  | data
```

---

## 🚀 Advanced Techniques

### Multi-Level Pivoting

```python
# Pivot with multiple index columns
result = df.pivot_table(
    index=['region', 'city'],
    columns=['year', 'quarter'],
    values='sales',
    aggfunc='sum'
)

# Flatten multi-level columns
result.columns = ['_'.join(map(str, col)) for col in result.columns]
result.reset_index(inplace=True)
```

### Wide to Long with Multiple Value Columns

```python
# Wide format:
# id | sales_Q1 | sales_Q2 | profit_Q1 | profit_Q2

result = df.melt(
    id_vars=['id'],
    value_vars=['sales_Q1', 'sales_Q2', 'profit_Q1', 'profit_Q2']
)

# Then split variable into metric and quarter
result[['metric', 'quarter']] = result['variable'].str.split('_', expand=True)
result = result.drop('variable', axis=1)
```

### Pivot and Fill Missing Values

```python
result = df.pivot_table(
    index='date',
    columns='product',
    values='sales',
    aggfunc='sum',
    fill_value=0  # Replace NaN with 0
)

# Or fill after pivot
result = df.pivot(index='date', columns='product', values='sales')
result = result.fillna(0)
```

### Custom Aggregation Functions

```python
def range_calc(x):
    return x.max() - x.min()

result = df.pivot_table(
    index='category',
    columns='year',
    values='sales',
    aggfunc=[np.mean, np.std, range_calc]
)
```

---

## ⚡ Performance Tips

| Tip | Speedup |
|-----|---------|
| Use `pivot()` instead of `pivot_table()` when no aggregation needed | 2-5x |
| Convert columns to categorical before pivot | 2-3x |
| Use `unstack()` on indexed data instead of `pivot()` | Faster for multi-index |

```python
# Optimize for repeated pivoting
df['category'] = df['category'].astype('category')
df['product'] = df['product'].astype('category')
```

---

## 🎓 Common Patterns

### Pivot Table with Subtotals

```python
result = df.pivot_table(
    index=['region', 'city'],
    columns='year',
    values='sales',
    aggfunc='sum',
    margins=True,
    margins_name='Total'
)
```

### Conditional Formatting in Wide Format

```python
pivoted = df.pivot(index='date', columns='product', values='sales')

# Highlight values > 1000
def highlight(val):
    return 'background-color: yellow' if val > 1000 else ''

pivoted.style.applymap(highlight)
```

### Unpivot Specific Columns with Pattern

```python
# Melt only columns starting with 'sales_'
sales_cols = [col for col in df.columns if col.startswith('sales_')]
result = df.melt(id_vars=['id'], value_vars=sales_cols)
```

### Transpose DataFrame

```python
# Swap rows and columns
transposed = df.T

# Or with specific column as new column names
transposed = df.set_index('id').T
```

---

## 🔥 Pivot vs Melt vs Stack

| Method | Direction | Best For |
|--------|-----------|----------|
| `pivot()` | Long → Wide | Unique index/column pairs, no aggregation |
| `pivot_table()` | Long → Wide | Duplicate pairs, needs aggregation |
| `melt()` | Wide → Long | Converting column headers to row values |
| `stack()` | Wide → Long | MultiIndex operations |
| `unstack()` | Long → Wide | MultiIndex operations |

---

## 📊 Real-World Example

```python
# Sales data: one row per transaction
# date       | store | product | sales
# 2024-01-01 | A     | Widget  | 100
# 2024-01-01 | A     | Gadget  | 150
# 2024-01-01 | B     | Widget  | 80

# Create daily sales by product and store
pivot = df.pivot_table(
    index='date',
    columns=['store', 'product'],
    values='sales',
    aggfunc='sum',
    fill_value=0
)

# Add rolling 7-day average
rolling_avg = pivot.rolling(window=7).mean()

# Melt back for plotting
melted = rolling_avg.reset_index().melt(
    id_vars='date',
    var_name=['store', 'product'],
    value_name='rolling_avg_sales'
)
```

---

**Next:** Master time series in [05_datetime_timeseries.md](05_datetime_timeseries.md)!
