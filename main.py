import argparse
import shutil
import os
import re
from os import walk
from typing import List, Tuple
import configparser
from html_utils.main import extract_body_content, extract_header_content
from fs_utils.main import get_absolute_path_of_where_this_script_exists

SCRIPT_DIR = get_absolute_path_of_where_this_script_exists()

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


def create_list_of_links_for_each_directory(directories: List[str]) -> str:
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


def create_list_of_links_for_each_html_file(files : List[str]) -> str:
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


def generate_links_for_header(theme :str) -> str:
    return f"""
   {'<link id="theme-stylesheet" rel="stylesheet" href="/search/dark_theme.css">' 
        if theme == 'dark' and search else ''}

   {'<link id="theme-stylesheet" rel="stylesheet" href="/search/dark_theme.css">' 
        if theme == 'light' and search else ''}

    {'<link rel="stylesheet" href="/search/search.css">' if search else ''}
    """


def generate_html_for_breadcrumb(rel_path: str) -> str:
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

def strip_output_dir(dir_path: str, output_dir: str) -> str:
    """
    Strips out the 'output_dir' part of the path and returns the subpath starting from the point after 'output_dir'.
    """
    if output_dir in dir_path:
        # Split at 'output_dir' and take the part after it
        dir_path = dir_path.split(output_dir, 1)[-1]
        if dir_path.startswith(os.sep):  # Remove leading slash if present
            dir_path = dir_path[1:]
    return dir_path

def create_index_file(
    output_dir: str,
    curr_output_dir_path: str,
    in_root_dir: bool,
    sub_dir_names: List[str],
    html_files: List[str],
    theme: str,
    wrapper: bool,
    search: bool,
    breadcrumb: bool,
    clobber_index_files: bool,
    use_existing_index_files: bool,
    merge_existing_index_files: bool
):
    BLANK_HTML_FILE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset=\"UTF-8\">
</head>
<body>
</body>
</html>
"""

    # Prepare content for header and body
    dir_name = get_end_of_path(strip_output_dir(curr_output_dir_path, output_dir))

    breadcrumb_content = ""
    if breadcrumb and not in_root_dir:
        breadcrumb_content = generate_html_for_breadcrumb(strip_output_dir(curr_output_dir_path, output_dir))

    html_dir_content = (
        f"""	<h2>directories</h2>
{create_list_of_links_for_each_directory(sub_dir_names)}"""
        if sub_dir_names else ""
    )

    html_file_content = (
        f"""	<h2>files</h2>
{create_list_of_links_for_each_html_file(html_files)}"""
        if html_files else ""
    )

    header_content = f"""
    <title>{dir_name}</title>
    {"" if theme == 'light' else "<style>body { background-color:black; color: white; }</style>"}
    {generate_links_for_header(theme) if search else ''}
"""

    body_content = f"""
    {"<div style='width: 70%; margin: 0 auto;'>" if wrapper else ""}
    {breadcrumb_content}
    <h1>{("root: " if in_root_dir else "") + dir_name}</h1>
{html_dir_content}
{html_file_content}
    {"</div>" if wrapper else ""}
    {body_search_content if search else ''}
