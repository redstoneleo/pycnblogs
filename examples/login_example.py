"""示例：登录和会话管理"""

from pycnblogs import CnblogsClient, AuthenticationError


def login_example():
    """保存PAT到配置文件"""
    # 从 https://account.cnblogs.com/settings/tokens 获取PAT
    pat = input("输入你的PAT: ").strip()
    
    if not pat:
        print("PAT不能为空")
        return
    
    config_path = CnblogsClient.login(pat)
    print(f"✓ PAT已保存到 {config_path}")


def verify_login():
    """验证登录是否有效"""
    try:
        with CnblogsClient() as client:
            user_info = client.user.get_info()
            print(f"\n✓ 登录成功!")
            print(f"  显示名称: {user_info.display_name}")
            print(f"  博客地址: {user_info.blog_app}")
            print(f"  粉丝数: {user_info.followers_count}")
    except AuthenticationError as e:
        print(f"\n✗ 认证失败: {e}")
    except Exception as e:
        print(f"\n✗ 错误: {e}")


def logout_example():
    """从配置文件删除PAT"""
    config_path = CnblogsClient.logout()
    print(f"✓ PAT已从 {config_path} 删除")


def main():
    print("=== 博客园登录示例 ===\n")
    
    while True:
        print("\n选项:")
        print("1. 登录（保存PAT）")
        print("2. 验证登录")
        print("3. 登出（删除PAT）")
        print("4. 退出")
        
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == "1":
            login_example()
        elif choice == "2":
            verify_login()
        elif choice == "3":
            logout_example()
        elif choice == "4":
            print("再见!")
            break
        else:
            print("无效选择")


if __name__ == "__main__":
    main()
