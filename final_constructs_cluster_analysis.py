#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Re-cluster Original Data to 7 Clusters with Survey Integration
Take the original UMAP coordinates with conversation_ids and re-cluster to 7 groups
"""

import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import plotly.graph_objects as go
import plotly.express as px
from scipy.spatial import ConvexHull
import os

def load_and_recluster_data():
    """Load original data and re-cluster to 7 groups"""
    print("Loading original UMAP data...")
    
    # Load original coordinates with conversation_ids
    original_coords = pd.read_csv("../umap_coordinates.csv")
    print(f"Loaded original data: {len(original_coords)} records, {original_coords['agg_cluster'].nunique()} clusters")
    
    # Extract coordinates for re-clustering
    coordinates = original_coords[['x', 'y']].values
    
    # Apply Agglomerative clustering to reduce to 7 clusters
    print("Re-clustering to 7 groups...")
    clustering = AgglomerativeClustering(n_clusters=7, linkage='ward')
    new_clusters = clustering.fit_predict(coordinates)
    
    # Add new cluster assignments
    original_coords['cluster_7'] = new_clusters
    
    # Load survey mapping data
    survey_file = "pid to survey.csv"
    if os.path.exists(survey_file):
        survey_df = pd.read_csv(survey_file)
        print(f"Loaded survey data: {len(survey_df)} records")
        
        # Merge with survey data using conversation_id (pid)
        merged_df = original_coords.merge(
            survey_df, 
            left_on='pid', 
            right_on='conversation_id', 
            how='left'
        )
        print(f"Merged data: {len(merged_df)} records")
        
        # Add bipolar terms information
        if 'construct' in merged_df.columns and 'construct_bipolar' in merged_df.columns:
            # construct = pole_a, construct_bipolar = pole_b
            merged_df['pole_a'] = merged_df['construct']
            merged_df['pole_b'] = merged_df['construct_bipolar']
        
        return merged_df
    else:
        print("Survey data not found, using coordinates only")
        return original_coords

def get_convex_hull_data(df, cluster_col='cluster_7'):
    """Calculate convex hull for each cluster"""
    hull_data = []
    
    for cluster in sorted(df[cluster_col].unique()):
        cluster_data = df[df[cluster_col] == cluster]
        if len(cluster_data) >= 3:  # Need at least 3 points to form convex hull
            try:
                points = cluster_data[['x', 'y']].values
                hull = ConvexHull(points)
                hull_points = points[hull.vertices]
                # Close the polygon
                hull_points = np.vstack([hull_points, hull_points[0]])
                
                hull_data.append({
                    'cluster': cluster,
                    'hull_x': hull_points[:, 0].tolist(),
                    'hull_y': hull_points[:, 1].tolist()
                })
            except Exception as e:
                print(f"Cannot calculate convex hull for cluster {cluster}: {e}")
    
    return hull_data

def create_interactive_plot_with_surveys(df):
    """Create interactive visualization with flexible survey filtering"""
    print("Creating interactive visualization...")
    
    # Get unique surveys if available
    surveys = []
    if 'survey_name' in df.columns:
        surveys = sorted(df['survey_name'].dropna().unique())
        print(f"Found {len(surveys)} surveys: {surveys}")
    
    # Get cluster colors
    clusters = sorted(df['cluster_7'].unique())
    colors = px.colors.qualitative.Set3
    if len(clusters) > len(colors):
        colors = colors * ((len(clusters) // len(colors)) + 1)
    color_map = dict(zip(clusters, colors[:len(clusters)]))
    
    # Survey colors for highlighting
    survey_colors = px.colors.qualitative.Pastel
    if len(surveys) > len(survey_colors):
        survey_colors = survey_colors * ((len(surveys) // len(survey_colors)) + 1)
    survey_color_map = dict(zip(surveys, survey_colors[:len(surveys)]))
    
    # Calculate convex hulls
    hull_data = get_convex_hull_data(df)
    
    # Create figure
    fig = go.Figure()
    
    # Add cluster boundaries (initially visible)
    for hull in hull_data:
        cluster = hull['cluster']
        fig.add_trace(go.Scatter(
            x=hull['hull_x'],
            y=hull['hull_y'],
            mode='lines',
            line=dict(color=color_map[cluster], width=2),
            fill='toself',
            fillcolor=color_map[cluster],
            opacity=0.2,
            name=f'Cluster {cluster} Boundary',
            showlegend=False,
            hoverinfo='skip',
            visible=True
        ))
    
    # Add data points for each cluster
    for cluster in clusters:
        cluster_data = df[df['cluster_7'] == cluster]
        
        # Prepare hover information
        hover_text = []
        for _, row in cluster_data.iterrows():
            text = f"Conversation ID: {row['pid']}<br>"
            text += f"Cluster: {row['cluster_7']}<br>"
            text += f"Coordinates: ({row['x']:.3f}, {row['y']:.3f})<br>"
            
            if 'survey_name' in row and pd.notna(row['survey_name']):
                text += f"Survey: {row['survey_name']}<br>"
            
            if 'pole_a' in row and 'pole_b' in row and pd.notna(row['pole_a']):
                text += f"Bipolar: {row['pole_a']} vs {row['pole_b']}"
            elif 'construct_bipolar' in row and pd.notna(row['construct_bipolar']):
                text += f"Construct: {row['construct_bipolar']}"
            
            hover_text.append(text)
        
        fig.add_trace(go.Scatter(
            x=cluster_data['x'],
            y=cluster_data['y'],
            mode='markers',
            marker=dict(
                color=color_map[cluster],
                size=8,
                opacity=0.8,
                line=dict(width=1, color='white')
            ),
            name=f'Cluster {cluster} ({len(cluster_data)} points)',
            text=hover_text,
            hovertemplate='%{text}<extra></extra>',
            visible=True
        ))
    
    # Add survey-specific traces for highlighting
    survey_traces_start = len(hull_data) + len(clusters)
    for survey in surveys:
        survey_data = df[df['survey_name'] == survey]
        
        # Prepare hover information for survey data
        hover_text = []
        for _, row in survey_data.iterrows():
            text = f"<b>SURVEY: {survey}</b><br>"
            text += f"Conversation ID: {row['pid']}<br>"
            text += f"Cluster: {row['cluster_7']}<br>"
            text += f"Coordinates: ({row['x']:.3f}, {row['y']:.3f})<br>"
            
            if 'pole_a' in row and 'pole_b' in row and pd.notna(row['pole_a']):
                text += f"Bipolar: {row['pole_a']} vs {row['pole_b']}"
            elif 'construct_bipolar' in row and pd.notna(row['construct_bipolar']):
                text += f"Construct: {row['construct_bipolar']}"
            
            hover_text.append(text)
        
        fig.add_trace(go.Scatter(
            x=survey_data['x'],
            y=survey_data['y'],
            mode='markers',
            marker=dict(
                color=survey_color_map[survey],
                size=10,
                opacity=0.9,
                line=dict(width=2, color='darkblue'),
                symbol='diamond'
            ),
            name=f'🔍 {survey} ({len(survey_data)} points)',
            text=hover_text,
            hovertemplate='%{text}<extra></extra>',
            visible=False  # Initially hidden
        ))
    
    # Create comprehensive button system
    buttons = []
    
    # Basic view controls
    buttons.extend([
        {
            'label': '🏠 Show All Data',
            'method': 'restyle',
            'args': [{'visible': [True] * (len(hull_data) + len(clusters)) + [False] * len(surveys)}]
        },
        {
            'label': '📊 Clusters Only',
            'method': 'restyle', 
            'args': [{'visible': [True] * len(hull_data) + [True] * len(clusters) + [False] * len(surveys)}]
        },
        {
            'label': '🎯 Surveys Only',
            'method': 'restyle',
            'args': [{'visible': [False] * (len(hull_data) + len(clusters)) + [True] * len(surveys)}]
        }
    ])
    
    # Cluster filter buttons
    if len(clusters) > 1:
        buttons.append({'label': '--- Cluster Filters ---', 'method': 'skip', 'args': []})
        for cluster in clusters:
            cluster_visibility = []
            # Hull visibility
            for hull in hull_data:
                cluster_visibility.append(hull['cluster'] == cluster)
            # Cluster points visibility
            for c in clusters:
                cluster_visibility.append(c == cluster)
            # Survey points (keep current state)
            cluster_visibility.extend([None] * len(surveys))
            
            buttons.append({
                'label': f'📍 Cluster {cluster} Only',
                'method': 'restyle',
                'args': [{'visible': cluster_visibility}]
            })
    
    # Survey toggle buttons
    if surveys:
        buttons.append({'label': '--- Survey Toggles ---', 'method': 'skip', 'args': []})
        
        for i, survey in enumerate(surveys):
            # Create visibility pattern for toggling this survey
            toggle_visibility = [None] * (len(hull_data) + len(clusters))
            survey_visibility = [False] * len(surveys)
            survey_visibility[i] = True  # Show only this survey
            toggle_visibility.extend(survey_visibility)
            
            buttons.append({
                'label': f'🔍 Highlight {survey}',
                'method': 'restyle',
                'args': [{'visible': toggle_visibility}]
            })
        
        # Add survey combination buttons
        buttons.append({'label': '--- Survey Combinations ---', 'method': 'skip', 'args': []})
        
        # Show multiple surveys at once
        for i in range(len(surveys)):
            for j in range(i+1, len(surveys)):
                combo_visibility = [False] * (len(hull_data) + len(clusters))
                survey_visibility = [False] * len(surveys)
                survey_visibility[i] = True
                survey_visibility[j] = True
                combo_visibility.extend(survey_visibility)
                
                buttons.append({
                    'label': f'🔍 {surveys[i]} + {surveys[j]}',
                    'method': 'restyle',
                    'args': [{'visible': combo_visibility}]
                })
        
        # Show all surveys
        buttons.append({
            'label': '🔍 All Surveys',
            'method': 'restyle',
            'args': [{'visible': [False] * (len(hull_data) + len(clusters)) + [True] * len(surveys)}]
        })
        
        # Combined view (clusters + surveys)
        buttons.append({
            'label': '🎯 Clusters + All Surveys',
            'method': 'restyle',
            'args': [{'visible': [True] * (len(hull_data) + len(clusters) + len(surveys))}]
        })
    
    # Set layout with improved controls
    fig.update_layout(
        title={
            'text': 'UMAP Clustering - Interactive Survey & Cluster Analysis',
            'x': 0.5,
            'font': {'size': 18}
        },
        xaxis_title='UMAP Dimension 1',
        yaxis_title='UMAP Dimension 2',
        width=1400,
        height=900,
        hovermode='closest',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=10)
        ),
        updatemenus=[
            {
                'buttons': buttons,
                'direction': 'down',
                'showactive': True,
                'x': 0.02,
                'y': 0.98,
                'xanchor': 'left',
                'yanchor': 'top',
                'bgcolor': 'rgba(255,255,255,0.8)',
                'bordercolor': 'rgba(0,0,0,0.2)',
                'borderwidth': 1
            }
        ],
        annotations=[
            dict(
                text="<b>Interactive Controls:</b><br>• 🏠 = All data<br>• 📊 = Clusters<br>• 🔍 = Survey highlight<br>• 📍 = Single cluster",
                x=0.02, y=0.85,
                xref="paper", yref="paper",
                align="left",
                showarrow=False,
                font=dict(size=10),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.2)",
                borderwidth=1
            )
        ]
    )
    
    return fig

def create_download_dataset(df):
    """Create a clean dataset for download with essential columns"""
    print("Creating download dataset...")
    
    # Select and rename columns for download
    download_df = df.copy()
    
    # Create essential columns for download
    download_columns = {
        'pid': 'User_ID',
        'survey_id': 'Survey_ID', 
        'survey_name': 'Survey_Name',
        'pole_a': 'Pole_A',
        'pole_b': 'Pole_B',
        'cluster_7': 'Cluster',
        'x': 'Coordinate_X',
        'y': 'Coordinate_Y'
    }
    
    # Check which columns exist and create download dataframe
    available_columns = {}
    for original, new_name in download_columns.items():
        if original in download_df.columns:
            available_columns[original] = new_name
    
    # Create clean download dataset
    clean_df = download_df[list(available_columns.keys())].copy()
    clean_df = clean_df.rename(columns=available_columns)
    
    # Add additional useful columns
    if 'User_ID' in clean_df.columns:
        # Add conversation index for easier reference
        clean_df['Conversation_Index'] = clean_df.groupby('User_ID').ngroup() + 1
    
    if 'Pole_A' in clean_df.columns and 'Pole_B' in clean_df.columns:
        # Create combined bipolar construct field
        clean_df['Bipolar_Construct'] = clean_df['Pole_A'].astype(str) + ' vs ' + clean_df['Pole_B'].astype(str)
    
    # Add cluster statistics
    if 'Cluster' in clean_df.columns:
        cluster_sizes = clean_df['Cluster'].value_counts().to_dict()
        clean_df['Cluster_Size'] = clean_df['Cluster'].map(cluster_sizes)
    
    # Sort by cluster and coordinates for better organization
    if 'Cluster' in clean_df.columns and 'Coordinate_X' in clean_df.columns:
        clean_df = clean_df.sort_values(['Cluster', 'Coordinate_X', 'Coordinate_Y'])
    
    # Reset index for clean numbering
    clean_df = clean_df.reset_index(drop=True)
    clean_df.index = clean_df.index + 1  # Start from 1
    clean_df.index.name = 'Row_ID'
    
    return clean_df

def save_final_version_files(df, output_dir):
    """Save all final version files to the specified directory"""
    print(f"Saving final version files to: {output_dir}")
    
    import os
    import shutil
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Create and save download dataset
    download_df = create_download_dataset(df)
    download_file = os.path.join(output_dir, "constructs_cluster_dataset.csv")
    download_df.to_csv(download_file)
    print(f"✅ Saved download dataset: {download_file}")
    
    # 2. Save the interactive visualization
    fig = create_interactive_plot_with_surveys(df)
    viz_file = os.path.join(output_dir, "interactive_constructs_cluster_visualization.html")
    fig.write_html(viz_file)
    print(f"✅ Saved interactive visualization: {viz_file}")
    
    # 3. Create and save statistics
    cluster_stats, survey_stats = create_statistics(df)
    
    cluster_stats_file = os.path.join(output_dir, "cluster_analysis_statistics.csv")
    cluster_stats.to_csv(cluster_stats_file, index=False)
    print(f"✅ Saved cluster statistics: {cluster_stats_file}")
    
    if survey_stats is not None:
        survey_stats_file = os.path.join(output_dir, "survey_analysis_statistics.csv")
        survey_stats.to_csv(survey_stats_file, index=False)
        print(f"✅ Saved survey statistics: {survey_stats_file}")
    
    # 4. Save the complete processed dataset
    complete_file = os.path.join(output_dir, "complete_processed_dataset.csv")
    df.to_csv(complete_file, index=False)
    print(f"✅ Saved complete dataset: {complete_file}")
    
    # 5. Create a summary report
    summary_file = os.path.join(output_dir, "dataset_summary.txt")
    with open(summary_file, 'w') as f:
        f.write("CONSTRUCTS CLUSTER ANALYSIS - DATASET SUMMARY\n")
        f.write("="*50 + "\n\n")
        f.write(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("DATASET OVERVIEW:\n")
        f.write(f"- Total data points: {len(df):,}\n")
        f.write(f"- Unique conversations: {df['pid'].nunique():,}\n")
        f.write(f"- Number of clusters: {df['cluster_7'].nunique()}\n")
        
        if 'survey_name' in df.columns:
            f.write(f"- Survey types: {df['survey_name'].dropna().nunique()}\n")
            f.write(f"- Survey names: {', '.join(sorted(df['survey_name'].dropna().unique()))}\n")
        
        f.write("\nCLUSTER DISTRIBUTION:\n")
        for cluster in sorted(df['cluster_7'].unique()):
            cluster_data = df[df['cluster_7'] == cluster]
            f.write(f"- Cluster {cluster}: {len(cluster_data):,} points from {cluster_data['pid'].nunique()} conversations\n")
        
        if 'survey_name' in df.columns:
            f.write("\nSURVEY DISTRIBUTION:\n")
            for survey in sorted(df['survey_name'].dropna().unique()):
                survey_data = df[df['survey_name'] == survey]
                f.write(f"- {survey}: {len(survey_data):,} points from {survey_data['pid'].nunique()} conversations\n")
        
        f.write("\nFILES INCLUDED:\n")
        f.write("- constructs_cluster_dataset.csv: Clean dataset for analysis\n")
        f.write("- interactive_constructs_cluster_visualization.html: Interactive visualization\n")
        f.write("- cluster_analysis_statistics.csv: Cluster statistics\n")
        f.write("- survey_analysis_statistics.csv: Survey statistics\n")
        f.write("- complete_processed_dataset.csv: Full processed dataset\n")
        f.write("- README.md: Documentation and usage guide\n")
    
    print(f"✅ Saved summary report: {summary_file}")
    
    return download_df, download_file

def create_statistics(df):
    """Create comprehensive statistics"""
    print("Generating statistics...")
    
    # Cluster statistics
    cluster_stats = []
    for cluster in sorted(df['cluster_7'].unique()):
        cluster_data = df[df['cluster_7'] == cluster]
        
        stats = {
            'Cluster': cluster,
            'Total Points': len(cluster_data),
            'Unique Conversations': cluster_data['pid'].nunique(),
            'Avg Points per Conversation': round(len(cluster_data) / cluster_data['pid'].nunique(), 1)
        }
        
        # Add survey information if available
        if 'survey_name' in cluster_data.columns:
            unique_surveys = cluster_data['survey_name'].dropna().nunique()
            stats['Surveys Represented'] = unique_surveys
            
            # Most common survey in this cluster
            if unique_surveys > 0:
                most_common_survey = cluster_data['survey_name'].value_counts().index[0]
                stats['Main Survey'] = most_common_survey
        
        # Add bipolar terms if available
        if 'pole_a' in cluster_data.columns and 'pole_b' in cluster_data.columns:
            # Create bipolar pairs for analysis
            cluster_data_clean = cluster_data.dropna(subset=['pole_a', 'pole_b'])
            if len(cluster_data_clean) > 0:
                bipolar_pairs = cluster_data_clean['pole_a'] + ' vs ' + cluster_data_clean['pole_b']
                top_pairs = bipolar_pairs.value_counts().head(3)
                constructs_text = "; ".join([f"{pair}" for pair, count in top_pairs.items()])
                stats['Common Bipolar Constructs'] = constructs_text[:120] + "..." if len(constructs_text) > 120 else constructs_text
        elif 'construct_bipolar' in cluster_data.columns:
            top_constructs = cluster_data['construct_bipolar'].value_counts().head(3)
            constructs_text = "; ".join([f"{construct}" for construct, count in top_constructs.items() if pd.notna(construct)])
            stats['Common Constructs'] = constructs_text[:100] + "..." if len(constructs_text) > 100 else constructs_text
        
        cluster_stats.append(stats)
    
    cluster_df = pd.DataFrame(cluster_stats)
    
    # Survey statistics if available
    survey_stats = None
    if 'survey_name' in df.columns:
        survey_data = []
        for survey in sorted(df['survey_name'].dropna().unique()):
            survey_subset = df[df['survey_name'] == survey]
            
            survey_data.append({
                'Survey': survey,
                'Total Points': len(survey_subset),
                'Unique Conversations': survey_subset['pid'].nunique(),
                'Clusters Represented': survey_subset['cluster_7'].nunique(),
                'Main Clusters': ', '.join(map(str, sorted(survey_subset['cluster_7'].value_counts().head(3).index)))
            })
        
        survey_stats = pd.DataFrame(survey_data)
    
    return cluster_df, survey_stats

def main():
    """Main function"""
    print("=== UMAP Re-clustering to 7 Groups with Survey Integration ===")
    
    # Load and re-cluster data
    df = load_and_recluster_data()
    
    # Save the re-clustered data (original location)
    reclustered_file = "umap_coordinates_7clusters_with_surveys.csv"
    df.to_csv(reclustered_file, index=False)
    print(f"Saved re-clustered data: {reclustered_file}")
    
    # Output statistics
    print(f"\nData Summary:")
    print(f"- Total data points: {len(df)}")
    print(f"- New clusters (7): {sorted(df['cluster_7'].unique())}")
    print(f"- Unique conversations: {df['pid'].nunique()}")
    
    if 'survey_name' in df.columns:
        print(f"- Surveys: {df['survey_name'].dropna().nunique()}")
    
    # Define final version output directory
    final_output_dir = "../final version of constructs cluster"
    
    # Save all final version files
    download_df, download_file = save_final_version_files(df, final_output_dir)
    
    # Also save to current directory for backward compatibility
    fig = create_interactive_plot_with_surveys(df)
    output_file = "umap_7clusters_with_surveys.html"
    fig.write_html(output_file)
    print(f"\nBackward compatibility: Interactive visualization saved: {output_file}")
    
    # Generate statistics for current directory
    cluster_stats, survey_stats = create_statistics(df)
    
    cluster_stats.to_csv("cluster_statistics_7_integrated.csv", index=False)
    print(f"Backward compatibility: Cluster statistics saved: cluster_statistics_7_integrated.csv")
    
    if survey_stats is not None:
        survey_stats.to_csv("survey_statistics_7_integrated.csv", index=False)
        print(f"Backward compatibility: Survey statistics saved: survey_statistics_7_integrated.csv")
    
    # Display download dataset info
    print(f"\n=== DOWNLOAD DATASET INFO ===")
    print(f"Download file: {download_file}")
    print(f"Download dataset shape: {download_df.shape}")
    print(f"Download dataset columns: {list(download_df.columns)}")
    
    print(f"\nDownload Dataset Preview:")
    print(download_df.head(3).to_string())
    
    # Display cluster summary
    print(f"\n=== CLUSTER SUMMARY ===")
    for _, row in cluster_stats.iterrows():
        print(f"Cluster {row['Cluster']}: {row['Total Points']} points from {row['Unique Conversations']} conversations")
    
    if survey_stats is not None:
        print(f"\n=== SURVEY SUMMARY ===")
        for _, row in survey_stats.iterrows():
            print(f"Survey '{row['Survey']}': {row['Total Points']} points, {row['Clusters Represented']} clusters")
    
    print(f"\n=== FINAL VERSION FILES ===")
    print(f"All final files saved to: {final_output_dir}")
    print(f"Main download file: {download_file}")
    print(f"Interactive visualization: {final_output_dir}/interactive_constructs_cluster_visualization.html")
    
    print(f"\n=== USAGE INSTRUCTIONS ===")
    print(f"1. Download dataset: Open {download_file}")
    print(f"2. Interactive analysis: Open the HTML visualization file")
    print(f"3. Statistical analysis: Check the statistics CSV files")
    print(f"4. Documentation: Read the README.md file in the final version folder")

if __name__ == "__main__":
    main()
