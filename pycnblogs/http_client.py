"""同步HTTP客户端"""

import requests
from typing import Dict, Any, Union
from .exceptions import APIError, AuthenticationError
from .result import Ok, Err, Result


class HTTPClient:
    """HTTP客户端"""
    
    def __init__(self, pat: str, timeout: float = 30.0):
        self.pat = pat
        self.timeout = timeout
        self.session = requests.Session()
    
    def close(self):
        """关闭会话"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.pat}",
            "Authorization-Type": "pat",
            "Content-Type": "application/json",
        }
    
    def get(self, url: str, raise_on_error: bool = True) -> Union[Dict[str, Any], Result]:
        """发送GET请求"""
        response = self.session.get(url, headers=self._get_headers(), timeout=self.timeout)
        return self._handle_response(response, raise_on_error)
    
    def get_with_params(self, url: str, params: Dict[str, Any], raise_on_error: bool = True) -> Union[Dict[str, Any], Result]:
        """发送带参数的GET请求"""
        response = self.session.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
        return self._handle_response(response, raise_on_error)
    
    def post(self, url: str, json: Dict[str, Any], raise_on_error: bool = False) -> Union[Dict[str, Any], Result]:
        """发送POST请求"""
        response = self.session.post(url, json=json, headers=self._get_headers(), timeout=self.timeout)
        return self._handle_response(response, raise_on_error)
    
    def put(self, url: str, json: Dict[str, Any], raise_on_error: bool = False) -> Union[Dict[str, Any], Result]:
        """发送PUT请求"""
        response = self.session.put(url, json=json, headers=self._get_headers(), timeout=self.timeout)
        return self._handle_response(response, raise_on_error)
    
    def delete(self, url: str, raise_on_error: bool = False) -> Union[Dict[str, Any], Result]:
        """发送DELETE请求"""
        response = self.session.delete(url, headers=self._get_headers(), timeout=self.timeout)
        return self._handle_response(response, raise_on_error)
    
    def _handle_response(self, response: requests.Response, raise_on_error: bool = False) -> Union[Dict[str, Any], Result]:
        """处理响应"""
        if response.status_code == 401:
            if raise_on_error:
                raise AuthenticationError("Invalid PAT token")
            return Err("Invalid PAT token", status_code=401)
        
        if response.status_code >= 400:
            error_text = response.text if response.text else f"HTTP {response.status_code}"
            if raise_on_error:
                raise APIError(f"API request failed: {error_text}", status_code=response.status_code)
            return Err(error_text, status_code=response.status_code)
        
        if response.status_code == 204:
            return {}
        
        try:
            return response.json()
        except Exception:
            return {}
