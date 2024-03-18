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
        filtersButton.textContent = "Fechar";

    } else {
        filtersContainer.style.display = "none";
        filtersButton.textContent = "Opções Avançadas";
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
