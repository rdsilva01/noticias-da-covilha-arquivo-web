if (document.getElementById("searchInput")) {
document.addEventListener("DOMContentLoaded", function() {
        var searchInput = document.getElementById("searchInput");

        document.getElementById('searchButton').addEventListener('click', function() {
            var searchQuery = searchInput.value.trim();
            if (searchQuery === '') {
                searchInput.value = searchInput.placeholder;
            }
            // Submit the form
            document.getElementById('searchForm').submit();
        });

        document.getElementById('')

        //searchInput.addEventListener("input", toggleButton);

        document.getElementById("searchForm").addEventListener("submit", function(event) {
            if (searchInput.value.trim() === '') {
                event.preventDefault();
                searchInput.value = searchInput.placeholder; // Fill input with placeholder value before submitting
            }
        });
    });
}
