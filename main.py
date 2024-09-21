import argparse
import shutil
import os
from os import walk
from typing import List, Tuple
import configparser


def create_argparser_and_get_args():
    parser = argparse.ArgumentParser(
        prog="fsweb",
        description="Create a browsable website from a series of scattered HTML files",
        epilog="Visit www.cuppajoeman.com for more information",
    )

    parser.add_argument(
        "--base-dir",
        help="The base directory which fsweb will recursively operate on, path is relative to the fsweb directory",
        required=True,
    )
    parser.add_argument(
        "--gen-dir",
        help="The directory that fsweb will output the modified files, path is relative to the fsweb directory",
        required=True,
    )
    parser.add_argument(
        "--theme",
        choices=["light", "dark"],
        help="Choose from 'dark' or 'light' themes",
    )
    parser.add_argument(
        "--wrapper", action="store_true", help="Add wrapper to every index file"
    )

    parser.add_argument(
        "--search",
        action="store_true",
        help="Add search functionality initiated by ctrl-space",
    )

    parser.add_argument(
        "--breadcrumb",
        action="store_true",
        help="Add breadcrumb navigation to every index file",
    )

    parser.add_argument(
        "--ini-layout",
        action="store_true",
        help="Show the layout of the fsweb_dir.ini file and exit",
    )

    args = parser.parse_args()

    if args.ini_layout:
        print_ini_layout()
        exit(0)

    return args


def print_ini_layout():
    print(
        """
    Layout of fsweb_dir.ini:
    
    [settings]
    ignore_files = file1.html, file2.html
    ignore_directories = dir1, dir2
    
    - ignore_files: A comma-separated list of file names to ignore in this directory.
    - ignore_directories: A comma-separated list of directory names to ignore in this directory.
    """
    )


def re_create_generated_directory(content_directory, generated_directory):
    if os.path.exists(generated_directory):
        shutil.rmtree(generated_directory)
    shutil.copytree(content_directory, generated_directory)


def get_end_of_path(path):
    return os.path.basename(os.path.normpath(path))


def load_fsweb_dir_ini(dir_path: str) -> Tuple[List[str], List[str]]:
    """Load the fsweb_dir.ini file if it exists and return lists of ignored files and directories."""
    config = configparser.ConfigParser()
    ini_file_path = os.path.join(dir_path, "fsweb_dir.ini")

    ignored_files = []
    ignored_directories = []

    if os.path.exists(ini_file_path):
        config.read(ini_file_path)

        if "settings" in config:
            ignored_files = [
                f.strip()
                for f in config["settings"].get("ignore_files", "").split(",")
                if f.strip()
            ]
            ignored_directories = [
                d.strip()
                for d in config["settings"].get("ignore_directories", "").split(",")
                if d.strip()
            ]

    return ignored_files, ignored_directories


def create_html_list_from_directories(directories):
    inner = ""
    for directory in directories:
        inner += (
            f"\t\t<li><a href='{directory}/index.html'>{directory}</a></li>\n"
        )

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


body_search_content = """
<div id="searchModal" class="modal">
   <div class="modal-content">
       <input type="text" id="searchInput" placeholder="Search...">
       <ul id="results"></ul>
   </div>
</div>


<script src="/search/fuzzysort.js"></script>
<script src="/search/search_callbacks.js"></script>
<script src="/search/search_list.js"></script>
<script src="/search/search.js"></script>
"""


def get_head_search_content(theme):
    return f"""
   {'<link id="theme-stylesheet" rel="stylesheet" href="/search/dark_theme.css">' 
        if theme == 'dark' and search else ''}

   {'<link id="theme-stylesheet" rel="stylesheet" href="/search/dark_theme.css">' 
        if theme == 'light' and search else ''}

    {'<link rel="stylesheet" href="/search/search.css">' if search else ''}
    """


def generate_breadcrumb(rel_path):
    path_parts = rel_path.split(os.sep)  # Split the path by directory separator
    breadcrumb = '<nav class="breadcrumb">\n<a href="/index.html">~</a>'

    # Iterate through path parts and generate links
    full_path = ""
    for part in path_parts:
        if part:  # Avoid empty parts
            full_path = os.path.join(full_path, part)
            breadcrumb += f'/<a href="/{full_path}/index.html">{part}</a>'

    breadcrumb += '\n</nav>'
    return breadcrumb

def strip_gen_dir(dir_path, gen_dir):
    """
    Strips out the 'gen_dir' part of the path and returns the subpath starting from the point after 'gen_dir'.
    """
    if gen_dir in dir_path:
        # Split at 'gen_dir' and take the part after it
        dir_path = dir_path.split(gen_dir, 1)[-1]
        if dir_path.startswith(os.sep):  # Remove leading slash if present
            dir_path = dir_path[1:]
    return dir_path

