// Get the modal and input elements
var modal = document.getElementById("searchModal");
var searchInput = document.getElementById("searchInput");

// Maximum number of results to display
var maxResults = 10;

// Track the currently selected index
var selectedIndex = -1;

// Function to toggle the modal
function toggleModal() {
    if (modal.style.display === "flex") {
        modal.style.display = "none";
    } else {
        modal.style.display = "flex";
        searchInput.focus();  // Automatically focus on the input
        clearSearch();        // Clear previous search contents
    }
}

// Function to clear search input and results
function clearSearch() {
    searchInput.value = "";    // Clear the search input
    document.getElementById("results").innerHTML = "";  // Clear the results list
    selectedIndex = -1;  // Reset selected index
}

// Open or close the modal when Shift + Space is pressed
document.onkeydown = function(event) {
    if (event.shiftKey && event.code === "Space") {
        event.preventDefault();  // Prevent the default space behavior
        toggleModal();
    }
    if (event.key === "Escape") {
        modal.style.display = "none";
    }
}

// Search through the array when a key is pressed
searchInput.oninput = function() {
    var query = this.value;

	const results = fuzzysort.go(query, search_list)

    // Update the results list
    var resultsList = document.getElementById("results");
    resultsList.innerHTML = "";  // Clear previous results

    results.forEach(function(result) {
        var li = document.createElement("li");
        li.textContent = result.target;
        resultsList.appendChild(li);
    });

    // Select the first item by default
    if (results.length > 0) {
        selectedIndex = 0;
        selectItem(selectedIndex);
    } else {
        selectedIndex = -1;
    }
}

// Handle Tab and Shift + Tab keys
searchInput.onkeydown = function(event) {
    var resultsList = document.getElementById("results");
    var items = resultsList.getElementsByTagName("li");

    if (event.key === "Tab") {
        event.preventDefault();  // Prevent the default tab behavior (moving focus)
        if (event.shiftKey) {
            if (selectedIndex > 0) {
                selectedIndex--;
            }
        } else {
            if (selectedIndex < items.length - 1) {
                selectedIndex++;
            }
        }
        selectItem(selectedIndex);
    } else if (event.key === "Enter") {
        if (selectedIndex >= 0 && selectedIndex < items.length) {
            on_select_callback(items[selectedIndex]);
        }
    }
}

// Function to select an item
function selectItem(index) {
    var resultsList = document.getElementById("results");
    var items = resultsList.getElementsByTagName("li");

    // Remove the 'selected' class from all items
    Array.from(items).forEach(function(item) {
        item.classList.remove("selected");
    });

    // Add the 'selected' class to the current item
    if (items[index]) {
        items[index].classList.add("selected");
        items[index].scrollIntoView({ block: 'nearest' });
    }
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
