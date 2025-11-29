"""完整示例 - 展示所有主要功能"""

from pycnblogs import CnblogsClient, Err, print_error


def main():
    print("=== pycnblogs 完整示例 ===\n")
    
    # 使用 with 语句，不需要 async/await
    with CnblogsClient() as client:
        # 1. 获取用户信息
        print("1. 获取用户信息...")
        user = client.user.get_info()
        print(f"   Hello, {user.display_name}!\n")
        
        # 2. 列出文章
        print("2. 列出文章...")
        posts, total = client.post.get_list(skip=0, take=5)
        print(f"   共 {total} 篇文章")
        for post in posts:
            print(f"   - {post.title}")
        print()
        
        # 3. 创建文章
        print("3. 创建文章...")
        result = client.post.create(
            title="Sync Test Post",
            body="# Test\n\nThis is a sync test.",
            publish=False
        )
        
        if isinstance(result, Err):
            print("   ✗ 创建失败")
            print_error(result, "      ")
        else:
            post_id = result
            print(f"   ✓ 创建成功，ID: {post_id}\n")
            
            # 4. 更新文章
            print("4. 更新文章...")
            result = client.post.update(post_id, publish=True)
            
            if isinstance(result, Err):
                print("   ✗ 更新失败")
                print_error(result, "      ")
            else:
                print(f"   ✓ 更新成功\n")
                
                # 5. 获取文章
                print("5. 获取文章...")
                post = client.post.get_one(post_id)
                print(f"   标题: {post.title}")
                print(f"   URL: {post.full_url}")
                print(f"   状态: {'已发布' if post.is_published else '草稿'}")
        
        print()
        
        # 6. 发布闪存
        print("6. 发布闪存...")
        result = client.ing.publish("Hello from sync API!")
        
        if result.is_ok():
            print("   ✓ 发布成功")
        else:
            print("   ✗ 发布失败")
            print_error(result, "      ")
        
        print()
        
        # 7. 获取闪存列表
        print("7. 获取闪存列表...")
        ings = client.ing.get_list(skip=0, take=3)
        print(f"   获取到 {len(ings)} 条闪存")
        for ing in ings:
            content_preview = ing.content[:30] + "..." if len(ing.content) > 30 else ing.content
            print(f"   - {ing.user_display_name}: {content_preview}")
    
    print("\n" + "=" * 60)
    print("✓ 完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
