from PIL import Image
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from datetime import datetime
import subprocess
import os
import shutil
import re
import streamlit as st

# Define the path to exiftool
EXIFTOOL_PATH = os.path.join(os.path.dirname(__file__), '../exiftool/exiftool.exe')

def __get_image_creation_date(file_path):
    try:
        date_str = None
        is_approx = False
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            with Image.open(file_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    date_str = exif_data.get(36867)
                if not date_str:
                    date_str = __get_xmp_date(file_path)
                if not date_str:
                    date_str = __get_icc_profile_date(file_path)
                    is_approx = True
        elif file_path.lower().endswith('.heic'):
            result = subprocess.run([EXIFTOOL_PATH, '-DateTimeOriginal', '-d', '%Y:%m:%d %H:%M:%S', file_path], capture_output=True, text=True)
            if result.stdout:
                date_str = result.stdout.split(': ')[-1].strip()
            if not date_str:
                date_str = __get_xmp_date(file_path)
            if not date_str:
                date_str = __get_icc_profile_date(file_path)
                is_approx = True

        if date_str:
            date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
            formatted_date = date_obj.strftime('%Y_%m_%d_%H_%M_%S')
            return f"aprox_{formatted_date}" if is_approx else formatted_date
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
    return None

def __get_xmp_date(file_path):
    try:
        result = subprocess.run([EXIFTOOL_PATH, '-XMP-photoshop:DateCreated', file_path], capture_output=True, text=True)
        if result.stdout:
            match = re.search(r'Date Created\s+:\s+(\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2})', result.stdout)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error al procesar XMP para {file_path}: {e}")
    return None

def __get_icc_profile_date(file_path):
    try:
        result = subprocess.run([EXIFTOOL_PATH, '-ICC-header:ProfileDateTime', file_path], capture_output=True, text=True)
        if result.stdout:
            match = re.search(r'Profile Date Time\s+:\s+(\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2})', result.stdout)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error al procesar ICC para {file_path}: {e}")
    return None

def __get_video_creation_date(file_path):
    try:
        parser = createParser(file_path)
        if parser:
            with parser:
                metadata = extractMetadata(parser)
                if metadata:
                    date_obj = metadata.get('creation_date')
                    if date_obj:
                        return date_obj.strftime('%Y_%m_%d_%H_%M_%S')
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
    return None

def __move_to_error_directory(file_path, base_error_path):
    extension = os.path.splitext(file_path)[1].lower()
    error_directory = os.path.join(base_error_path, extension.lstrip('.'))
    os.makedirs(error_directory, exist_ok=True)
    new_file_path = os.path.join(error_directory, os.path.basename(file_path))
    shutil.move(file_path, new_file_path)
    print(f"Archivo movido a error: {new_file_path}")

def __rename_image_files(file_path, base_error_path):
    new_file_name = __get_image_creation_date(file_path)
    if new_file_name:
        new_file_path = os.path.join(os.path.dirname(file_path), f"{new_file_name}{os.path.splitext(file_path)[-1]}")
        new_file_path = __get_unique_filename(new_file_path)
        shutil.move(file_path, new_file_path)
        print(f"Archivo renombrado: {new_file_path}")
        return True
    else:
        __move_to_error_directory(file_path, base_error_path)
        return False

def __rename_video_files(file_path, base_error_path):
    new_file_name = __get_video_creation_date(file_path)
    if new_file_name:
        new_file_path = os.path.join(os.path.dirname(file_path), f"{new_file_name}{os.path.splitext(file_path)[-1]}")
        new_file_path = __get_unique_filename(new_file_path)
        shutil.move(file_path, new_file_path)
        print(f"Archivo renombrado: {new_file_path}")
        return True
    else:
        __move_to_error_directory(file_path, base_error_path)
        return False

def __get_unique_filename(file_path):
    base, extension = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path
    while os.path.exists(new_file_path):
        new_file_path = f"{base}_{counter}{extension}"
        counter += 1
    return new_file_path

def rename_files_in_folder(folder_path, ext_list):
    error_directory = os.path.join(folder_path, "error")
    total_files = 0
    renamed_files = 0
    error_files = 0

    files_to_process = [os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files if os.path.splitext(file)[1].lower() in ext_list]

    progress_bar = st.progress(0)

    for idx, file_path in enumerate(files_to_process):
        extension = os.path.splitext(file_path)[1].lower()
        success = False

        if extension in ['.jpg', '.jpeg', '.png', '.heic']:
            success = __rename_image_files(file_path, error_directory)
        elif extension in ['.mov', '.mp4']:
            success = __rename_video_files(file_path, error_directory)
        
        if success:
            renamed_files += 1
        else:
            error_files += 1
        
        total_files += 1
        progress_bar.progress((idx + 1) / len(files_to_process))

    st.success(f"Proceso completado: {total_files} archivos procesados, {renamed_files} renombrados correctamente, {error_files} con error.")

def get_information(directory):
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"{directory} is not a valid directory")

    from collections import defaultdict
    file_extensions = defaultdict(int)

    for _, _, files in os.walk(directory):
        for file in files:
            extension = os.path.splitext(file)[1].lower()
            file_extensions[extension] += 1

    return dict(file_extensions)
