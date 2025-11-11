# Performance Optimization Secrets

Speed up your pandas code with these battle-tested optimization techniques.

---

## 🎯 Quick Reference

| Technique | Speedup | When to Use |
|-----------|---------|-------------|
| Vectorization | 10-100x | Replace loops and `.apply()` |
| Categorical dtype | 2-5x | Columns with few unique values |
| `eval()` / `query()` | 2-5x | Complex numerical expressions |
| Chunking | Memory-bound | Process large files incrementally |
| NumPy operations | 5-50x | Numerical computations |
| Avoid chained indexing | 2-10x | Multiple filtering steps |

---

## 💡 Pro Tips

### 1. Vectorization: Avoid Loops at All Costs

```python
# ❌ Slow: looping
total = 0
for idx, row in df.iterrows():
    total += row['value'] * row['quantity']

# ✅ Fast: vectorized
total = (df['value'] * df['quantity']).sum()

# ❌ Slow: apply with lambda
df['total'] = df.apply(lambda row: row['value'] * row['quantity'], axis=1)

# ✅ Fast: vectorized column operations
df['total'] = df['value'] * df['quantity']
```

**Speedup: 10-100x**

### 2. Use Categorical Data Type

```python
# For columns with limited unique values (< 50% unique)
df['category'] = df['category'].astype('category')
df['country'] = df['country'].astype('category')

# Memory savings and faster operations
# Before: object dtype (strings) - slow
# After: category dtype - 2-5x faster groupby, merge, etc.
```

**Benefits:**
- 50-90% less memory
- 2-5x faster groupby operations
- Faster sorting and merging

### 3. Use `eval()` and `query()` for Expressions

```python
# ❌ Standard pandas (slower for complex expressions)
df['result'] = df['a'] + df['b'] * df['c'] - df['d'] / df['e']

# ✅ Faster with eval (uses numexpr under the hood)
df['result'] = df.eval('a + b * c - d / e')

# ❌ Boolean filtering
result = df[(df['a'] > 5) & (df['b'] < 10) & (df['c'] == 'active')]

# ✅ Faster with query
result = df.query('a > 5 and b < 10 and c == "active"')
```

**Speedup: 2-5x for large DataFrames (>100K rows)**

### 4. Read CSV in Chunks

```python
# For files too large for memory
chunk_size = 100000
chunks = []

for chunk in pd.read_csv('huge_file.csv', chunksize=chunk_size):
    # Process each chunk
    chunk_processed = chunk[chunk['status'] == 'active']
    chunks.append(chunk_processed)

result = pd.concat(chunks, ignore_index=True)
```

### 5. Specify dtypes When Reading

```python
# Let pandas infer (slower, uses more memory)
df = pd.read_csv('data.csv')

# Specify dtypes (faster, less memory)
dtypes = {
    'id': 'int32',
    'category': 'category',
    'price': 'float32',
    'date': 'str'  # Parse separately if needed
}

df = pd.read_csv('data.csv', dtype=dtypes)
```

**Memory savings: 50-75%**

### 6. Use NumPy for Numerical Computations

```python
# ❌ Pandas apply
df['result'] = df['values'].apply(lambda x: np.sqrt(x) * 2)

# ✅ Direct NumPy
df['result'] = np.sqrt(df['values'].values) * 2

# Even better: vectorized pandas method
df['result'] = df['values'].pow(0.5) * 2
```

### 7. Avoid Chained Indexing

```python
# ❌ Chained (creates copies, slow)
df[df['age'] > 30]['salary'] = 50000

# ✅ Use .loc (operates on view, fast)
df.loc[df['age'] > 30, 'salary'] = 50000
```

### 8. Use `.values` or `.to_numpy()` for Pure NumPy Speed

```python
# When you don't need pandas features
arr = df['column'].values  # Returns numpy array

# Fastest for pure numerical operations
result = arr * 2 + 10
df['result'] = result
```

### 9. Parallel Processing with Dask

```python
import dask.dataframe as dd

# Convert to Dask DataFrame (lazy evaluation)
ddf = dd.from_pandas(df, npartitions=4)

# Operations are parallelized automatically
result = ddf.groupby('category')['sales'].mean().compute()

# Or read large CSV with Dask
ddf = dd.read_csv('huge_file.csv')
```

### 10. Use `isin()` Instead of Multiple Conditions

