import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_absolute_path, file_path))
    
        # True or False
        valid_target_directory = os.path.commonpath([working_absolute_path, target_file_path]) == working_absolute_path
    
        if not valid_target_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        
        parent_dir = os.path.dirname(target_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
        
    except Exception as e:
        return f"Error: {e}"
    
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates or overwrites a file at the specified path relative to the working directory "
                "with the provided content. Creates necessary parent directories if they don't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write/create, relative to the working directory. "
                            "Examples: 'output.txt', 'data/results.csv', 'logs/2025-01/error.log'",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The full text content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)