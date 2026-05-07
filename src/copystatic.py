import os
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    directories = os.listdir(source_dir_path)
    for item in directories:
        full_source_path = os.path.join(source_dir_path, item)
        full_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(full_source_path):
            print(f" * {full_source_path} -> {full_dest_path}")
            shutil.copy(full_source_path, full_dest_path)
        else:
            copy_files_recursive(full_source_path, full_dest_path)