```python
# ❌ Slow
df[(df['status'] == 'active') | (df['status'] == 'pending') | (df['status'] == 'review')]

# ✅ Fast
df[df['status'].isin(['active', 'pending', 'review'])]
```

---

## 🚀 Advanced Optimization

### Memory-Efficient Downcasting

```python
def downcast_dtypes(df):
    """Reduce memory by downcasting numeric types"""
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df

# Example: int64 → int8 saves 87.5% memory
df = downcast_dtypes(df)
```

### Use `map()` for Simple Transformations

```python
# ❌ Slow: apply
df['category_code'] = df['category'].apply(lambda x: category_mapping[x])

# ✅ Fast: map
category_mapping = {'A': 1, 'B': 2, 'C': 3}
df['category_code'] = df['category'].map(category_mapping)
```

### Efficient String Operations

```python
# Use .str accessor (vectorized)
df['email_domain'] = df['email'].str.split('@').str[1]

# For repeated operations, convert to categorical first
df['category'] = df['category'].astype('category')
```

### Index Optimization

```python
# Set index for repeated lookups
df_indexed = df.set_index('id')

# Fast lookup by index
value = df_indexed.loc[12345]

# Fast filtering on index
subset = df_indexed.loc[10000:20000]
```

---

## ⚡ Performance Comparison Table

| Operation | Slow | Fast | Speedup |
|-----------|------|------|---------|
| Loop with `iterrows()` | `for i, row in df.iterrows()` | Vectorized operations | 100x+ |
| Apply with axis=1 | `df.apply(func, axis=1)` | Vectorized column ops | 10-50x |
| Multiple OR conditions | `(a) \| (b) \| (c)` | `.isin([a,b,c])` | 5-10x |
| String filtering | `.apply(lambda x: 'text' in x)` | `.str.contains('text')` | 10-20x |
| GroupBy on object dtype | `object` dtype | `category` dtype | 2-5x |

---

## 🎓 Profiling & Benchmarking

### Time Your Code

```python
# Magic command in Jupyter
%timeit df['result'] = df['a'] * df['b']

# In scripts
import time
start = time.time()
# ... your code ...
print(f"Elapsed: {time.time() - start:.2f}s")

# More accurate with timeit module
import timeit
timeit.timeit('df["a"] * df["b"]', globals=globals(), number=1000)
```

### Memory Profiling

```python
# Check DataFrame memory usage
df.info(memory_usage='deep')

# Memory per column
df.memory_usage(deep=True)

# Identify memory hogs
df.memory_usage(deep=True).sort_values(ascending=False).head(10)
```

### Line Profiler (Find Bottlenecks)

```python
# Install: pip install line_profiler
# Use %lprun magic in Jupyter

%lprun -f my_function my_function(df)
```

---

## 🔥 Real-World Optimization Example

```python
# ❌ BEFORE: Slow (2.5 seconds for 1M rows)
def slow_process(df):
    result = []
    for idx, row in df.iterrows():
        if row['status'] == 'active' and row['amount'] > 100:
            value = row['amount'] * 1.1 - row['discount']
            result.append(value)
        else:
            result.append(0)
    df['result'] = result
    return df

# ✅ AFTER: Fast (0.02 seconds for 1M rows)
def fast_process(df):
    mask = (df['status'] == 'active') & (df['amount'] > 100)
    df['result'] = 0
    df.loc[mask, 'result'] = df.loc[mask, 'amount'] * 1.1 - df.loc[mask, 'discount']
    return df

# 125x faster! 🚀
```

---

## 📝 Memory-Saving Checklist

- [ ] Use categorical dtype for low-cardinality columns
- [ ] Specify dtypes when reading CSV
- [ ] Downcast numeric types (int64 → int32/int16)
- [ ] Read large files in chunks
- [ ] Delete intermediate DataFrames you don't need
- [ ] Use `del df` and `gc.collect()` to free memory

```python
import gc

# Process in chunks
for chunk in pd.read_csv('huge.csv', chunksize=100000):
    process(chunk)
    del chunk  # Explicit delete
    gc.collect()  # Garbage collection
```

---

## 🎯 Quick Wins Summary

1. **Replace `.apply()` with vectorized operations** → 10-100x faster
2. **Use categorical dtype** → 50-90% less memory
3. **Use `.query()` for complex filters** → 2-5x faster
4. **Specify dtypes when reading** → 50-75% less memory
5. **Use `.isin()` instead of multiple OR** → 5-10x faster

---

**Next:** Master string operations in [07_string_operations.md](07_string_operations.md)!
