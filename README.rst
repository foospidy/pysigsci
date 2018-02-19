Signal Sciences
==================

.. image:: https://img.shields.io/pypi/v/pysigsci.svg
    :target: https://pypi.python.org/pypi/pysigsci/
    :alt: Latest Version

.. image:: https://travis-ci.org/pyca/pysigsci.svg?branch=master
    :target: https://travis-ci.org/pyca/pysigsci

``pysigsci`` is a Python wrapper and CLI tool for the `Signal Sciences REST API`_.

Installation
------------
.. code-block:: bash

    $ pip install pysigsci

CLI usage
---------
.. code-block:: bash

    $ pysigsci --get requests

Module usage
------------
.. code-block:: python

    from pysigsci import sigsciapi
    sigsci = sigsciapi.SigSciApi("myemail", "mypassword")
    sigsci.corp = "mycorp"
    sigsci.site = "mysite"

    params = {"q": "from:-1d tag:XSS"}
    print(sigsci.get_requests(parameters=params))

More details and the latest updates can be found on the `GitHub Project Page`_.

.. _Signal Sciences REST API: https://docs.signalsciences.net/api/
.. _GitHub Project Page: https://github.com/foospidy/pysigsci