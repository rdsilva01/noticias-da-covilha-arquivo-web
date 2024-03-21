// FOR THE SEARCH BAR
document.addEventListener("DOMContentLoaded", function() {

    var searchForm = document.getElementById("searchForm");
    var searchInput = document.getElementById("searchInput");
    var searchButton = document.getElementById("searchButton");
    
    function toggleButton() {
        if (searchInput.value.trim() === '') {
            searchButton.disabled = true;
        } else {
            searchButton.disabled = false;
        }
    }

    toggleButton();

    searchInput.addEventListener("input", toggleButton);

    searchForm.addEventListener("submit", function(event) {
        if (searchInput.value.trim() === '') {
            // If search input is empty, prevent form submission
            event.preventDefault();
        }
    });
});