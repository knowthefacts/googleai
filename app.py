import streamlit as st
import pandas as pd # Add pandas import

# Set page config for a more appealing look
st.set_page_config(layout="wide", page_title="Interactive Data Editor Pro", page_icon="✨")

st.markdown("""
<style>
/* General body style */
body {
    font-family: 'Arial', sans-serif;
    color: #333; /* Default text color */
}

/* Style for main title */
.main-title {
    color: #0068C9; /* Streamlit blue */
    text-align: center;
    font-weight: bold;
    padding-bottom: 20px;
}

/* Style for headers */
h1, h2, h3 {
    color: #2c3e50; /* Dark blue-gray */
}

/* Custom styling for Streamlit buttons */
.stButton>button {
    border: 1px solid #0068C9; /* Streamlit blue border */
    border-radius: 5px;
    color: #0068C9; /* Streamlit blue text */
    background-color: white;
    padding: 8px 20px;
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    border-color: #005AA3;
    color: white;
    background-color: #0068C9; /* Streamlit blue background */
}
.stButton>button:focus {
    outline: none !important;
    box-shadow: 0 0 0 2px #E0E0E0; /* Light grey focus ring */
}


/* Styling for containers */
.custom-container {
    padding: 20px;
    border-radius: 10px;
    background-color: #f9f9f9; /* Very light gray background */
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px; /* Add some space between containers */
}

/* Sidebar styling */
.css-1d391kg { /* This selector might be specific to Streamlit versions, target with caution */
    background-color: #f0f2f6; /* Light background for sidebar */
}
.stRadio > label {
    font-weight: bold;
    color: #2c3e50;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for navigation and dataframe if they don't exist
if 'page' not in st.session_state:
    st.session_state.page = "Upload Data" # Default page
if 'df' not in st.session_state:
    st.session_state.df = None

# App title and description
st.markdown("<h1 class='main-title'>📊 Interactive Data Editor Pro ✨</h1>", unsafe_allow_html=True)
st.markdown("👋 Welcome! Upload your data, edit with powerful tools, and view or download your results. Let's make data handling intuitive and delightful!")

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")
# Using st.radio for a more traditional nav feel, and to ensure one selection
page_options = ["Upload Data", "Edit Data", "View Data"]
# Get current page index for radio default
current_page_index = page_options.index(st.session_state.page) if st.session_state.page in page_options else 0
st.session_state.page = st.sidebar.radio("Go to", page_options, index=current_page_index, key="nav_radio")


# Conditional page rendering based on session_state.page
if st.session_state.page == "Upload Data":
    st.header("📤 Upload Your Data")
    with st.container(): # Applying custom-container styling might need CSS to target default .stContainer
        st.markdown("Upload a CSV or Excel file to begin. Your data will be accessible across all sections of the app.")
        
        uploaded_file = st.file_uploader("📂 Choose your data file", type=['csv', 'xlsx'], help="Supports CSV and Excel files.")

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.success("✅ File uploaded successfully! A preview is shown below.")
            st.subheader("📊 Data Preview (First 5 rows):")
            st.dataframe(st.session_state.df.head())
        except pd.errors.EmptyDataError:
            st.error("⚠️ Error reading file: The file is empty. Please upload a file with data.")
            st.session_state.df = None
        except pd.errors.ParserError:
            st.error("⚠️ Error reading file: Could not parse the file. Please ensure it's a valid CSV or Excel file and is not corrupted.")
            st.session_state.df = None
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred while reading the file: {e}. Please ensure the file is a valid CSV or Excel file.")
            st.session_state.df = None # Reset dataframe on error
    elif st.session_state.df is not None:
        # If a file was previously uploaded and user navigates back
        st.info("ℹ️ Previously uploaded data is still loaded. You can view it below or upload a new file to replace it.")
        st.subheader("📊 Current Data Preview (First 5 rows):")
        st.dataframe(st.session_state.df.head())


elif st.session_state.page == "Edit Data":
    st.header("✏️ Edit Your Data")
    if st.session_state.df is not None:
        with st.container():
            st.markdown("Modify your data using the tools below. Remember to **Commit Changes** to save them to the current session.")

            edited_df = st.session_state.df.copy()

            # --- Column Deletion ---
            st.subheader("🗑️ Delete Columns")
            columns_to_delete = st.multiselect("Select columns to remove:", options=edited_df.columns, help="Choose one or more columns to delete.")
            if columns_to_delete:
                edited_df = edited_df.drop(columns=columns_to_delete)
                st.success(f"Successfully deleted columns: {', '.join(columns_to_delete)}. Preview below reflects this change.")
                # Data editor below will use the modified edited_df

            # --- Data Editor ---
            st.subheader("✍️ Edit Table Content")
            st.info("ℹ️ You can directly edit cell values in the table. Double-click a cell to start editing. Add or delete rows using the tools at the bottom of the table.")
            edited_df = st.data_editor(edited_df, num_rows="dynamic", key="data_editor_main", height=400) # Set height

            # --- Basic Filtering ---
            st.subheader("🔍 Filter Data")
            if not edited_df.empty:
                col1, col2 = st.columns(2) # Layout filter controls
                with col1:
                    filter_column = st.selectbox("Select column to filter by:", options=edited_df.columns, key="filter_col_edit", help="Choose the column you want to filter.")
                
                if filter_column:
                    unique_values = pd.Series(edited_df[filter_column].unique()).dropna() # Ensure unique, non-NA values for selectbox
                    
                    with col2:
                        if len(unique_values) < 50 and not unique_values.empty:
                            filter_value = st.selectbox(f"Select value in '{filter_column}' to keep rows:", options=unique_values, key="filter_val_edit", help="Only rows with this value will be kept.")
                            if st.button("Apply Filter", key="apply_filter_btn_edit", help="Click to apply the filter based on selected value."):
                                filtered_df_temp = edited_df[edited_df[filter_column] == filter_value].reset_index(drop=True)
                                if filtered_df_temp.empty:
                                    st.warning("⚠️ The filter resulted in no data. The table below shows the data before this filter was applied.")
                                else:
                                    edited_df = filtered_df_temp
                                    st.success(f"Applied filter: '{filter_column}' == '{filter_value}'.")
                        elif unique_values.empty:
                             st.markdown(f"<span style='color: orange;'>Column '{filter_column}' has no filterable values (all unique or empty).</span>", unsafe_allow_html=True)
                        else: # Too many unique values, use text input
                            filter_text = st.text_input(f"Enter value in '{filter_column}' to filter by:", key="filter_text_edit", help="Type the exact value to filter for.")
                            if st.button("Apply Text Filter", key="apply_text_filter_btn_edit", help="Click to apply the filter based on the entered text.") and filter_text:
                                try:
                                    col_dtype = edited_df[filter_column].dtype
                                    # Convert filter_text to the column's dtype for comparison
                                    if pd.api.types.is_numeric_dtype(col_dtype):
                                        # Handle potential float conversion for columns that might appear integer-like but are float
                                        if edited_df[filter_column].apply(lambda x: isinstance(x, float) and x.is_integer()).all():
                                             filter_text_converted = float(filter_text) # or int(float(filter_text)) if sure
                                        else:
                                             filter_text_converted = pd.to_numeric(filter_text)
                                    elif pd.api.types.is_datetime64_any_dtype(col_dtype):
                                        filter_text_converted = pd.to_datetime(filter_text)
                                    elif pd.api.types.is_boolean_dtype(col_dtype):
                                        # Handle boolean conversion robustly
                                        if filter_text.lower() in ['true', 't', 'yes', 'y', '1']:
                                            filter_text_converted = True
                                        elif filter_text.lower() in ['false', 'f', 'no', 'n', '0']:
                                            filter_text_converted = False
                                        else:
                                            raise ValueError("Boolean column can only be filtered by true/false values.")
                                    else: # String or other types
                                        filter_text_converted = str(filter_text) # Ensure it's a string for direct comparison if object type
                                    
                                    filtered_df_temp = edited_df[edited_df[filter_column] == filter_text_converted].reset_index(drop=True)
                                    if filtered_df_temp.empty:
                                        st.warning("⚠️ The filter resulted in no data. The table below shows the data before this filter was applied.")
                                    else:
                                        edited_df = filtered_df_temp
                                        st.success(f"Applied filter: '{filter_column}' == '{filter_text_converted}'.")
                                except ValueError as ve:
                                    st.error(f"⚠️ Error in filter input: {ve}. Could not convert '{filter_text}' for column '{filter_column}'. Please enter a compatible value (e.g., number for numeric columns, true/false for boolean).")
                                except Exception as e:
                                    st.error(f"⚠️ Error applying filter: {e}")
            elif not edited_df.empty and edited_df.columns.empty:
                 st.info("ℹ️ The current dataset has columns but no data to filter.")
            elif edited_df.empty:
                 st.info("ℹ️ The current dataset is empty. Filtering options are not available.")
            
            st.markdown("---")
            # --- Save changes ---
            if st.button("💾 Commit Changes to Session", key="commit_changes_edit", help="Saves all modifications made above to the current session's data."):
                st.session_state.df = edited_df.copy()
                st.success("✅ All changes committed to the current session! You can view the updated data in the 'View Data' section or continue editing.")
                st.balloons() # A little celebration for saving
                st.rerun()

            st.subheader("📝 Current Data (reflects uncommitted edits):")
            st.dataframe(edited_df)

    else:
        st.warning("⚠️ Please upload data in the 'Upload Data' section first to enable editing features.")

elif st.session_state.page == "View Data":
    st.header("📄 View and Download Your Data")
    if st.session_state.df is not None:
        with st.container():
            st.markdown("Here is your current active dataset. Review it and download it as a CSV file if needed.")
            
            st.subheader("🖼️ Full Data View")
            if st.session_state.df.empty:
                st.info("ℹ️ The dataset is currently empty. There is no data to display or download.")
            else:
                st.dataframe(st.session_state.df)

                # --- Download Button ---
                st.subheader("📥 Download Data")
                st.markdown("Click the button below to download your current data as a CSV file.")

                @st.cache_data 
                def convert_df_to_csv(df_to_convert):
                    return df_to_convert.to_csv(index=False).encode('utf-8')

                csv_data = convert_df_to_csv(st.session_state.df.copy()) 

                st.download_button(
                    label="⬇️ Download data as CSV",
                    data=csv_data,
                    file_name='edited_data.csv',
                    mime='text/csv',
                    key='download_csv_button_view',
                    help="Downloads the current dataset as a CSV file."
                )
                st.markdown("---")
                # Displaying DataFrame dimensions
                rows, cols = st.session_state.df.shape
                st.markdown(f"**Rows:** `{rows}` | **Columns:** `{cols}`")
            
            # Update sidebar status regardless of whether df is empty or not,
            # as it reflects the committed state.
            if 'df' in st.session_state and st.session_state.df is not None:
                rows, cols = st.session_state.df.shape
                if rows > 0:
                    st.sidebar.success(f"Active data: {rows} rows, {cols} cols.")
                else:
                    st.sidebar.info("Data loaded: 0 rows.") # More specific if empty
            else:
                st.sidebar.info("No data loaded yet.")


    else:
        st.warning("⚠️ No data available. Please upload data in the 'Upload Data' section first.")
