import argparse 
import shutil
import os
from os import walk
from typing import List

def create_argparser_and_get_args():
    parser = argparse.ArgumentParser(prog="fsweb", description="Create a browsable website from a series of scattered html files", epilog="visit www.cuppajoeman.com for more information")

    parser.add_argument("--base-dir", help="the base directory which fast-html will recursively operate on, path is relative to the fast-html directory")
    parser.add_argument("--gen-dir", help="the directory that fast-html will output the modified files, path is relative to the fast-html directory")
    parser.add_argument("--theme", choices=['light', 'dark'], help="choose from 'dark' or 'light' themes")
    parser.add_argument("--wrapper", action='store_true', help="add wrapper to every index file")

    args = parser.parse_args()
    return args

def re_create_generated_directory(content_directory, generated_directory):
    if os.path.exists(generated_directory):
        shutil.rmtree(generated_directory)
    shutil.copytree(content_directory, generated_directory)

def get_end_of_path(path):
    return os.path.basename(os.path.normpath(path))

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

def create_index_file(dir_path: str, in_root_dir : bool, sub_dir_names: List[str], html_files: List[str], theme: str, wrapper: bool):

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


    index_file_path = None
    if in_root_dir:
        index_file_path = dir_path + "/index.html"    
    else:
        index_file_path = dir_path + "/generated_index.html"

    assert(index_file_path is not None)


    f = open(index_file_path, "w")
    f.write(index_page_body)
    f.close()

def create_index_files(generated_directory, theme: str, wrapper: bool):
    first_iteration = True
    for dir_path, sub_dir_names, file_names in walk(generated_directory):
        print(f"\n==== starting work on {dir_path} ====")

        html_files = []
        for relative_file_path in file_names:
            is_html_file = relative_file_path[-4:] == "html"

            if is_html_file:
                html_files.append(relative_file_path)

        print(f"~~~> generating index file with links to dirs: {sub_dir_names}, and files: {html_files}")
        create_index_file(dir_path, first_iteration, sub_dir_names, html_files, theme, wrapper)

        first_iteration = False
        print(f"==== done with {dir_path} ====\n")


if __name__ == "__main__":

    args = create_argparser_and_get_args()

    if args.base_dir and args.gen_dir: # good this is valid
        script_directory = os.path.dirname(os.path.realpath(__file__))
        re_create_generated_directory(args.base_dir, args.gen_dir)

        theme = 'light'
        if args.theme:
            theme = args.theme

        wrapper = False
        if args.wrapper:
            wrapper = True

        create_index_files(args.gen_dir, theme, wrapper)
    else:
        print("Error: You must specify base-dir, gen-dir")
