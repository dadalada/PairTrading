# 设置指南 / Setup Guide

## 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 配置API凭证 / Configure API Credentials

编辑 `RKDRetriever.py` 文件的第22-24行 / Edit lines 22-24 in `RKDRetriever.py`:

```python
self.username = 'your_email@example.com'  # 替换为您的用户名
self.password = 'your_password'           # 替换为您的密码
self.appid = 'YourApplicationID'          # 替换为您的应用ID
```

### 3. 准备股票代码数据 / Prepare Stock Ticker Data

项目已包含示例文件 `sp500_tickers_RIC.csv`，包含10只股票。

如需添加更多股票，请按以下格式编辑：
```
Ticker,RIC
AAPL,AAPL.O
MSFT,MSFT.OQ
...
```

**RIC代码格式说明**:
- `.O` = NYSE股票
- `.OQ` = NASDAQ股票
- `.N` = 纽约证券交易所
- 其他交易所请查阅Refinitiv文档

### 4. 运行代码 / Run the Code

#### 方法1：使用Jupyter Notebook
```bash
jupyter notebook Interface2ChangeForFinal.ipynb
```

#### 方法2：使用Python脚本
```python
from DataProcessor import DataProcessor
from RKDRetriever import RKDRetriever

# 初始化数据处理器
dp = DataProcessor('2020-01-01T00:00:00', '2023-12-31T23:59:59')

# 获取数据
stocks = dp.get_Stocks()
index = dp.get_index()
```

## 文件说明 / File Descriptions

### 核心模块 / Core Modules

- **RKDRetriever.py**: 从Refinitiv API获取数据
- **DataProcessor.py**: 数据预处理和清洗
- **FeatureEngineering.py**: 技术指标计算
- **PairsSelection.py**: 配对选择算法
- **stdout.py**: 实用工具函数（文件命名等）

### 数据文件 / Data Files

- **sp500_tickers_RIC.csv**: 股票代码映射表（必需）
- **data/**: 缓存的市场数据（自动创建）
- **output/**: 输出文件目录（自动创建）

### 配置文件 / Configuration Files

- **requirements.txt**: Python依赖包列表
- **README.md**: 详细项目文档（英文）
- **SETUP_GUIDE.md**: 本设置指南（中英文）

## 验证安装 / Verify Installation

运行以下命令检查环境配置：

```bash
python3 -c "
import numpy, pandas, sklearn, statsmodels, ta, matplotlib, seaborn, requests, openpyxl
print('✓ All dependencies installed successfully!')
"
```

如果看到成功消息，说明所有依赖都已正确安装。

## 常见问题 / Common Issues

### Q1: ModuleNotFoundError
**问题**: `ModuleNotFoundError: No module named 'XXX'`

**解决方案**:
```bash
pip install -r requirements.txt
```

### Q2: FileNotFoundError: sp500_tickers_RIC.csv
**问题**: 找不到股票代码文件

**解决方案**:
- 确保 `sp500_tickers_RIC.csv` 在项目根目录
- 文件格式必须是两列：Ticker,RIC

### Q3: Authentication failed
**问题**: API认证失败

**解决方案**:
- 检查 `RKDRetriever.py` 中的凭证是否正确
- 确认API订阅仍然有效
- 检查网络连接

### Q4: No row field, indicating that there may be no data
**问题**: 某些股票没有数据

**解决方案**:
- 检查RIC代码是否正确
- 确认日期范围有效
- 某些股票可能在该时期未交易，这是正常的

## 性能优化建议 / Performance Tips

1. **首次运行会较慢**: 需要下载所有历史数据
2. **后续运行会快**: 使用缓存数据
3. **减少股票数量**: 如果测试，可以只用5-10只股票
4. **缩短时间范围**: 减少训练窗口大小

## 系统要求 / System Requirements

- **Python**: 3.8 或更高
- **内存**: 建议 8GB+
- **磁盘空间**: 至少 2GB（用于数据缓存）
- **网络**: 稳定的互联网连接（用于API调用）

## 下一步 / Next Steps

安装完成后，请阅读 `README.md` 了解：
- 算法原理
- 参数配置
- 回测结果解读
- 高级功能

---

**需要帮助？**
如有问题，请查看 README.md 中的 Troubleshooting 部分。
