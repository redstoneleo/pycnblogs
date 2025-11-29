"""示例：文章操作"""

from pycnblogs import CnblogsClient, Err, print_error


def main():
    with CnblogsClient() as client:
        # 创建草稿
        print("创建新文章...")
        result = client.post.create(
            title="Test Post from pycnblogs",
            body="# Hello\n\n这是使用 pycnblogs 创建的测试文章。",
            publish=False
        )
        
        if isinstance(result, Err):
            print("创建失败")
            print_error(result)
            return
        
        post_id = result
        print(f"创建成功，文章ID: {post_id}")
        
        # 获取文章
        print("\n获取文章...")
        post = client.post.get_one(post_id)
        print(f"标题: {post.title}")
        print(f"状态: {'已发布' if post.is_published else '草稿'}")
        print(f"URL: {post.url}")
        
        # 更新文章
        print("\n更新文章...")
        result = client.post.update(
            post_id,
            body="# Hello World\n\n文章已更新！",
        )
        
        if isinstance(result, Err):
            print("更新失败")
            print_error(result)
            return
        
        print("更新成功")
        
        # 列出所有文章
        print("\n列出所有文章...")
        posts, total = client.post.get_list(skip=0, take=5)
        print(f"共 {total} 篇文章")
        for p in posts:
            status = "✓" if p.is_published else "○"
            print(f"  [{status}] {p.title}")
        
        # 删除文章（取消注释以删除）
        # print(f"\n删除文章 {post_id}...")
        # result = client.post.delete(post_id)
        # if result.is_ok():
        #     print("删除成功")


if __name__ == "__main__":
    main()
