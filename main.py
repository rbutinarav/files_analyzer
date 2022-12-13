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
if 'local' not in st.session_state:
    st.session_state.local = False
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

#show a button asking user to load new files
load_files = st.sidebar.button('Load new files')
if load_files == True:
    st.session_state.file_names_loaded = False
    folder=''
#show the st.session_state.variables (for debug only)
#st.write("Session state variables:")
#st.write(st.session_state)

#1. LOAD FILE NAMES

if st.session_state.file_names_loaded == False:
    #read file contents in a folder and create a list of file names
    if os.path.exists(folder)==False:
        #ask the user to choose the files to upload
        files = st.file_uploader("Choose the files you would like to analyze (you can select one or more): ", type=['csv'], accept_multiple_files=True)
        if files != []:
            file_list = [file.name for file in files]
            st.session_state_files = files
            st.session_state.file_list = file_list
            st.session_state.file_names_loaded = True      

    else:  #this works for local files (put your files in the folder defined in the PARAMETERS section)
        st.session_state.local = True
        full_file_list = os.listdir(folder)
        file_list = [file for file in full_file_list if file.endswith('.csv')]
        st.session_state.file_list = file_list
        st.session_state.file_names_loaded = True        

#2. SELECT FILES
if st.session_state.file_names_loaded == True:
    file_list = st.session_state.file_list
    files = st.session_state_files
    #select first item in the file list adding "All" as the first item
    selected_files_box = st.selectbox('Select the file(s) to analyze:', ['All'] + file_list)
    
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
    load_data = st.button('Analyze')

    if load_data == True or (st.session_state.data_loaded == True and st.session_state.selected_files == selected_files):
        for file in selected_files:
            #read the file
            if st.session_state.local == True: #this works for local files
                df = pd.read_csv(folder + '/' + file)
            else:                              #this works for uploaded files
                #st.write('selected file',file)
                #st.write('selected files',selected_files)
                #st.write('file index',file_list.index(file))
                df = pd.read_csv(files[file_list.index(file)])
                #display the name of the file in bold font
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
        st.session_state.data_loaded = True
        st.session_state.selected_files = selected_files

        ##some bugs to fix for uploaded files
        ##duplicate files are not shown
        ##repeated selections cause the app to crash