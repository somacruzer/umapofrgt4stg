# 双极构念聚类分析系统 - 项目总览 🎯

## 📖 项目概述

本系统是一个完整的双极构念(Bipolar Constructs)聚类分析和可视化解决方案，支持从原始数据处理到交互式可视化的全流程分析。

### 🎯 核心功能
- **数据整合**: 合并UMAP坐标和调查数据
- **智能聚类**: 从667个微聚类优化到7个有意义的聚类
- **交互式可视化**: 支持多层级筛选和高亮显示
- **数据下载**: 生成标准化的分析数据集
- **统计分析**: 自动生成聚类和调查统计报告

### 📊 数据规模
- **4,096条数据记录**
- **358个唯一对话**
- **7个优化聚类**
- **5种调查类型**
- **100%数据完整性**

## 🏗️ 环境要求

### 推荐配置
- **操作系统**: macOS, Linux, Windows
- **Python**: 3.9 - 3.13 (推荐3.13)
- **内存**: 最少4GB，推荐8GB
- **存储**: 最少2GB可用空间

### 核心依赖
```bash
numpy>=2.1.0       # 数值计算
pandas>=2.2.0      # 数据处理
scipy>=1.14.0      # 科学计算
scikit-learn>=1.6.0 # 机器学习
plotly>=6.0.0      # 交互式可视化
umap-learn>=0.5.0  # 降维算法
```

## 📁 项目结构

```
final version of constructs cluster/
├── 🎯 核心脚本
│   ├── final_constructs_cluster_analysis.py    # 主分析脚本
│   └── validate_environment.py                 # 环境验证脚本
│
├── 📊 输出数据
│   ├── constructs_cluster_dataset.csv          # 用户下载数据集
│   ├── complete_processed_dataset.csv          # 完整处理数据
│   ├── cluster_analysis_statistics.csv         # 聚类统计
│   ├── survey_analysis_statistics.csv          # 调查统计
│   └── dataset_summary.txt                     # 数据摘要
│
├── 🎨 可视化
│   └── interactive_constructs_cluster_visualization.html
│
├── 📋 输入数据
│   └── pid to survey.csv                       # 调查映射文件
│
└── 📖 文档
    ├── README.md                               # 项目说明
    ├── COMPLETE_SETUP_GUIDE.md                # 完整配置指南  
    ├── QUICK_START.md                          # 快速开始
    ├── DATA_USAGE_GUIDE_CN.md                 # 数据使用指南
    └── PROJECT_OVERVIEW.md                    # 本文件
```

## 🚀 快速开始

### 1️⃣ 环境设置
```bash
# 创建conda环境
conda create -n sebrt python=3.13 -y
conda activate sebrt

# 安装依赖
pip install numpy pandas scipy scikit-learn plotly umap-learn
```

### 2️⃣ 环境验证
```bash
# 验证环境配置
python validate_environment.py
```

### 3️⃣ 运行分析
```bash
# 执行完整分析
python final_constructs_cluster_analysis.py
```

### 4️⃣ 查看结果
```bash
# 在浏览器中打开可视化
open interactive_constructs_cluster_visualization.html
```

## 📈 核心输出说明

### 🎨 交互式可视化
**文件**: `interactive_constructs_cluster_visualization.html`

**功能特性**:
- 🏠 **全数据显示**: 查看完整数据集
- 📊 **聚类模式**: 仅显示聚类边界和数据点
- 🎯 **调查模式**: 高亮显示特定调查数据
- 🔍 **智能筛选**: 支持单调查、多调查组合筛选
- 📍 **聚类聚焦**: 单独查看特定聚类
- 🎭 **混合视图**: 同时显示聚类和调查信息

### 📊 用户下载数据集
**文件**: `constructs_cluster_dataset.csv`

**核心字段**:
| 字段 | 说明 | 用途 |
|------|------|------|
| User_ID | 用户标识 | 追踪个体行为 |
| Survey_ID | 调查ID | 区分调查项目 |
| Survey_Name | 调查名称 | 调查类型分析 |
| Pole_A / Pole_B | 双极构念 | 语义分析 |
| Cluster | 聚类编号 | 群体分析 |
| UMAP_X / UMAP_Y | 坐标 | 空间分析 |

