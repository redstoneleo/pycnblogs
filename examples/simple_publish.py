"""最简单的发布闪存示例"""

from pycnblogs import CnblogsClient


def main():
    with CnblogsClient() as client:
        # 发布闪存 - 简单直接，不用担心重复内容
        result = client.ing.publish("Hello from pycnblogs! 🎉")
        
        if result.is_ok():
            print("✓ 发布成功！")
        else:
            print(f"✗ 发布失败: {result.error}")


if __name__ == "__main__":
    main()
