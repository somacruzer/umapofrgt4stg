# 快速开始指南 ⚡

## 🚀 5分钟快速启动

### 第1步: 环境确认
```bash
# 检查conda是否安装
conda --version

# 检查当前环境
conda info --envs
```

### 第2步: 激活环境
```bash
# 如果sebrt环境已存在
conda activate sebrt

# 如果需要创建新环境
conda create -n sebrt python=3.13 -y
conda activate sebrt
pip install numpy pandas scipy scikit-learn plotly umap-learn
```

### 第3步: 运行分析
```bash
# 进入项目目录
cd "/Users/liuyunxing/Documents/upload/sentence-transformers/bipolar analysis output/final version of constructs cluster"

# 运行分析脚本
python final_constructs_cluster_analysis.py
```

### 第4步: 查看结果
```bash
# 在浏览器中打开可视化
open interactive_constructs_cluster_visualization.html

# 查看下载数据
head -5 constructs_cluster_dataset.csv
```

## 🎯 核心功能速览

### 主要文件说明

| 文件名 | 功能 | 用途 |
|--------|------|------|
| `final_constructs_cluster_analysis.py` | 主分析脚本 | 生成所有结果 |
| `interactive_constructs_cluster_visualization.html` | 交互式可视化 | 浏览器中查看 |
| `constructs_cluster_dataset.csv` | 下载数据集 | 用于进一步分析 |
| `COMPLETE_SETUP_GUIDE.md` | 完整指南 | 详细配置说明 |

### 数据下载字段

- `User_ID`: 用户标识
- `Survey_ID`: 调查ID  
- `Survey_Name`: 调查名称
- `Pole_A` / `Pole_B`: 双极构念
- `Cluster`: 聚类编号 (0-6)
- `UMAP_X` / `UMAP_Y`: 坐标

## 🔧 常见问题快速解决

### Q: 包导入错误
```bash
conda activate sebrt
pip install --upgrade plotly pandas numpy scikit-learn
```

### Q: 文件路径错误
```bash
# 确认当前目录
pwd
# 检查必需文件
ls -la "../umap_coordinates.csv"
ls -la "pid to survey.csv"
```

### Q: 内存不足
```python
# 检查内存
import psutil
print(f'可用内存: {psutil.virtual_memory().available / 1024**3:.1f} GB')
```

## 📊 快速数据分析

### 在Python中快速查看数据
```python
import pandas as pd

# 读取数据
df = pd.read_csv('constructs_cluster_dataset.csv')

# 快速统计
print(f"总记录: {len(df)}")
print(f"用户数: {df['User_ID'].nunique()}")
print(f"聚类分布:\n{df['Cluster'].value_counts().sort_index()}")
print(f"调查分布:\n{df['Survey_Name'].value_counts()}")
```

### 在Excel中快速分析
1. 打开 `constructs_cluster_dataset.csv`
2. 创建数据透视表
3. 行: `Cluster`, 列: `Survey_Name`, 值: `计数`

## 🎯 直接使用模板

### 模板1: 聚类分析
```python
import pandas as pd
df = pd.read_csv('constructs_cluster_dataset.csv')

# 聚类特征
for cluster in sorted(df['Cluster'].unique()):
    cluster_data = df[df['Cluster'] == cluster]
    print(f"\n聚类 {cluster}:")
    print(f"  用户数: {cluster_data['User_ID'].nunique()}")
    print(f"  主要调查: {cluster_data['Survey_Name'].mode()[0]}")
    print(f"  主要构念: {cluster_data['Pole_A'].value_counts().index[0]}")
```

### 模板2: 调查对比
```python
import pandas as pd
df = pd.read_csv('constructs_cluster_dataset.csv')

# 调查对比
cross_table = pd.crosstab(df['Survey_Name'], df['Cluster'])
print("调查 vs 聚类分布:")
print(cross_table)
```

## 🎨 可视化模板

### 简单散点图
```python
import plotly.express as px
df = pd.read_csv('constructs_cluster_dataset.csv')

fig = px.scatter(df, x='UMAP_X', y='UMAP_Y', 
                 color='Survey_Name', 
                 symbol='Cluster',
                 title='聚类分布图')
fig.show()
```

## 💡 最佳实践

### DO ✅
- 使用conda环境管理依赖
- 定期检查数据完整性
- 保存分析结果和代码
- 使用交互式可视化探索数据

### DON'T ❌
- 不要在base环境中安装包
- 不要跳过数据验证步骤
- 不要删除原始数据文件
- 不要忽略错误信息

## 🔄 故障恢复

### 完全重置环境
```bash
# 删除环境
conda deactivate
conda env remove -n sebrt

# 重新创建
conda create -n sebrt python=3.13 -y
conda activate sebrt
pip install numpy pandas scipy scikit-learn plotly umap-learn sentence-transformers

# 重新运行
python final_constructs_cluster_analysis.py
```

---

*遇到问题？查看 `COMPLETE_SETUP_GUIDE.md` 获取详细说明*
