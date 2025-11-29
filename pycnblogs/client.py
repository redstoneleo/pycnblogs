"""博客园客户端"""

from typing import Optional, List, Tuple, Union
from .http_client import HTTPClient
from .models import PostEntry, UserInfo, IngEntry, NewsEntry, FavEntry
from .result import Ok, Err, Result
from .session import save_pat, load_pat, remove_pat
from .constants import BLOG_BACKEND, OPENAPI


class PostAPI:
    """文章API"""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    def get_count(self) -> int:
        """获取文章总数"""
        url = f"{BLOG_BACKEND}/posts/list"
        params = {"t": 1, "p": 1, "s": 1}
        data = self.client.get_with_params(url, params)
        return data.get("postsCount", 0)
    
    def get_one(self, post_id: int) -> PostEntry:
        """获取单篇文章"""
        url = f"{BLOG_BACKEND}/posts/{post_id}"
        data = self.client.get(url)
        
        if "blogPost" in data:
            post_data = data["blogPost"]
        else:
            post_data = data
        
        return PostEntry(
            id=post_data["id"],
            title=post_data["title"],
            url=post_data["url"],
            create_time=post_data["datePublished"],
            modify_time=post_data["dateUpdated"],
            is_draft=post_data["isDraft"],
            is_pinned=post_data["isPinned"],
            is_published=post_data["isPublished"],
            comment_count=post_data.get("feedBackCount"),
            body=post_data.get("postBody"),
            tags=post_data.get("tags"),
        )
    
    def get_list(self, skip: int = 0, take: int = 10) -> Tuple[List[PostEntry], int]:
        """获取文章列表"""
        url = f"{BLOG_BACKEND}/posts/list"
        params = {"t": 1, "p": 1, "s": 1}
        data = self.client.get_with_params(url, params)
        total = data.get("postsCount", 0)
        
        if total == 0:
            return [], 0
        
        posts = []
        start_page = skip + 1
        end_page = min(skip + take, total)
        
        for page in range(start_page, end_page + 1):
            params = {"t": 1, "p": page, "s": 1}
            data = self.client.get_with_params(url, params)
            
            post_list = data.get("postList", [])
            if post_list:
                item = post_list[0]
                posts.append(PostEntry(
                    id=item["id"],
                    title=item["title"],
                    url=item["url"],
                    create_time=item["datePublished"],
                    modify_time=item["dateUpdated"],
                    is_draft=item["isDraft"],
                    is_pinned=item["isPinned"],
                    is_published=item["isPublished"],
                    comment_count=item.get("feedBackCount"),
                ))
        
        return posts, total
    
    def create(self, title: str, body: str, publish: bool = False) -> Union[int, Result]:
        """创建文章"""
        url = f"{BLOG_BACKEND}/posts"
        payload = {
            "postType": 1,
            "title": title,
            "postBody": body,
            "isPublished": publish,
            "displayOnHomePage": True,
        }
        result = self.client.post(url, payload, raise_on_error=False)
        
        if isinstance(result, Err):
            return result
        return result.get("id", 0)
    
    def update(
        self,
        post_id: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        publish: Optional[bool] = None,
    ) -> Union[int, Result]:
        """更新文章"""
        current = self.get_one(post_id)
        
        url = f"{BLOG_BACKEND}/posts"
        payload = {
            "id": post_id,
            "postType": 1,
            "title": title if title is not None else current.title,
            "postBody": body if body is not None else current.body,
            "isPublished": publish if publish is not None else current.is_published,
            "displayOnHomePage": True,
        }
        
        result = self.client.post(url, payload, raise_on_error=False)
        
        if isinstance(result, Err):
            return result
        
        if isinstance(result, dict) and "id" in result:
            return result["id"]
        return post_id
    
    def delete(self, post_id: int) -> Result:
        """删除文章"""
        url = f"{BLOG_BACKEND}/posts/{post_id}"
        result = self.client.delete(url, raise_on_error=False)
        
        if isinstance(result, Err):
            return result
        return Ok(None)


class UserAPI:
    """用户API"""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    def get_info(self) -> UserInfo:
        """获取用户信息"""
        url = f"{OPENAPI}/users"
        data = self.client.get(url)
        
        return UserInfo(
            user_id=data["UserId"],
            space_user_id=data["SpaceUserID"],
            blog_id=data["BlogId"],
            display_name=data["DisplayName"],
            face=data["Face"],
            avatar=data["Avatar"],
            seniority=data["Seniority"],
            blog_app=data["BlogApp"],
            following_count=data["FollowingCount"],
            followers_count=data["FollowerCount"],
            is_vip=data["IsVip"],
            joined=data["Joined"],
        )


