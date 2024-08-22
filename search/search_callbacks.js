// Function to handle opening the selected item
function on_select_callback(item) {
    console.log("Opened:", item.textContent);  // Placeholder callback for when Enter is pressed
    window.location.href = '/' + item.textContent
}
