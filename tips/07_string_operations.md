# String & Regex Operations Guide

Master text manipulation and pattern matching in pandas with powerful string methods.

---

## 🎯 Quick Reference

| Operation | Method | Example |
|-----------|--------|---------|
| Case conversion | `.str.lower()` / `.upper()` | `df['name'].str.upper()` |
| Contains pattern | `.str.contains()` | `df['email'].str.contains('@gmail')` |
| Replace text | `.str.replace()` | `df['text'].str.replace('old', 'new')` |
| Extract with regex | `.str.extract()` | `df['code'].str.extract(r'(\d{3})')` |
| Split string | `.str.split()` | `df['name'].str.split(' ')` |
| Strip whitespace | `.str.strip()` | `df['text'].str.strip()` |

---

## 💡 Pro Tips

### 1. Case Conversion

```python
# Convert to lowercase
df['name'] = df['name'].str.lower()

# Convert to uppercase
df['code'] = df['code'].str.upper()

# Title case (first letter of each word capitalized)
df['title'] = df['title'].str.title()

# Capitalize (only first letter)
df['sentence'] = df['sentence'].str.capitalize()
```

### 2. Check for Pattern Presence

```python
# Contains substring (case-sensitive)
df['is_gmail'] = df['email'].str.contains('@gmail.com')

# Case-insensitive
df['has_python'] = df['skills'].str.contains('python', case=False)

# Handle NaN values
df['has_pattern'] = df['text'].str.contains('pattern', na=False)

# Regex pattern
df['has_digits'] = df['text'].str.contains(r'\d+', regex=True)
```

### 3. String Replacement

```python
# Simple replacement
df['clean'] = df['text'].str.replace('old', 'new')

# Case-insensitive replacement
df['clean'] = df['text'].str.replace('old', 'new', case=False)

# Regex replacement (remove all digits)
df['no_digits'] = df['text'].str.replace(r'\d+', '', regex=True)

# Multiple replacements
df['clean'] = df['text'].str.replace(r'[^\w\s]', '', regex=True)  # Remove punctuation
```

### 4. Extract with Regex

```python
# Extract first match
df['area_code'] = df['phone'].str.extract(r'(\d{3})')

# Extract multiple groups
df[['first', 'last']] = df['name'].str.extract(r'(\w+)\s+(\w+)')

# Extract all matches (returns list)
df['all_numbers'] = df['text'].str.findall(r'\d+')

# Extract email domain
df['domain'] = df['email'].str.extract(r'@(.+)')
```

### 5. Split and Expand

```python
# Split and get specific part
df['first_name'] = df['full_name'].str.split(' ').str[0]
df['last_name'] = df['full_name'].str.split(' ').str[-1]

# Expand into multiple columns
df[['first', 'last']] = df['name'].str.split(' ', n=1, expand=True)

# Split by regex pattern
df['parts'] = df['text'].str.split(r'[,;]')

# Reverse split (from right)
df['extension'] = df['filename'].str.rsplit('.', n=1).str[-1]
```

### 6. Strip and Clean

```python
# Remove leading/trailing whitespace
df['clean'] = df['text'].str.strip()

# Remove specific characters from ends
df['clean'] = df['text'].str.strip('.,!? ')

# Remove leading whitespace only
df['clean'] = df['text'].str.lstrip()

# Remove trailing whitespace only
df['clean'] = df['text'].str.rstrip()
```

### 7. String Length and Padding

```python
# Get length
df['name_length'] = df['name'].str.len()

# Pad with zeros (left)
df['id_padded'] = df['id'].astype(str).str.zfill(5)  # '3' → '00003'

# Pad with spaces
df['padded'] = df['text'].str.pad(width=10, side='left', fillchar='0')

# Center text
df['centered'] = df['text'].str.center(width=20, fillchar=' ')
```

### 8. StartsWith and EndsWith

```python
# Check prefix
df['is_admin'] = df['username'].str.startswith('admin_')

# Check suffix
df['is_python_file'] = df['filename'].str.endswith('.py')

# Multiple options
df['is_code'] = df['filename'].str.endswith(('.py', '.js', '.java'))
```

### 9. Slice Strings

```python
# Get first 3 characters
df['prefix'] = df['code'].str[:3]

# Get last 3 characters
df['suffix'] = df['code'].str[-3:]

# Slice range
df['middle'] = df['text'].str[5:10]

# Get character at position
df['first_char'] = df['text'].str[0]
```

### 10. Join and Concatenate

```python
# Join with delimiter
df['full_address'] = df['street'] + ', ' + df['city'] + ', ' + df['state']

# Using str.cat
df['full_name'] = df['first_name'].str.cat(df['last_name'], sep=' ')

# Join with Series
df['combined'] = df['col1'].str.cat([df['col2'], df['col3']], sep=' | ')
```

---

## 🚀 Advanced Regex Patterns

### Email Extraction

```python
# Extract email addresses
df['email'] = df['text'].str.extract(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')

# Validate email format
df['is_valid_email'] = df['email'].str.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
```

### Phone Number Patterns

