# 双极构念聚类数据使用指南 📊

## 🎯 数据下载功能概述

系统自动生成用户友好的数据下载文件，包含所有关键信息，便于进一步分析和研究。

## 📋 下载数据集说明

### 主要下载文件：`constructs_cluster_dataset.csv`

该文件包含以下8个核心字段：

| 字段名 | 说明 | 示例值 | 用途 |
|--------|------|--------|------|
| `User_ID` | 用户唯一标识符 | `user_001`, `user_358` | 追踪个体用户 |
| `Survey_ID` | 调查项目ID | `b2b8d8e1-3557-4355` | 区分不同调查 |
| `Survey_Name` | 调查名称 | `Construct Elaboration` | 调查类型识别 |
| `Pole_A` | 双极构念A极 | `Traditional` | 构念的一端 |
| `Pole_B` | 双极构念B极 | `Innovative` | 构念的另一端 |
| `Cluster` | 聚类编号 | `0`, `1`, `2`, `3`, `4`, `5`, `6` | 7个聚类组 |
| `UMAP_X` | X轴坐标 | `4.768` | 可视化位置 |
| `UMAP_Y` | Y轴坐标 | `4.328` | 可视化位置 |

## 🔍 数据使用示例

### 基础数据探索

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取下载的数据
df = pd.read_csv('constructs_cluster_dataset.csv')

# 数据概览
print("数据集基本信息:")
print(f"总记录数: {len(df)}")
print(f"用户数: {df['User_ID'].nunique()}")
print(f"调查类型: {df['Survey_Name'].nunique()}")
print(f"聚类数: {df['Cluster'].nunique()}")

# 数据分布
print("\n聚类分布:")
print(df['Cluster'].value_counts().sort_index())

print("\n调查分布:")
print(df['Survey_Name'].value_counts())
```

### 聚类分析

```python
# 聚类特征分析
cluster_stats = df.groupby('Cluster').agg({
    'User_ID': 'nunique',
    'Survey_Name': lambda x: x.mode()[0],  # 最常见的调查
    'Pole_A': lambda x: ', '.join(x.value_counts().head(3).index),
    'UMAP_X': ['mean', 'std'],
    'UMAP_Y': ['mean', 'std']
}).round(3)

print("聚类特征统计:")
print(cluster_stats)
```

### 调查交叉分析

```python
# 调查与聚类交叉表
cross_table = pd.crosstab(df['Cluster'], df['Survey_Name'])
print("聚类 vs 调查交叉表:")
print(cross_table)

# 计算百分比
cross_pct = pd.crosstab(df['Cluster'], df['Survey_Name'], normalize='index') * 100
print("\n聚类内调查分布百分比:")
print(cross_pct.round(1))
```

### 双极构念分析

```python
# 构念对分析
df['Bipolar_Construct'] = df['Pole_A'] + ' vs ' + df['Pole_B']

# 最常见的构念对
top_constructs = df['Bipolar_Construct'].value_counts().head(10)
print("Top 10 双极构念对:")
print(top_constructs)

# 按聚类的构念分布
for cluster in sorted(df['Cluster'].unique()):
    cluster_data = df[df['Cluster'] == cluster]
    top_3 = cluster_data['Bipolar_Construct'].value_counts().head(3)
    print(f"\n聚类 {cluster} 的主要构念:")
    print(top_3)
```

## 📈 高级分析示例

### 1. 聚类质量评估

```python
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import silhouette_score

# 计算轮廓系数
coords = df[['UMAP_X', 'UMAP_Y']].values
labels = df['Cluster'].values
silhouette_avg = silhouette_score(coords, labels)
print(f"平均轮廓系数: {silhouette_avg:.3f}")

# 聚类内距离和聚类间距离
for cluster in sorted(df['Cluster'].unique()):
    cluster_coords = df[df['Cluster'] == cluster][['UMAP_X', 'UMAP_Y']].values
    if len(cluster_coords) > 1:
        intra_dist = pdist(cluster_coords).mean()
        print(f"聚类 {cluster} 内部平均距离: {intra_dist:.3f}")
```

### 2. 调查偏好模式分析

```python
# 每个调查的聚类偏好
survey_preferences = {}
for survey in df['Survey_Name'].unique():
    survey_data = df[df['Survey_Name'] == survey]
    cluster_dist = survey_data['Cluster'].value_counts(normalize=True).sort_index()
    survey_preferences[survey] = cluster_dist

preferences_df = pd.DataFrame(survey_preferences).fillna(0)
print("调查的聚类偏好模式:")
print(preferences_df.round(3))
```

### 3. 用户行为分析

```python
# 用户多样性分析
user_diversity = df.groupby('User_ID').agg({
    'Cluster': 'nunique',
    'Survey_Name': 'nunique', 
    'Bipolar_Construct': 'nunique'
}).rename(columns={
    'Cluster': 'clusters_engaged',
    'Survey_Name': 'surveys_participated',
    'Bipolar_Construct': 'unique_constructs'
})

