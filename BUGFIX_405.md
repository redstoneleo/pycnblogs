# Bug修复：HTTP 405 错误

## 问题

用户报告在更新文章时遇到 `HTTP 405 (Method Not Allowed)` 错误：

```
✗ 更新失败
错误: HTTP 405
状态码: 405
```

## 原因

Python代码使用了错误的HTTP方法和URL来更新文章：

```python
# ❌ 错误的实现
url = f"{BLOG_BACKEND}/posts/{post_id}"
result = await self.client.put(url, payload)  # PUT方法
```

但是博客园API实际上要求：
- 使用 **POST** 方法（不是PUT）
- URL是 `/posts`（不是 `/posts/{id}`）
- payload中需要包含 `id` 字段

## 解决方案

修改 `post.update()` 方法，使用正确的HTTP方法和URL：

```python
# ✅ 正确的实现
url = f"{BLOG_BACKEND}/posts"
payload = {
    "id": post_id,  # 在payload中包含id
    "postType": 1,
    "title": title if title is not None else current.title,
    "postBody": body if body is not None else current.body,
    "isPublished": publish if publish is not None else current.is_published,
    "displayOnHomePage": True,
}
result = await self.client.post(url, payload)  # POST方法
```

## 验证

运行测试脚本验证修复：

```bash
python test_post_update_fix.py
```

预期输出：

```
1. 创建草稿...
   ✓ 创建成功，ID: 12345

2. 更新标题...
   ✓ 更新成功

3. 发布文章...
   ✓ 发布成功

4. 验证更新...
   标题: Updated Title
   状态: 已发布
   URL: https://www.cnblogs.com/...

✓ 文章更新功能正常！
```

## 影响的文件

- `pycnblogs/api/post.py` - 修复 `update()` 方法

## 相关问题

这个问题是因为没有参考原始Rust代码的实现。Rust代码正确地使用了POST方法：

```rust
// Rust实现
let url = blog_backend!("/posts");  // 不包含id
client.post(url).json(&json)        // POST方法
```

## 经验教训

1. 在实现API客户端时，应该参考原始实现
2. HTTP 405错误通常意味着使用了错误的HTTP方法
3. 不同的API可能有不同的约定（有些用PUT更新，有些用POST）

## 测试

现在 `examples/correct_usage.py` 应该能正常工作：

```bash
python examples/correct_usage.py
```

预期输出：

```
=== 正确的使用方式 ===

1. 创建草稿...
   ✓ 创建成功，文章ID: 12345

2. 更新并发布...
   ✓ 更新成功

3. 获取文章...
   ✓ 标题: My First Post
   ✓ URL: https://www.cnblogs.com/...
   ✓ 状态: 已发布

✓ 程序正常结束！
```
