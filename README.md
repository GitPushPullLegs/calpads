# CALPADS

## Setup

Install dependencies by running `pip install -r src/requirements.txt`

##  How to use

```python
from src.client import CALPADS

# Start the client with your CALPADS credentials
client = CALPADS(username="USERNAME", password="PASSWORD")

# Execute any method from the extensions directory like so:
leas = client.core.get_leas()
print(leas)

# or

janes_demographics = client.student.demographics(ssid=12345)
print(janes_demographics)
```