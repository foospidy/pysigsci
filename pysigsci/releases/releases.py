"""
Signal Sciences Releases Module
"""

import requests


MODULES = ['apache',
           'dotnet',
           'golang',
           'haproxy',
           'iis',
           'java',
           'nginx',
           'nodejs',
           'php',
           'python']

def get_latest_module_versions():
    """
    Returns lastest module versions
    """

    module_dict = {}

    for module in MODULES:
        module_dict[module] = get_latest_module_version(module)

    return module_dict

def get_latest_module_version(module='apache'):
    """
    Returns lastest version of provided module
    """

    url = 'https://dl.signalsciences.net/sigsci-module-{}/VERSION'.format(module)
    response = requests.get(url)
    return response.text.strip()

def get_latest_agent_version():
    """
    Returns lastest version agent
    """

    response = requests.get('https://dl.signalsciences.net/sigsci-agent/VERSION')
    return response.text.strip()
