"""
依赖包测试脚本
用于验证所有必要的包是否正确安装
"""

import sys

def test_import(module_name, import_statement):
    """测试模块导入"""
    try:
        exec(import_statement)
        print(f"✓ {module_name} - 导入成功")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - 导入失败: {e}")
        return False
    except Exception as e:
        print(f"⚠️ {module_name} - 其他错误: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("DeepSORT车流量统计系统 - 依赖包测试")
    print("=" * 50)
    
    tests = [
        ("Python版本", f"assert sys.version_info >= (3, 7), 'Python版本需要3.7+'"),
        ("NumPy", "import numpy as np"),
        ("OpenCV", "import cv2"),
        ("Ultralytics YOLO", "from ultralytics import YOLO"),
        ("PyTorch", "import torch"),
        ("TorchVision", "import torchvision"),
    ]
    
    # 基础依赖测试
    success_count = 0
    for name, statement in tests:
        if test_import(name, statement):
            success_count += 1
    
    # DeepSORT特殊测试
    print("\n" + "-" * 30)
    print("DeepSORT导入测试:")
    print("-" * 30)
    
    deepsort_success = False
    
    # 方式1
    try:
        from deep_sort_realtime import DeepSort
        print("✓ DeepSort - 导入成功 (deep_sort_realtime)")
        deepsort_success = True
    except ImportError as e1:
        print(f"❌ 方式1失败: {e1}")
        
        # 方式2
        try:
            from deep_sort_realtime.deepsort_tracker import DeepSort
            print("✓ DeepSort - 导入成功 (deepsort_tracker)")
            deepsort_success = True
        except ImportError as e2:
            print(f"❌ 方式2失败: {e2}")
    
    if deepsort_success:
        success_count += 1
        
        # 测试DeepSort初始化
        try:
            tracker = DeepSort(max_age=30, n_init=3)
            print("✓ DeepSort - 初始化成功")
        except Exception as e:
            print(f"⚠️ DeepSort - 初始化失败: {e}")
    
    # 总结
    print("\n" + "=" * 50)
    total_tests = len(tests) + 1  # +1 for DeepSort
    if success_count == total_tests:
        print("🎉 所有依赖包测试通过！可以正常运行程序。")
        print("运行命令: python main_deepsort.py")
    else:
        print(f"⚠️ {total_tests - success_count} 个依赖包存在问题")
        print("请查看 INSTALL_GUIDE.md 获取安装帮助")
    
    print("=" * 50)

if __name__ == "__main__":
    main()