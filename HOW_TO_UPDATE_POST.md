# 如何更改博文内容

## 快速开始

### 1. 获取文章ID

有两种方式获取文章ID：

#### 方式A：从博客园后台

1. 登录博客园
2. 进入"我的博客" → "文章管理"
3. 点击要编辑的文章
4. 查看URL，例如：`https://i.cnblogs.com/posts/edit?postid=19242175`
5. `19242175` 就是文章ID

#### 方式B：通过代码获取

```python
import asyncio
from pycnblogs import CnblogsClient

async def main():
    async with CnblogsClient() as client:
        # 获取文章列表
        posts, total = await client.post.get_list(skip=0, take=10)
        
        # 显示所有文章
        for post in posts:
            print(f"ID: {post.id}, 标题: {post.title}")

asyncio.run(main())
```

### 2. 更改文章内容

#### 只改标题

```python
import asyncio
from pycnblogs import CnblogsClient, Err, print_error

async def main():
    async with CnblogsClient() as client:
        post_id = 19242175  # 你的文章ID
        
        result = await client.post.update(
            post_id,
            title="新的标题"
        )
        
        if isinstance(result, Err):
            print_error(result)
        else:
            print("✓ 标题已更新")

asyncio.run(main())
```

#### 只改内容

```python
async def main():
    async with CnblogsClient() as client:
        post_id = 19242175
        
        result = await client.post.update(
            post_id,
            body="""# 新的内容

这是更新后的文章内容。

## 章节1

内容1
"""
        )
        
        if isinstance(result, Err):
            print_error(result)
        else:
            print("✓ 内容已更新")

asyncio.run(main())
```

#### 同时改标题和内容

```python
async def main():
    async with CnblogsClient() as client:
        post_id = 19242175
        
        result = await client.post.update(
            post_id,
            title="新标题",
            body="# 新内容\n\n这是新的文章内容。"
        )
        
        if isinstance(result, Err):
            print_error(result)
        else:
            print("✓ 标题和内容都已更新")

asyncio.run(main())
```

#### 发布文章

```python
async def main():
    async with CnblogsClient() as client:
        post_id = 19242175
        
        # 发布文章
        result = await client.post.update(post_id, publish=True)
        
        # 或者改为草稿
        # result = await client.post.update(post_id, publish=False)
        
        if isinstance(result, Err):
            print_error(result)
        else:
            print("✓ 文章已发布")

asyncio.run(main())
```

## 完整示例

### 示例1：修改现有文章

```python
import asyncio
from pycnblogs import CnblogsClient, Err, print_error

async def main():
    async with CnblogsClient() as client:
        # 1. 指定文章ID
        post_id = 19242175
        
        # 2. 获取当前内容
        post = await client.post.get_one(post_id)
        print(f"当前标题: {post.title}")
        
        # 3. 更新内容
        result = await client.post.update(
            post_id,
            title="更新后的标题",
            body="# 更新后的内容\n\n这是新内容。"
        )
        
        if isinstance(result, Err):
            print_error(result)
            return
        
        # 4. 验证更新
        post = await client.post.get_one(post_id)
        print(f"新标题: {post.title}")
        print(f"URL: {post.full_url}")

asyncio.run(main())
```

### 示例2：批量更新

```python
async def main():
    async with CnblogsClient() as client:
        # 获取所有草稿
        posts, _ = await client.post.get_list(skip=0, take=100)
        drafts = [p for p in posts if p.is_draft]
        
        # 批量添加标签
        for draft in drafts:
            new_title = f"[更新] {draft.title}"
            result = await client.post.update(draft.id, title=new_title)
            
            if isinstance(result, Err):
                print(f"✗ {draft.title}")
            else:
                print(f"✓ {draft.title}")

asyncio.run(main())
```

### 示例3：从文件读取内容

```python
async def main():
    async with CnblogsClient() as client:
        post_id = 19242175
        
        # 从文件读取内容
        with open("post_content.md", "r", encoding="utf-8") as f:
            new_content = f.read()
        
        # 更新文章
        result = await client.post.update(post_id, body=new_content)
        
        if isinstance(result, Err):
            print_error(result)
        else:
            print("✓ 内容已从文件更新")

asyncio.run(main())
```

## 使用现有示例

### 使用 simple_update.py

1. 打开 `examples/simple_update.py`
2. 修改 `post_id = 19242175` 为你的文章ID
3. 修改 `title` 和 `body` 为你想要的内容
4. 运行：`python examples/simple_update.py`

### 使用 update_post_content.py

1. 运行：`python examples/update_post_content.py`
2. 选择操作：
   - `1` - 更改指定文章内容
   - `2` - 更新已存在的文章
   - `3` - 批量更新文章

## 注意事项

### ✅ 推荐做法

1. **更新前先获取当前内容**
   ```python
   post = await client.post.get_one(post_id)
   print(f"当前标题: {post.title}")
   ```

2. **总是检查返回值**
   ```python
   result = await client.post.update(...)
   if isinstance(result, Err):
       print_error(result)
       return
   ```

3. **使用 full_url 查看结果**
   ```python
   post = await client.post.get_one(post_id)
   print(post.full_url)
   ```

### ❌ 避免的做法

1. **不检查错误**
   ```python
   # ❌ 危险
   await client.post.update(post_id, title="新标题")
   # 如果失败了怎么办？
   ```

2. **使用不存在的文章ID**
   ```python
   # ❌ 会失败
   await client.post.update(999999, title="标题")
   ```

## 常见问题

### Q: 如何只更新标题不改内容？

A: 只传 `title` 参数：

```python
result = await client.post.update(post_id, title="新标题")
```

### Q: 如何只更新内容不改标题？

A: 只传 `body` 参数：

```python
result = await client.post.update(post_id, body="新内容")
```

### Q: 如何把已发布的文章改为草稿？

A: 设置 `publish=False`：

```python
result = await client.post.update(post_id, publish=False)
```

### Q: 更新失败怎么办？

A: 检查错误信息：

```python
if isinstance(result, Err):
    print_error(result)  # 显示详细错误
```

### Q: 如何批量更新多篇文章？

A: 使用循环：

```python
post_ids = [123, 456, 789]
for post_id in post_ids:
    result = await client.post.update(post_id, title="新标题")
    if isinstance(result, Err):
        print(f"✗ {post_id}")
    else:
        print(f"✓ {post_id}")
```

## 示例代码

- `examples/simple_update.py` - 简单更新示例
- `examples/update_post_content.py` - 完整更新示例
- `examples/correct_usage.py` - 正确使用方式

## 快速参考

```python
# 更新标题
await client.post.update(post_id, title="新标题")

# 更新内容
await client.post.update(post_id, body="新内容")

# 更新标题和内容
await client.post.update(post_id, title="新标题", body="新内容")

# 发布文章
await client.post.update(post_id, publish=True)

# 改为草稿
await client.post.update(post_id, publish=False)

# 同时更新所有
await client.post.update(
    post_id,
    title="新标题",
    body="新内容",
    publish=True
)
```
