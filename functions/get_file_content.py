import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_absolute_path, file_path))
    
        # True or False
        valid_target_directory = os.path.commonpath([working_absolute_path, target_file_path]) == working_absolute_path
    
        if not valid_target_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read
        with open(target_file_path, "r") as f:
            read_data = f.read(MAX_CHARS)
            if f.read(1):
                read_data += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                
        return read_data
        
    except Exception as e:
        return f"Error: {e}"
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file relative to the working directory. "
                "For large files, content is truncated at the configured maximum character limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory (e.g. 'data.csv', 'src/main.py', 'folder/note.txt')",
            ),
        },
        required=["file_path"],
    ),
)