"""
pysigsciapi module
"""

import datetime
import calendar
from .sigsciapi import SigSciApi

def parse_time_delta(delta):
    """
    Parse "human" readable time to epoch
    Examples: -2d or -1h or -10m
    """
    now = datetime.datetime.utcnow().replace(second=0, microsecond=0)

    if delta.startswith('-'):
        time_value = None
        delta_value = int(delta[1:-1])

        if delta[-1:].lower() == 'd':
            time_value = now - datetime.timedelta(days=delta_value)

        elif delta[-1].lower() == 'h':
            time_value = now - datetime.timedelta(hours=delta_value)

        elif delta[-1].lower() == 'm':
            time_value = now - datetime.timedelta(minutes=delta_value)

        if time_value is not None:
            epoch = calendar.timegm(time_value.utctimetuple())
            return epoch

    return False
