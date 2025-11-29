"""示例：闪存操作"""

from pycnblogs import CnblogsClient


def main():
    with CnblogsClient() as client:
        # 发布闪存
        print("发布闪存...")
        client.ing.publish("Hello from pycnblogs! 🚀")
        print("闪存发布成功")
        
        # 列出最近的闪存
        print("\n最近的闪存:")
        ings = client.ing.get_list(skip=0, take=10, ing_type=1)
        
        for ing in ings:
            print(f"\n{ing.user_display_name} (@{ing.user_alias})")
            print(f"  {ing.content}")
            print(f"  💬 {ing.comment_count} 评论 | ❤️ {ing.lucky_count} 点赞")
            print(f"  🕒 {ing.create_time}")
            
            # 获取这条闪存的评论
            if ing.comment_count > 0:
                comments = client.ing.get_comments(ing.id)
                for comment in comments[:3]:  # 显示前3条评论
                    print(f"    └─ {comment.user_display_name}: {comment.content}")


if __name__ == "__main__":
    main()
