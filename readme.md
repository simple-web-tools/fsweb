# fsweb

Are you tired of manually adding html files to pages via links? This project is aimed at those who want to maintain a directory of html files, automatically generate a directory hierarchy that will allow users to explore and find pages on your site, without you having to create links to them by hand.

<img width="715" height="573" alt="image" src="https://github.com/user-attachments/assets/a8b75fdd-9b65-46f6-ad26-990d3ba75762" />

The above is an example of how it can be used, note that the example uses has custom styling but by default this project doesn't impose any styling.

## how

By running this script it will generate custom index pages with the necessary html to allow it to be viewed as we would in the filesystem. Note that it does this entirely in a new directory so that your original content is not changed.

## usage

By default the script will generate the smallest possible working example, there will be no custom html or css. For some this will be good enough.

There are options that can be toggled on:
* add_wrapper: pushes the content inward from the left and right side of the page
* theme: can be set to "dark" or "light"

If you want to augment these html files further (such as changing the structure and adding your own css), then you must define a method called `create_custom_html(current_directory, contained_directories, contained_files)`, which outputs a valid html page.

When the script runs with your custom method, it will create index pages based on how you defined it.

## ignoring files and directories

Sometimes you have files or subdirectories that you don't want showing up in the generated index pages. You can control this on a per directory basis by placing a file named `fsweb.ini` inside any directory where you want ignore rules to apply.

The format of `fsweb.ini` looks like this:

```ini
[settings]
ignore_files = file1.html, file2.html
ignore_directories = dir1, dir2
```

* `ignore_files`: a comma separated list of file name patterns to ignore in this directory.
* `ignore_directories`: a comma separated list of directory name patterns to ignore in this directory.

A few things worth knowing:

* The rules only apply to the directory the `fsweb.ini` file lives in. If you want to ignore things in a nested directory, place a `fsweb.ini` inside that directory as well.
* The patterns are interpreted as regular expressions, not glob patterns. For example, `draft.*` will match `draft.html`, `drafts`, and `draft_2024.html`. A pattern like `*.html` will not behave the way it does in a shell.
* Ignored subdirectories are skipped entirely, so their contents will not be walked into or appear anywhere in the generated output.
* Ignored files are excluded from both the generated index pages and the search list when search is enabled.

If you ever forget the layout, you can run the script with the `--ini-layout` (or `-il`) flag and it will print the expected format and exit.
