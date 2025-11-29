# pycnblogs 项目总结

## 项目简介

pycnblogs 是博客园（Cnblogs）的 Python SDK，提供简单直观的同步API。

## 核心特性

- ✅ **同步API** - 简单直观，不需要 async/await
- ✅ **完整功能** - 文章、闪存、新闻、收藏
- ✅ **错误处理** - Result类型，不抛出异常
- ✅ **URL处理** - 自动补全协议
- ✅ **易于使用** - 简洁的API设计

## 快速示例

```python
from pycnblogs import CnblogsClient, Err, print_error

with CnblogsClient() as client:
    # 创建文章
    result = client.post.create("标题", "内容")
    
    if isinstance(result, Err):
        print_error(result)
    else:
        post_id = result
        
        # 更新文章
        client.post.update(post_id, publish=True)
        
        # 获取文章
        post = client.post.get_one(post_id)
        print(post.full_url)
```

## 项目结构

```
pycnblogs/
├── __init__.py              # 主入口
├── client.py                # 客户端
├── http_client.py           # HTTP客户端
├── models.py                # 数据模型
├── result.py                # Result类型
├── exceptions.py            # 异常定义
├── utils.py                 # 辅助函数
├── session.py               # PAT管理
└── constants.py             # 常量定义

examples/
├── complete_example.py      # 完整示例
├── simple_update.py         # 简单更新
├── update_post_content.py   # 批量更新
├── login_example.py         # 登录示例
├── display_errors.py        # 错误显示
└── url_handling.py          # URL处理

docs/
├── README.md                # 项目介绍
├── QUICKSTART.md            # 快速开始
├── HOW_TO_UPDATE_POST.md    # 更新文章指南
├── ERROR_HANDLING_GUIDE.md  # 错误处理指南
├── URL_HANDLING.md          # URL处理说明
├── SYNC_MIGRATION.md        # 迁移指南
└── BUGFIX_405.md            # 405错误修复
```

## 主要API

### CnblogsClient

```python
with CnblogsClient(pat=None, timeout=30.0) as client:
    # 使用 client
    pass
```

### PostAPI

- `create(title, body, publish)` - 创建文章
- `update(post_id, title, body, publish)` - 更新文章
- `get_one(post_id)` - 获取文章
- `get_list(skip, take)` - 列出文章
- `delete(post_id)` - 删除文章

### IngAPI

- `publish(content, is_private, ignore_duplicate)` - 发布闪存
- `get_list(skip, take, ing_type)` - 列出闪存
- `comment(ing_id, content)` - 评论闪存

### UserAPI

- `get_info()` - 获取用户信息

### NewsAPI

- `get_list(skip, take)` - 获取新闻列表

### FavAPI

- `get_list(skip, take)` - 获取收藏列表

## 依赖

- Python 3.8+
- requests >= 2.28.0

## 安装

```bash
pip install -e .
```

## 文档

- `README.md` - 项目介绍
- `QUICKSTART.md` - 快速开始
- `HOW_TO_UPDATE_POST.md` - 更新文章
- `ERROR_HANDLING_GUIDE.md` - 错误处理
- `URL_HANDLING.md` - URL处理
- `SYNC_MIGRATION.md` - 迁移指南

## 示例

- `examples/complete_example.py` - 完整示例
- `examples/simple_update.py` - 简单更新
- `examples/update_post_content.py` - 批量更新

## 版本历史

### v0.2.0 (当前)

- 🎉 完全改为同步API
- ✅ 使用 requests 替代 httpx
- ✅ 移除 async/await
- ✅ 更简单、更直观

### v0.1.0

- ✅ 初始版本（异步API）
- ✅ 完整功能支持

## 许可证

MIT

## 链接

- 原始 Rust CLI: https://github.com/cnblogs/cli
- 博客园: https://www.cnblogs.com
