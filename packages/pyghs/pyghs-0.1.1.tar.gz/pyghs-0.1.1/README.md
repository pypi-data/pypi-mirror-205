# GHS

Storage csv file in github repository.

## Installation

```bash
pip install pyghs
```

## Usage

```python
from ghs import GHS
import pandas as pd
import asyncio

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

# Create a GHS instance
ghs = GHS("YOUR_GITHUB_TOKEN", "YOUR_GITHUB_REPOSITORY")
# Create a csv file in github repository
asyncio.run(ghs.create("test.csv", df))

# Get a csv file from github repository
df = asyncio.run(ghs.get("test.csv"))
print(df)

asyncio.run(ghs.close())
```

This prints:

```bash
   a  b
0  1  4
1  2  5
2  3  6
```
