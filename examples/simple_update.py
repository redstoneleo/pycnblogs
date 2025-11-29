"""简单示例：更改博文内容"""

from pycnblogs import CnblogsClient, Err, print_error


def main():
    with CnblogsClient() as client:
        print("=== 简单更改博文内容 ===\n")
        
        # 步骤1：指定要更改的文章ID
        # 你可以从博客园后台或者通过 get_list() 获取文章ID
        post_id = 19242175  # 👈 修改为你的文章ID
        
        print(f"文章ID: {post_id}\n")
        
        # 步骤2：更改标题
        print("1. 更改标题...")
        result = client.post.update(
            post_id,
            title="新的标题"  # 👈 修改为你想要的标题
        )
        
        if isinstance(result, Err):
            print("   ✗ 失败")
            print_error(result, "      ")
            return
        
        print("   ✓ 成功\n")
        
        # 步骤3：更改内容
        print("2. 更改内容...")
        result = client.post.update(
            post_id,
            body="""# 新的内容

这是更新后的文章内容。

## 第一部分

内容1

## 第二部分

内容2
"""  # 👈 修改为你想要的内容
        )
        
        if isinstance(result, Err):
            print("   ✗ 失败")
            print_error(result, "      ")
            return
        
        print("   ✓ 成功\n")
        
        # 步骤4：查看结果
        print("3. 查看结果...")
        post = client.post.get_one(post_id)
        print(f"   标题: {post.title}")
        print(f"   URL: {post.full_url}")
        print(f"   状态: {'已发布' if post.is_published else '草稿'}")
        
        print("\n✓ 完成！")


if __name__ == "__main__":
    main()
