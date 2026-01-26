import os

def get_files_info(working_directory, directory="."):
    try:
        working_absolute_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_absolute_path, directory))
    
        # True or False
        valid_target_directory = os.path.commonpath([working_absolute_path, target_directory]) == working_absolute_path
    
        if not valid_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
    
        target_dir_list = os.listdir(target_directory)
        directory_data = []
        for item in target_dir_list:
            size = os.path.getsize(os.path.join(target_directory, item))
            isDir = os.path.isdir(os.path.join(target_directory, item))
            current_data = f"- {item}: file_size={size}, is_dir={isDir}"
            directory_data.append(current_data)
        return "\n".join(directory_data)
    
    except Exception as e:
        return f"Error: {e}"