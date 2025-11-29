"""Data models for Cnblogs API responses."""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class PostEntry:
    """Blog post entry."""
    id: int
    title: str
    url: str
    create_time: str
    modify_time: str
    is_draft: bool
    is_pinned: bool
    is_published: bool
    comment_count: Optional[int] = None
    body: Optional[str] = None
    tags: Optional[List[str]] = None
    
    @property
    def full_url(self) -> str:
        """Get full URL with protocol."""
        if self.url.startswith("http"):
            return self.url
        return f"https:{self.url}"


@dataclass
class UserInfo:
    """User information."""
    user_id: str
    space_user_id: int
    blog_id: int
    display_name: str
    face: str
    avatar: str
    seniority: str
    blog_app: str
    following_count: int
    followers_count: int
    is_vip: bool
    joined: str


@dataclass
class IngEntry:
    """Ing (status) entry."""
    id: int
    content: str
    user_alias: str
    user_display_name: str
    create_time: str
    comment_count: int
    lucky_count: int


@dataclass
class IngCommentEntry:
    """Ing comment entry."""
    id: int
    content: str
    user_alias: str
    user_display_name: str
    create_time: str


@dataclass
class NewsEntry:
    """News entry."""
    id: int
    title: str
    summary: str
    url: str
    view_count: int
    comment_count: int
    digg_count: int
    create_time: str
    
    @property
    def full_url(self) -> str:
        """Get full URL with protocol."""
        if self.url.startswith("http"):
            return self.url
        return f"https:{self.url}"


@dataclass
class FavEntry:
    """Favorite (wz) entry."""
    id: int
    title: str
    url: str
    create_time: str
    
    @property
    def full_url(self) -> str:
        """Get full URL with protocol."""
        if self.url.startswith("http"):
            return self.url
        return f"https:{self.url}"
