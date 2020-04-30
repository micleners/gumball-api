"""
Utility functions
"""
import os
import typing


def update_from_env(mapping: typing.MutableMapping) -> typing.MutableMapping:
    """
    Update values of a provided mapping with vars set in the os environment

    :param mapping: collection of values to update

    >>> conf = {'foo': 'BAR', 'home': 'untouchable', 'HOME': 'some_default'}
    >>> conf is update_from_env(conf)
    True

    >>> conf['HOME'] == os.getenv('HOME')
    True

    """
    for k, v in os.environ.items():
        if k in mapping:
            mapping[k] = v
    return mapping
