from .drb_xquery import DrbXQuery
from . import _version
from .drb_xquery_context import DynamicContext

__version__ = _version.get_versions()['version']
__all__ = ['DrbXQuery', 'DynamicContext']
del _version