print("用户参与度统计:")
print(user_diversity.describe())

# 高活跃用户
high_activity = user_diversity[user_diversity['clusters_engaged'] >= 3]
print(f"\n跨多聚类用户数: {len(high_activity)}")
```

## 📊 可视化建议

### 使用Plotly创建自定义图表

```python
import plotly.express as px
import plotly.graph_objects as go

# 1. 聚类分布饼图
cluster_counts = df['Cluster'].value_counts().sort_index()
fig1 = px.pie(values=cluster_counts.values, 
              names=[f'Cluster {i}' for i in cluster_counts.index],
              title='聚类分布')
fig1.show()

# 2. 调查参与度条形图
survey_counts = df['Survey_Name'].value_counts()
fig2 = px.bar(x=survey_counts.values, y=survey_counts.index,
              orientation='h', title='调查参与度')
fig2.show()

# 3. 2D散点图（按调查着色）
fig3 = px.scatter(df, x='UMAP_X', y='UMAP_Y', 
                  color='Survey_Name', 
                  symbol='Cluster',
                  title='UMAP聚类 - 按调查着色')
fig3.show()
```

### 使用Seaborn进行统计可视化

```python
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 聚类-调查热力图
plt.figure(figsize=(10, 6))
cross_table = pd.crosstab(df['Cluster'], df['Survey_Name'])
sns.heatmap(cross_table, annot=True, fmt='d', cmap='Blues')
plt.title('聚类 vs 调查分布热力图')
plt.show()

# 2. 坐标分布箱型图
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(data=df, x='Cluster', y='UMAP_X', ax=axes[0])
sns.boxplot(data=df, x='Cluster', y='UMAP_Y', ax=axes[1])
axes[0].set_title('X坐标分布')
axes[1].set_title('Y坐标分布')
plt.tight_layout()
plt.show()
```

## 💾 数据导出选项

### 按聚类导出

```python
# 为每个聚类创建单独文件
for cluster in sorted(df['Cluster'].unique()):
    cluster_data = df[df['Cluster'] == cluster]
    filename = f'cluster_{cluster}_data.csv'
    cluster_data.to_csv(filename, index=False)
    print(f"导出 {filename}: {len(cluster_data)} 记录")
```

### 按调查导出

```python
# 为每个调查创建单独文件
for survey in df['Survey_Name'].unique():
    survey_data = df[df['Survey_Name'] == survey]
    filename = f'survey_{survey.replace(" ", "_")}_data.csv'
    survey_data.to_csv(filename, index=False)
    print(f"导出 {filename}: {len(survey_data)} 记录")
```

### 摘要报告导出

```python
# 创建摘要报告
summary_report = {
    'dataset_overview': {
        'total_records': len(df),
        'unique_users': df['User_ID'].nunique(),
        'unique_surveys': df['Survey_Name'].nunique(),
        'clusters': df['Cluster'].nunique()
    },
    'cluster_distribution': df['Cluster'].value_counts().to_dict(),
    'survey_distribution': df['Survey_Name'].value_counts().to_dict(),
    'top_constructs': df['Bipolar_Construct'].value_counts().head(5).to_dict()
}

import json
with open('analysis_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary_report, f, ensure_ascii=False, indent=2)
```

## 🔗 与其他工具集成

### R语言使用

```r
# 在R中读取数据
library(readr)
library(dplyr)
library(ggplot2)

df <- read_csv("constructs_cluster_dataset.csv")

# 基础统计
summary(df)

# 聚类可视化
ggplot(df, aes(x = UMAP_X, y = UMAP_Y, color = factor(Cluster))) +
  geom_point(alpha = 0.7) +
  labs(title = "UMAP Clustering Visualization",
       color = "Cluster") +
  theme_minimal()
```

### Excel分析

1. **数据透视表**: 使用Cluster和Survey_Name创建交叉分析
2. **条件格式**: 高亮显示特定聚类或调查
3. **图表创建**: 制作聚类分布饼图和调查参与度柱状图

## 📝 研究建议

### 分析流程推荐

1. **数据探索** (5-10分钟)
   - 查看数据概览和基本统计
   - 检查数据质量和完整性

2. **聚类分析** (15-20分钟)
   - 分析聚类分布和特征
   - 评估聚类质量

3. **调查分析** (15-20分钟)
   - 调查参与度分析
   - 跨调查比较

4. **构念分析** (20-30分钟)
   - 双极构念模式识别
   - 语义相似性分析

5. **可视化报告** (15-20分钟)
   - 创建关键图表
   - 生成研究报告

### 研究问题示例

- 不同调查的参与者是否表现出不同的聚类偏好？
- 某些双极构念是否更容易聚集在特定区域？
- 用户的多样性程度如何影响聚类分布？
- 是否存在调查特异性的构念模式？

---

*该指南提供了全面的数据使用方法，支持多种分析需求和研究目标。*
