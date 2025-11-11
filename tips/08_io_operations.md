# Data I/O Operations Guide

Master reading and writing data in multiple formats with pandas.

---

## 🎯 Quick Reference

| Format | Read | Write |
|--------|------|-------|
| **CSV** | `pd.read_csv()` | `df.to_csv()` |
| **Excel** | `pd.read_excel()` | `df.to_excel()` |
| **JSON** | `pd.read_json()` | `df.to_json()` |
| **Parquet** | `pd.read_parquet()` | `df.to_parquet()` |
| **SQL** | `pd.read_sql()` | `df.to_sql()` |
| **HTML** | `pd.read_html()` | `df.to_html()` |
| **Clipboard** | `pd.read_clipboard()` | `df.to_clipboard()` |

---

## 💡 Pro Tips

### 1. CSV: Fast and Efficient Reading

```python
# Basic read
df = pd.read_csv('data.csv')

# Specify dtypes for speed and memory savings
df = pd.read_csv('data.csv', dtype={'id': 'int32', 'category': 'category'})

# Parse dates automatically
df = pd.read_csv('data.csv', parse_dates=['date_column'])

# Skip rows
df = pd.read_csv('data.csv', skiprows=3)

# Read only specific columns
df = pd.read_csv('data.csv', usecols=['name', 'age', 'salary'])

# Handle different delimiters
df = pd.read_csv('data.tsv', sep='\t')

# Read compressed files
df = pd.read_csv('data.csv.gz', compression='gzip')
```

### 2. CSV: Memory-Efficient Chunking

```python
# Read in chunks (for huge files)
chunk_size = 100000
chunks = []

for chunk in pd.read_csv('huge_file.csv', chunksize=chunk_size):
    # Process each chunk
    chunk_filtered = chunk[chunk['status'] == 'active']
    chunks.append(chunk_filtered)

df = pd.concat(chunks, ignore_index=True)
```

### 3. CSV: Writing Options

```python
# Basic write
df.to_csv('output.csv', index=False)

# Specify encoding
df.to_csv('output.csv', encoding='utf-8', index=False)

# Choose delimiter
df.to_csv('output.tsv', sep='\t', index=False)

# Append to existing file
df.to_csv('output.csv', mode='a', header=False, index=False)

# Write only specific columns
df.to_csv('output.csv', columns=['name', 'age'], index=False)

# Compress on write
df.to_csv('output.csv.gz', compression='gzip', index=False)
```

### 4. Excel: Read Multiple Sheets

```python
# Read specific sheet
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Read all sheets into a dictionary
sheets = pd.read_excel('data.xlsx', sheet_name=None)
df_sheet1 = sheets['Sheet1']
df_sheet2 = sheets['Sheet2']

# Read multiple specific sheets
sheets = pd.read_excel('data.xlsx', sheet_name=['Sales', 'Inventory'])

# Skip rows and use specific columns
df = pd.read_excel('data.xlsx', skiprows=2, usecols='A:D')
```

### 5. Excel: Write Multiple Sheets

```python
# Write single sheet
df.to_excel('output.xlsx', sheet_name='Data', index=False)

# Write multiple sheets
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df1.to_excel(writer, sheet_name='Sales', index=False)
    df2.to_excel(writer, sheet_name='Inventory', index=False)
    df3.to_excel(writer, sheet_name='Summary', index=False)

# Append to existing Excel file
with pd.ExcelWriter('existing.xlsx', mode='a', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='NewSheet', index=False)
```

### 6. Parquet: Fast and Compact

```python
# Write Parquet (smaller, faster than CSV)
df.to_parquet('data.parquet', compression='snappy')

# Read Parquet
df = pd.read_parquet('data.parquet')

# Read specific columns only (very fast!)
df = pd.read_parquet('data.parquet', columns=['name', 'age', 'salary'])

# Compression options: 'snappy', 'gzip', 'brotli'
df.to_parquet('data.parquet', compression='gzip')
```

**Why Parquet?**
- 5-10x smaller than CSV
- 10-100x faster to read/write
- Preserves data types
- Column-wise compression

### 7. JSON: Read and Write

```python
# Read JSON
df = pd.read_json('data.json')

# Handle different orientations
df = pd.read_json('data.json', orient='records')
# orient options: 'split', 'records', 'index', 'columns', 'values'

# Read from JSON string
json_string = '{"name": ["Alice", "Bob"], "age": [25, 30]}'
df = pd.read_json(json_string)

# Write JSON
df.to_json('output.json', orient='records', indent=2)

# Write as JSON lines (newline-delimited JSON)
df.to_json('output.jsonl', orient='records', lines=True)
```

### 8. SQL: Read from Database

```python
import sqlite3

# SQLite example
conn = sqlite3.connect('database.db')
df = pd.read_sql('SELECT * FROM users WHERE age > 25', conn)
conn.close()

# PostgreSQL example (requires psycopg2)
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:password@localhost:5432/mydb')
df = pd.read_sql('SELECT * FROM sales', engine)

# Read entire table
df = pd.read_sql_table('users', engine)

# Read with query
query = '''
    SELECT u.name, o.total 
    FROM users u 
    JOIN orders o ON u.id = o.user_id
    WHERE o.date > '2024-01-01'
'''
df = pd.read_sql(query, engine)
```

### 9. SQL: Write to Database

```python
import sqlite3

conn = sqlite3.connect('database.db')

# Write DataFrame to SQL table
df.to_sql('users', conn, if_exists='replace', index=False)
# if_exists options: 'fail', 'replace', 'append'

# Append to existing table
df.to_sql('users', conn, if_exists='append', index=False)

conn.close()

# With SQLAlchemy
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:password@localhost:5432/mydb')
df.to_sql('sales', engine, if_exists='append', index=False)
```

