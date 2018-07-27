# pysigsci

[![Latest Version](https://img.shields.io/pypi/v/pysigsci.svg)](https://pypi.python.org/pypi/pysigsci/)
[![Build Status](https://travis-ci.org/foospidy/pysigsci.svg?branch=master)](https://travis-ci.org/foospidy/pysigsci)

Python module and CLI tool for the [Signal Sciences](https://docs.signalsciences.net/api/) API.

### Installation

`pip install pysigsci`

### CLI Usage

`$ pysigsci --get requests`

To see all options run: `$ pysigsci --help`

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

### CLI Configuration Audit Tool

Use the command `pysigscia` to audit configuration across sites. This provides basic functionality to help ensure your
configurations are consistent.

#### Usage

First download all configurations with the following command:

```
$ pysigscia --get-config
```

Next, run the command options that suits your needs. When specifying a site name use the "short name".

Compare a site to all other sites, for all configurations:

```
$ pysigscia --compare <site_name>
```

Compare a site to one other site, for all configurations:

```
$ pysigscia --compare <site_name> --to <site_name>
```

Compare a site to all other sites, for a specific configuration:

```
$ pysigscia --compare <site_name> --configs request_rules
```

Compare a site to one other site, for a specific configuration:

```
$ pysigscia --compare <site_name> --to <site_name> --configs redactions
```

When specifying a specific config the following are supported:

- request_rules
- signal_rules
- templated_rules
- advanced_rules
- redactions
- custom_signals
- custom_alerts
- header_links
- integrations

#### Output

The `pysigscia` command outputs to standard out. For large configuration data, it will be best to redirect the output to a text file for review, example: `$ pysigscia --compare <site_name> > $HOME/Desktop/sigsci_config_audit.txt`