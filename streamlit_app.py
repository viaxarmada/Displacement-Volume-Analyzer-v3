import streamlit as st
import json
import os
from pathlib import Path
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Displacement Volume Analyzer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #0a1929;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1e3a5f;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: white;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2196f3;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #132f4c 100%);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #2196f3;
        box-shadow: 0 4px 6px rgba(33, 150, 243, 0.3);
    }
    .result-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .result-unit {
        font-size: 1.2rem;
        color: #90caf9;
    }
    h1 {
        color: #66b2ff !important;
    }
    h2, h3 {
        color: #90caf9 !important;
    }
    .stButton>button {
        background-color: #2196f3;
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1976d2;
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.4);
    }
    .success-message {
        background-color: #1b5e20;
        color: #a5d6a7;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Data management
DATA_FILE = 'dva_data.json'

def load_data():
    """Load sample data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    return []
        except (json.JSONDecodeError, ValueError):
            # If JSON is corrupted, return empty list
            return []
    return []

def save_data(samples):
    """Save sample data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(samples, f, indent=2)
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")

def initialize_data():
    """Initialize with sample data if file doesn't exist"""
    if not os.path.exists(DATA_FILE):
        sample_data = [
            {'id': 'Sample-001', 'weight': 150, 'unit': 'grams'},
            {'id': 'Sample-002', 'weight': 5.5, 'unit': 'ounces'},
            {'id': 'Sample-003', 'weight': 2.3, 'unit': 'pounds'},
            {'id': 'Sample-004', 'weight': 0.75, 'unit': 'kilograms'},
            {'id': 'Sample-005', 'weight': 250, 'unit': 'grams'}
        ]
        save_data(sample_data)

def calculate_volume(weight, unit):
    """Calculate volume conversions"""
    conversions = {
        'grams': {'mm³': 1000, 'cm³': 1, 'in³': 0.061023744},
        'ounces': {'mm³': 28316.8466, 'cm³': 28.3168466, 'in³': 1.7295904},
        'pounds': {'mm³': 453592.37, 'cm³': 453.59237, 'in³': 27.6806742},
        'kilograms': {'mm³': 1000000, 'cm³': 1000, 'in³': 61.023744}
    }
    
    results = conversions[unit]
    return {
        'mm³': weight * results['mm³'],
        'cm³': weight * results['cm³'],
        'in³': weight * results['in³']
    }

def ensure_valid_json_file(filename, default_data=None):
    """Ensure JSON file exists and is valid"""
    if default_data is None:
        default_data = []
    
    if not os.path.exists(filename):
        # Create file with default data
        try:
            with open(filename, 'w') as f:
                json.dump(default_data, f, indent=2)
        except:
            pass
    else:
        # Validate existing file
        try:
            with open(filename, 'r') as f:
                content = f.read().strip()
                if not content:
                    # Empty file, write default
                    with open(filename, 'w') as f:
                        json.dump(default_data, f, indent=2)
                else:
                    # Try to parse
                    json.loads(content)
        except (json.JSONDecodeError, ValueError):
            # Corrupted file, backup and recreate
            try:
                if os.path.exists(filename):
                    os.rename(filename, f"{filename}.backup")
            except:
                pass
            with open(filename, 'w') as f:
                json.dump(default_data, f, indent=2)

# Initialize session state
if 'samples' not in st.session_state:
    initialize_data()
    st.session_state.samples = load_data()

if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# Header
col1, col2 = st.columns([1, 4])

with col1:
    # Display logo if available
    if os.path.exists('dva_logo.png'):
        st.image('dva_logo.png', width=120)
    else:
        st.markdown("# 🔬")

with col2:
    st.markdown("# Displacement Volume Analyzer")
    st.markdown("### Water Displacement Calculator")
    st.markdown("*Based on Archimedes' Principle - Water density at 4°C (1 g/mL)*")

st.markdown("---")

# Initialize session state for projects
if 'projects' not in st.session_state:
    st.session_state.projects = []
    
    # Ensure JSON file is valid before trying to load
    ensure_valid_json_file('dva_projects.json', [])
    
    # Load projects from file if exists
    if os.path.exists('dva_projects.json'):
        try:
            with open('dva_projects.json', 'r') as f:
                content = f.read().strip()
                if content:  # Check if file is not empty
                    st.session_state.projects = json.loads(content)
                else:
                    st.session_state.projects = []
        except (json.JSONDecodeError, ValueError) as e:
            # If JSON is corrupted, start with empty list and backup bad file
            st.session_state.projects = []
            # Optionally backup the corrupted file
            if os.path.exists('dva_projects.json'):
                try:
                    os.rename('dva_projects.json', 'dva_projects.json.backup')
                except:
                    pass

if 'current_project_id' not in st.session_state:
    st.session_state.current_project_id = None

if 'project_counter' not in st.session_state:
    # Initialize counter from existing projects or start at 1000
    if st.session_state.projects:
        max_id = max([p['project_number'] for p in st.session_state.projects])
        st.session_state.project_counter = max_id + 1
    else:
        st.session_state.project_counter = 1000

# Initialize with default values on first load
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = True
    st.session_state.project_name = 'New Project'
    st.session_state.project_date = datetime.now().date()
    st.session_state.designer = 'Designer Name'
    st.session_state.project_description = 'Project description here'
    st.session_state.contact_info = 'contact@email.com'
    st.session_state.primary_weight = 100.0
    st.session_state.primary_unit = 'grams'
    st.session_state.box_length = 10.0
    st.session_state.box_width = 10.0
    st.session_state.box_height = 10.0
    st.session_state.dimension_unit = 'cm'
    st.session_state.box_result_unit = 'cubic cm'

def save_projects():
    """Save projects to JSON file"""
    try:
        with open('dva_projects.json', 'w') as f:
            json.dump(st.session_state.projects, f, indent=2)
    except Exception as e:
        st.error(f"Error saving projects: {str(e)}")

def create_new_project():
    """Create a new project and reset form with default values"""
    st.session_state.current_project_id = None
    st.session_state.project_counter += 1
    
    # Set default values for project info
    st.session_state.project_name = 'New Project'
    st.session_state.project_date = datetime.now().date()
    st.session_state.designer = 'Designer Name'
    st.session_state.project_description = 'Project description here'
    st.session_state.contact_info = 'contact@email.com'
    
    # Set default calculator values
    st.session_state.primary_weight = 100.0
    st.session_state.primary_unit = 'grams'
    if 'primary_volume_mm3' in st.session_state:
        del st.session_state.primary_volume_mm3
    
    # Set default box values
    st.session_state.box_length = 10.0
    st.session_state.box_width = 10.0
    st.session_state.box_height = 10.0
    st.session_state.dimension_unit = 'cm'
    st.session_state.box_result_unit = 'cubic cm'
    if 'box_volume_mm3' in st.session_state:
        del st.session_state.box_volume_mm3
    
    st.rerun()

def save_current_project():
    """Save or update current project"""
    
    # Gather all project data
    # Use stored project_date or current date
    project_date = st.session_state.get('project_date', datetime.now().date())
    # Convert date to string if it's a date object
    if hasattr(project_date, 'strftime'):
        project_date_str = project_date.strftime('%Y-%m-%d')
    else:
        project_date_str = str(project_date)
    
    project_data = {
        'project_number': st.session_state.get('current_project_number', st.session_state.project_counter),
        'project_name': st.session_state.get('project_name', ''),
        'date': project_date_str,
        'designer': st.session_state.get('designer', ''),
        'description': st.session_state.get('project_description', ''),
        'contact': st.session_state.get('contact_info', ''),
        # Primary product data
        'weight': st.session_state.get('primary_weight', 0.0),
        'weight_unit': st.session_state.get('primary_unit', 'grams'),
        'primary_volume_mm3': st.session_state.get('primary_volume_mm3', 0.0),
        # Box data
        'box_length': st.session_state.get('box_length', 0.0),
        'box_width': st.session_state.get('box_width', 0.0),
        'box_height': st.session_state.get('box_height', 0.0),
        'dimension_unit': st.session_state.get('dimension_unit', 'cm'),
        'box_result_unit': st.session_state.get('box_result_unit', 'cubic cm'),
        'box_volume_mm3': st.session_state.get('box_volume_mm3', 0.0),
        'last_modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Update existing or add new
    if st.session_state.current_project_id is not None:
        # Update existing project
        for i, p in enumerate(st.session_state.projects):
            if p['project_number'] == st.session_state.current_project_id:
                st.session_state.projects[i] = project_data
                break
    else:
        # Add new project
        st.session_state.projects.append(project_data)
        st.session_state.current_project_id = project_data['project_number']
    
    save_projects()
    return True

def load_project(project_number):
    """Load a project's data into the form"""
    for project in st.session_state.projects:
        if project['project_number'] == project_number:
            st.session_state.current_project_id = project_number
            st.session_state.current_project_number = project['project_number']
            st.session_state.project_name = project['project_name']
            # Convert date string to date object
            try:
                st.session_state.project_date = datetime.strptime(project['date'], '%Y-%m-%d').date()
            except:
                st.session_state.project_date = datetime.now().date()
            st.session_state.designer = project['designer']
            st.session_state.project_description = project['description']
            st.session_state.contact_info = project['contact']
            st.session_state.primary_weight = project['weight']
            st.session_state.primary_unit = project['weight_unit']
            st.session_state.primary_volume_mm3 = project['primary_volume_mm3']
            st.session_state.box_length = project['box_length']
            st.session_state.box_width = project['box_width']
            st.session_state.box_height = project['box_height']
            st.session_state.dimension_unit = project['dimension_unit']
            st.session_state.box_result_unit = project['box_result_unit']
            st.session_state.box_volume_mm3 = project['box_volume_mm3']
            st.rerun()
            break

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔬 Analyzer", "📁 Project Results", "📋 Primary Results", "⚙️ Primary Data"])

# TAB 1: Analyzer
with tab1:
    # Check if there's a project to load from Project Results tab
    if 'project_to_load' in st.session_state and st.session_state.project_to_load is not None:
        project = st.session_state.project_to_load
        
        # Load all project data into the form (non-widget keys first)
        st.session_state.current_project_id = project['project_number']
        st.session_state.current_project_number = project['project_number']
        
        # Convert date string to date object if needed
        try:
            if isinstance(project['date'], str):
                st.session_state.project_date = datetime.strptime(project['date'], '%Y-%m-%d').date()
            else:
                st.session_state.project_date = project['date']
        except:
            st.session_state.project_date = datetime.now().date()
        
        # Clear the load flag
        st.session_state.project_to_load = None
        
        # Show success message
        st.success(f"✅ Project {project['project_number']} loaded successfully! You can now edit it.")
        
        # Force rerun to populate widget values
        time.sleep(0.5)
        st.rerun()
    
    # Project Info Section
    st.markdown("## Project Information")
    
    col_new, col_save = st.columns([1, 1])
    
    with col_new:
        if st.button("🆕 New Project", use_container_width=True):
            create_new_project()
    
    with col_save:
        if st.button("💾 Save Project", use_container_width=True):
            if save_current_project():
                st.success("✅ Project saved successfully!")
                time.sleep(1)
                st.rerun()
    
    # Project info fields
    col1, col2 = st.columns([1, 1])
    
    with col1:
        project_number = st.text_input(
            "Project Number",
            value=str(st.session_state.get('current_project_number', st.session_state.project_counter)),
            disabled=True,
            key="project_number_display"
        )
        st.session_state.current_project_number = int(project_number)
        
        project_name = st.text_input(
            "Project Name",
            value=st.session_state.get('project_name', 'New Project'),
            placeholder="Enter project name",
            key="project_name"
        )
        
        # Auto-set current date (hidden from user)
        if 'project_date' not in st.session_state:
            st.session_state.project_date = datetime.now().date()
        
        # Display date (read-only)
        st.text_input(
            "Date",
            value=st.session_state.project_date.strftime('%Y-%m-%d'),
            disabled=True,
            key="project_date_display"
        )
    
    with col2:
        designer = st.text_input(
            "Designer",
            value=st.session_state.get('designer', 'Designer Name'),
            placeholder="Enter designer name",
            key="designer"
        )
        
        description = st.text_area(
            "Description",
            value=st.session_state.get('project_description', 'Project description here'),
            placeholder="Enter project description",
            height=100,
            key="project_description"
        )
        
        contact = st.text_input(
            "Contact Info",
            value=st.session_state.get('contact_info', 'contact@email.com'),
            placeholder="Email or phone",
            key="contact_info"
        )
    
    st.markdown("---")
    
    st.markdown("## Primary Product Volume Calculator")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### Input")
        
        weight = st.number_input(
            "Weight of Water",
            min_value=0.0,
            value=100.0,
            step=0.1,
            format="%.2f",
            key="primary_weight"
        )
        
        unit = st.selectbox(
            "Unit",
            ["grams", "ounces", "pounds", "kilograms"],
            index=0,
            key="primary_unit"
        )
        
        calculate_btn = st.button("🔬 Calculate Volume", use_container_width=True)
    
    with col2:
        st.markdown("### Results")
        
        if calculate_btn or weight:
            results = calculate_volume(weight, unit)
            
            # Store primary volume in session state for later use
            st.session_state.primary_volume_mm3 = results['mm³']
            
            # Display results in columns
            result_col1, result_col2, result_col3 = st.columns(3)
            
            with result_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #ff6b6b; font-weight: bold; font-size: 1.1rem;">Cubic Millimeters</div>
                    <div class="result-value" style="color: #ff6b6b;">{results['mm³']:,.2f}</div>
                    <div class="result-unit">mm³</div>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #4ecdc4; font-weight: bold; font-size: 1.1rem;">Cubic Centimeters</div>
                    <div class="result-value" style="color: #4ecdc4;">{results['cm³']:,.2f}</div>
                    <div class="result-unit">cm³</div>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #95e1d3; font-weight: bold; font-size: 1.1rem;">Cubic Inches</div>
                    <div class="result-value" style="color: #95e1d3;">{results['in³']:,.3f}</div>
                    <div class="result-unit">in³</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Conversion reference
            st.markdown("---")
            st.markdown("### Conversion Reference")
            st.info(f"""
            **1 {unit}** of water equals:
            - {results['mm³']:,.2f} mm³
            - {results['cm³']:,.2f} cm³  
            - {results['in³']:,.3f} in³
            """)
    
    # Secondary Packaging Section
    st.markdown("---")
    st.markdown("## Secondary Packaging")
    st.markdown("### Box Dimensions Calculator")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("### Input Box Dimensions")
        
        # Dimension inputs
        box_length = st.number_input(
            "Length",
            min_value=0.0,
            value=10.0,
            step=0.1,
            format="%.2f",
            key="box_length"
        )
        
        box_width = st.number_input(
            "Width",
            min_value=0.0,
            value=10.0,
            step=0.1,
            format="%.2f",
            key="box_width"
        )
        
        box_height = st.number_input(
            "Height",
            min_value=0.0,
            value=10.0,
            step=0.1,
            format="%.2f",
            key="box_height"
        )
        
        dimension_unit = st.selectbox(
            "Dimension Unit",
            ["cm", "mm", "inches", "feet"],
            index=0,
            key="dimension_unit"
        )
        
        result_unit_box = st.selectbox(
            "Result Unit",
            ["cubic cm", "cubic mm", "cubic inches"],
            index=0,
            key="box_result_unit"
        )
        
        calc_box_btn = st.button("📦 Calculate Box Volume", use_container_width=True)
    
    with col2:
        st.markdown("### Box Volume Results")
        
        if calc_box_btn or (box_length and box_width and box_height):
            # Convert all dimensions to mm first (base unit)
            dimension_to_mm = {
                "mm": 1,
                "cm": 10,
                "inches": 25.4,
                "feet": 304.8
            }
            
            # Calculate volume in mm³
            length_mm = box_length * dimension_to_mm[dimension_unit]
            width_mm = box_width * dimension_to_mm[dimension_unit]
            height_mm = box_height * dimension_to_mm[dimension_unit]
            
            box_volume_mm3 = length_mm * width_mm * height_mm
            
            # Convert to requested unit
            mm3_to_result = {
                "cubic mm": 1,
                "cubic cm": 0.001,
                "cubic inches": 0.000061023744
            }
            
            box_volume_result = box_volume_mm3 * mm3_to_result[result_unit_box]
            
            # Store box volume in session state
            st.session_state.box_volume_mm3 = box_volume_mm3
            
            # Display box volume
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #ffa726; font-weight: bold; font-size: 1.1rem;">Box Volume</div>
                <div class="result-value" style="color: #ffa726;">{box_volume_result:,.2f}</div>
                <div class="result-unit">{result_unit_box}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### Remaining Volume Analysis")
            
            # Calculate remaining volume if primary volume exists
            if 'primary_volume_mm3' in st.session_state and st.session_state.primary_volume_mm3 > 0:
                remaining_volume_mm3 = box_volume_mm3 - st.session_state.primary_volume_mm3
                
                remaining_unit = st.selectbox(
                    "Remaining Volume Unit",
                    ["cubic cm", "cubic mm", "cubic inches", "cubic feet"],
                    index=0,
                    key="remaining_unit"
                )
                
                # Conversion factors from mm³
                mm3_to_remaining = {
                    "cubic mm": 1,
                    "cubic cm": 0.001,
                    "cubic inches": 0.000061023744,
                    "cubic feet": 0.000000035315
                }
                
                remaining_volume_result = remaining_volume_mm3 * mm3_to_remaining[remaining_unit]
                
                # Calculate Volume Efficiency Percentage
                if box_volume_mm3 > 0:
                    volume_efficiency_percentage = (st.session_state.primary_volume_mm3 / box_volume_mm3) * 100
                    remaining_space_percentage = (remaining_volume_mm3 / box_volume_mm3) * 100
                else:
                    volume_efficiency_percentage = 0
                    remaining_space_percentage = 0
                
                # Display remaining volume
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="color: #66b2ff; font-weight: bold; font-size: 1rem;">Box Volume</div>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #66b2ff; margin: 10px 0;">
                            {box_volume_mm3 * mm3_to_remaining[remaining_unit]:,.2f}
                        </div>
                        <div class="result-unit">{remaining_unit}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="color: #ab47bc; font-weight: bold; font-size: 1rem;">Product Volume</div>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #ab47bc; margin: 10px 0;">
                            {st.session_state.primary_volume_mm3 * mm3_to_remaining[remaining_unit]:,.2f}
                        </div>
                        <div class="result-unit">{remaining_unit}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Remaining volume
                color = "#4caf50" if remaining_volume_result > 0 else "#f44336"
                st.markdown(f"""
                <div class="metric-card" style="border-color: {color};">
                    <div style="color: {color}; font-weight: bold; font-size: 1.2rem;">Remaining Volume</div>
                    <div class="result-value" style="color: {color};">{remaining_volume_result:,.2f}</div>
                    <div class="result-unit">{remaining_unit}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Volume Efficiency Percentage
                st.markdown("---")
                col_eff1, col_eff2 = st.columns(2)
                
                with col_eff1:
                    # Determine color based on efficiency
                    if volume_efficiency_percentage >= 80:
                        eff_color = "#4caf50"  # Green - Good efficiency
                        eff_status = "Excellent"
                    elif volume_efficiency_percentage >= 60:
                        eff_color = "#8bc34a"  # Light green - Acceptable
                        eff_status = "Good"
                    elif volume_efficiency_percentage >= 40:
                        eff_color = "#ffc107"  # Yellow - Moderate
                        eff_status = "Moderate"
                    else:
                        eff_color = "#ff9800"  # Orange - Low efficiency
                        eff_status = "Low"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="border-color: {eff_color};">
                        <div style="color: {eff_color}; font-weight: bold; font-size: 1.2rem;">Volume Efficiency</div>
                        <div style="font-size: 2.5rem; font-weight: bold; color: {eff_color}; margin: 10px 0;">
                            {volume_efficiency_percentage:.1f}%
                        </div>
                        <div class="result-unit">Space Utilization - {eff_status}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_eff2:
                    # Remaining space percentage
                    remaining_color = "#2196f3" if remaining_space_percentage > 0 else "#f44336"
                    st.markdown(f"""
                    <div class="metric-card" style="border-color: {remaining_color};">
                        <div style="color: {remaining_color}; font-weight: bold; font-size: 1.2rem;">Remaining Space</div>
                        <div style="font-size: 2.5rem; font-weight: bold; color: {remaining_color}; margin: 10px 0;">
                            {remaining_space_percentage:.1f}%
                        </div>
                        <div class="result-unit">Available Capacity</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Status messages
                if remaining_volume_result < 0:
                    st.error("⚠️ Warning: Product volume exceeds box capacity!")
                else:
                    st.success(f"✅ Box has sufficient space with {remaining_volume_result:,.2f} {remaining_unit} remaining")
            else:
                st.info("💡 Calculate the Primary Product Volume first to see remaining space analysis")

# TAB 2: Project Results
with tab2:
    st.markdown("## Project Results")
    
    # Load Project button at top
    col_button1, col_button2, col_button3 = st.columns([2, 1, 1])
    
    with col_button2:
        load_to_calc_btn = st.button("📂 Load to Calculator", use_container_width=True, type="primary")
    
    with col_button3:
        delete_btn = st.button("🗑️ Delete Selected", use_container_width=True)
    
    if st.session_state.projects:
        st.markdown("---")
        st.markdown("### Project Summary Table")
        
        # Initialize selected projects list in session state
        if 'selected_project_indices' not in st.session_state:
            st.session_state.selected_project_indices = []
        
        # Create columns for checkboxes and table
        col_select, col_table = st.columns([0.6, 9.4])
        
        with col_select:
            st.markdown("**Select**")
            # Create checkbox for each project
            for idx in range(len(st.session_state.projects)):
                # Use checkbox that can be toggled on/off
                is_selected = idx in st.session_state.selected_project_indices
                
                if st.checkbox("", value=is_selected, key=f"select_project_{idx}", label_visibility="collapsed"):
                    # Add to selection if not already there
                    if idx not in st.session_state.selected_project_indices:
                        st.session_state.selected_project_indices.append(idx)
                else:
                    # Remove from selection if it's there
                    if idx in st.session_state.selected_project_indices:
                        st.session_state.selected_project_indices.remove(idx)
        
        with col_table:
            # Display project info as table with optimized column widths
            display_df = []
            for project in st.session_state.projects:
                display_df.append({
                    'Project #': project['project_number'],
                    'Project Name': project['project_name'],
                    'Designer': project['designer'],
                    'Description': project['description'][:50] + '...' if len(project['description']) > 50 else project['description'],
                    'Date': project['date']
                })
            
            # Display with column configuration for optimized widths
            st.dataframe(
                display_df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Project #": st.column_config.NumberColumn(
                        "Project #",
                        width="small",  # Optimized to fit project number
                    ),
                    "Project Name": st.column_config.TextColumn(
                        "Project Name",
                        width="medium",
                    ),
                    "Designer": st.column_config.TextColumn(
                        "Designer",
                        width="small",
                    ),
                    "Description": st.column_config.TextColumn(
                        "Description",
                        width="large",
                    ),
                    "Date": st.column_config.TextColumn(
                        "Date",
                        width="small",
                    ),
                }
            )
        
        # Show how many projects are selected
        if st.session_state.selected_project_indices:
            st.info(f"📌 {len(st.session_state.selected_project_indices)} project(s) selected")
        
        st.markdown("---")
        
        # Add to overview button (moved below table)
        col_add1, col_add2, col_add3 = st.columns([2, 1, 1])
        
        with col_add2:
            if st.button("➕ Add Selected to Overview", use_container_width=True):
                if st.session_state.selected_project_indices:
                    added_count = 0
                    for idx in st.session_state.selected_project_indices:
                        project = st.session_state.projects[idx]
                        if not any(p['project_number'] == project['project_number'] for p in st.session_state.loaded_projects_overview):
                            st.session_state.loaded_projects_overview.append(project)
                            added_count += 1
                    
                    if added_count > 0:
                        st.success(f"Added {added_count} project(s) to overview")
                        st.rerun()
                    else:
                        st.info("All selected projects are already in overview")
                else:
                    st.warning("⚠️ Please select at least one project")
        
        # Handle Load to Calculator button
        if load_to_calc_btn:
            if st.session_state.selected_project_indices:
                # Load the first selected project to calculator
                first_selected_idx = st.session_state.selected_project_indices[0]
                selected_project = st.session_state.projects[first_selected_idx]
                
                # Set ALL session state values for the project (these are NOT widget keys, so it's safe)
                st.session_state.current_project_id = selected_project['project_number']
                st.session_state.current_project_number = selected_project['project_number']
                st.session_state.project_name = selected_project['project_name']
                st.session_state.designer = selected_project['designer']
                st.session_state.project_description = selected_project['description']
                st.session_state.contact_info = selected_project['contact']
                
                # Convert date string to date object
                try:
                    if isinstance(selected_project['date'], str):
                        st.session_state.project_date = datetime.strptime(selected_project['date'], '%Y-%m-%d').date()
                    else:
                        st.session_state.project_date = selected_project['date']
                except:
                    st.session_state.project_date = datetime.now().date()
                
                # Load calculator values
                st.session_state.primary_weight = selected_project['weight']
                st.session_state.primary_unit = selected_project['weight_unit']
                st.session_state.primary_volume_mm3 = selected_project['primary_volume_mm3']
                
                # Load box values
                st.session_state.box_length = selected_project['box_length']
                st.session_state.box_width = selected_project['box_width']
                st.session_state.box_height = selected_project['box_height']
                st.session_state.dimension_unit = selected_project['dimension_unit']
                st.session_state.box_result_unit = selected_project['box_result_unit']
                st.session_state.box_volume_mm3 = selected_project['box_volume_mm3']
                
                # Store project to load flag
                st.session_state.project_to_load = selected_project
                
                # Add all selected projects to overview
                if 'loaded_projects_overview' not in st.session_state:
                    st.session_state.loaded_projects_overview = []
                
                for idx in st.session_state.selected_project_indices:
                    project = st.session_state.projects[idx]
                    if not any(p['project_number'] == project['project_number'] for p in st.session_state.loaded_projects_overview):
                        st.session_state.loaded_projects_overview.append(project)
                
                st.success(f"✅ Project {selected_project['project_number']} - {selected_project['project_name']} loaded to Analyzer")
                st.info("💡 Switch to the Analyzer tab to see and edit the project")
            else:
                st.warning("⚠️ Please select at least one project")
        
        # Handle Delete button
        if delete_btn:
            if st.session_state.selected_project_indices:
                # Sort in reverse to delete from end first (avoid index shifting)
                for idx in sorted(st.session_state.selected_project_indices, reverse=True):
                    deleted_project = st.session_state.projects[idx]
                    st.session_state.projects.pop(idx)
                    st.success(f"✅ Deleted project {deleted_project['project_number']}")
                
                save_projects()
                st.session_state.selected_project_indices = []  # Clear selection
                time.sleep(1)
                st.rerun()
            else:
                st.warning("⚠️ Please select at least one project to delete")
        
        # Project Overview Section
        st.markdown("---")
        st.markdown("## Project Overview")
        st.markdown("### Detailed Project Information")
        
        # Initialize overview list
        if 'loaded_projects_overview' not in st.session_state:
            st.session_state.loaded_projects_overview = []
        
        # Display all loaded projects in overview
        if st.session_state.loaded_projects_overview:
            for idx, project in enumerate(st.session_state.loaded_projects_overview):
                with st.expander(f"📋 Project {project['project_number']} - {project['project_name']}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Project Information")
                        st.info(f"""
                        **Project Number:** {project['project_number']}  
                        **Project Name:** {project['project_name']}  
                        **Designer:** {project['designer']}  
                        **Date:** {project['date']}  
                        **Contact:** {project['contact']}  
                        **Description:** {project['description']}
                        """)
                    
                    with col2:
                        st.markdown("#### Calculation Results")
                        
                        # Primary product volume
                        results = calculate_volume(project['weight'], project['weight_unit'])
                        
                        st.success(f"""
                        **Primary Product:**  
                        Weight: {project['weight']} {project['weight_unit']}  
                        
                        **Volumes:**  
                        • {results['mm³']:,.2f} mm³  
                        • {results['cm³']:,.2f} cm³  
                        • {results['in³']:,.3f} in³
                        """)
                        
                        # Box volume if available
                        if project.get('box_volume_mm3', 0) > 0:
                            st.info(f"""
                            **Secondary Packaging:**  
                            Dimensions: {project['box_length']} × {project['box_width']} × {project['box_height']} {project['dimension_unit']}  
                            Box Volume: {project['box_volume_mm3']:,.2f} mm³
                            """)
                    
                    # Remove button for this project
                    if st.button(f"Remove from Overview", key=f"remove_overview_{idx}"):
                        st.session_state.loaded_projects_overview.pop(idx)
                        st.rerun()
            
            # Clear all button
            if st.button("🗑️ Clear All from Overview"):
                st.session_state.loaded_projects_overview = []
                st.rerun()
            
            # Comparison Section - Remaining Volume Analysis
            st.markdown("---")
            st.markdown("## Remaining Volume Comparison")
            
            # Filter projects that have box volume data
            projects_with_boxes = [p for p in st.session_state.loaded_projects_overview if p.get('box_volume_mm3', 0) > 0]
            
            if projects_with_boxes:
                comparison_unit = st.selectbox(
                    "Select unit for comparison:",
                    ["cubic mm", "cubic cm", "cubic inches", "cubic feet"],
                    key="comparison_unit_select"
                )
                
                # Conversion factors from mm³
                mm3_to_unit = {
                    "cubic mm": 1,
                    "cubic cm": 0.001,
                    "cubic inches": 0.000061023744,
                    "cubic feet": 0.000000035315
                }
                
                conversion_factor = mm3_to_unit[comparison_unit]
                
                for project in projects_with_boxes:
                    box_volume_mm3 = project['box_volume_mm3']
                    product_volume_mm3 = project['primary_volume_mm3']
                    remaining_volume_mm3 = box_volume_mm3 - product_volume_mm3
                    
                    # Convert to selected unit
                    box_volume = box_volume_mm3 * conversion_factor
                    product_volume = product_volume_mm3 * conversion_factor
                    remaining_volume = remaining_volume_mm3 * conversion_factor
                    
                    # Calculate percentage
                    if box_volume_mm3 > 0:
                        percentage_remaining = (remaining_volume_mm3 / box_volume_mm3) * 100
                        percentage_used = (product_volume_mm3 / box_volume_mm3) * 100
                    else:
                        percentage_remaining = 0
                        percentage_used = 0
                    
                    # Display comparison card
                    with st.container():
                        st.markdown(f"### {project['project_name']}")
                        
                        col1, col2, col3, col4, col5 = st.columns(5)
                        
                        with col1:
                            st.metric(
                                "Box Volume",
                                f"{box_volume:,.2f}",
                                delta=None
                            )
                            st.caption(comparison_unit)
                        
                        with col2:
                            st.metric(
                                "Product Volume",
                                f"{product_volume:,.2f}",
                                delta=f"{percentage_used:.1f}% used"
                            )
                            st.caption(comparison_unit)
                        
                        with col3:
                            st.metric(
                                "Remaining Volume",
                                f"{remaining_volume:,.2f}",
                                delta=f"{percentage_remaining:.1f}% free" if remaining_volume >= 0 else "Overflow!"
                            )
                            st.caption(comparison_unit)
                        
                        with col4:
                            # Volume Efficiency Percentage
                            if percentage_used >= 80:
                                eff_delta = "Excellent"
                                eff_color = "normal"
                            elif percentage_used >= 60:
                                eff_delta = "Good"
                                eff_color = "normal"
                            elif percentage_used >= 40:
                                eff_delta = "Moderate"
                                eff_color = "off"
                            else:
                                eff_delta = "Low"
                                eff_color = "inverse"
                            
                            st.metric(
                                "Volume Efficiency",
                                f"{percentage_used:.1f}%",
                                delta=eff_delta,
                                delta_color=eff_color
                            )
                            st.caption("Space Utilization")
                        
                        with col5:
                            # Visual indicator
                            if percentage_remaining >= 20:
                                st.success("✅ Good Space")
                            elif percentage_remaining >= 5:
                                st.warning("⚠️ Tight Fit")
                            else:
                                st.error("❌ Too Full")
                        
                        # Progress bar
                        if box_volume_mm3 > 0:
                            st.progress(min(percentage_used / 100, 1.0))
                            st.caption(f"Space Utilization: {percentage_used:.1f}% | Remaining: {percentage_remaining:.1f}%")
                        
                        st.markdown("---")
            else:
                st.info("💡 No projects with box volume data in overview. Add projects with complete calculations to see comparison.")
        else:
            st.info("📋 No projects in overview. Click 'Add Selected to Overview' to analyze projects.")
    
    else:
        st.info("📋 No projects saved yet. Create a project in the Calculator tab!")

# TAB 3: Primary Results
with tab3:
    st.markdown("## Primary Results - Batch Conversion Results")
    
    if st.button("🔄 Refresh Results"):
        st.session_state.samples = load_data()
        st.rerun()
    
    if st.session_state.samples:
        # Create results table
        results_data = []
        
        for sample in st.session_state.samples:
            volumes = calculate_volume(sample['weight'], sample['unit'])
            results_data.append({
                'Sample ID': sample['id'],
                'Weight': f"{sample['weight']:.2f}",
                'Unit': sample['unit'],
                'Volume (mm³)': f"{volumes['mm³']:,.2f}",
                'Volume (cm³)': f"{volumes['cm³']:,.2f}",
                'Volume (in³)': f"{volumes['in³']:,.3f}"
            })
        
        # Display as dataframe
        st.dataframe(
            results_data,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown(f"**Total Samples:** {len(results_data)}")
        
    else:
        st.warning("No samples available. Add samples in the Primary Data tab.")

# TAB 4: Primary Data
with tab4:
    st.markdown("## Primary Data Manager")
    
    # CSV Upload Section
    st.markdown("### 📤 Import Data from CSV")
    st.info("Upload a CSV file with columns: Sample ID, Weight, Unit")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            
            # Expected column names (case-insensitive)
            expected_cols = ['sample id', 'weight', 'unit']
            df.columns = df.columns.str.lower().str.strip()
            
            # Validate columns
            if all(col in df.columns for col in expected_cols):
                st.success(f"✅ CSV file loaded successfully! Found {len(df)} samples.")
                
                # Preview data
                st.markdown("**Preview:**")
                st.dataframe(df.head(), use_container_width=True)
                
                if st.button("📥 Import These Samples", use_container_width=True):
                    imported_count = 0
                    skipped_count = 0
                    
                    for _, row in df.iterrows():
                        sample_id = str(row['sample id']).strip()
                        
                        # Skip if ID already exists
                        if any(s['id'] == sample_id for s in st.session_state.samples):
                            skipped_count += 1
                            continue
                        
                        # Validate unit
                        unit = str(row['unit']).lower().strip()
                        if unit not in ['grams', 'ounces', 'pounds', 'kilograms']:
                            skipped_count += 1
                            continue
                        
                        try:
                            weight = float(row['weight'])
                            st.session_state.samples.append({
                                'id': sample_id,
                                'weight': weight,
                                'unit': unit
                            })
                            imported_count += 1
                        except (ValueError, TypeError):
                            skipped_count += 1
                            continue
                    
                    save_data(st.session_state.samples)
                    st.success(f"✅ Imported {imported_count} samples! Skipped {skipped_count} (duplicates or invalid data).")
                    time.sleep(1.5)
                    st.rerun()
            else:
                st.error(f"❌ Invalid CSV format. Expected columns: 'Sample ID', 'Weight', 'Unit'. Found: {', '.join(df.columns)}")
                st.info("Please ensure your CSV has these exact column headers (case-insensitive).")
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Add New Sample")
        
        with st.form("add_sample_form"):
            new_id = st.text_input("Sample ID", placeholder="e.g., Sample-006")
            new_weight = st.number_input("Weight", min_value=0.0, value=100.0, step=0.1)
            new_unit = st.selectbox("Unit", ["grams", "ounces", "pounds", "kilograms"])
            
            submitted = st.form_submit_button("➕ Add Sample", use_container_width=True)
            
            if submitted:
                if new_id.strip():
                    # Check for duplicate ID
                    if any(s['id'] == new_id for s in st.session_state.samples):
                        st.error(f"Sample ID '{new_id}' already exists!")
                    else:
                        st.session_state.samples.append({
                            'id': new_id,
                            'weight': new_weight,
                            'unit': new_unit
                        })
                        save_data(st.session_state.samples)
                        st.success(f"✅ Sample '{new_id}' added successfully!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Please enter a Sample ID")
    
    with col2:
        st.markdown("### Existing Samples")
        
        if st.session_state.samples:
            st.markdown(f"**Total: {len(st.session_state.samples)} samples**")
            
            # Display samples with delete option
            for idx, sample in enumerate(st.session_state.samples):
                col_a, col_b = st.columns([4, 1])
                
                with col_a:
                    st.text(f"{sample['id']} - {sample['weight']:.2f} {sample['unit']}")
                
                with col_b:
                    if st.button("🗑️", key=f"delete_{idx}"):
                        st.session_state.samples.pop(idx)
                        save_data(st.session_state.samples)
                        st.success(f"Deleted {sample['id']}")
                        time.sleep(0.5)
                        st.rerun()
        else:
            st.info("No samples yet. Add your first sample!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #90caf9; padding: 20px;'>
    <p><strong>Displacement Volume Analyzer v1.0</strong></p>
    <p>Developed by <strong>Yuttana Chiaravalloti</strong>. All rights reserved.</p>
    <p>Built with precision using Python and Streamlit | Where science meets simplicity 🔬</p>
</div>
""", unsafe_allow_html=True)
