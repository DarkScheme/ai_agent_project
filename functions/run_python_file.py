import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a file at a given file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file to execute, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file."
            )
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=None):
    
    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, file_path))

    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
    # print("DEBUG: entered run_python_file aaaaaa")
    if valid_target_dir == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'


    if not os.path.isfile(target_dir):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_dir]
    if args is not None:
        # print("DEBUG: entered run_python_file bbbbbbbbbbb")
        for arg in args:
            command.append(arg)
    
    try:
        CompletedProcess = subprocess.run(command, cwd=absolute_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)

        output_string = ""
        # print("DEBUG: entered run_python_file ccccccccccccc")

        if CompletedProcess.returncode != 0:
            output_string = output_string + f"Process exited with code {CompletedProcess.returncode}"

        if CompletedProcess.stdout == "" and CompletedProcess.stderr == "":
            output_string = output_string + "No output produced"
        else:
            output_string = output_string + "STDOUT:" + CompletedProcess.stdout
            output_string = output_string + "STDERR:" + CompletedProcess.stderr

        return output_string

    except Exception as e:
        # print("DEBUG: entered run_python_file ddddddddddddddd")
        return f"Error: executing Python file: {e}"
        