if  (document.getElementById("searchIndexInput")) {
    document.addEventListener("DOMContentLoaded", function() {
            var searchInput = document.getElementById("searchIndexInput");
            var placeholders = [
                "UBI",
                "Covilhã",
                "Serra da Estrela",
                "Rampa da Serra",
                "Leões",
                "Vítor Pereira",
                "Sócrates"
            ];
        
            function setRandomPlaceholder() {
                var randomIndex = Math.floor(Math.random() * placeholders.length);
                searchInput.placeholder = placeholders[randomIndex];
            }
        
            setRandomPlaceholder();

            var currPlaceholder = searchInput.placeholder;
            // when a radio button is clicked, submit
            var radioButtons = document.querySelectorAll('input[type="radio"]');
            radioButtons.forEach(function(radioButton) {
                radioButton.addEventListener('click', function() {
                    searchInput.placeholder = currPlaceholder;
                    if (searchInput.value.trim() === '') {
                        searchInput.value = searchInput.placeholder;
                    }
                    document.getElementById('searchForm').submit();
                });
            });

        
            document.getElementById('searchButton').addEventListener('click', function() {
                var searchQuery = searchInput.value.trim();
                if (searchQuery === '') {
                    searchInput.value = searchInput.placeholder;
                }
                // Submit the form
                document.getElementById('searchForm').submit();
            });
        
            // searchInput.addEventListener("input", toggleButton);
        
            document.getElementById("searchForm").addEventListener("submit", function(event) {
                if (searchInput.value.trim() === '') {
                    event.preventDefault();
                    searchInput.value = searchInput.placeholder; // Fill input with placeholder value before submitting
                }
            });
        });
}
        

// FILTERS
function toggleFilters() {
    var filtersContainer = document.querySelector('.filters-container');
    var filtersButton = document.querySelector('#showFiltersBtn')
    if (filtersContainer.style.display === "none" || filtersContainer.style.display === "") {
        filtersContainer.style.display = "flex";
        filtersButton.querySelector('#textoOpcoes').textContent = "Fechar";
        filtersButton.querySelector('#iconeOpcoes').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
            <path d="M4.854 4.146a.5.5 0 0 1 .708 0L8 7.293l2.146-2.147a.5.5 0 1 1 .708.708L8.707 8l2.147 2.146a.5.5 0 1 1-.708.708L8 8.707 5.854 10.854a.5.5 0 0 1-.708-.708L7.293 8 5.146 5.854a.5.5 0 0 1 0-.708z"/>
        </svg>`;
    } else {
        filtersContainer.style.display = "none";
        filtersButton.querySelector('#textoOpcoes').textContent = "Opções Avançadas";
        filtersButton.querySelector('#iconeOpcoes').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear-wide-connected" viewBox="0 0 16 16">
            <path d="M7.068.727c.243-.97 1.62-.97 1.864 0l.071.286a.96.96 0 0 0 1.622.434l.205-.211c.695-.719 1.888-.03 1.613.931l-.08.284a.96.96 0 0 0 1.187 1.187l.283-.081c.96-.275 1.65.918.931 1.613l-.211.205a.96.96 0 0 0 .434 1.622l.286.071c.97.243.97 1.62 0 1.864l-.286.071a.96.96 0 0 0-.434 1.622l.211.205c.719.695.03 1.888-.931 1.613l-.284-.08a.96.96 0 0 0-1.187 1.187l.081.283c.275.96-.918 1.65-1.613.931l-.205-.211a.96.96 0 0 0-1.622.434l-.071.286c-.243.97-1.62.97-1.864 0l-.071-.286a.96.96 0 0 0-1.622-.434l-.205.211c-.695.719-1.888.03-1.613-.931l.08-.284a.96.96 0 0 0-1.186-1.187l-.284.081c-.96.275-1.65-.918-.931-1.613l.211-.205a.96.96 0 0 0-.434-1.622l-.286-.071c-.97-.243-.97-1.62 0-1.864l.286-.071a.96.96 0 0 0 .434-1.622l-.211-.205c-.719-.695-.03-1.888.931-1.613l.284.08a.96.96 0 0 0 1.187-1.186l-.081-.284c-.275-.96.918-1.65 1.613-.931l.205.211a.96.96 0 0 0 1.622-.434zM12.973 8.5H8.25l-2.834 3.779A4.998 4.998 0 0 0 12.973 8.5m0-1a4.998 4.998 0 0 0-7.557-3.779l2.834 3.78zM5.048 3.967l-.087.065zm-.431.355A4.98 4.98 0 0 0 3.002 8c0 1.455.622 2.765 1.615 3.678L7.375 8zm.344 7.646.087.065z"/>
        </svg>`;
    }
}