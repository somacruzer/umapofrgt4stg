# UMAP Cluster Analysis Dashboard - v0 Ready

A modern, interactive web application for visualizing and analyzing UMAP clustering data with construct relationships and survey information. **Optimized for v0.dev deployment**.

## 🚀 Live Demo Features

- **Interactive Visualization**: Modern plotly-based scatter plots with hover information
- **Advanced Filtering**: Filter by clusters, surveys, and search constructs
- **Real-time Statistics**: Dynamic cluster and survey statistics
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Glass morphism design with smooth animations
- **English Only**: All content optimized for English-speaking users

## 📊 Data Overview

The dashboard analyzes **4,098 data points** across:
- **7 clusters** of related constructs
- **Multiple surveys** (Positive, Contrast and Reflection, etc.)
- **Bipolar constructs** showing opposing concepts
- **Unique user conversations** tracked by conversation ID

## 🛠 Technology Stack

- **Frontend**: React 18, Tailwind CSS
- **Visualization**: Plotly.js
- **Styling**: Custom CSS with glass morphism effects
- **Fonts**: Inter (Google Fonts)
- **Data**: CSV parsing with client-side processing

## 🎯 Deploy to v0.dev (Recommended)

### Step 1: Copy the HTML Code
Copy the complete code from `index.html` - this is a self-contained React application that includes:
- All necessary dependencies from CDNs
- Complete data processing logic
- Modern responsive UI
- Interactive filtering system

### Step 2: Upload Data
Upload the `constructs_cluster_dataset.csv` file to your v0 project or host it on a CDN.

### Step 3: Update Data Path (if needed)
If you host the CSV elsewhere, update this line in the code:
```javascript
const response = await fetch('constructs_cluster_dataset.csv');
```

### Step 4: Deploy
Your dashboard will be live instantly with full interactivity!

## 🎛 Dashboard Features

### Main Visualization
- **Scatter Plot**: UMAP coordinates with cluster coloring
- **Hover Information**: Detailed tooltips with user ID, construct details, and coordinates
- **Interactive Legend**: Click to hide/show specific clusters
- **Zoom & Pan**: Full plotly interaction capabilities

### Filtering System
- **Search Bar**: Search across constructs, poles, and surveys
- **Cluster Filters**: Toggle individual clusters on/off
- **Survey Filters**: Filter by specific survey types
- **Reset Button**: Clear all filters instantly

### Statistics Dashboard
- **Overview Cards**: Total points, users, clusters, surveys
- **Cluster Table**: Detailed statistics per cluster
- **Survey Table**: Distribution across survey types
- **Real-time Updates**: Statistics update with filters

## 📋 Quick Local Testing

```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve .

# Then open http://localhost:8000
```

## 🎨 UI Design

- **Glass Morphism**: Semi-transparent elements with backdrop blur
- **Gradient Header**: Purple to blue gradient
- **Modern Colors**: Carefully chosen color palette for accessibility
- **Responsive Grid**: Adapts to all screen sizes
- **Smooth Animations**: Hover effects and transitions

## 📱 Mobile Optimized

- **Touch-friendly**: Large buttons and touch targets
- **Responsive Tables**: Horizontal scroll on small screens
- **Stacked Layout**: Single column on mobile devices
- **Readable Text**: Appropriate font sizes for all devices

## 🚀 Performance Features

- **CDN Libraries**: Fast loading from reliable CDNs
- **Client-side Processing**: No server required
- **Efficient Filtering**: Immediate response to user input
- **Lazy Plot Updates**: Plot redraws only when necessary

## 🛡 Browser Support

- **Chrome**: 90+ (recommended)
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

## 📄 Alternative Deployment Options

### Netlify
1. Upload `index.html` and `constructs_cluster_dataset.csv`
2. Deploy via drag-and-drop
3. Live instantly

### Vercel
1. Push to GitHub
2. Connect to Vercel
3. Zero-config deployment

### GitHub Pages
1. Push to repository
2. Enable Pages in settings
3. Select source branch

## 🔧 Customization

### Colors
Easily modify the color palette:
```javascript
const colors = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57',
    '#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43'
];
```

### Layout
All styling uses Tailwind CSS classes - easy to customize:
- Header: `gradient-bg text-white py-8`
- Cards: `glass-morphism rounded-xl p-6 shadow-soft`
- Buttons: `px-6 py-2 bg-blue-500 text-white rounded-lg`

## 📞 Support

For deployment issues:
1. Check browser console for errors
2. Verify CSV data loads correctly
3. Test with different browsers
4. Ensure all CDN dependencies load

---

**🎯 Ready for v0.dev!** Copy the code, upload your data, and deploy your modern UMAP clustering dashboard in minutes.

## Files Included

- `index.html` - Complete self-contained dashboard
- `constructs_cluster_dataset.csv` - Data file (4,098 records)
- `README.md` - This deployment guide
- Other analysis files (see original README)
