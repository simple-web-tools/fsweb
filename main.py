# we need to be able to walk the directory
# for each directory we end up in, we need to get all the files which exist in that directory
# after doing that we will generate the required html for that.

import shutil
import os
from os import walk

script_directory = os.path.dirname(os.path.realpath(__file__))

generated_directory = script_directory + "/fsweb_generated"
content_directory = script_directory + "/content"

if os.path.exists(generated_directory):
    shutil.rmtree(generated_directory)
shutil.copytree(content_directory, generated_directory)

os.chdir("fsweb_generated")
content_directory = os.getcwd()

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


first_iteration = True

for dir_path, dir_names, file_names in walk(content_directory):

    html_files = []
    directory_name = get_end_of_path(dir_path)
    relative_directory_path = os.path.relpath(dir_path, script_directory)
    print(directory_name, relative_directory_path)

    for relative_file_path in file_names:
        full_path = os.path.join(dir_path, relative_file_path)
        is_html_file = relative_file_path[-4:] == "html"

        if is_html_file:
            html_files.append(relative_file_path)

    if len(dir_names) == 0:
        html_dir_content = ""
    else:
        html_dir_content = f"""\t<h2>directories</h2>
{create_html_list_from_directories(dir_names)}"""

    if len(html_files) == 0:
        html_file_content = ""
    else:
        html_file_content = f"""\t<h2>files</h2>
{create_html_list_from_html_files(html_files)}"""

    index_page_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{directory_name}</title>
</head>
<body>
    <h1>{("root: " if first_iteration else "") + directory_name}</h1>
{html_dir_content}
{html_file_content}
</body>
</html>
    """

    index_file_path = dir_path + "/generated_index.html"

    f = open(index_file_path, "w")
    f.write(index_page_body)
    f.close()

    first_iteration = False
