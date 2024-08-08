import argparse
import shutil
import os
from os import walk
from typing import List, Tuple
import configparser

def create_argparser_and_get_args():
    parser = argparse.ArgumentParser(prog="fsweb", description="Create a browsable website from a series of scattered HTML files", epilog="Visit www.cuppajoeman.com for more information")

    parser.add_argument("--base-dir", help="The base directory which fsweb will recursively operate on, path is relative to the fsweb directory", required=True)
    parser.add_argument("--gen-dir", help="The directory that fsweb will output the modified files, path is relative to the fsweb directory", required=True)
    parser.add_argument("--theme", choices=['light', 'dark'], help="Choose from 'dark' or 'light' themes")
    parser.add_argument("--wrapper", action='store_true', help="Add wrapper to every index file")
    
    parser.add_argument("--ini-layout", action='store_true', help="Show the layout of the fsweb_dir.ini file and exit")

    args = parser.parse_args()
    
    if args.ini_layout:
        print_ini_layout()
        exit(0)
        
    return args

def print_ini_layout():
    print("""
    Layout of fsweb_dir.ini:
    
    [settings]
    ignore_files = file1.html, file2.html
    ignore_directories = dir1, dir2
    
    - ignore_files: A comma-separated list of file names to ignore in this directory.
    - ignore_directories: A comma-separated list of directory names to ignore in this directory.
    """)

def re_create_generated_directory(content_directory, generated_directory):
    if os.path.exists(generated_directory):
        shutil.rmtree(generated_directory)
    shutil.copytree(content_directory, generated_directory)

def get_end_of_path(path):
    return os.path.basename(os.path.normpath(path))

def load_fsweb_dir_ini(dir_path: str) -> Tuple[List[str], List[str]]:
    """Load the fsweb_dir.ini file if it exists and return lists of ignored files and directories."""
    config = configparser.ConfigParser()
    ini_file_path = os.path.join(dir_path, 'fsweb_dir.ini')
    
    ignored_files = []
    ignored_directories = []
    
    if os.path.exists(ini_file_path):
        config.read(ini_file_path)
        
        if 'settings' in config:
            ignored_files = [f.strip() for f in config['settings'].get('ignore_files', '').split(',') if f.strip()]
            ignored_directories = [d.strip() for d in config['settings'].get('ignore_directories', '').split(',') if d.strip()]
    
    return ignored_files, ignored_directories

def create_html_list_from_directories(directories):
    inner = ""
    for directory in directories:
        inner += f"\t\t<li><a href='{directory}/generated_index.html'>{directory}</a></li>\n"

    inner = inner[:-1]  # remove ending new line

    return f"""\t<ul>
{inner}
\t</ul>
"""

def create_html_list_from_html_files(files):
    inner = ""
    for file in files:
        inner += f"\t\t<li><a href='{file}'>{file[:-5]}</a></li>\n"

    inner = inner[:-1]  # remove ending new line

    return f"""\t<ul>
{inner}
\t</ul>
    """

def create_index_file(dir_path: str, in_root_dir: bool, sub_dir_names: List[str], html_files: List[str], theme: str, wrapper: bool):

    dir_name = get_end_of_path(dir_path)
    if len(sub_dir_names) == 0:
        html_dir_content = ""
    else:
        html_dir_content = f"""\t<h2>directories</h2>
{create_html_list_from_directories(sub_dir_names)}"""

    if len(html_files) == 0:
        html_file_content = ""
    else:
        html_file_content = f"""\t<h2>files</h2>
{create_html_list_from_html_files(html_files)}"""

    index_page_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{dir_name}</title>
    {"" if theme == 'light' else "<style>body { background-color:black; color: white; }</style>"}
</head>
<body>
    {"<div style='width: 70%; margin: 0 auto;'>" if wrapper else ""}
    <h1>{("root: " if in_root_dir else "") + dir_name}</h1>
{html_dir_content}
{html_file_content}
    {"</div>" if wrapper else ""}
</body>
</html>
    """

    index_file_path = os.path.join(dir_path, "index.html" if in_root_dir else "generated_index.html")
    
    with open(index_file_path, "w") as f:
        f.write(index_page_body)

def create_index_files(generated_directory, theme: str, wrapper: bool):
    first_iteration = True
    for dir_path, sub_dir_names, file_names in walk(generated_directory):
        print(f"\n==== Starting work on {dir_path} ====")

        ignored_files, ignored_directories = load_fsweb_dir_ini(dir_path)

        # Filter out ignored directories and files
        sub_dir_names[:] = [d for d in sub_dir_names if d not in ignored_directories]
        html_files = [f for f in file_names if f.endswith(".html") and f not in ignored_files]

        print(f"~~~> Generating index file with links to dirs: {sub_dir_names}, and files: {html_files}")
        create_index_file(dir_path, first_iteration, sub_dir_names, html_files, theme, wrapper)

        first_iteration = False
        print(f"==== Done with {dir_path} ====\n")

if __name__ == "__main__":

    args = create_argparser_and_get_args()

    if args.base_dir and args.gen_dir:
        script_directory = os.path.dirname(os.path.realpath(__file__))
        re_create_generated_directory(args.base_dir, args.gen_dir)

        theme = args.theme if args.theme else 'light'
        wrapper = args.wrapper

        create_index_files(args.gen_dir, theme, wrapper)
    else:
        print("Error: You must specify --base-dir and --gen-dir")
