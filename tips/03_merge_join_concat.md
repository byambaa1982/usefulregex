# Merge, Join & Concat Like a Pro

Master combining DataFrames with these essential joining techniques.

---

## 🎯 Quick Reference

| Operation | Use Case | Example |
|-----------|----------|---------|
| **Inner Join** | Keep only matching rows | `pd.merge(df1, df2, on='id', how='inner')` |
| **Left Join** | Keep all from left | `pd.merge(df1, df2, on='id', how='left')` |
| **Right Join** | Keep all from right | `pd.merge(df1, df2, on='id', how='right')` |
| **Outer Join** | Keep all from both | `pd.merge(df1, df2, on='id', how='outer')` |
| **Concat Rows** | Stack DataFrames | `pd.concat([df1, df2], ignore_index=True)` |
| **Concat Columns** | Side by side | `pd.concat([df1, df2], axis=1)` |

---

## 💡 Pro Tips

### 1. Merge on Multiple Columns

```python
# Merge on multiple keys
result = pd.merge(
    orders, 
    customers, 
    on=['customer_id', 'country'],
    how='left'
)
```

### 2. Handle Different Column Names

```python
# When key columns have different names
result = pd.merge(
    df1, 
    df2, 
    left_on='employee_id', 
    right_on='emp_id',
    how='inner'
)
```

### 3. Use Suffixes for Overlapping Columns

```python
# Default suffixes are '_x' and '_y'
result = pd.merge(df1, df2, on='id', suffixes=('_old', '_new'))

# Now you have: value_old, value_new instead of value_x, value_y
```

### 4. Validate Merge Types

```python
# Ensure one-to-one relationship
pd.merge(df1, df2, on='id', validate='one_to_one')

# Ensure many-to-one relationship
pd.merge(df1, df2, on='id', validate='many_to_one')

# Will raise error if assumption violated!
```

### 5. Indicator Column to Track Merge Source

```python
result = pd.merge(df1, df2, on='id', how='outer', indicator=True)

# New column '_merge' shows: 'left_only', 'right_only', or 'both'
result['_merge'].value_counts()

# Filter to rows only in left
only_in_left = result[result['_merge'] == 'left_only']
```

### 6. Merge on Index

```python
# Both DataFrames using index
result = pd.merge(df1, df2, left_index=True, right_index=True)

# Or use .join() - cleaner for index merges
result = df1.join(df2, how='left')

# Mixed: index and column
result = pd.merge(df1, df2, left_on='id', right_index=True)
```

### 7. Cross Join (Cartesian Product)

```python
# Every combination of rows from both DataFrames
result = pd.merge(df1, df2, how='cross')

# Useful for generating combinations
dates = pd.DataFrame({'date': pd.date_range('2024-01-01', periods=7)})
products = pd.DataFrame({'product': ['A', 'B', 'C']})
combinations = pd.merge(dates, products, how='cross')
```

### 8. Concat with Keys for Multi-Index

```python
# Stack with hierarchical index to track source
result = pd.concat(
    [df_2020, df_2021, df_2022],
    keys=['2020', '2021', '2022'],
    names=['year', 'row_id']
)

# Access specific year
result.loc['2021']
```

### 9. Ignore Index When Concatenating

```python
# ❌ Will keep original indices (can cause duplicates)
result = pd.concat([df1, df2])

# ✅ Create fresh sequential index
result = pd.concat([df1, df2], ignore_index=True)
```

### 10. Concat Only Matching Columns

```python
# inner: only columns present in ALL DataFrames
result = pd.concat([df1, df2, df3], join='inner')

# outer (default): all columns, fills NaN for missing
result = pd.concat([df1, df2, df3], join='outer')
```

---

## 🚀 Advanced Techniques

### Merge with Tolerance (Nearest Match)

```python
# For time-series or numeric approximate matching
pd.merge_asof(
    trades,
    quotes,
    on='timestamp',
    by='ticker',
    direction='backward',  # 'forward', 'nearest'
    tolerance=pd.Timedelta('10ms')
)
```

### Multiple DataFrames in One Go

```python
from functools import reduce

dfs = [df1, df2, df3, df4]

# Sequential merge
result = reduce(
    lambda left, right: pd.merge(left, right, on='id', how='outer'),
    dfs
)
```

### Conditional Merge Logic

```python
# Only merge if price difference is within 5%
def custom_merge(df1, df2):
    merged = pd.merge(df1, df2, on='product', suffixes=('_a', '_b'))
    mask = abs(merged['price_a'] - merged['price_b']) / merged['price_a'] <= 0.05
    return merged[mask]
```

### Update DataFrame with Another

```python
# Update df1 with values from df2 where they overlap
df1.update(df2)

# Or use combine_first to fill only NaN values
result = df1.combine_first(df2)
```

---

## ⚡ Performance Tips

| Technique | When to Use | Speedup |
|-----------|-------------|---------|
| Set index before joining | Joining on same column repeatedly | 5-10x |
| Use categorical dtype for join keys | Large DataFrames with repeated values | 2-5x |
| Sort before `merge_asof` | Required for `merge_asof` to work | N/A |
| Use `merge` instead of `apply` + `map` | Lookups/enrichment | 10-100x |

```python
# Set index once, then join multiple times
df1_indexed = df1.set_index('id')
df2_indexed = df2.set_index('id')

result1 = df1_indexed.join(df2_indexed)
result2 = df1_indexed.join(df3_indexed)  # Fast second join
```

---

## 🎓 Common Patterns

### Left Join and Fill Missing Values

```python
result = pd.merge(df1, df2, on='id', how='left')
result['col_from_df2'] = result['col_from_df2'].fillna(0)
```

### Check for Unmatched Rows

```python
merged = pd.merge(df1, df2, on='id', how='outer', indicator=True)

# Rows in df1 but not in df2
unmatched_left = merged[merged['_merge'] == 'left_only']

# Rows in df2 but not in df1
unmatched_right = merged[merged['_merge'] == 'right_only']
```

### Stacking DataFrames with Source Label

```python
df1['source'] = 'dataset_A'
df2['source'] = 'dataset_B'
combined = pd.concat([df1, df2], ignore_index=True)
```

### Enrich Data with Lookup Table

```python
# Add country names to country codes
country_lookup = pd.DataFrame({
    'code': ['US', 'UK', 'CA'],
    'name': ['United States', 'United Kingdom', 'Canada']
})

df_enriched = pd.merge(df, country_lookup, left_on='country_code', right_on='code', how='left')
```

---

## 🔥 Merge vs Join vs Concat

| Method | Best For | Key Difference |
|--------|----------|----------------|
| `pd.merge()` | Combining on columns | Most flexible, SQL-like |
| `.join()` | Combining on index | Cleaner syntax for index joins |
| `pd.concat()` | Stacking DataFrames | Vertical/horizontal concatenation |
| `pd.merge_asof()` | Time-series fuzzy matching | Nearest match within tolerance |

---

**Next:** Learn reshaping in [04_reshape_pivot.md](04_reshape_pivot.md)!
