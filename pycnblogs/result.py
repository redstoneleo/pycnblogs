"""Result type for API operations (similar to Rust's Result)."""

from typing import TypeVar, Generic, Optional, Union, Dict, Any
from dataclasses import dataclass
import json

T = TypeVar('T')
E = TypeVar('E')


@dataclass
class Ok(Generic[T]):
    """Success result."""
    value: T
    
    def is_ok(self) -> bool:
        return True
    
    def is_err(self) -> bool:
        return False
    
    def unwrap(self) -> T:
        return self.value
    
    def unwrap_or(self, default: T) -> T:
        return self.value
    
    def unwrap_or_else(self, fn) -> T:
        return self.value


@dataclass
class Err(Generic[E]):
    """Error result."""
    error: E
    status_code: Optional[int] = None
    
    def is_ok(self) -> bool:
        return False
    
    def is_err(self) -> bool:
        return True
    
    def unwrap(self):
        raise RuntimeError(f"Called unwrap on Err: {self.error}")
    
    def unwrap_or(self, default):
        return default
    
    def unwrap_or_else(self, fn):
        return fn(self.error)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert error to dictionary format.
        Returns the original error data if it's JSON, otherwise wraps it.
        """
        try:
            # Try to parse as JSON and return directly
            return json.loads(self.error)
        except (json.JSONDecodeError, TypeError):
            # If not JSON, return as plain text with metadata
            return {
                "message": str(self.error),
                "status_code": self.status_code
            }
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert error to JSON string.
        
        Args:
            indent: JSON indentation level (default: 2)
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    def get_message(self) -> str:
        """Extract error message from error data."""
        if not self.error:
            return f"HTTP {self.status_code}" if self.status_code else "Unknown error"
        
        try:
            error_data = json.loads(self.error)
            
            # Try different message fields
            if "Message" in error_data:
                return error_data["Message"]
            elif "message" in error_data:
                return error_data["message"]
            elif "errors" in error_data and isinstance(error_data["errors"], list):
                return ", ".join(str(e) for e in error_data["errors"])
            else:
                return str(self.error)
        except (json.JSONDecodeError, TypeError):
            return str(self.error)


Result = Union[Ok[T], Err[str]]
