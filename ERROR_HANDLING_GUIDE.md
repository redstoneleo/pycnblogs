# 错误处理指南

## 概述

pycnblogs 提供了灵活的错误处理机制，支持多种错误处理模式。

## Result类型

所有写操作（POST/PUT/DELETE）返回 `Result` 类型或直接返回值（成功时）。

### 成功情况

```python
# 创建文章成功
post_id = await client.post.create(title="标题", body="内容")
# post_id 是 int 类型

# 发布闪存成功
result = await client.ing.publish("内容")
# result 是 Ok(None)
```

### 失败情况

```python
# 创建文章失败
result = await client.post.create(title="", body="")
# result 是 Err 对象
```

## 错误检查方法

### 方法1：使用 isinstance

```python
from pycnblogs import Err

result = await client.post.create(title="标题", body="内容")

if isinstance(result, Err):
    print(f"失败: {result.get_message()}")
else:
    post_id = result
    print(f"成功，ID: {post_id}")
```

### 方法2：使用 is_ok() / is_err()

```python
result = await client.ing.publish("内容")

if result.is_ok():
    print("成功")
else:
    print(f"失败: {result.get_message()}")
```

## 获取错误信息

### 简单消息

```python
if isinstance(result, Err):
    message = result.get_message()
    print(f"错误: {message}")
```

### JSON格式

```python
if isinstance(result, Err):
    json_str = result.to_json()
    print(json_str)
    # 输出原始错误JSON（不添加额外嵌套）:
    # {
    #   "Message": "相同闪存已发布",
    #   "Data": {},
    #   ...
    # }
    # 或
    # {
    #   "errors": ["相同标题的博文已存在"],
    #   "type": 0
    # }
```

### 字典格式

```python
if isinstance(result, Err):
    error_dict = result.to_dict()
    
    # 处理不同的错误格式
    if "errors" in error_dict:
        for err in error_dict["errors"]:
            print(f"- {err}")
    elif "Message" in error_dict:
        print(f"错误: {error_dict['Message']}")
```

## Err对象API

### 属性

- `error: str` - 原始错误信息（通常是JSON字符串）
- `status_code: int` - HTTP状态码

### 方法

- `is_ok() -> bool` - 返回 False
- `is_err() -> bool` - 返回 True
- `get_message() -> str` - 提取错误消息
- `to_dict() -> dict` - 转换为字典
- `to_json() -> str` - 转换为JSON字符串
- `unwrap()` - 抛出异常
- `unwrap_or(default)` - 返回默认值

## 完整示例

### 示例1：创建文章

```python
import asyncio
from pycnblogs import CnblogsClient, Err

async def main():
    async with CnblogsClient() as client:
        # 创建文章
        result = await client.post.create(
            title="测试文章",
            body="内容",
            publish=False
        )
        
        # 检查结果
        if isinstance(result, Err):
            print("创建失败")
            
            # 优雅地显示错误
            error_dict = result.to_dict()
            if "errors" in error_dict:
                for err in error_dict["errors"]:
                    print(f"  - {err}")
            else:
                print(f"  {result.get_message()}")
            return
        
        post_id = result
        print(f"创建成功，ID: {post_id}")
        
        # 更新文章
        result = await client.post.update(post_id, publish=True)
        
        if isinstance(result, Err):
            print("更新失败")
            print(f"  {result.get_message()}")
            return
        
        print("更新成功")

asyncio.run(main())
```

### 示例2：发布闪存

```python
async with CnblogsClient() as client:
    result = await client.ing.publish("测试内容")
    
    if result.is_ok():
        print("✓ 发布成功")
    else:
        print("✗ 发布失败")
        print(f"  错误: {result.get_message()}")
        print(f"  状态码: {result.status_code}")
```

### 示例3：批量操作

```python
async with CnblogsClient() as client:
    messages = ["消息1", "消息2", "消息3"]
    
    for msg in messages:
        result = await client.ing.publish(msg)
        
        if result.is_ok():
            print(f"✓ {msg}")
        else:
            print(f"✗ {msg}: {result.get_message()}")
```

## 错误类型

### 常见错误

1. **重复内容** (400)
   ```json
   {
     "Message": "相同闪存已发布"
   }
   ```

2. **认证失败** (401)
   ```json
   {
     "Message": "Invalid PAT token"
   }
   ```

3. **权限不足** (403)
   ```json
   {
     "Message": "没有权限"
   }
   ```

4. **资源不存在** (404)
   ```json
   {
     "Message": "文章不存在"
   }
   ```

## 最佳实践

### 1. 总是检查写操作的结果

```python
# ✓ 好
result = await client.post.create(title="标题", body="内容")
if isinstance(result, Err):
    handle_error(result)

# ✗ 不好（可能会出错）
post_id = await client.post.create(title="标题", body="内容")
# 如果失败，post_id 是 Err 对象，不是 int
```

### 2. 使用 get_message() 获取友好的错误信息

```python
if isinstance(result, Err):
    # ✓ 好 - 提取消息
    print(result.get_message())
    
    # ✗ 不好 - 原始JSON
    print(result.error)
```

### 3. 记录完整错误信息用于调试

```python
if isinstance(result, Err):
    # 显示给用户
    print(f"操作失败: {result.get_message()}")
    
    # 记录到日志
    logger.error(f"API错误: {result.to_json()}")
```

### 4. 批量操作不要中断

```python
# ✓ 好 - 继续处理其他项
for item in items:
    result = await client.ing.publish(item)
    if result.is_err():
        print(f"跳过: {item}")
        continue
    # 处理成功的情况

# ✗ 不好 - 一个失败就全部停止
for item in items:
    await client.ing.publish(item)  # 如果失败会怎样？
```

## 与异常的对比

### 使用Result（推荐）

```python
result = await client.post.create(title="标题", body="内容")
if isinstance(result, Err):
    print(f"失败: {result.get_message()}")
else:
    print(f"成功: {result}")
```

**优点：**
- 明确的错误处理
- 不会中断程序流程
- 更好的错误信息
- 适合批量操作

### 使用异常

```python
try:
    user = await client.user.get_info()
    print(user.display_name)
except APIError as e:
    print(f"失败: {e}")
```

**优点：**
- 简洁（成功路径）
- Python传统方式

**缺点：**
- 容易忘记处理
- 中断程序流程

## 总结

- **写操作**（POST/PUT/DELETE）：返回 Result 或值
- **读操作**（GET）：抛出异常
- 使用 `isinstance(result, Err)` 检查错误
- 使用 `result.get_message()` 获取友好消息
- 使用 `result.to_json()` 获取完整错误信息
- 批量操作时不要让一个错误中断全部流程
