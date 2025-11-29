"""
pycnblogs - Python SDK for Cnblogs API

A Python module for interacting with Cnblogs (博客园) API.
"""

# 主客户端
from .client import CnblogsClient

# 数据模型
from .models import PostEntry, UserInfo, IngEntry, NewsEntry, FavEntry

# 异常
from .exceptions import CnblogsError, AuthenticationError, APIError

# Result类型
from .result import Ok, Err, Result

# 辅助函数
from .utils import format_error, print_error

__version__ = "0.2.0"
__all__ = [
    # 客户端
    "CnblogsClient",
    # 数据模型
    "PostEntry",
    "UserInfo",
    "IngEntry",
    "NewsEntry",
    "FavEntry",
    # 异常
    "CnblogsError",
    "AuthenticationError",
    "APIError",
    # Result类型
    "Ok",
    "Err",
    "Result",
    # 辅助函数
    "format_error",
    "print_error",
]
