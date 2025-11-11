# Selection & Filtering Pro Tips

Master the art of selecting and filtering DataFrames with these essential techniques.

---

## 🎯 Quick Reference

| Technique | Use Case | Example |
|-----------|----------|---------|
| `.loc[]` | Label-based selection | `df.loc[df['age'] > 30, ['name', 'salary']]` |
| `.iloc[]` | Position-based selection | `df.iloc[0:5, [0, 2]]` |
| `.query()` | SQL-like filtering | `df.query('age > 30 and salary < 100000')` |
| `.isin()` | Multiple value matching | `df[df['country'].isin(['USA', 'UK'])]` |
| `.between()` | Range filtering | `df[df['age'].between(25, 35)]` |

---

## 💡 Pro Tips

### 1. Use `.query()` for Readable Complex Filters

Instead of chaining conditions:
```python
# ❌ Hard to read
result = df[(df['age'] > 25) & (df['salary'] > 50000) & (df['dept'] == 'Engineering')]

# ✅ Clean and readable
result = df.query('age > 25 and salary > 50000 and dept == "Engineering"')
```

### 2. Filter with External Variables Using `@`

```python
min_age = 25
departments = ['Engineering', 'Sales']

# Use @ to reference external variables
df.query('age > @min_age and dept in @departments')
```

### 3. Combine `.loc` with Boolean Indexing

```python
# Select specific columns for filtered rows
high_earners = df.loc[df['salary'] > 100000, ['name', 'dept', 'salary']]
```

### 4. Use `.isin()` for Multiple Values

```python
# ❌ Verbose
df[(df['country'] == 'USA') | (df['country'] == 'UK') | (df['country'] == 'Canada')]

# ✅ Concise
df[df['country'].isin(['USA', 'UK', 'Canada'])]
```

### 5. Negate with `~` (Tilde)

```python
# Select rows NOT in the list
df[~df['status'].isin(['inactive', 'pending'])]

# Rows where name doesn't contain 'test'
df[~df['name'].str.contains('test', case=False, na=False)]
```

### 6. Filter by String Patterns

```python
# Starts with
df[df['email'].str.startswith('admin')]

# Contains (case-insensitive)
df[df['name'].str.contains('john', case=False, na=False)]

# Matches regex
df[df['phone'].str.match(r'^\+1-\d{3}-\d{3}-\d{4}$')]
```

### 7. Select Columns by Type

```python
# All numeric columns
numeric_df = df.select_dtypes(include=['number'])

# All object/string columns
text_df = df.select_dtypes(include=['object'])

# Exclude datetime columns
df.select_dtypes(exclude=['datetime'])
```

### 8. Filter Rows with `.between()`

```python
# Ages between 25 and 35 (inclusive)
df[df['age'].between(25, 35)]

# Exclusive bounds
df[df['age'].between(25, 35, inclusive='neither')]
```

### 9. Sample Random Rows

```python
# 10 random rows
df.sample(n=10)

# 10% of the data
df.sample(frac=0.1)

# Reproducible sampling
df.sample(n=100, random_state=42)
```

### 10. Use `.mask()` and `.where()` for Conditional Selection

```python
# Replace values > 100 with NaN
df['salary'].mask(df['salary'] > 100000)

# Keep only values > 50000, replace others with 0
df['salary'].where(df['salary'] > 50000, 0)
```

---

## 🚀 Advanced: Multi-Index Selection

```python
# Set multi-index
df_multi = df.set_index(['country', 'city'])

# Select all rows for USA
df_multi.loc['USA']

# Select specific city in USA
df_multi.loc[('USA', 'New York')]

# Select multiple countries
df_multi.loc[['USA', 'UK']]

# Cross-section: all 'New York' regardless of country
df_multi.xs('New York', level='city')
```

---

## ⚡ Performance Tips

1. **Use `.query()` for large DataFrames** – it's optimized with numexpr
2. **Avoid chained indexing** – use `.loc` instead of `df[df['col'] > 5]['other_col']`
3. **Filter early** – reduce data size before expensive operations
4. **Use categorical dtype** for columns with few unique values

```python
# Convert to categorical for faster filtering
df['country'] = df['country'].astype('category')
```

---

## 🎓 Common Pitfalls

### Chained Assignment Warning
```python
# ❌ Can cause SettingWithCopyWarning
df[df['age'] > 30]['salary'] = 50000

# ✅ Use .loc instead
df.loc[df['age'] > 30, 'salary'] = 50000
```

### Missing Data in String Operations
```python
# ❌ Will raise error if NaN present
df[df['name'].str.contains('John')]

# ✅ Handle NaN explicitly
df[df['name'].str.contains('John', na=False)]
```

---

**Next:** Check out [02_groupby_aggregation.md](02_groupby_aggregation.md) for powerful grouping techniques!
