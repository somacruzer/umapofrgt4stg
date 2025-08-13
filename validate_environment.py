#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境和数据验证脚本
Environment and Data Validation Script

运行此脚本来验证系统环境和数据文件是否正确配置
Run this script to validate system environment and data files
"""

import sys
import os
import importlib
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🐍 Python版本检查...")
    version = sys.version_info
    print(f"   Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print("   ✅ Python版本符合要求 (>=3.9)")
        return True
    else:
        print("   ❌ Python版本过低，需要3.9或更高版本")
        return False

def check_required_packages():
    """检查必需的Python包"""
    print("\n📦 包依赖检查...")
    
    required_packages = {
        'numpy': '1.20.0',
        'pandas': '1.3.0', 
        'scipy': '1.7.0',
        'sklearn': '1.0.0',
        'plotly': '5.0.0',
        'umap': '0.5.0'
    }
    
    all_good = True
    
    for package_name, min_version in required_packages.items():
        try:
            if package_name == 'sklearn':
                import sklearn
                module = sklearn
                package_display = 'scikit-learn'
            elif package_name == 'umap':
                import umap
                module = umap
                package_display = 'umap-learn'
            else:
                module = importlib.import_module(package_name)
                package_display = package_name
            
            version = getattr(module, '__version__', 'unknown')
            print(f"   ✅ {package_display}: {version}")
            
        except ImportError:
            print(f"   ❌ {package_display}: 未安装")
            all_good = False
        except Exception as e:
            print(f"   ⚠️  {package_display}: 检查时出错 ({e})")
            all_good = False
    
    return all_good

def check_data_files():
    """检查必需的数据文件"""
    print("\n📄 数据文件检查...")
    
    required_files = [
        ('../umap_coordinates.csv', '原始UMAP坐标文件'),
        ('pid to survey.csv', 'Survey映射文件')
    ]
    
    all_files_exist = True
    
    for file_path, description in required_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"   ✅ {description}: {file_path} ({file_size:,} bytes)")
            
            # 快速检查文件内容
            try:
                import pandas as pd
                df = pd.read_csv(file_path)
                print(f"      📊 数据行数: {len(df)}, 列数: {len(df.columns)}")
                print(f"      📋 列名: {list(df.columns)[:5]}...")
            except Exception as e:
                print(f"      ⚠️  文件读取警告: {e}")
                
        else:
            print(f"   ❌ {description}: {file_path} (文件不存在)")
            all_files_exist = False
    
    return all_files_exist

def check_system_resources():
    """检查系统资源"""
    print("\n💻 系统资源检查...")
    
    try:
        import psutil
        
        # 内存检查
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        memory_available_gb = memory.available / (1024**3)
        
        print(f"   💾 总内存: {memory_gb:.1f} GB")
        print(f"   💾 可用内存: {memory_available_gb:.1f} GB")
        
        if memory_available_gb >= 4:
            print("   ✅ 内存充足")
            memory_ok = True
        else:
            print("   ⚠️  可用内存较低，建议至少4GB")
            memory_ok = False
        
        # 磁盘检查
        disk = psutil.disk_usage('.')
        disk_free_gb = disk.free / (1024**3)
        print(f"   💽 可用磁盘空间: {disk_free_gb:.1f} GB")
        
        if disk_free_gb >= 2:
            print("   ✅ 磁盘空间充足")
            disk_ok = True
        else:
            print("   ⚠️  磁盘空间较低，建议至少2GB")
            disk_ok = False
            
        return memory_ok and disk_ok
        
    except ImportError:
        print("   ⚠️  psutil未安装，无法检查系统资源")
        print("   安装命令: pip install psutil")
        return True
    except Exception as e:
        print(f"   ⚠️  系统资源检查错误: {e}")
        return True

def test_core_functionality():
    """测试核心功能"""
    print("\n🧪 核心功能测试...")
    
    try:
        # 测试数据处理
        import pandas as pd
        import numpy as np
        
        test_data = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'cluster': np.random.randint(0, 7, 100)
        })
        print("   ✅ 数据处理功能正常")
        
        # 测试聚类
        from sklearn.cluster import AgglomerativeClustering
        clustering = AgglomerativeClustering(n_clusters=3)
        clustering.fit(test_data[['x', 'y']])
        print("   ✅ 聚类功能正常")
        
        # 测试可视化
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_scatter(x=test_data['x'], y=test_data['y'])
        print("   ✅ 可视化功能正常")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 功能测试失败: {e}")
        return False

def generate_report():
    """生成验证报告"""
    print("\n" + "="*50)
    print("📋 环境验证报告")
    print("="*50)
    
    checks = [
        ("Python版本", check_python_version()),
        ("包依赖", check_required_packages()),
        ("数据文件", check_data_files()),
        ("系统资源", check_system_resources()),
        ("核心功能", test_core_functionality())
    ]
    
    all_passed = True
    for check_name, result in checks:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 所有检查通过！系统准备就绪。")
        print("现在可以运行: python final_constructs_cluster_analysis.py")
    else:
        print("⚠️  存在问题，请解决后重新运行验证。")
        print("详细解决方案请查看 COMPLETE_SETUP_GUIDE.md")
    print("="*50)
    
    return all_passed

def main():
    """主函数"""
    print("🔍 双极构念聚类分析系统 - 环境验证")
    print("Bipolar Constructs Clustering Analysis - Environment Validation")
    print("-" * 60)
    
    # 运行所有检查并生成报告
    success = generate_report()
    
    # 保存验证结果
    import datetime
    with open('validation_result.txt', 'w', encoding='utf-8') as f:
        f.write(f"环境验证结果: {'通过' if success else '失败'}\n")
        f.write(f"验证时间: {datetime.datetime.now()}\n")
        f.write(f"Python版本: {sys.version}\n")
    
    print(f"\n验证结果已保存到: validation_result.txt")
    
    if success:
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
