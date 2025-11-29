"""示例：URL处理"""

from pycnblogs import CnblogsClient, Err


def main():
    with CnblogsClient() as client:
        print("=== URL处理示例 ===\n")
        
        # 获取文章列表
        print("1. 获取文章列表...")
        posts, total = client.post.get_list(skip=0, take=3)
        
        print(f"   找到 {len(posts)} 篇文章:\n")
        
        for i, post in enumerate(posts, 1):
            print(f"   文章 {i}:")
            print(f"   标题: {post.title}")
            print(f"   原始URL: {post.url}")
            print(f"   完整URL: {post.full_url}")
            print()
        
        # 获取新闻列表
        print("2. 获取新闻列表...")
        news_list = client.news.get_list(skip=0, take=3)
        
        print(f"   找到 {len(news_list)} 条新闻:\n")
        
        for i, news in enumerate(news_list, 1):
            print(f"   新闻 {i}:")
            print(f"   标题: {news.title}")
            print(f"   原始URL: {news.url}")
            print(f"   完整URL: {news.full_url}")
            print()
        
        # 获取收藏列表
        print("3. 获取收藏列表...")
        favs = client.fav.get_list(skip=0, take=3)
        
        print(f"   找到 {len(favs)} 个收藏:\n")
        
        for i, fav in enumerate(favs, 1):
            print(f"   收藏 {i}:")
            print(f"   标题: {fav.title}")
            print(f"   原始URL: {fav.url}")
            print(f"   完整URL: {fav.full_url}")
            print()
        
        print("=" * 60)
        print("提示:")
        print("  - 使用 .url 获取原始URL（可能缺少协议）")
        print("  - 使用 .full_url 获取完整URL（自动添加 https:）")
        print("=" * 60)


if __name__ == "__main__":
    main()
