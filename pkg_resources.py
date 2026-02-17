"""Compatibility shim: expose pkg_resources when it's not importable directly
on this Python/setuptools/pip combination by forwarding to pip's vendored copy.
"""
try:
    from pip._vendor import pkg_resources as _pkg_resources
except Exception:
    _pkg_resources = None

if _pkg_resources is None:
    raise ImportError('pkg_resources compatibility shim could not find pip._vendor.pkg_resources')

from pip._vendor.pkg_resources import *
