import streamlit as st
import streamlit.components.v1 as components
import tkinter as tk
from tkinter import filedialog
from file_handler import get_information, rename_files_in_folder
from utils import ChangeButtonColour, toggle_extension

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    folder_selected = filedialog.askdirectory()
    root.destroy()
    return folder_selected

st.title("iCloud Media Orderer")

if 'folder_path' not in st.session_state:
    st.session_state.folder_path = ""
if 'file_extensions' not in st.session_state:
    st.session_state.file_extensions = {}
if 'selected_extensions' not in st.session_state:
    st.session_state.selected_extensions = []

if st.button("Select Directory"):
    folder_path = select_folder()
    if folder_path:
        st.session_state.folder_path = folder_path
        try:
            file_extensions = get_information(folder_path)
            st.session_state.file_extensions = file_extensions
            st.session_state.selected_extensions = [ext for ext in file_extensions.keys()]
        except NotADirectoryError as e:
            st.error(str(e))
    else:
        st.error("No folder selected")

if st.session_state.folder_path:
    st.write("File Extensions in the Selected Directory:")

    ext_data = []
    for ext, count in st.session_state.file_extensions.items():
        ext_data.append((ext, count))

    cols = st.columns(5)

    for idx, (ext, count) in enumerate(ext_data):
        is_selected = ext in st.session_state.selected_extensions
        button_text = f"{ext} ({count})"
        
        with cols[idx % 5]:
            if st.button(button_text, key=f"btn_{ext}", on_click=toggle_extension, args=(ext,)):
                st.session_state.selected_extensions = st.session_state.selected_extensions

            if is_selected:
                ChangeButtonColour(button_text, 'black', '#d4edda')
            else:
                ChangeButtonColour(button_text, 'black', '#f8d7da')

query_params = st.query_params
if 'extension' in query_params:
    toggle_extension(query_params['extension'][0])

if st.session_state.folder_path:
    if st.button("Order"):
        rename_files_in_folder(st.session_state.folder_path, st.session_state.selected_extensions)
