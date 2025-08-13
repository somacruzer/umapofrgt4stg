# 双极构念聚类分析系统 - 完整环境配置与操作指南

## 📋 系统概述

本系统提供双极构念(Bipolar Constructs)的UMAP聚类分析和交互式可视化功能，支持多survey数据整合、灵活筛选和数据下载。

## 🏗️ 第一部分：环境搭建

### 1.1 系统要求

- **操作系统**: macOS, Linux, Windows
- **Python版本**: 3.9 - 3.13
- **内存**: 至少 8GB RAM
- **存储**: 至少 2GB 可用空间

### 1.2 Conda环境创建

#### 步骤1: 创建新的conda环境
```bash
# 创建名为sebrt的新环境，使用Python 3.13
conda create -n sebrt python=3.13 -y

# 激活环境
conda activate sebrt
```

#### 步骤2: 安装核心依赖包
```bash
# 安装科学计算包
conda install numpy=2.1.3 pandas=2.2.3 scipy=1.14.1 -y

# 安装机器学习包
conda install scikit-learn=1.6.1 -y

# 安装可视化包
conda install plotly=6.0.1 -y

# 安装UMAP (通过pip，因为conda版本可能不是最新)
pip install umap-learn

# 安装sentence-transformers
pip install sentence-transformers
```

#### 步骤3: 验证安装
```bash
python -c "
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial import ConvexHull
import umap
print('所有包安装成功！')
print('NumPy版本:', np.__version__)
print('Pandas版本:', pd.__version__)
print('Plotly版本:', go.__version__)
"
```

### 1.3 替代环境配置（如果上述方法有问题）

#### 使用requirements.txt方式：
```bash
# 创建环境
conda create -n sebrt python=3.13 -y
conda activate sebrt

# 创建requirements.txt文件
cat > requirements.txt << 'EOF'
numpy==2.1.3
pandas==2.2.3
scipy==1.14.1
scikit-learn==1.6.1
plotly==6.0.1
umap-learn>=0.5.3
sentence-transformers>=2.2.0
EOF

# 安装依赖
pip install -r requirements.txt
```

## 📂 第二部分：数据准备

### 2.1 数据文件结构

系统需要以下输入文件：

#### 必需文件：
1. **原始UMAP坐标文件** (`../umap_coordinates.csv`)
```csv
index,pid,agg_cluster,x,y
0,01903166-988A-4E13-B883-878582894D29,21,4.7684383,4.328492
1,01903166-988A-4E13-B883-878582894D29,25,1.4595591,2.9183085
...
```

2. **Survey映射文件** (`pid to survey.csv`)
```csv
conversation_id,construct,construct_bipolar,survey_id,survey_name,survey_endTime
01903166-988A-4E13-B883-878582894D29,Traditional,Innovative,b2b8d8e1-3557,Construct Elaboration,2025-01-08 07:37:18
01903166-988A-4E13-B883-878582894D29,Richness,Lightness,b2b8d8e1-3557,Construct Elaboration,2025-01-08 07:37:18
...
```

### 2.2 数据格式说明

#### UMAP坐标文件格式：
- `index`: 数据点索引
- `pid`: 对话ID (conversation_id)
- `agg_cluster`: 原始聚类编号
- `x`, `y`: UMAP坐标

#### Survey映射文件格式：
- `conversation_id`: 对话ID (对应pid)
- `construct`: 双极构念的A极 (pole_a)
- `construct_bipolar`: 双极构念的B极 (pole_b)
- `survey_id`: 调查ID
- `survey_name`: 调查名称
- `survey_endTime`: 调查结束时间

### 2.3 数据准备检查清单

```bash
# 检查文件是否存在
ls -la "../umap_coordinates.csv"
ls -la "pid to survey.csv"

# 检查文件格式和内容
head -5 "../umap_coordinates.csv"
head -5 "pid to survey.csv"

# 检查数据完整性
python -c "
import pandas as pd
coords = pd.read_csv('../umap_coordinates.csv')
survey = pd.read_csv('pid to survey.csv')
print(f'坐标数据: {len(coords)} 行')
print(f'Survey数据: {len(survey)} 行')
print(f'唯一对话ID: {coords[\"pid\"].nunique()}')
print(f'Survey类型: {survey[\"survey_name\"].nunique()}')
"
```

## 🚀 第三部分：系统运行

### 3.1 下载和准备脚本

```bash
# 确保在正确目录
cd "/Users/liuyunxing/Documents/upload/sentence-transformers/bipolar analysis output/final version of constructs cluster"

# 确认脚本存在
ls -la final_constructs_cluster_analysis.py
```

### 3.2 运行分析系统

```bash
# 激活环境
conda activate sebrt

# 运行完整分析
python final_constructs_cluster_analysis.py
```

### 3.3 预期输出

运行成功后会生成以下文件：

#### 数据文件：
- `complete_processed_dataset.csv` - 完整处理后的数据集
- `constructs_cluster_dataset.csv` - 用户下载的精简数据集
- `cluster_analysis_statistics.csv` - 聚类分析统计
- `survey_analysis_statistics.csv` - 调查分析统计
- `dataset_summary.txt` - 数据集摘要

#### 可视化文件：
- `interactive_constructs_cluster_visualization.html` - 交互式可视化

