# fsweb

Are you tired of manually adding html files to pages via links? This project is aimed at those who want to maintain a directory of html files and have pages that automatically link to all files and directories that a regular filesystem would.

## how

By running this script it will generate custom index pages with the necessary html to allow it to be viewed as we would in the filesystem. Note that it does this entirely in a new directory so that your original content is not changed.

## usage

By default the script will generate the smallest possible working example, there will be no custom html or css. For some this will be good enough.

There are options that can be toggled on:
* add_wrapper: pushes the content inward from the left and right side of the page
* theme: can be set to "dark" or "light"

If you want to augment these html files further (such as changing the structure and adding your own css), then you must define a method called `create_custom_html(current_directory, contained_directories, contained_files)`, which outputs a valid html page.

When the script runs with your custom method, it will create index pages based on how you defined it.
