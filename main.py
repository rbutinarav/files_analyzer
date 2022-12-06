import pandas as pd
import streamlit as st
import os as os

#PARAMETERS
folder='dataset'

#INZIALIZE SESSION STATE
if "file_names_loaded" not in st.session_state:
    st.session_state.file_names_loaded = False
if 'file_list' not in st.session_state:
    st.session_state.file_list = []
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
#if 'selection_files_box' not in st.session_state:
#    st.session_state.selection_files_box = []
#if "show_preview" not in st.session_state:
#    st.session_state.show_preview = True
#if "show_statistics" not in st.session_state:
#    st.session_state.show_statistics = True
if "selected_files" not in st.session_state:
    st.session_state.selected_files = []

#MAIN LOOP
st.title("Data Loader and Analyzer")

#show the st.session_state.variables (for debug only)
#st.write("Session state variables:")
#st.write(st.session_state)

#1. LOAD FILE NAMES

#check if file names are loaded, if not load them
if st.session_state.file_names_loaded == False:
    #read file contents in a folder and create a list of file names
    full_file_list = os.listdir(folder)
    #select files with match *.csv
    file_list = [file for file in full_file_list if file.endswith('.csv')]
    st.session_state.file_list = file_list
    st.session_state.file_names_loaded = True

#if file names are loaded, load them in file_list from session state variable
else:
    file_list=st.session_state.file_list


#2. SELECT FILES

#select first item in the file list adding "All" as the first item
selected_files_box = st.selectbox('Select a file', ['All'] + file_list)
if selected_files_box == 'All':
    selected_files = file_list
#create a list from a single item
else:
    selected_files = [selected_files_box]
#selected_files

#create on the left a select box with "show data" option
show_preview = st.sidebar.selectbox('Show preview', ['Yes', 'No'])
show_statistics = st.sidebar.selectbox('Show statistics', ['Yes', 'No'])

#create button to load data
load_data = st.button('Load data')

if load_data == True or (st.session_state.data_loaded == True and st.session_state.selected_files == selected_files):
#create a loop to read all files in the folder    
    for file in selected_files:
        #read the file
        df = pd.read_csv(folder + '/' + file)
        #display 1000 reacords of the file       
        
        if show_preview == "Yes":
            st.write('First 1000 rows of',file,df.head(1000))

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

    st.session_state.data_loaded = True
    st.session_state.selected_files = selected_files