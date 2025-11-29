# 迁移到同步API

## 重大变更

pycnblogs v0.2.0 已完全改为同步API，不再使用异步。

## 为什么改为同步？

1. **更简单** - 不需要理解 async/await
2. **更直观** - 代码更容易阅读和调试
3. **更适合** - 博客管理场景通常是顺序操作
4. **更易用** - 新手友好

## 迁移指南

### 之前（异步）

```python
import asyncio
from pycnblogs import CnblogsClient

async def main():
    async with CnblogsClient() as client:
        user = await client.user.get_info()
        print(user.display_name)

asyncio.run(main())
```

### 现在（同步）

```python
from pycnblogs import CnblogsClient

with CnblogsClient() as client:
    user = client.user.get_info()
    print(user.display_name)
```

## 主要变化

### 1. 移除 async/await

```python
# 之前
async def main():
    async with CnblogsClient() as client:
        result = await client.post.create("标题", "内容")

# 现在
def main():
    with CnblogsClient() as client:
        result = client.post.create("标题", "内容")
```

### 2. 移除 asyncio.run()

```python
# 之前
asyncio.run(main())

# 现在
main()
```

### 3. 使用 with 而不是 async with

```python
# 之前
async with CnblogsClient() as client:
    pass

# 现在
with CnblogsClient() as client:
    pass
```

## 完整示例对比

### 创建文章

#### 之前（异步）

```python
import asyncio
from pycnblogs import CnblogsClient, Err, print_error

async def main():
    async with CnblogsClient() as client:
        result = await client.post.create(
            title="标题",
            body="内容",
            publish=False
        )
        
        if isinstance(result, Err):
            print_error(result)
        else:
            post_id = result
            result = await client.post.update(post_id, publish=True)
            
            if isinstance(result, Err):
                print_error(result)
            else:
                post = await client.post.get_one(post_id)
                print(post.full_url)

asyncio.run(main())
```

#### 现在（同步）

```python
from pycnblogs import CnblogsClient, Err, print_error

with CnblogsClient() as client:
    result = client.post.create(
        title="标题",
        body="内容",
        publish=False
    )
    
    if isinstance(result, Err):
        print_error(result)
    else:
        post_id = result
        result = client.post.update(post_id, publish=True)
        
        if isinstance(result, Err):
            print_error(result)
        else:
            post = client.post.get_one(post_id)
            print(post.full_url)
```

### 批量操作

#### 之前（异步 - 并发）

```python
async with CnblogsClient() as client:
    tasks = [client.post.update(i, title="新标题") for i in range(1, 11)]
    results = await asyncio.gather(*tasks)
```

#### 现在（同步 - 顺序）

```python
with CnblogsClient() as client:
    for i in range(1, 11):
        result = client.post.update(i, title="新标题")
        if isinstance(result, Err):
            print(f"✗ {i}")
        else:
            print(f"✓ {i}")
```

## API变化

所有API保持不变，只是移除了 async/await：

| 操作 | 之前 | 现在 |
|------|------|------|
| 获取用户 | `await client.user.get_info()` | `client.user.get_info()` |
| 创建文章 | `await client.post.create()` | `client.post.create()` |
| 更新文章 | `await client.post.update()` | `client.post.update()` |
| 获取文章 | `await client.post.get_one()` | `client.post.get_one()` |
| 列出文章 | `await client.post.get_list()` | `client.post.get_list()` |
| 删除文章 | `await client.post.delete()` | `client.post.delete()` |
| 发布闪存 | `await client.ing.publish()` | `client.ing.publish()` |
| 列出闪存 | `await client.ing.get_list()` | `client.ing.get_list()` |

## 依赖变化

### 之前

```
httpx>=0.24.0
```

### 现在

```
requests>=2.28.0
```

## 更新步骤

1. **更新依赖**
   ```bash
   pip install -U pycnblogs
   ```

2. **移除 async/await**
   - 删除所有 `async` 关键字
   - 删除所有 `await` 关键字
   - 删除 `asyncio.run()`

3. **更新 with 语句**
   - `async with` → `with`

4. **测试代码**
   ```bash
   python your_script.py
   ```

## 示例代码

查看以下示例了解新的同步API：

- `examples/sync_example.py` - 完整示例
- `examples/simple_update.py` - 更新文章
- `examples/correct_usage.py` - 正确用法

## 常见问题

### Q: 为什么改为同步？

A: 博客管理场景通常是顺序操作，同步API更简单直观。

### Q: 性能会变差吗？

A: 对于单个操作，性能相同。批量操作会慢一些，但代码更简单。

### Q: 还能用异步吗？

A: 旧版本的异步代码在 `client.py` 中保留，但不再推荐使用。

### Q: 如何批量操作？

A: 使用循环：

```python
with CnblogsClient() as client:
    for post_id in post_ids:
        client.post.update(post_id, title="新标题")
```

## 优势

### 同步API的优势

1. **代码更简单**
   - 不需要 async/await
   - 不需要 asyncio.run()
   - 更少的样板代码

2. **更易调试**
   - 堆栈跟踪更清晰
   - 断点调试更容易

3. **更易学习**
   - 新手友好
   - 不需要理解异步概念

4. **更适合脚本**
   - 命令行工具
   - 自动化脚本
   - 简单任务

## 总结

pycnblogs v0.2.0 完全改为同步API，使代码更简单、更直观、更易用。

迁移很简单：
1. 移除 async/await
2. 移除 asyncio.run()
3. async with → with

就这么简单！🎉