class IngAPI:
    """闪存API"""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    def publish(self, content: str, is_private: bool = False, ignore_duplicate: bool = True) -> Result:
        """发布闪存"""
        url = f"{OPENAPI}/statuses"
        payload = {
            "content": content,
            "isPrivate": is_private,
            "clientType": 13,
        }
        result = self.client.post(url, payload, raise_on_error=False)
        
        if isinstance(result, Err):
            if ignore_duplicate and "相同闪存已发布" in result.error:
                return Ok(None)
            return result
        return Ok(None)
    
    def get_list(self, skip: int = 0, take: int = 10, ing_type: int = 1) -> List[IngEntry]:
        """获取闪存列表"""
        url = f"{OPENAPI}/statuses/@{ing_type}?pageIndex={skip // take + 1}&pageSize={take}"
        data = self.client.get(url)
        
        ings = []
        for item in data:
            ings.append(IngEntry(
                id=item["Id"],
                content=item["Content"],
                user_alias=item["UserAlias"],
                user_display_name=item["UserDisplayName"],
                create_time=item["DateAdded"],
                comment_count=item["CommentCount"],
                lucky_count=item.get("LuckyCount", 0),
            ))
        
        return ings
    
    def comment(self, ing_id: int, content: str) -> Result:
        """评论闪存"""
        url = f"{OPENAPI}/statuses/{ing_id}/comments"
        payload = {"content": content}
        result = self.client.post(url, payload, raise_on_error=False)
        
        if isinstance(result, Err):
            return result
        return Ok(None)


class NewsAPI:
    """新闻API"""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    def get_list(self, skip: int = 0, take: int = 10) -> List[NewsEntry]:
        """获取新闻列表"""
        page_index = skip // take + 1
        url = f"{OPENAPI}/newsitems/@sitehome?pageIndex={page_index}&pageSize={take}"
        data = self.client.get(url)
        
        news_list = []
        for item in data:
            news_list.append(NewsEntry(
                id=item["Id"],
                title=item["Title"],
                summary=item["Summary"],
                url=item["Url"],
                view_count=item["ViewCount"],
                comment_count=item["CommentCount"],
                digg_count=item["DiggCount"],
                create_time=item["DateAdded"],
            ))
        
        return news_list


class FavAPI:
    """收藏API"""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    def get_list(self, skip: int = 0, take: int = 10) -> List[FavEntry]:
        """获取收藏列表"""
        page_index = skip // take + 1
        url = f"{OPENAPI}/wz?pageIndex={page_index}&pageSize={take}"
        data = self.client.get(url)
        
        favs = []
        for item in data:
            favs.append(FavEntry(
                id=item["Id"],
                title=item["Title"],
                url=item["Url"],
                create_time=item["DateAdded"],
            ))
        
        return favs


class CnblogsClient:
    """博客园客户端"""
    
    def __init__(self, pat: Optional[str] = None, timeout: float = 30.0):
        """
        初始化客户端
        
        Args:
            pat: Personal Access Token（可选，不提供则从~/.cnbrc加载）
            timeout: 请求超时时间（秒）
        """
        if pat is None:
            pat = load_pat()
        
        self.pat = pat
        self.timeout = timeout
        self._http_client: Optional[HTTPClient] = None
        self._post: Optional[PostAPI] = None
        self._user: Optional[UserAPI] = None
        self._ing: Optional[IngAPI] = None
        self._news: Optional[NewsAPI] = None
        self._fav: Optional[FavAPI] = None
    
    def __enter__(self):
        self._http_client = HTTPClient(self.pat, self.timeout)
        self._post = PostAPI(self._http_client)
        self._user = UserAPI(self._http_client)
        self._ing = IngAPI(self._http_client)
        self._news = NewsAPI(self._http_client)
        self._fav = FavAPI(self._http_client)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._http_client:
            self._http_client.close()
    
    @property
    def post(self) -> PostAPI:
        """文章API"""
        if self._post is None:
            raise RuntimeError("Client must be used as context manager")
        return self._post
    
    @property
    def user(self) -> UserAPI:
        """用户API"""
        if self._user is None:
            raise RuntimeError("Client must be used as context manager")
        return self._user
    
    @property
    def ing(self) -> IngAPI:
        """闪存API"""
        if self._ing is None:
            raise RuntimeError("Client must be used as context manager")
        return self._ing
    
    @property
    def news(self) -> NewsAPI:
        """新闻API"""
        if self._news is None:
            raise RuntimeError("Client must be used as context manager")
        return self._news
    
    @property
    def fav(self) -> FavAPI:
        """收藏API"""
        if self._fav is None:
            raise RuntimeError("Client must be used as context manager")
        return self._fav
    
    @staticmethod
    def login(pat: str) -> str:
        """保存PAT到配置文件"""
        config_path = save_pat(pat)
        return str(config_path)
    
    @staticmethod
    def logout() -> str:
        """从配置文件删除PAT"""
        config_path = remove_pat()
        return str(config_path)
