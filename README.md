# pysigsci

[![Build Status](https://travis-ci.org/foospidy/pysigsci.svg?branch=master)](https://travis-ci.org/foospidy/pysigsci)

Python module and CLI tool for the [Signal Sciences](https://docs.signalsciences.net/api/) API.

### Installation

`pip install pysigsci`

### CLI Usage

`$ pysigsci --get requests`

### Module Usage

```
from pysigsci import sigsciapi
sigsci = sigsciapi.SigSciApi("myemail", "mypassword")
sigsci.corp = "mycorp"
sigsci.site = "mysite"

params = {"q": "from:-1d tag:XSS"}
print(sigsci.get_requests(parameters=params))
```

Also see [example.py](example.py) as a reference.
