# PyOpenFigi

Unofficial Python wrapper for the [OpenFIGI API](https://www.openfigi.com/api) v3.

The wrapper is build with `requests` for HTTP requests and `Pydantic` for object modeling.

## API description

The OpenFIGI API can be used with or without API key.
Getting an API key is free and loosens the [rate limits](https://www.openfigi.com/api#rate-limit).

| endpoint | description                                                                                |
|----------|--------------------------------------------------------------------------------------------|
| mapping  | Map third-party identifiers to FIGIs                                                       |
| search   | Search for FIGIs using keywords and optional filters                                       |
| filter   | Search for FIGIs using keywords and optional filters (contains the total number of results |

## Installation

PyOpenFigi is published on PyPi. To install it, simply run:

```commandline
pip install pyopenfigi
```

## Usage

### The `mapping` endpoint

Maps third-party identifiers to FIGIS.
The method takes a list of `MappingJob` objects as argument and returns a list of `MappingJobResult`. The result of
the request located at index i in the list of mapping jobs is located at index i in the list of results.

```python
from pyopenfigi import OpenFigi, MappingJob

mapping_job = MappingJob(id_type="TICKER", id_value="IBM", exch_code="US")
mapping_jobs = [mapping_job]
results = OpenFigi().map(mapping_jobs)
```
```commandline
>>> results
[MappingJobResultFigiList(data=[FigiResult(figi='BBG000BLNNH6', security_type='Common Stock', market_sector='Equity', ticker='IBM', name='INTL BUSINESS MACHINES CORP', exch_code='US', share_class_figi='BBG001S5S399', composite_figi='BBG000BLNNH6', security_type2='Common Stock', security_description='IBM', metadata=None)])]
```

### The `MappingJob` object

The `MappingJob` object only has 2 required fields which are `id_type` and `id_value`. The other fields are optional
but subject to specific rules in case they are provided. The rules are modeled with `Pydantic`.

There is a list of examples for common use cases.

### The _Enum-like_ properties

Some of the properties in the `MappingJob` objects are "enum-like". For each of these properties, it is possible to
retrieve the current list of accepted values via specific methods:

| property        | method                   | description |
|-----------------|--------------------------|-------------|
| id_type         | `get_id_types()`         |             |
| exch_code       | `get_exch_codes()`       |             |
| mic_code        | `get_mic_codes()`        |             |
| currency        | `get_currencies()`       |             |
| market_sec_des  | `get_market_sec_des()`   |             |
| security_type   | `get_security_types()`   |             |
| security_type_2 | `get_security_types_2()` |             |
| state_code      | `get_state_codes()`      |             |

### The `filter` endpoint

Note: max 15000 results (all US tickers)

## Troubleshooting

### Exceptions

Several kinds of errors can occur.

The `MappingJob` and `Query` are modeled as *Pydantic* objects and therefore need to be properly instantiated. 
If an error occurs, a `ValidationError` from *Pydantic* will be raised. 
In case these objects are instantiated programmatically, it could be worth checking for exceptions as follows:

```python3
from pydantic import ValidationError

from pyopenfigi import MappingJob

tickers = ["IBM", "XRX", "TSLA", None, "MSFT"]

mapping_jobs = []
for ticker in tickers:
    try:
        mapping_job = MappingJob(id_type="TICKER", id_value=ticker, exch_code="US")
        mapping_jobs.append(mapping_job)
    except ValidationError:
        print(f"Error when trying to build a MappingJob with {ticker=}")
        continue
```

In case the status code of the HTTP response is not 200, an HTTPError exception will be raised.

```python
from pyopenfigi import OpenFigi
from pyopenfigi.exceptions import HTTPError

try:
    results = OpenFigi().map(mapping_jobs)

except HTTPError as e:
    print(f"{e}")
```