## 📊 第四部分：功能使用指南

### 4.1 交互式可视化

#### 打开可视化：
```bash
# 在浏览器中打开
open interactive_constructs_cluster_visualization.html
# 或直接双击HTML文件
```

#### 主要功能：
1. **🏠 Show All Data** - 显示所有数据
2. **📊 Clusters Only** - 仅显示聚类
3. **🎯 Surveys Only** - 仅显示调查数据
4. **🔍 Highlight [Survey]** - 高亮特定调查
5. **📍 Cluster X Only** - 显示特定聚类

### 4.2 数据下载功能

#### 下载的CSV文件包含：
- `User_ID`: 用户标识 (基于conversation_id)
- `Survey_ID`: 调查ID
- `Survey_Name`: 调查名称
- `Pole_A`: 双极构念A极
- `Pole_B`: 双极构念B极  
- `Cluster`: 聚类编号 (0-6)
- `UMAP_X`: X坐标
- `UMAP_Y`: Y坐标

#### 使用下载数据：
```python
import pandas as pd

# 读取下载的数据
df = pd.read_csv('constructs_cluster_dataset.csv')

# 基本统计
print(df.describe())
print(df['Cluster'].value_counts())
print(df['Survey_Name'].value_counts())

# 分析示例
cluster_survey = pd.crosstab(df['Cluster'], df['Survey_Name'])
print(cluster_survey)
```

## 🔧 第五部分：故障排除

### 5.1 常见问题

#### 问题1: 包导入错误
```bash
# 解决方案：重新安装包
conda activate sebrt
pip install --upgrade plotly pandas numpy scikit-learn scipy
```

#### 问题2: 文件路径错误
```bash
# 检查文件路径
pwd
ls -la "../umap_coordinates.csv"
ls -la "pid to survey.csv"
```

#### 问题3: 内存不足
```bash
# 监控内存使用
python -c "
import psutil
print(f'可用内存: {psutil.virtual_memory().available / 1024**3:.1f} GB')
"
```

### 5.2 环境重置

如果环境出现问题，可以完全重置：

```bash
# 删除旧环境
conda deactivate
conda env remove -n sebrt

# 重新创建环境
conda create -n sebrt python=3.13 -y
conda activate sebrt

# 重新安装包
pip install numpy pandas scipy scikit-learn plotly umap-learn sentence-transformers
```

### 5.3 数据验证

```bash
# 运行数据验证脚本
python -c "
import pandas as pd
import numpy as np

# 检查数据完整性
try:
    coords = pd.read_csv('../umap_coordinates.csv')
    survey = pd.read_csv('pid to survey.csv')
    
    print('✅ 文件读取成功')
    print(f'坐标数据: {len(coords)} 行, {len(coords.columns)} 列')
    print(f'Survey数据: {len(survey)} 行, {len(survey.columns)} 列')
    
    # 检查必需列
    required_coords = ['index', 'pid', 'agg_cluster', 'x', 'y']
    required_survey = ['conversation_id', 'construct', 'construct_bipolar', 'survey_name']
    
    for col in required_coords:
        if col not in coords.columns:
            print(f'❌ 坐标文件缺少列: {col}')
        else:
            print(f'✅ 坐标文件包含: {col}')
    
    for col in required_survey:
        if col not in survey.columns:
            print(f'❌ Survey文件缺少列: {col}')
        else:
            print(f'✅ Survey文件包含: {col}')
            
    print('数据验证完成!')
    
except Exception as e:
    print(f'❌ 错误: {e}')
"
```

## 📈 第六部分：高级使用

### 6.1 自定义聚类数量

如需修改聚类数量（默认7个），编辑脚本中的参数：

```python
# 在final_constructs_cluster_analysis.py中找到这行：
clustering = AgglomerativeClustering(n_clusters=7, linkage='ward')

# 修改为所需数量，例如5个聚类：
clustering = AgglomerativeClustering(n_clusters=5, linkage='ward')
```

### 6.2 批处理多个数据集

```bash
# 创建批处理脚本
cat > batch_process.py << 'EOF'
import os
import subprocess

datasets = [
    'dataset1',
    'dataset2', 
    'dataset3'
]

for dataset in datasets:
    print(f"处理数据集: {dataset}")
    os.chdir(f"/path/to/{dataset}")
    subprocess.run(['python', 'final_constructs_cluster_analysis.py'])
    print(f"完成: {dataset}")
EOF

python batch_process.py
```

### 6.3 性能优化

对于大型数据集，可以调整这些参数：

```python
# 减少UMAP计算复杂度
umap_reducer = umap.UMAP(
    n_neighbors=15,    # 默认15，减少到10-15
    min_dist=0.1,      # 默认0.1
    n_components=2,    # 保持2D
    random_state=42,
    metric='cosine'
)

# 使用更快的聚类算法
from sklearn.cluster import KMeans
clustering = KMeans(n_clusters=7, random_state=42)
```

## 📞 支持与联系

如遇问题，请提供以下信息：
1. 错误信息的完整截图
2. Python版本和包版本
3. 输入数据文件的前几行
4. 运行环境(macOS/Linux/Windows)

---

*最后更新: 2025年7月24日*
