# Displacement Volume Analyzer 🔬

**Professional web application for water displacement volume analysis with project management and PDF reporting**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

![DVA Logo](dva_logo.png)

## 📋 Overview

Displacement Volume Analyzer (DVA) is a modern, web-based application built with Streamlit for calculating water displacement volumes based on Archimedes' Principle. It provides comprehensive project management, multi-unit conversions, volume efficiency analysis, and professional PDF reporting capabilities.

**Perfect for:**
- 🔬 Laboratory Work - Quality control and material testing
- 🏭 Manufacturing - Product packaging optimization  
- 📚 Education - Demonstrating volume displacement principles
- 🔍 Research - Documenting experimental results

## ✨ Key Features

### Core Functionality
- ✅ Multi-unit support (grams, ounces, pounds, kg / mm³, cm³, in³, ft³)
- ✅ Primary product volume calculator
- ✅ Secondary packaging (box) calculator
- ✅ Automatic remaining volume analysis
- ✅ Real-time volume efficiency percentage
- ✅ Color-coded status indicators

### Project Management
- ✅ Create and save unlimited projects
- ✅ Auto-incrementing project numbers
- ✅ Multi-project selection and comparison
- ✅ Project overview dashboard
- ✅ Batch operations

### Professional Reporting
- ✅ PDF report generation
- ✅ Comprehensive project details
- ✅ Multi-project comparison tables
- ✅ Volume efficiency metrics
- ✅ Timestamped documentation

### Data Management
- ✅ CSV file import
- ✅ JSON-based storage
- ✅ Sample data management
- ✅ Auto-save functionality

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/displacement-volume-analyzer.git
cd displacement-volume-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

### Requirements

- Python 3.7+
- streamlit>=1.28.0
- pandas>=2.0.0
- reportlab>=4.0.0

## 📖 Usage Guide

### 1️⃣ Analyzer Tab

**Create a Project:**
1. Click "🆕 New Project"
2. Enter project details (name, designer, description)
3. Calculate primary product volume
4. Calculate secondary packaging
5. View volume efficiency percentage
6. Click "💾 Save Project"

### 2️⃣ Project Results Tab

**Manage Projects:**
1. View all projects in summary table
2. Select projects using checkboxes
3. Click "➕ Add Selected to Overview"
4. View detailed project forms
5. Compare volume efficiency across projects
6. Click "📄 Output Report" for PDF

**Delete Projects:**
- Select projects → Click "🗑️ Delete Selected"

### 3️⃣ Primary Results Tab

- View batch conversion results
- See all sample data in table format

### 4️⃣ Primary Data Tab

- Import CSV files (columns: Sample ID, Weight, Unit)
- Add samples manually
- Manage existing samples

## 🔧 Technical Details

### Scientific Basis

Based on water density at 4°C (39.2°F) = 1 g/mL (Archimedes' Principle)

### Conversion Formulas

| Unit | mm³ | cm³ | in³ |
|------|-----|-----|-----|
| 1 gram | 1,000 | 1 | 0.061024 |
| 1 ounce | 28,316.85 | 28.32 | 1.7296 |
| 1 pound | 453,592.37 | 453.59 | 27.68 |
| 1 kilogram | 1,000,000 | 1,000 | 61.02 |

### Volume Efficiency Ratings

- **80%+** → Excellent (efficient space use)
- **60-80%** → Good (acceptable)
- **40-60%** → Moderate (could be better)
- **<40%** → Low (underutilized)

## 🌐 Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Select your repository
5. Deploy!

Your app will be live at: `https://yourusername-app-name.streamlit.app`

## 📁 Project Structure

```
displacement-volume-analyzer/
├── streamlit_app.py          # Main application
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
├── dva_logo.png              # Logo (400x400)
├── dva_icon.png              # Icon (128x128)
├── dva_data.json             # Sample data
├── dva_projects.json         # Project data
└── .streamlit/
    └── config.toml           # Theme config
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👤 Author

**Yuttana Chiaravalloti**  
All rights reserved.

## 📧 Contact

- GitHub Issues: [Report a bug](https://github.com/yourusername/displacement-volume-analyzer/issues)
- Email: your-email@example.com

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- PDF generation with [ReportLab](https://www.reportlab.com)
- Based on Archimedes' Principle

## 📊 Roadmap

- [ ] Multi-language support
- [ ] Cloud database integration
- [ ] Excel export
- [ ] Temperature-dependent calculations
- [ ] Advanced visualization
- [ ] User authentication

---

**Built with precision using Python and Streamlit | Where science meets simplicity 🔬**

*Version 1.0.0 - February 2026*
