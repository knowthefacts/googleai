# Streamlit Interactive Data Editor Pro

## Overview
The Streamlit Interactive Data Editor Pro is a user-friendly web application designed for easy uploading, interactive editing, and viewing of tabular data. Built with Streamlit and Pandas, it provides a seamless experience for modifying datasets directly in your browser and downloading the results.

## ✨ Features
-   **📄 Upload Data:** Supports uploading data from CSV and Excel (`.xlsx`) files.
-   **✍️ Interactive Data Editing:**
    -   Directly edit cell values in an interactive table.
    -   Add or delete rows dynamically.
    -   Utilizes Streamlit's powerful `st.data_editor` for a spreadsheet-like experience.
-   **🗑️ Column Deletion:** Easily select and remove one or more columns from your dataset.
-   **🔍 Data Filtering:** Filter data based on values in a selected column. Supports different input types based on data and uniqueness.
-   **📊 View and Inspect Data:** Clearly view the entire dataset, along with its dimensions (rows and columns).
-   **📥 Download Edited Data:** Download the modified dataset as a CSV file.
-   **🎨 User-Friendly Interface:** Styled for a pleasant and intuitive user experience with clear navigation and feedback.

## 🛠️ Requirements
-   Python 3.7+
-   Libraries:
    -   `streamlit`
    -   `pandas`
    -   `openpyxl` (for Excel file support)

## 🚀 Setup and Installation
1.  **Clone the repository (or download the files):**
    ```bash
    # Replace <repository_url> with the actual URL of your repository
    git clone <repository_url>
    cd <repository_directory_name> # e.g., streamlit-interactive-data-editor
    ```
    If you downloaded the files as a ZIP, extract them and navigate into the directory.

2.  **Install the required libraries:**
    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install streamlit pandas openpyxl
    ```

## ▶️ Running the App
Once the setup is complete, you can run the Streamlit app using the following command in your terminal:
```bash
streamlit run app.py
```
This will typically open the application in your default web browser.

## 🗺️ Navigating the App
The application is divided into three main sections, accessible via the sidebar navigation:

1.  **📤 Upload Data:**
    -   This is the starting point where you can upload your CSV or Excel file.
    -   A preview of the first few rows of the uploaded data is displayed upon successful upload.
    -   The uploaded data is stored in the session and becomes available in the "Edit Data" and "View Data" sections.

2.  **✏️ Edit Data:**
    -   This section provides tools to modify your dataset.
    -   **Delete Columns:** Select and remove columns.
    -   **Edit Table Content:** Directly manipulate data within the `st.data_editor` interface, including adding or deleting rows.
    -   **Filter Data:** Apply filters to narrow down your data based on column values.
    -   Changes made here are staged. You must click "Commit Changes to Session" to save them to the current session's active dataset. A preview of uncommitted edits is shown.

3.  **📄 View and Download Your Data:**
    -   Displays the current state of your (potentially edited) dataset in full.
    -   Shows the dimensions (number of rows and columns) of the data.
    -   Allows you to download the data as a CSV file.

##🎨 UI/UX Enhancements
The application incorporates custom CSS styling for a more polished and professional look. Interactive elements, feedback messages, and navigation are designed to be intuitive, making the data editing process as smooth as possible. Enjoy a more delightful data handling experience!

---
*This README provides a guide to setting up and using the Streamlit Interactive Data Editor Pro.*
