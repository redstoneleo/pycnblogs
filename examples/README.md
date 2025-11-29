# pycnblogs 示例

这个目录包含 pycnblogs 的使用示例。

## 前提条件

1. 安装 pycnblogs:
   ```bash
   pip install -e .
   ```

2. 获取 PAT (Personal Access Token):
   https://account.cnblogs.com/settings/tokens

## 示例列表

### 基础示例

- **complete_example.py** - 完整示例
  ```bash
  python examples/complete_example.py
  ```

- **login_example.py** - 登录和会话管理
  ```bash
  python examples/login_example.py
  ```

### 文章操作

- **simple_update.py** - 简单的文章更新示例
  ```bash
  python examples/simple_update.py
  ```

- **update_post_content.py** - 完整的文章更新示例（包含批量操作）
  ```bash
  python examples/update_post_content.py
  ```

### 其他示例

- **display_errors.py** - 优雅地显示错误信息
  ```bash
  python examples/display_errors.py
  ```

- **url_handling.py** - URL处理示例
  ```bash
  python examples/url_handling.py
  ```

## 快速开始

### 1. 登录

```python
from pycnblogs import CnblogsClient

# 保存 PAT
CnblogsClient.login("your_pat_here")
```

### 2. 基本使用

```python
from pycnblogs import CnblogsClient, Err, print_error

with CnblogsClient() as client:
    # 获取用户信息
    user = client.user.get_info()
    print(f"Hello, {user.display_name}!")
    
    # 创建文章
    result = client.post.create("标题", "内容")
    
    if isinstance(result, Err):
        print_error(result)
    else:
        print(f"创建成功: {result}")
```

## 常见任务

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

### 发布闪存

```python
with CnblogsClient() as client:
    result = client.ing.publish("Hello!")
    
    if result.is_ok():
        print("发布成功")
```

### 批量操作

```python
with CnblogsClient() as client:
    posts, _ = client.post.get_list(skip=0, take=10)
    
    for post in posts:
        if post.is_draft:
            client.post.update(post.id, publish=True)
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
```

## 文档

- `README.md` - 项目介绍
- `HOW_TO_UPDATE_POST.md` - 如何更新文章
- `ERROR_HANDLING_GUIDE.md` - 错误处理指南
- `URL_HANDLING.md` - URL处理说明

## 提示

- 所有API都是同步的，不需要 async/await
- 使用 `with` 语句管理客户端
- 检查返回值是否为 `Err` 对象
- 使用 `full_url` 属性获取完整URL
