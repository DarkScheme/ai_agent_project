import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file from at a given path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Reads content from a file at a given path, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)


def get_file_content(working_directory, file_path):
    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, file_path))

    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

    if valid_target_dir == False:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
            
        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if not f.read(1) == "":
                file_content_string += f'[... File "{file_path}" turncated at {MAX_CHARS} characters]'
            return file_content_string
    except:
        return "Error: Something went wrong durin reading the file"


    
