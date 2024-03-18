var currentSecondaryNavSection = null;

function toggleSecondaryNav(section, element) {
    var secondaryNavItems = document.querySelectorAll('#secondaryNav .nav-item');
    var secondaryNav = document.querySelector('#secondaryNavMain');
    var secondaryNavItem = document.getElementById(section + 'Item');

    // If nothing is pressed and the secondary navigation is closed, or if a different section is pressed, open the secondary navigation
    if (currentSecondaryNavSection !== section || secondaryNav.style.display === 'none' || secondaryNav.style.display === '') {
        secondaryNav.style.display = 'block';
        currentSecondaryNavSection = section;
    }

    secondaryNavItems.forEach(function(item) {
        item.style.opacity = '0';
        item.style.display = 'none';
    });

    secondaryNavItem.style.display = 'block';
    secondaryNavItem.style.opacity = '1';

    var primaryNavItems = document.querySelectorAll('.navbar-nav .nav-item');
    primaryNavItems.forEach(function(item) {
        item.classList.remove('active-nav-item');
    });

    element.parentNode.classList.add('active-nav-item');
}


// FOR THE SEARCH BAR
document.addEventListener("DOMContentLoaded", function() {

    var placeholders = [
        "Rampa da Serra da Estrela 2012...",
        "Eleições 2016...",
        "Leões da Serra...",

    ];

    var searchInput = document.getElementById("searchInput");

    function setRandomPlaceholder() {
        var randomIndex = Math.floor(Math.random() * placeholders.length);
        searchInput.placeholder = placeholders[randomIndex];
    }

    setRandomPlaceholder();

    var searchForm = document.getElementById("searchForm");
    searchForm.addEventListener("submit", function(event) {

        event.preventDefault();
        //...
    });
});

$(document).ready(function() {
    var showMore = false;
    
    // Initially hide articles beyond the first 5
    $('.article-far-right:gt(4)').addClass('d-none');

    $('#verMaisBtn').click(function() {
        showMore = !showMore;
        if (showMore) {
            $('.article-far-right.d-none').removeClass('d-none');
            $('#verMaisBtn').text('Ver Menos');
        } else {
            $('.article-far-right:gt(4)').addClass('d-none');
            $('#verMaisBtn').text('Ver Mais');
        }
    });
});

// FILTERS
function toggleFilters() {
    var filtersContainer = document.querySelector('.filters-container');
    var filtersButton = document.querySelector('#showFiltersBtn')
    if (filtersContainer.style.display === "none") {
        filtersContainer.style.display = "flex";
        filtersButton.innerHTML= `<svg xmlns="http://www.w3.org/2000/svg" width="29" height="29" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
      </svg>`;

    } else {
        filtersContainer.style.display = "none";
        filtersButton.textContent = "";
        filtersButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="29" height="29" fill="currentColor" class="bi bi-gear-wide-connected text-light" viewBox="0 0 16 16">
        <path d="M7.068.727c.243-.97 1.62-.97 1.864 0l.071.286a.96.96 0 0 0 1.622.434l.205-.211c.695-.719 1.888-.03 1.613.931l-.08.284a.96.96 0 0 0 1.187 1.187l.283-.081c.96-.275 1.65.918.931 1.613l-.211.205a.96.96 0 0 0 .434 1.622l.286.071c.97.243.97 1.62 0 1.864l-.286.071a.96.96 0 0 0-.434 1.622l.211.205c.719.695.03 1.888-.931 1.613l-.284-.08a.96.96 0 0 0-1.187 1.187l.081.283c.275.96-.918 1.65-1.613.931l-.205-.211a.96.96 0 0 0-1.622.434l-.071.286c-.243.97-1.62.97-1.864 0l-.071-.286a.96.96 0 0 0-1.622-.434l-.205.211c-.695.719-1.888.03-1.613-.931l.08-.284a.96.96 0 0 0-1.186-1.187l-.284.081c-.96.275-1.65-.918-.931-1.613l.211-.205a.96.96 0 0 0-.434-1.622l-.286-.071c-.97-.243-.97-1.62 0-1.864l.286-.071a.96.96 0 0 0 .434-1.622l-.211-.205c-.719-.695-.03-1.888.931-1.613l.284.08a.96.96 0 0 0 1.187-1.186l-.081-.284c-.275-.96.918-1.65 1.613-.931l.205.211a.96.96 0 0 0 1.622-.434zM12.973 8.5H8.25l-2.834 3.779A4.998 4.998 0 0 0 12.973 8.5m0-1a4.998 4.998 0 0 0-7.557-3.779l2.834 3.78zM5.048 3.967l-.087.065zm-.431.355A4.98 4.98 0 0 0 3.002 8c0 1.455.622 2.765 1.615 3.678L7.375 8zm.344 7.646.087.065z"/>
      </svg>`;
    }
}

function toggleStatistics() {
    var statisticsContainer = document.querySelector('.statistics-container');
    var button = document.querySelector('.toggle-button');
    if (statisticsContainer.style.display === 'none') {
        statisticsContainer.style.display = 'block';
        button.textContent = 'FECHAR ESTATÍSTICAS';
    } else {
        statisticsContainer.style.display = 'none';
        button.textContent = 'VER ESTATÍSTICAS';
    }
}