### 10. Clipboard: Quick Copy-Paste

```python
# Copy from clipboard (from Excel, Google Sheets, etc.)
df = pd.read_clipboard()

# Copy to clipboard
df.to_clipboard(index=False)

# Then paste into Excel/Sheets with Ctrl+V
```

---

## 🚀 Advanced I/O Techniques

### Read HTML Tables from Web

```python
# Read all tables from a webpage
tables = pd.read_html('https://example.com/data-page')

# Get first table
df = tables[0]

# With requests for authentication
import requests
response = requests.get('https://example.com/data', headers={'Authorization': 'Bearer token'})
tables = pd.read_html(response.content)
df = tables[0]
```

### Feather: Fast for Temporary Storage

```python
# Write Feather (fastest I/O, preserves types)
df.to_feather('data.feather')

# Read Feather
df = pd.read_feather('data.feather')

# Great for intermediate results in pipelines
```

### HDF5: Large Datasets

```python
# Write to HDF5
df.to_hdf('data.h5', key='df', mode='w')

# Read from HDF5
df = pd.read_hdf('data.h5', 'df')

# Append to existing HDF5
df.to_hdf('data.h5', key='df2', mode='a')

# Fixed vs table format
df.to_hdf('data.h5', key='df', format='table')  # Queryable
```

### Pickle: Fastest for Pandas Objects

```python
# Write pickle (preserves all pandas features)
df.to_pickle('data.pkl')

# Read pickle
df = pd.read_pickle('data.pkl')

# ⚠️ Warning: Only use pickle for trusted data sources
# Pickle can execute arbitrary code
```

---

## ⚡ Performance Comparison

| Format | Read Speed | Write Speed | File Size | Best For |
|--------|------------|-------------|-----------|----------|
| **CSV** | Slow | Medium | Large | Compatibility |
| **Parquet** | Very Fast | Very Fast | Small | Production |
| **Feather** | Fastest | Fastest | Medium | Temporary |
| **Pickle** | Very Fast | Very Fast | Medium | Pandas-specific |
| **HDF5** | Fast | Fast | Small | Large datasets |
| **JSON** | Slow | Medium | Large | APIs, web |
| **Excel** | Very Slow | Slow | Medium | Business users |

---

## 🎓 Common Patterns

### Read CSV with Custom Settings

```python
df = pd.read_csv(
    'data.csv',
    sep=',',
    encoding='utf-8',
    parse_dates=['date'],
    dtype={'id': 'int32', 'category': 'category'},
    na_values=['NA', 'N/A', 'null', ''],
    thousands=',',
    decimal='.',
    usecols=['id', 'name', 'date', 'amount'],
    skiprows=1,
    nrows=10000,  # Read first 10k rows only
)
```

### Export for Excel Users

```python
# Clean format for Excel
with pd.ExcelWriter('report.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
    
    # Get workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Data']
    
    # Add formatting
    header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
    worksheet.set_row(0, None, header_format)
    
    # Auto-fit columns
    for i, col in enumerate(df.columns):
        column_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
        worksheet.set_column(i, i, column_len)
```

### Backup Before Overwrite

```python
import os
from datetime import datetime

# Create timestamped backup
if os.path.exists('data.csv'):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'data_backup_{timestamp}.csv'
    os.rename('data.csv', backup_name)

# Write new file
df.to_csv('data.csv', index=False)
```

### Read from URL

```python
# Read CSV from URL
url = 'https://example.com/data.csv'
df = pd.read_csv(url)

# Read Excel from URL
url = 'https://example.com/data.xlsx'
df = pd.read_excel(url)

# Read JSON from API
import requests
response = requests.get('https://api.example.com/data')
df = pd.DataFrame(response.json())
```

---

## 🔥 Best Practices

### File Format Selection

```python
# For production pipelines: Parquet
df.to_parquet('data.parquet', compression='snappy')

# For sharing with non-technical users: Excel
df.to_excel('report.xlsx', index=False)

# For temporary storage between scripts: Feather or Pickle
df.to_feather('temp.feather')

# For APIs and web: JSON
df.to_json('api_response.json', orient='records')

# For archival: CSV with compression
df.to_csv('archive.csv.gz', compression='gzip', index=False)
```

### Error Handling

```python
import os

try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    print("File not found!")
    df = pd.DataFrame()  # Empty DataFrame
except pd.errors.EmptyDataError:
    print("File is empty!")
    df = pd.DataFrame()
except Exception as e:
    print(f"Error reading file: {e}")
    df = pd.DataFrame()

# Check if file exists before reading
if os.path.exists('data.csv'):
    df = pd.read_csv('data.csv')
else:
    print("File does not exist")
```

---

## 📊 Real-World Example: ETL Pipeline

```python
import pandas as pd
from sqlalchemy import create_engine

# Extract: Read from multiple sources
df_csv = pd.read_csv('sales_data.csv', parse_dates=['date'])
df_excel = pd.read_excel('inventory.xlsx', sheet_name='Current')
df_json = pd.read_json('customers.json')

# Transform: Clean and merge
df_csv['date'] = pd.to_datetime(df_csv['date'])
df_merged = df_csv.merge(df_excel, on='product_id', how='left')
df_final = df_merged.merge(df_json, on='customer_id', how='left')

# Load: Write to database and backup
engine = create_engine('postgresql://user:pass@localhost:5432/db')
df_final.to_sql('sales_enriched', engine, if_exists='replace', index=False)

# Backup as Parquet
df_final.to_parquet(f'backup_{pd.Timestamp.now():%Y%m%d}.parquet')

print(f"✅ Processed {len(df_final)} records")
```

---

**🎉 You've mastered pandas I/O operations!** Check out [01_selection_filtering.md](01_selection_filtering.md) to continue exploring!
