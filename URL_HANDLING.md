# URL处理说明

## 问题

博客园API返回的URL缺少协议部分：

```python
post = await client.post.get_one(post_id)
print(post.url)  # 输出: //www.cnblogs.com/username/p/12345
```

## 解决方案

所有包含URL的模型都提供了 `full_url` 属性，自动添加 `https:` 协议：

```python
post = await client.post.get_one(post_id)
print(post.url)       # //www.cnblogs.com/username/p/12345
print(post.full_url)  # https://www.cnblogs.com/username/p/12345
```

## 支持的模型

### PostEntry

```python
post = await client.post.get_one(post_id)
print(post.url)       # 原始URL
print(post.full_url)  # 完整URL（带协议）
```

### NewsEntry

```python
news_list = await client.news.get_list(skip=0, take=10)
for news in news_list:
    print(news.url)       # 原始URL
    print(news.full_url)  # 完整URL（带协议）
```

### FavEntry

```python
favs = await client.fav.get_list(skip=0, take=10)
for fav in favs:
    print(fav.url)       # 原始URL
    print(fav.full_url)  # 完整URL（带协议）
```

## 使用建议

### 推荐做法

```python
# ✅ 使用 full_url 获取完整URL
post = await client.post.get_one(post_id)
print(f"访问文章: {post.full_url}")

# ✅ 在浏览器中打开
import webbrowser
webbrowser.open(post.full_url)
```

### 不推荐做法

```python
# ❌ 直接使用 url（缺少协议）
post = await client.post.get_one(post_id)
print(f"访问文章: {post.url}")  # 输出: //www.cnblogs.com/...
```

## 实现细节

`full_url` 是一个 `@property`，会自动检查URL是否已包含协议：

```python
@property
def full_url(self) -> str:
    """Get full URL with protocol."""
    if self.url.startswith("http"):
        return self.url
    return f"https:{self.url}"
```

这意味着：
- 如果URL已经包含 `http://` 或 `https://`，直接返回
- 如果URL以 `//` 开头，添加 `https:` 前缀

## 示例

### 示例1：显示文章URL

```python
async with CnblogsClient() as client:
    post = await client.post.get_one(post_id)
    print(f"标题: {post.title}")
    print(f"URL: {post.full_url}")
```

### 示例2：在浏览器中打开

```python
import webbrowser

async with CnblogsClient() as client:
    posts, _ = await client.post.get_list(skip=0, take=5)
    for post in posts:
        if post.is_published:
            webbrowser.open(post.full_url)
```

### 示例3：生成Markdown链接

```python
async with CnblogsClient() as client:
    posts, _ = await client.post.get_list(skip=0, take=10)
    
    print("# 我的文章\n")
    for post in posts:
        if post.is_published:
            print(f"- [{post.title}]({post.full_url})")
```

### 示例4：对比原始URL和完整URL

```python
async with CnblogsClient() as client:
    post = await client.post.get_one(post_id)
    
    print(f"原始URL: {post.url}")
    # 输出: //www.cnblogs.com/username/p/12345
    
    print(f"完整URL: {post.full_url}")
    # 输出: https://www.cnblogs.com/username/p/12345
```

## 完整示例

查看 `examples/url_handling.py` 了解更多用法。

## 总结

- 使用 `.url` 获取原始URL（API返回的格式）
- 使用 `.full_url` 获取完整URL（自动添加协议）
- 推荐在需要访问URL时使用 `.full_url`
