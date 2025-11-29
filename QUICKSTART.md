# pycnblogs 快速开始

5分钟上手 pycnblogs！

## 安装

```bash
pip install -e .
```

## 1. 获取 PAT

访问 https://account.cnblogs.com/settings/tokens 创建 Personal Access Token。

## 2. 登录

```python
from pycnblogs import CnblogsClient

# 保存 PAT（只需要做一次）
CnblogsClient.login("your_pat_here")
```

## 3. 开始使用

```python
from pycnblogs import CnblogsClient, Err, print_error

# 使用 with 语句
with CnblogsClient() as client:
    # 获取用户信息
    user = client.user.get_info()
    print(f"Hello, {user.display_name}!")
    
    # 列出文章
    posts, total = client.post.get_list(skip=0, take=5)
    print(f"\n你有 {total} 篇文章:")
    for post in posts:
        print(f"  - {post.title}")
    
    # 发布闪存
    result = client.ing.publish("Hello from pycnblogs! 🎉")
    
    if result.is_ok():
        print("\n闪存发布成功!")
    else:
        print("\n闪存发布失败:")
        print_error(result)
```

## 常用操作

### 创建文章

```python
with CnblogsClient() as client:
    # 创建草稿
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
```

### 更新文章

```python
with CnblogsClient() as client:
    # 更新标题
    client.post.update(post_id, title="新标题")
    
    # 更新内容
    client.post.update(post_id, body="新内容")
    
    # 发布文章
    client.post.update(post_id, publish=True)
```

### 获取文章

```python
with CnblogsClient() as client:
    post = client.post.get_one(post_id)
    print(f"标题: {post.title}")
    print(f"URL: {post.full_url}")
    print(f"状态: {'已发布' if post.is_published else '草稿'}")
```

### 发布闪存

```python
with CnblogsClient() as client:
    result = client.ing.publish("今天天气不错!")
    
    if result.is_ok():
        print("发布成功")
```

### 获取新闻

```python
with CnblogsClient() as client:
    news_list = client.news.get_list(skip=0, take=10)
    
    for news in news_list:
        print(f"{news.title} - {news.view_count}次浏览")
```

## 错误处理

```python
from pycnblogs import Err, print_error

result = client.post.create("标题", "内容")

if isinstance(result, Err):
    # 简单方式
    print_error(result)
    
    # 或者获取消息
    print(result.get_message())
```

## 提示

1. **使用 with 语句** - 自动管理连接
   ```python
   with CnblogsClient() as client:
       # 使用 client
       pass
   ```

2. **检查错误** - 写操作可能返回 Err
   ```python
   result = client.post.create(...)
   if isinstance(result, Err):
       print_error(result)
   ```

3. **使用 full_url** - 获取完整URL
   ```python
   post = client.post.get_one(post_id)
   print(post.full_url)  # https://www.cnblogs.com/...
   ```

4. **批量操作** - 使用循环
   ```python
   for post_id in post_ids:
       client.post.update(post_id, title="新标题")
   ```

## 下一步

- 查看 `examples/` 目录了解更多示例
- 阅读 `HOW_TO_UPDATE_POST.md` 学习如何更新文章
- 阅读 `ERROR_HANDLING_GUIDE.md` 了解错误处理

Happy blogging! 🚀