def create_index_file(
    gen_dir: str,
    dir_path: str,
    in_root_dir: bool,
    sub_dir_names: List[str],
    html_files: List[str],
    theme: str,
    wrapper: bool,
    search: bool,
    breadcrumb: bool
):



    dir_name = get_end_of_path(strip_gen_dir(dir_path, gen_dir))

    print(f"DEBOGG {dir_path} bred {strip_gen_dir(dir_path, gen_dir)}")


  # Add breadcrumbs if enabled
    breadcrumb_content = ""
    if breadcrumb and not in_root_dir:
        breadcrumb_content = generate_breadcrumb(strip_gen_dir(dir_path, gen_dir))


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
    {get_head_search_content(theme) if search else ''}
</head>
<body>
    {"<div style='width: 70%; margin: 0 auto;'>" if wrapper else ""}
    {breadcrumb_content}
    <h1>{("root: " if in_root_dir else "") + dir_name}</h1>
{html_dir_content}
{html_file_content}
    {"</div>" if wrapper else ""}
    {body_search_content if search else ''}
</body>
</html>
    """

    index_file_path = os.path.join(
        dir_path, "index.html" 
    )

    with open(index_file_path, "w") as f:
        f.write(index_page_body)


def add_text_to_html(html_file_path, head_text, body_text):
    # Read the content of the HTML file
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Find the closing head tag and insert the head_text before it
    head_index = html_content.find("</head>")
    if head_index != -1:
        html_content = (
            html_content[:head_index] + head_text + "\n" + html_content[head_index:]
        )

    # Find the closing body tag and insert the body_text before it
    body_index = html_content.find("</body>")
    if body_index != -1:
        html_content = (
            html_content[:body_index] + body_text + "\n" + html_content[body_index:]
        )

    # Write the modified content back to the HTML file
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(html_content)


def create_index_files(generated_directory, theme: str, wrapper: bool, search: bool, breadcrumb: bool):

    if search:
        shutil.copytree("search", generated_directory + "/search")

    first_iteration = True
    for dir_path, sub_dir_names, file_names in walk(generated_directory):
        print(f"\n==== Starting work on {dir_path} ====")

        ignored_files, ignored_directories = load_fsweb_dir_ini(dir_path)

        # Filter out ignored directories and files
        sub_dir_names[:] = [d for d in sub_dir_names if d not in ignored_directories]
        html_files = [
            f for f in file_names if f.endswith(".html") and f not in ignored_files
        ]

        if search:
            print("~~~> Modifying html files to include search functionality")
            for html_file in html_files:

                html_file_path = os.path.join(dir_path, html_file)
                add_text_to_html(
                    html_file_path, get_head_search_content(theme), body_search_content
                )

        print(
            f"~~~> Generating index file with links to dirs: {sub_dir_names}, and files: {html_files}"
        )

        create_index_file(
            generated_directory,
            dir_path, first_iteration, sub_dir_names, html_files, theme, wrapper, search, breadcrumb
        )

        first_iteration = False
        print(f"==== Done with {dir_path} ====\n")


def generate_search_list_file(generated_dir):
    """
    generates list of files to be searched by the search feature
    todo: need to handle dirs as well, just doing files
    """

    print("generating search list")
    file_list = []
    for root, dirs, files in os.walk(generated_dir):

        ignored_files, ignored_directories = load_fsweb_dir_ini(root)

        html_files = [
            f for f in files if f.endswith(".html") and f not in ignored_files
        ]
        for html_file in html_files:
            relative_path = os.path.relpath(os.path.join(root, html_file), generated_dir)
            file_list.append(
                relative_path.replace("\\", "/")
            )  # Replace backslashes with forward slashes for JS compatibility

    with open(generated_dir + "/search/search_list.js", "w") as f:
        f.write("const search_list = [\n")
        for file in file_list:
            f.write(f'    "{file}",\n')
        f.write("];\n")


if __name__ == "__main__":

    args = create_argparser_and_get_args()

    if args.base_dir and args.gen_dir:
        script_directory = os.path.dirname(os.path.realpath(__file__))
        re_create_generated_directory(args.base_dir, args.gen_dir)

        theme = args.theme if args.theme else "light"
        wrapper = args.wrapper
        search = args.search
        breadcrumb = args.breadcrumb

        create_index_files(args.gen_dir, theme, wrapper, search, breadcrumb)

        if search:
            generate_search_list_file(args.gen_dir)

    else:
        print("Error: You must specify --base-dir and --gen-dir")
