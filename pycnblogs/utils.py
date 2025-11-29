"""Utility functions for pycnblogs."""

from typing import Optional
from .result import Err


def format_error(result: Err, prefix: str = "") -> str:
    """
    Format error message in a user-friendly way.
    
    Args:
        result: Err object
        prefix: Prefix for each line (for indentation)
    
    Returns:
        Formatted error message
    """
    error_dict = result.to_dict()
    lines = []
    
    # Handle different error formats
    if "errors" in error_dict and isinstance(error_dict["errors"], list):
        # Format: {"errors": ["error1", "error2"], "type": 0}
        lines.append(f"{prefix}错误:")
        for err in error_dict["errors"]:
            lines.append(f"{prefix}  - {err}")
    elif "Message" in error_dict:
        # Format: {"Message": "error message", "Data": {}, ...}
        lines.append(f"{prefix}错误: {error_dict['Message']}")
    elif "message" in error_dict:
        # Format: {"message": "error message"}
        lines.append(f"{prefix}错误: {error_dict['message']}")
    else:
        # Other formats: show raw JSON
        lines.append(f"{prefix}错误: {result.to_json(indent=None)}")
    
    # Add status code if available
    if result.status_code:
        lines.append(f"{prefix}状态码: {result.status_code}")
    
    return "\n".join(lines)


def print_error(result: Err, prefix: str = ""):
    """
    Print error message in a user-friendly way.
    
    Args:
        result: Err object
        prefix: Prefix for each line (for indentation)
    """
    print(format_error(result, prefix))
