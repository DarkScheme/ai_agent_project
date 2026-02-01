import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file a file at a given specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Writes to a file given a file path, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to be written into the file"
            )
        },
        required=["file_path", "content"]
    ),
)


def write_file(working_directory, file_path, content):

    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, file_path))

    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

    if valid_target_dir == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'


    if os.path.isdir(target_dir):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    parent_dir = os.path.dirname(target_dir)
    os.makedirs(parent_dir, exist_ok=True)

    try:
        with open(target_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        return f'Error: writing to the file went wrong'
    





