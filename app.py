import streamlit as st
import pandas as pd

# Function to load Excel file
def load_excel():
    file_path = 'ct_ops_workup_tracker.xlsx'
    excel_data = pd.read_excel(file_path, sheet_name='Sheet1')  # Load data from the specified Excel file

    # Remove commas from 'Intelegrid Number' column
    excel_data['Intelegrid Number'] = excel_data['Intelegrid Number'].astype(str).str.replace(',', '')
    
    # Convert 'Need by Date' column to datetime and extract date portion
    excel_data['Need by Date'] = pd.to_datetime(excel_data['Need by Date']).dt.date

    return excel_data

# Streamlit app
def main():
    st.title("CT Report Progress")

    # Display initial Case Tracker data
    uploaded_file = load_excel()
    
    if uploaded_file is not None:
        excel_data = load_excel().copy()
        
        # Sort by 'Submission Date' column from longest ago to shortest ago
        excel_data['Submission Date'] = pd.to_datetime(excel_data['Submission Date'])
        excel_data = excel_data.sort_values(by='Submission Date', ascending=True)
        
        # Get unique WCS email entries
        unique_emails = excel_data['WCS Email'].dropna().unique().tolist()

        # Filter by WCS email
        selected_email = st.sidebar.selectbox('Filter by WCS Email', ['All'] + unique_emails)

        # Apply WCS email filter
        if selected_email != 'All':
            excel_data = excel_data[excel_data['WCS Email'] == selected_email]

        # Display the data
        st.write("### Case Tracker:")
        st.dataframe(excel_data)


        if st.button('Refresh Data'):
            excel_data = load_excel().copy()  # Reload the data  

if __name__ == "__main__":
    main()
