import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_absolute_path, file_path))
    
        # True or False
        valid_target_directory = os.path.commonpath([working_absolute_path, target_file_path]) == working_absolute_path
    
        if not valid_target_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        
        process_result = subprocess.run(command, cwd = working_absolute_path, capture_output=True, text=True, timeout=30)
        
        # build output string
        output_list = []
        if process_result.returncode != 0:
            output_list.append(f"Process exited with code {process_result.returncode}")
            
            
        if (not process_result.stdout) and (not process_result.stderr):
            output_list.append("No output produced")
        else:
            if process_result.stdout:
                output_list.append(f"STDOUT: {process_result.stdout}")
            if process_result.stderr:
                output_list.append(f"STDERR: {process_result.stderr}")
        
        return '\n'.join(output_list)
        
    
    except Exception as e:
        return f"Error: executing Python file: {e}"