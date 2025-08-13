# Data Usage Guide - Quick Reference

## 🎯 **Main Download File**
**File**: `constructs_cluster_dataset.csv`
**Purpose**: Ready-to-use dataset for analysis and research

## 📊 **Key Columns for Analysis**

### Essential Fields:
- **User_ID**: Unique conversation identifier 
- **Survey_ID**: Survey session identifier
- **Survey_Name**: Survey type (5 categories)
- **Pole_A & Pole_B**: Bipolar construct poles
- **Cluster**: Cluster assignment (0-6)
- **Coordinate_X/Y**: Visualization coordinates

### Additional Fields:
- **Conversation_Index**: Sequential numbering (1-358)
- **Bipolar_Construct**: "Pole_A vs Pole_B" format
- **Cluster_Size**: Points per cluster

## 🔧 **Quick Analysis Examples**

### Excel/Google Sheets:
1. Open `constructs_cluster_dataset.csv`
2. Create pivot tables using Cluster and Survey_Name
3. Filter by specific surveys or clusters
4. Analyze construct patterns

### Python:
```python
import pandas as pd
df = pd.read_csv('constructs_cluster_dataset.csv')
print(df.groupby('Cluster')['Survey_Name'].value_counts())
```

### R:
```r
data <- read.csv('constructs_cluster_dataset.csv')
table(data$Cluster, data$Survey_Name)
```

## 🎨 **Interactive Visualization**
**File**: `interactive_constructs_cluster_visualization.html`
- Open in web browser
- Use dropdown for filtering
- Hover for detailed information

## 📈 **Dataset Quick Facts**
- **Records**: 4,096 data points
- **Conversations**: 358 unique conversations  
- **Clusters**: 7 clusters (optimized from 667)
- **Surveys**: 5 survey types
- **Quality**: 100% complete essential data

## 🎯 **Common Research Questions**

1. **"Which surveys cluster together?"**
   - Filter by individual surveys in visualization
   - Check survey_analysis_statistics.csv

2. **"What constructs define each cluster?"**
   - Group by Cluster, analyze Bipolar_Construct
   - Check cluster_analysis_statistics.csv

3. **"How are coordinates distributed?"**
   - Plot Coordinate_X vs Coordinate_Y by Cluster
   - Use interactive visualization

4. **"Which cluster is most diverse?"**
   - Check Cluster_Size column
   - Count unique Survey_Name per Cluster

## 💡 **Pro Tips**
- Use User_ID to track individual conversation patterns
- Combine Survey_Name + Cluster for detailed segmentation  
- Coordinate_X/Y are perfect for spatial analysis
- Bipolar_Construct provides human-readable construct pairs