### 📈 统计报告
- **聚类统计**: 每个聚类的规模、特征、主要构念
- **调查统计**: 各调查的分布、聚类偏好、参与度
- **数据摘要**: 整体数据质量和分布概览

## 🔧 高级功能

### 自定义聚类数量
```python
# 修改聚类数量 (默认7)
clustering = AgglomerativeClustering(n_clusters=5, linkage='ward')
```

### 调整可视化参数
```python
# 修改图表尺寸和样式
fig.update_layout(
    width=1600,   # 调整宽度
    height=1000,  # 调整高度
    title_font_size=20  # 调整标题大小
)
```

### 数据筛选示例
```python
# 按调查筛选
survey_data = df[df['Survey_Name'] == 'Construct Elaboration']

# 按聚类筛选  
cluster_data = df[df['Cluster'] == 0]

# 复合筛选
filtered = df[(df['Survey_Name'] == 'Positive') & (df['Cluster'].isin([0,1,2]))]
```

## 🎯 使用场景

### 学术研究
- **心理学研究**: 个人构念理论分析
- **认知科学**: 概念结构研究
- **语言学**: 语义关系分析
- **社会科学**: 群体认知模式研究

### 商业应用
- **用户行为分析**: 理解用户认知偏好
- **产品定位**: 基于构念的市场细分
- **品牌研究**: 品牌认知结构分析
- **调研分析**: 多维度调查数据整合

### 技术应用
- **机器学习**: 特征工程和数据预处理
- **数据可视化**: 高维数据降维展示
- **聚类算法**: 无监督学习应用
- **交互设计**: 用户界面优化参考

## 🏆 系统优势

### 🎯 **技术优势**
- **高效算法**: 使用UMAP进行高质量降维
- **智能聚类**: 自动优化聚类数量和质量
- **响应式设计**: 支持大规模数据实时交互
- **模块化架构**: 易于扩展和定制

### 📊 **分析优势**
- **多维度整合**: 同时分析构念、调查、聚类三个维度
- **灵活筛选**: 支持15+种不同的数据视图
- **质量保证**: 自动数据验证和完整性检查
- **标准化输出**: 兼容多种分析工具的数据格式

### 🎨 **用户体验优势**
- **零代码操作**: 浏览器即可进行复杂分析
- **直观可视**: 空间位置直接反映相似性
- **即时反馈**: 实时筛选和高亮显示
- **专业输出**: 可直接用于论文和报告的图表

## 🛠️ 故障排除

### 常见问题及解决方案

#### 环境问题
```bash
# 包冲突
conda env remove -n sebrt
conda create -n sebrt python=3.13 -y

# 依赖缺失
pip install --upgrade pip
pip install -r requirements.txt
```

#### 数据问题
```bash
# 文件路径
ls -la "../umap_coordinates.csv"
ls -la "pid to survey.csv"

# 数据验证
python validate_environment.py
```

#### 性能问题
```python
# 内存优化
df = pd.read_csv('data.csv', dtype={'cluster': 'int8'})

# 显示优化
fig.update_traces(marker_size=6)  # 减小点大小
```

## 📞 技术支持

### 日志和调试
系统自动生成详细日志，包括：
- 数据处理步骤记录
- 聚类算法参数
- 可视化生成过程
- 错误信息和警告

### 性能监控
使用内置的性能监控功能：
- 内存使用情况
- 处理时间统计
- 数据质量评估
- 系统资源利用率

### 扩展开发
系统采用模块化设计，支持：
- 自定义聚类算法
- 新的数据源集成
- 可视化样式定制
- 输出格式扩展

## 🔄 更新日志

### v1.0.0 (2025-07-24)
- ✅ 初始版本发布
- ✅ 完整的数据处理管道
- ✅ 交互式可视化系统
- ✅ 数据下载功能
- ✅ 环境验证脚本
- ✅ 完整文档系统

### 🎯 未来规划
- 📊 支持更多聚类算法选择
- 🎨 可视化主题定制
- 📱 移动端适配
- 🔗 API接口开发
- 🤖 自动化报告生成

---

**项目维护**: 双极构念聚类分析团队  
**最后更新**: 2025年7月24日  
**版本**: v1.0.0
