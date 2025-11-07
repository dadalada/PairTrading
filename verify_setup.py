#!/usr/bin/env python3
"""
Setup Verification Script for PairTrading Project
This script checks if your environment is properly configured.
"""

import sys
import os


def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (需要 3.8+)")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'numpy',
        'pandas',
        'sklearn',
        'statsmodels',
        'ta',
        'matplotlib',
        'seaborn',
        'requests',
        'openpyxl'
    ]

    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (未安装)")
            all_installed = False

    return all_installed


def check_files():
    """Check if all required files exist"""
    required_files = [
        'RKDRetriever.py',
        'DataProcessor.py',
        'FeatureEngineering.py',
        'PairsSelection.py',
        'stdout.py',
        'sp500_tickers_RIC.csv',
        'Interface2ChangeForFinal.ipynb',
        'requirements.txt',
        'README.md'
    ]

    all_exist = True
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename} (未找到)")
            all_exist = False

    return all_exist


def check_modules():
    """Check if custom modules can be imported"""
    sys.path.insert(0, '.')

    modules = [
        'RKDRetriever',
        'DataProcessor',
        'FeatureEngineering',
        'PairsSelection',
        'stdout'
    ]

    all_importable = True
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}.py 可以导入")
        except Exception as e:
            print(f"✗ {module}.py 导入失败: {e}")
            all_importable = False

    return all_importable


def check_csv_format():
    """Check if CSV file has correct format"""
    try:
        with open('sp500_tickers_RIC.csv', 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                # Check if first line has comma
                if ',' in lines[0]:
                    print(f"✓ sp500_tickers_RIC.csv 格式正确 ({len(lines)} 行)")
                    return True
                else:
                    print("✗ sp500_tickers_RIC.csv 格式错误（需要逗号分隔）")
                    return False
            else:
                print("✗ sp500_tickers_RIC.csv 是空文件")
                return False
    except Exception as e:
        print(f"✗ 无法读取 sp500_tickers_RIC.csv: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 70)
    print("PairTrading 项目环境检查")
    print("=" * 70)

    print("\n[1/5] 检查 Python 版本...")
    python_ok = check_python_version()

    print("\n[2/5] 检查依赖包...")
    deps_ok = check_dependencies()

    print("\n[3/5] 检查必需文件...")
    files_ok = check_files()

    print("\n[4/5] 检查模块导入...")
    modules_ok = check_modules()

    print("\n[5/5] 检查CSV文件格式...")
    csv_ok = check_csv_format()

    print("\n" + "=" * 70)
    print("检查结果汇总")
    print("=" * 70)

    all_ok = python_ok and deps_ok and files_ok and modules_ok and csv_ok

    if all_ok:
        print("✓ 所有检查通过！您的环境配置正确。")
        print("\n下一步：")
        print("  1. 编辑 RKDRetriever.py 配置API凭证")
        print("  2. 运行 jupyter notebook Interface2ChangeForFinal.ipynb")
        return 0
    else:
        print("✗ 发现问题，请按照上述提示解决。")
        print("\n常见解决方案：")
        if not deps_ok:
            print("  • 安装依赖: pip install -r requirements.txt")
        if not files_ok:
            print("  • 确保所有文件都在项目目录中")
        if not modules_ok:
            print("  • 检查Python文件语法是否正确")
        if not csv_ok:
            print("  • 确保CSV文件格式为: Ticker,RIC")
        return 1


if __name__ == '__main__':
    exit(main())