```python
# Extract US phone numbers
df['phone'] = df['text'].str.extract(r'(\d{3}[-.]?\d{3}[-.]?\d{4})')

# Normalize phone format
df['phone_clean'] = df['phone'].str.replace(r'\D', '', regex=True)  # Remove non-digits

# Format as (123) 456-7890
df['phone_formatted'] = df['phone_clean'].str.replace(
    r'(\d{3})(\d{3})(\d{4})', 
    r'(\1) \2-\3',
    regex=True
)
```

### URL Parsing

```python
# Extract domain from URL
df['domain'] = df['url'].str.extract(r'https?://(?:www\.)?([^/]+)')

# Extract protocol
df['protocol'] = df['url'].str.extract(r'(https?|ftp)://')

# Extract path
df['path'] = df['url'].str.extract(r'https?://[^/]+(/.*)')
```

### Price and Currency

```python
# Extract prices
df['price'] = df['text'].str.extract(r'\$?([\d,]+\.?\d*)')

# Clean and convert to float
df['price_float'] = df['price'].str.replace(',', '').astype(float)

# Extract currency symbol
df['currency'] = df['text'].str.extract(r'([$€£¥])')
```

---

## ⚡ Performance Tips

| Tip | Speedup |
|-----|---------|
| Use `.str.contains()` instead of `.apply(lambda x: 'text' in x)` | 10-20x |
| Compile regex once with `re.compile()` for repeated use | 2-5x |
| Use categorical dtype for string columns with few unique values | 2-5x |
| Avoid `.str` accessor in loops – vectorize instead | 100x+ |

```python
import re

# ❌ Slow: compile regex every time
df['match'] = df['text'].str.contains(r'complex\s+pattern\s+\d+')

# ✅ Fast: compile once
pattern = re.compile(r'complex\s+pattern\s+\d+')
df['match'] = df['text'].str.contains(pattern)
```

---

## 🎓 Common Patterns

### Clean Text Data

```python
def clean_text(text_series):
    """Comprehensive text cleaning"""
    return (text_series
            .str.lower()                          # Lowercase
            .str.strip()                          # Remove leading/trailing space
            .str.replace(r'\s+', ' ', regex=True) # Collapse multiple spaces
            .str.replace(r'[^\w\s]', '', regex=True) # Remove punctuation
           )

df['clean_text'] = clean_text(df['raw_text'])
```

### Extract Numbers from Text

```python
# Extract all numbers as list
df['numbers'] = df['text'].str.findall(r'\d+')

# Get first number
df['first_number'] = df['text'].str.extract(r'(\d+)').astype(float)

# Sum all numbers in text
df['total'] = df['text'].str.findall(r'\d+').apply(lambda x: sum(int(i) for i in x) if x else 0)
```

### Split Name into Parts

```python
# Handle "Last, First Middle"
df[['last', 'first_middle']] = df['name'].str.split(',', n=1, expand=True)
df['first'] = df['first_middle'].str.split().str[0]
df['middle'] = df['first_middle'].str.split().str[1:].str.join(' ')
```

### Normalize Whitespace

```python
# Replace multiple spaces with single space
df['text'] = df['text'].str.replace(r'\s+', ' ', regex=True)

# Remove all whitespace
df['no_space'] = df['text'].str.replace(r'\s', '', regex=True)
```

### Create Slug from Title

```python
def slugify(text_series):
    """Convert title to URL-friendly slug"""
    return (text_series
            .str.lower()
            .str.replace(r'[^\w\s-]', '', regex=True)
            .str.replace(r'[\s_]+', '-', regex=True)
            .str.strip('-')
           )

df['slug'] = slugify(df['title'])
# "Hello World!" → "hello-world"
```

---

## 🔥 Regex Cheat Sheet

| Pattern | Meaning | Example |
|---------|---------|---------|
| `\d` | Any digit | `\d{3}` matches "123" |
| `\w` | Word character | `\w+` matches "hello" |
| `\s` | Whitespace | `\s+` matches spaces/tabs |
| `[abc]` | Any of a, b, c | `[aeiou]` matches vowels |
| `[^abc]` | Not a, b, or c | `[^0-9]` matches non-digits |
| `+` | One or more | `\d+` matches "123" |
| `*` | Zero or more | `\w*` matches "" or "hello" |
| `?` | Zero or one | `colou?r` matches "color" or "colour" |
| `{n}` | Exactly n | `\d{4}` matches "2024" |
| `{n,m}` | Between n and m | `\d{2,4}` matches "12" to "1234" |
| `^` | Start of string | `^\d` matches digit at start |
| `$` | End of string | `\d$` matches digit at end |
| `\|` | OR | `cat\|dog` matches "cat" or "dog" |
| `()` | Capture group | `(\d{3})-(\d{4})` captures parts |

---

## 📊 Real-World Example: Clean Contact Data

```python
# Raw data
# name           | phone          | email
# "  JOHN DOE  " | "123-456-7890" | "JOHN@GMAIL.COM"

# Clean names
df['name'] = df['name'].str.strip().str.title()

# Normalize phone numbers
df['phone_clean'] = (df['phone']
                     .str.replace(r'\D', '', regex=True)  # Remove non-digits
                     .str.replace(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', regex=True))

# Normalize emails
df['email'] = df['email'].str.lower().str.strip()

# Extract domain
df['email_provider'] = df['email'].str.extract(r'@(.+)')

# Validate email
df['valid_email'] = df['email'].str.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
```

---

**Next:** Master data I/O in [08_io_operations.md](08_io_operations.md)!
