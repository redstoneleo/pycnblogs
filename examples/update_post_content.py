"""示例：更改博文内容"""

from pycnblogs import CnblogsClient, Err, print_error


def main():
    with CnblogsClient() as client:
        print("=== 更改博文内容示例 ===\n")
        
        # 方式1：通过文章ID更改
        print("方式1：通过文章ID更改内容\n")
        
        # 替换为你的文章ID
        post_id = 19242175  # 修改为你要更新的文章ID
        
        # 获取当前文章
        print(f"1. 获取文章 {post_id}...")
        try:
            post = client.post.get_one(post_id)
            print(f"   当前标题: {post.title}")
            print(f"   当前状态: {'已发布' if post.is_published else '草稿'}")
            print()
        except Exception as e:
            print(f"   ✗ 获取失败: {e}")
            return
        
        # 更改标题
        print("2. 更改标题...")
        new_title = "更新后的标题"
        result = client.post.update(post_id, title=new_title)
        
        if isinstance(result, Err):
            print("   ✗ 更新失败")
            print_error(result, "      ")
            return
        
        print(f"   ✓ 标题已更新为: {new_title}\n")
        
        # 更改内容
        print("3. 更改内容...")
        new_body = """# 更新后的内容

这是更新后的文章内容。

## 章节1

内容1

## 章节2

内容2
"""
        result = client.post.update(post_id, body=new_body)
        
        if isinstance(result, Err):
            print("   ✗ 更新失败")
            print_error(result, "      ")
            return
        
        print(f"   ✓ 内容已更新\n")
        
        # 同时更改标题和内容
        print("4. 同时更改标题和内容...")
        result = client.post.update(
            post_id,
            title="最终标题",
            body="# 最终内容\n\n这是最终的文章内容。"
        )
        
        if isinstance(result, Err):
            print("   ✗ 更新失败")
            print_error(result, "      ")
            return
        
        print(f"   ✓ 标题和内容都已更新\n")
        
        # 发布文章
        print("5. 发布文章...")
        result = client.post.update(post_id, publish=True)
        
        if isinstance(result, Err):
            print("   ✗ 发布失败")
            print_error(result, "      ")
            return
        
        print(f"   ✓ 文章已发布\n")
        
        # 验证更新
        print("6. 验证更新...")
        post = client.post.get_one(post_id)
        print(f"   最终标题: {post.title}")
        print(f"   最终状态: {'已发布' if post.is_published else '草稿'}")
        print(f"   URL: {post.full_url}")
        
        print("\n" + "=" * 60)
        print("✓ 博文内容更新完成！")
        print("=" * 60)


def update_existing_post():
    """更新已存在的文章"""
    with CnblogsClient() as client:
        print("\n=== 更新已存在的文章 ===\n")
        
        # 1. 列出所有文章，选择要更新的
        print("1. 获取文章列表...")
        posts, total = client.post.get_list(skip=0, take=10)
        
        print(f"   找到 {total} 篇文章:\n")
        for i, post in enumerate(posts, 1):
            status = "已发布" if post.is_published else "草稿"
            print(f"   {i}. [{status}] {post.title} (ID: {post.id})")
        
        print()
        
        # 2. 选择要更新的文章（这里选择第一篇）
        if posts:
            post_to_update = posts[0]
            print(f"2. 选择更新文章: {post_to_update.title} (ID: {post_to_update.id})\n")
            
            # 3. 更新内容
            print("3. 更新内容...")
            new_content = f"""# {post_to_update.title}

这是更新后的内容。

## 原始内容

{post_to_update.body if post_to_update.body else '无'}
"""
            
            result = client.post.update(
                post_to_update.id,
                body=new_content
            )
            
            if isinstance(result, Err):
                print("   ✗ 更新失败")
                print_error(result, "      ")
            else:
                print("   ✓ 更新成功")
                print(f"   URL: {post_to_update.full_url}")


def batch_update_posts():
    """批量更新文章"""
    with CnblogsClient() as client:
        print("\n=== 批量更新文章 ===\n")
        
        # 获取所有草稿
        print("1. 获取所有草稿...")
        posts, total = client.post.get_list(skip=0, take=100)
        drafts = [p for p in posts if p.is_draft]
        
        print(f"   找到 {len(drafts)} 篇草稿\n")
        
        # 批量添加标签
        print("2. 批量添加标签...")
        for i, draft in enumerate(drafts[:5], 1):  # 只处理前5篇
            print(f"   处理 {i}/{min(5, len(drafts))}: {draft.title}")
            
            # 在标题后添加标签
            new_title = f"{draft.title} [已更新]"
            result = client.post.update(draft.id, title=new_title)
            
            if isinstance(result, Err):
                print(f"      ✗ 失败")
            else:
                print(f"      ✓ 成功")
        
        print("\n   ✓ 批量更新完成")


if __name__ == "__main__":
    print("选择操作:")
    print("1. 更改指定文章内容")
    print("2. 更新已存在的文章")
    print("3. 批量更新文章")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        main()
    elif choice == "2":
        update_existing_post()
    elif choice == "3":
        batch_update_posts()
    else:
        print("无效选择")
