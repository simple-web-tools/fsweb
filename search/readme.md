# Search Modal

This project provides a simple implementation of a search modal with light and dark themes. 

## File Structure

- `dark_theme.css`: Defines styles for the dark theme.
- `light_theme.css`: Defines styles for the light theme.
- `search.css`: Contains common styles for the search modal, using theme variables.
- `search.js`: Handles the functionality of the search modal, including opening/closing the modal, searching, and theme switching.
- `index.html`: Example HTML file demonstrating how to use the provided CSS and JavaScript.

## How to use

1. **Include CSS Files**

   To use the search modal, include the CSS files in your HTML file. You need to choose one theme (light or dark) by setting the appropriate stylesheet in the `index.html` file.

   ```html
   <link id="theme-stylesheet" rel="stylesheet" href="light_theme.css"> <!-- Change to dark_theme.css for dark theme -->
   <link rel="stylesheet" href="search.css">
   ```

2. **Create Your HTML File**

   You can use the provided `index.html` as a template. Ensure that the CSS and JavaScript files are correctly linked.

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Search Modal Setup</title>
       <link id="theme-stylesheet" rel="stylesheet" href="light_theme.css"> <!-- Change to dark_theme.css for dark theme -->
       <link rel="stylesheet" href="search.css">
   </head>
   <body>
       <div id="searchModal" class="modal">
           <div class="modal-content">
               <input type="text" id="searchInput" placeholder="Search...">
               <ul id="results"></ul>
           </div>
       </div>
   
       <script src="fuzzysort.js"></script>
       <script src="search_callbacks.js"></script>
       <script src="search_list.js"></script>
       <script src="search.js"></script>
   </body>
   </html>
   ```

3. **Switch Themes**

   To switch between light and dark themes, change the `href` attribute of the `<link id="theme-stylesheet">` element in your `index.html` file.

   - For light theme: `href="light_theme.css"`
   - For dark theme: `href="dark_theme.css"`

4. **JavaScript Functionality**

   The `script.js` file handles:
   - Opening and closing the modal with `Shift + Space` and `Escape` keys.
   - Searching through a list of numbers (1 to 100) as you type.
   - Navigating through search results using `Tab` and `Shift + Tab`.
   - Selecting and interacting with search results.

5. **Search List**
   - you can specify the list of data to search with by creating a list variable called data in `search_list.js`

6. **Custom Callbacks**
   - You can define the behavior when an item from the search list is selected in `search_callbacks.js`

6. **Customizing**

   - **Add Mock Data**: Modify the `data` array in `search.js` if you want to use different mock data.
   - **Modify Styles**: Update `search.css`, `dark_theme.css`, and `light_theme.css` to match your desired look and feel.

## How It Works

1. **Modal Behavior**: The modal is hidden by default and only appears when `Shift + Space` is pressed. Pressing `Escape` closes the modal.

2. **Search Functionality**: As you type in the search input, results are filtered and displayed. You can navigate through the results using `Tab` and `Shift + Tab`. Pressing `Enter` selects the highlighted result (currently, it logs the selected item).

3. **Theme Switching**: The theme can be switched by changing the CSS file linked in the HTML.