"""

    output_index_file_path = os.path.join(curr_output_dir_path, "index.html")
    output_index_exists = os.path.exists(output_index_file_path)

    if output_index_exists:
        if clobber_index_files:
            # Write the blank HTML file as the initial content
            with open(output_index_file_path, "w", encoding="utf-8") as file:
                file.write(BLANK_HTML_FILE)
            add_text_to_header_and_body_of_html(output_index_file_path, header_content, body_content)

        if merge_existing_index_files:
            print("bloogas", output_index_file_path)
            # Merge content from existing file
            with open(output_index_file_path, "r", encoding="utf-8") as file:
                existing_content = file.read()
            existing_body = extract_body_content(existing_content)
            existing_header = extract_header_content(existing_content)
            print("existing_body")
            print(existing_body)
            print("existing_header")
            print(existing_header)
            header_content = existing_header + "\n" + header_content
            body_content = existing_body + "\n" + body_content

            # Write the merged content back to the file
            with open(output_index_file_path, "w", encoding="utf-8") as file:
                file.write(BLANK_HTML_FILE)
            add_text_to_header_and_body_of_html(output_index_file_path, header_content, body_content)

        if use_existing_index_files:
            pass # by default if none of the above are true, then the default behavior is to leave existing index files

    else:
        # Write the blank HTML file as the initial content
        with open(output_index_file_path, "w", encoding="utf-8") as file:
            file.write(BLANK_HTML_FILE)
        add_text_to_header_and_body_of_html(output_index_file_path, header_content, body_content)


def add_text_to_header_and_body_of_html(html_file_path :str, head_text: str, body_text: str) -> None:
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # find the closing head tag and insert the head_text before it
    head_index = html_content.find("</head>")
    if head_index != -1:
        html_content = (
            html_content[:head_index] + head_text + "\n" + html_content[head_index:]
        )

    # find the closing body tag and insert the body_text before it
    body_index = html_content.find("</body>")
    if body_index != -1:
        html_content = (
            html_content[:body_index] + body_text + "\n" + html_content[body_index:]
        )

    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(html_content)


def create_index_files(
    output_dir: str, 
    theme: str, 
    wrapper: bool, 
    search: bool, 
    breadcrumb: bool, 
    clobber_index_files: bool,
    use_existing_index_files: bool,
    merge_existing_index_files: bool
) -> None:

    if search:
        shutil.copytree(SCRIPT_DIR + "/search", output_dir + "/search")

    first_iteration = True
    for output_dir_path, sub_dir_names, file_names in walk(output_dir):
        print(f"\n==== Starting work on {output_dir_path} ====")

        ignored_files, ignored_directories = load_fsweb_dir_ini(output_dir_path)

        sub_dir_names[:] = [
            d for d in sub_dir_names 
            if not any(re.match(pattern, d) for pattern in ignored_directories)
        ]

        html_files = [
            f for f in file_names 
            if f.endswith(".html") and not any(re.match(pattern, f) for pattern in ignored_files)
        ]

        if search:
            print("~~~> Modifying html files to include search functionality")
            for html_file in html_files:
                html_file_path = os.path.join(output_dir_path, html_file)
                add_text_to_header_and_body_of_html(
                    html_file_path, generate_links_for_header(theme), body_search_content
                )

        print(
            f"~~~> Generating index file with links to dirs: {sub_dir_names}, and files: {html_files}"
        )

        create_index_file(
            output_dir,
            output_dir_path, first_iteration, sub_dir_names, html_files, theme, wrapper, search, breadcrumb, clobber_index_files, use_existing_index_files, merge_existing_index_files
        )

        first_iteration = False
        print(f"==== Done with {output_dir_path} ====\n")


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
            f for f in files 
            if f.endswith(".html") and not any(re.match(pattern, f) for pattern in ignored_files)
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

def create_argparser_and_get_args():
    parser = argparse.ArgumentParser(
        prog="fsweb",
        description="Create a browsable website from a series of scattered HTML files",
        epilog="Visit www.cuppajoeman.com for more information",
    )

    parser.add_argument(
        "-s", "--source-dir",
        help="The source directory which fsweb will recursively process, path is relative to the fsweb directory",
        required=True,
    )
    parser.add_argument(
        "-o", "--output-dir",
        default = "fsweb_generated_dir",
        help="The directory that fsweb will output the modified files, path is relative to the fsweb directory"
    )
    parser.add_argument(
        "-t", "--theme",
        choices=["light", "dark"],
        help="Choose from 'dark' or 'light' themes",
    )
    parser.add_argument(
        "-w", "--wrapper", action="store_true", help="Add wrapper to every index file. Pushes the content towards the middle of the screen"
    )
    parser.add_argument(
        "-ifm",
        "--index-file-mode",
        choices=["use", "clobber", "merge"],
        required=True,
        help=(
            "Specify the mode for handling index files: "
            "'use' to use existing index files, "
            "'clobber' to overwrite them with the generated content, "
            "'merge' to combine existing content with the generated content"
        ),
    )
    parser.add_argument(
        "-x", "--search",
        action="store_true",
        help="Add search functionality initiated by ctrl-space",
    )

    parser.add_argument(
        "-b", "--breadcrumb",
        action="store_true",
        help="Add breadcrumb navigation to every index file",
    )

    parser.add_argument(
        "-il", "--ini-layout",
        action="store_true",
        help="Show the layout of the fsweb_dir.ini file and exit",
    )

    args = parser.parse_args()

    if args.ini_layout:
        print_ini_layout()
        exit(0)

    return args


if __name__ == "__main__":

    args = create_argparser_and_get_args()

    if args.source_dir and args.output_dir:
        script_directory = os.path.dirname(os.path.realpath(__file__))
        re_create_generated_directory(args.source_dir, args.output_dir)

        theme = args.theme if args.theme else "light"
        wrapper = args.wrapper
        search = args.search
        breadcrumb = args.breadcrumb
        clobber_index_files = args.index_file_mode == "clobber"
        use_existing_index_files = args.index_file_mode == "use"
        merge_existing_index_files = args.index_file_mode == "merge"

        create_index_files(args.output_dir, theme, wrapper, search, breadcrumb, clobber_index_files, use_existing_index_files, merge_existing_index_files)

        if search:
            generate_search_list_file(args.output_dir)

    else:
        print("Error: You must specify --base-dir and --gen-dir")
