# pycnblogs

Python SDK for Cnblogs (博客园) API - 简单、直观的博客管理工具

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 特性

- ✅ **同步API** - 简单直观，不需要 async/await
- ✅ **完整功能** - 支持文章、闪存、新闻、收藏等所有功能
- ✅ **错误处理** - Result类型，不抛出异常
- ✅ **类型安全** - 使用dataclass定义数据模型
- ✅ **URL处理** - 自动补全协议
- ✅ **易于使用** - 简洁的API设计

## 安装

```bash
pip install -e .
```

## 快速开始

### 1. 登录

获取你的PAT：https://account.cnblogs.com/settings/tokens

```python
from pycnblogs import CnblogsClient

# 保存PAT到 ~/.cnbrc
CnblogsClient.login("your_pat_here")
```

### 2. 使用

```python
from pycnblogs import CnblogsClient, Err, print_error

# 使用 with 语句，不需要 async/await
with CnblogsClient() as client:
    # 获取用户信息
    user = client.user.get_info()
    print(f"Hello, {user.display_name}!")
    
    # 创建文章
    result = client.post.create(
        title="我的第一篇文章",
        body="# Hello\n\n这是内容",
        publish=False
    )
    
    if isinstance(result, Err):
        print_error(result)
    else:
        post_id = result
        print(f"创建成功: {post_id}")
        
        # 更新文章
        client.post.update(post_id, publish=True)
        
        # 获取文章
        post = client.post.get_one(post_id)
        print(f"URL: {post.full_url}")
```

## 主要功能

### 文章管理

```python
with CnblogsClient() as client:
    # 创建文章
    post_id = client.post.create("标题", "内容", publish=False)
    
    # 更新文章
    client.post.update(post_id, title="新标题")
    
    # 获取文章
    post = client.post.get_one(post_id)
    
    # 列出文章
    posts, total = client.post.get_list(skip=0, take=10)
    
    # 删除文章
    client.post.delete(post_id)
```

### 闪存管理

```python
with CnblogsClient() as client:
    # 发布闪存
    client.ing.publish("Hello!")
    
    # 列出闪存
    ings = client.ing.get_list(skip=0, take=10)
    
    # 评论闪存
    client.ing.comment(ing_id, "评论内容")
```

### 其他功能

```python
with CnblogsClient() as client:
    # 获取新闻
    news = client.news.get_list(skip=0, take=10)
    
    # 获取收藏
    favs = client.fav.get_list(skip=0, take=10)
```

## 错误处理

```python
from pycnblogs import Err, print_error

result = client.post.create("标题", "内容")

if isinstance(result, Err):
    # 方式1：使用辅助函数
    print_error(result)
    
    # 方式2：获取消息
    print(result.get_message())
    
    # 方式3：获取JSON
    print(result.to_json())
else:
    post_id = result
    print(f"成功: {post_id}")
```

## URL处理

API返回的URL缺少协议，使用 `full_url` 属性获取完整URL：

```python
post = client.post.get_one(post_id)
print(post.url)       # //www.cnblogs.com/username/p/12345
print(post.full_url)  # https://www.cnblogs.com/username/p/12345
```

## 示例

查看 `examples/` 目录：

- `sync_example.py` - 完整示例
- `simple_update.py` - 更新文章
- `update_post_content.py` - 批量更新

## 文档

- `QUICKSTART_PYTHON.md` - 快速开始
- `HOW_TO_UPDATE_POST.md` - 如何更新文章
- `ERROR_HANDLING_GUIDE.md` - 错误处理指南
- `URL_HANDLING.md` - URL处理说明
- `SYNC_MIGRATION.md` - 从异步迁移

## API参考

### CnblogsClient

```python
with CnblogsClient(pat=None, timeout=30.0) as client:
    # pat: 可选，不提供则从 ~/.cnbrc 加载
    # timeout: 请求超时时间（秒）
    pass
```

### PostAPI

```python
# 创建文章
post_id = client.post.create(title, body, publish=False)

# 更新文章
client.post.update(post_id, title=None, body=None, publish=None)

# 获取文章
post = client.post.get_one(post_id)

# 列出文章
posts, total = client.post.get_list(skip=0, take=10)

# 删除文章
client.post.delete(post_id)
```

### IngAPI

```python
# 发布闪存
client.ing.publish(content, is_private=False, ignore_duplicate=True)

# 列出闪存
ings = client.ing.get_list(skip=0, take=10, ing_type=1)

# 评论闪存
client.ing.comment(ing_id, content)
```

### UserAPI

```python
# 获取用户信息
user = client.user.get_info()
```

## 依赖

- Python 3.8+
- requests >= 2.28.0

## 许可证

MIT

## 链接

- 原始Rust CLI: https://github.com/cnblogs/cli
- 博客园: https://www.cnblogs.com

## 更新日志

### v0.2.0 (2024-XX-XX)

- 🎉 **重大变更**：完全改为同步API
- ✅ 移除 async/await，代码更简单
- ✅ 使用 requests 替代 httpx
- ✅ 更适合博客管理场景

### v0.1.0 (2024-XX-XX)

- ✅ 初始版本（异步API）
- ✅ 完整功能支持
- ✅ Result类型错误处理
