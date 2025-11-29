"""示例：优雅地显示错误信息"""

from pycnblogs import CnblogsClient, Err


def display_error(result: Err, prefix: str = ""):
    """优雅地显示错误信息"""
    error_dict = result.to_dict()
    
    # 处理不同的错误格式
    if "errors" in error_dict and isinstance(error_dict["errors"], list):
        # 格式1: {"errors": ["错误1", "错误2"], "type": 0}
        print(f"{prefix}错误:")
        for err in error_dict["errors"]:
            print(f"{prefix}  - {err}")
    elif "Message" in error_dict:
        # 格式2: {"Message": "错误消息", "Data": {}, ...}
        print(f"{prefix}错误: {error_dict['Message']}")
    elif "message" in error_dict:
        # 格式3: {"message": "错误消息"}
        print(f"{prefix}错误: {error_dict['message']}")
    else:
        # 其他格式：显示原始JSON
        print(f"{prefix}错误: {result.to_json(indent=None)}")
    
    # 显示状态码（如果有）
    if result.status_code:
        print(f"{prefix}状态码: {result.status_code}")


def main():
    with CnblogsClient() as client:
        print("=== 优雅的错误显示示例 ===\n")
        
        # 示例1：创建重复标题的文章
        print("1. 创建文章（可能重复）...")
        result = client.post.create(
            title="Test Post",
            body="Content",
            publish=False
        )
        
        if isinstance(result, Err):
            display_error(result, "   ")
        else:
            print(f"   ✓ 创建成功，ID: {result}")
        
        print()
        
        # 示例2：发布重复闪存
        print("2. 发布闪存（测试重复）...")
        result = client.ing.publish("Test content", ignore_duplicate=False)
        
        if result.is_err():
            display_error(result, "   ")
        else:
            print(f"   ✓ 发布成功")
        
        print()
        
        # 示例3：对比不同的显示方式
        print("3. 对比不同的错误显示方式...")
        result = client.post.create(
            title="Test Post",
            body="Content",
            publish=False
        )
        
        if isinstance(result, Err):
            print("\n   方式1 - 简单消息:")
            print(f"      {result.get_message()}")
            
            print("\n   方式2 - 原始JSON:")
            print(f"      {result.to_json(indent=None)}")
            
            print("\n   方式3 - 格式化JSON:")
            print("      " + result.to_json().replace("\n", "\n      "))
            
            print("\n   方式4 - 优雅显示:")
            display_error(result, "      ")
        
        print("\n" + "=" * 60)
        print("推荐使用 display_error() 函数来显示错误")
        print("=" * 60)


if __name__ == "__main__":
    main()
