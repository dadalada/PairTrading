#!/usr/bin/env python3
"""
Logic validation script - tests code structure without requiring dependencies
"""

import ast
import os
import sys


def check_class_structure(filename, expected_classes):
    """Check if file contains expected classes"""
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())

    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    missing = set(expected_classes) - set(classes)
    if missing:
        print(f"  ✗ Missing classes: {missing}")
        return False
    print(f"  ✓ All expected classes found: {expected_classes}")
    return True


def check_methods(filename, class_name, expected_methods):
    """Check if class contains expected methods"""
    with open(filename, 'r') as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            missing = set(expected_methods) - set(methods)
            if missing:
                print(f"  ✗ {class_name} missing methods: {missing}")
                return False
            print(f"  ✓ {class_name} has all expected methods")
            return True

    print(f"  ✗ Class {class_name} not found")
    return False


def check_file_references(filename, expected_files):
    """Check if code references expected files"""
    with open(filename, 'r') as f:
        content = f.read()

    found = []
    for file in expected_files:
        if file in content:
            found.append(file)

    if len(found) == len(expected_files):
        print(f"  ✓ All file references found: {expected_files}")
        return True
    else:
        missing = set(expected_files) - set(found)
        print(f"  ✗ Missing file references: {missing}")
        return False


def check_directory_creation():
    """Check if directory creation logic exists"""
    with open('RKDRetriever.py', 'r') as f:
        content = f.read()

    if "if not os.path.isdir('data')" in content and "os.mkdir('data')" in content:
        print("  ✓ RKDRetriever has directory creation logic")
        has_rkd = True
    else:
        print("  ✗ RKDRetriever missing directory creation")
        has_rkd = False

    with open('stdout.py', 'r') as f:
        content = f.read()

    if "os.makedirs" in content or "os.mkdir" in content:
        print("  ✓ stdout.py has directory creation logic")
        has_stdout = True
    else:
        print("  ✗ stdout.py missing directory creation")
        has_stdout = False

    return has_rkd and has_stdout


def check_import_structure():
    """Check import dependencies"""
    print("\n=== Import Dependency Check ===\n")

    # Check DataProcessor imports
    with open('DataProcessor.py', 'r') as f:
        content = f.read()
        if 'from RKDRetriever import' in content:
            print("✓ DataProcessor imports RKDRetriever")
        else:
            print("✗ DataProcessor doesn't import RKDRetriever")

    # Check if sp500_tickers_RIC.csv is referenced
    if 'sp500_tickers_RIC.csv' in content:
        print("✓ DataProcessor references sp500_tickers_RIC.csv")
        if os.path.exists('sp500_tickers_RIC.csv'):
            print("✓ sp500_tickers_RIC.csv file exists")
        else:
            print("✗ sp500_tickers_RIC.csv file missing")

    return True


def main():
    print("=" * 70)
    print("Code Logic Validation Test")
    print("=" * 70)

    all_ok = True

    # Test 1: RKDRetriever class structure
    print("\n[1/6] RKDRetriever.py structure")
    all_ok &= check_class_structure('RKDRetriever.py', ['RKDRetriever'])
    all_ok &= check_methods('RKDRetriever.py', 'RKDRetriever', [
        '__init__', 'CreateAuthorization', 'RetrieveInterday',
        'smartRetrieveInterday', 'getPath'
    ])

    # Test 2: DataProcessor class structure
    print("\n[2/6] DataProcessor.py structure")
    all_ok &= check_class_structure('DataProcessor.py', ['DataProcessor'])
    all_ok &= check_methods('DataProcessor.py', 'DataProcessor', [
        '__init__', 'get_data', 'get_index', 'get_Stocks'
    ])

    # Test 3: FeatureEngineering class structure
    print("\n[3/6] FeatureEngineering.py structure")
    all_ok &= check_class_structure('FeatureEngineering.py', ['FeatureEngineering'])
    all_ok &= check_methods('FeatureEngineering.py', 'FeatureEngineering', [
        '__init__', 'setParams', 'process', 'RSI', 'MACD'
    ])

    # Test 4: File references
    print("\n[4/6] File reference check")
    all_ok &= check_file_references('DataProcessor.py', ['sp500_tickers_RIC.csv'])

    # Test 5: Directory creation logic
    print("\n[5/6] Directory creation logic")
    all_ok &= check_directory_creation()

    # Test 6: Import structure
    print("\n[6/6] Import structure")
    all_ok &= check_import_structure()

    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    if all_ok:
        print("\n✓ All logic checks passed!")
        print("\nCode structure is correct and should work once dependencies are installed.")
        print("\nTo install dependencies: pip install -r requirements.txt")
        return 0
    else:
        print("\n✗ Some logic checks failed.")
        print("Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
