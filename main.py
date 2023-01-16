import pandas as pd
import streamlit as st
import os as os

#this program will analyze the files uploaded by the user to spot anomalies

st.title("File Analyzer")

#inizialize variables

if "analyze_already_clicked" not in st.session_state:
    st.session_state.analyze_already_clicked = False

selected_files = []


#create on the left a select box with "show data" option
show_preview = st.sidebar.selectbox('Show preview', ['Yes', 'No'])
show_statistics = st.sidebar.selectbox('Show statistics', ['Yes', 'No'])

#ask the user to choose the files to upload
files_uploaded = st.file_uploader("Choose the files you would like to upload (you can select one or more): ", type=['csv'], accept_multiple_files=True)

if files_uploaded != []:
    file_uploaded_list = [file.name for file in files_uploaded]  
    #st.session_state_files = files
    #st.session_state.file_list = file_list
    #st.session_state.files_loaded = True
    #st.experimental_rerun()

#2. ASK WHICH FILES TO ANALYZE
if files_uploaded !=[]:
    selected_files = st.selectbox('Select the file(s) to analyze:', ['All'] + file_uploaded_list)

    if selected_files == 'All':
        selected_files = file_uploaded_list

    else:
        selected_files = [selected_files]
    
if selected_files != []:
    #create button to perform the analysis
    analyze = st.button('Analyze')

if analyze == True or (st.session_state.analyze_already_clicked == True and selected_files == st.session_state.selected_files):
    st.session_state.analyze_already_clicked = True
    st.session_state.selected_files = selected_files

    for file in selected_files:
        df = pd.read_csv(files_uploaded[file_uploaded_list.index(file)])
        st.write('**File:**',file)
    
        #display 1000 records of the file       
        
        if show_preview == "Yes":
            st.write('First 1000 rows:',df.head(1000))

        if show_statistics == "Yes":
            #count the number of rows
            st.write('Number of rows',df.shape[0])
            #create a new dataframe with the number of unique values per column
            df_unique_count = pd.DataFrame(df.nunique(), columns=['Unique values'])
            #add the number of null values per column
            df_unique_count['Null values'] = df.isnull().sum()
            #add the number of duplicated values
            df_unique_count['Duplicated values'] = df.shape[0] - df_unique_count['Unique values']
            #add tbe number of duplicated rows
            st.write('Number of unique and duplicated values per column',df_unique_count)

            #let the user select a column to show the duplicated values, default is blank
            selected_column = st.selectbox('Select a column to show duplicated values', [''] + list(df.columns))
            if selected_column != '':
                #show the duplicated values, order by the selected column
                st.write('Duplicated values',df[df.duplicated(subset=selected_column, keep=False)].sort_values(selected_column))