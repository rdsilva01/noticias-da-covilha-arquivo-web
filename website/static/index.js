document.addEventListener("DOMContentLoaded", function() {
    var cursorCircle = document.getElementById("cursor-circle");

    document.addEventListener("mousemove", function(e) {
        var x = e.clientX;
        var y = e.clientY;
        cursorCircle.style.left = x + "px";
        cursorCircle.style.top = y + "px";
    });
});


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

    var search_titles = [
        `UM <span class="border-bottom border-danger border-3 px-1 lh-base">SLOGAN</span>`
        // `<span class="border-bottom border-danger border-3 px-1 lh-base">Tradição</span> em Páginas`,
        // `<span class="border-bottom border-danger border-3 px-1 lh-base">Curiosidade Desperta</span>, Explore!`,
        // `Um Arquivo <span class="border-bottom border-danger border-3 px-1 lh-base">Vivo</span>`
    ];

    var placeholders = [
        "Rampa da Serra da Estrela 2012...",
        "Eleições 2016...",
        "Leões da Serra...",
    ];

    var searchForm = document.getElementById("searchForm");
    var searchInput = document.getElementById("searchInput");
    var searchButton = document.getElementById("searchButton");
    var searchTitle = document.getElementById("searchTitle");

    function setRandomIndex() {
        var randomIndex = Math.floor(Math.random() * placeholders.length);
        var randomIndexSearchInput = Math.floor(Math.random() * search_titles.length);
        searchInput.placeholder = placeholders[randomIndex];
        searchTitle.innerHTML = search_titles[randomIndexSearchInput];
    }

    setRandomIndex();

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
        filtersButton.innerHTML= `Fechar Opções Avançadas `;
        // <svg xmlns="http://www.w3.org/2000/svg" width="29" height="29" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
        // <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
        // </svg>

    } else {
        filtersContainer.style.display = "none";
        filtersButton.textContent = "";
        filtersButton.innerHTML = `Opções Avançadas`;
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
/*
// STATS
var selectElement = document.getElementById('yearSelect');
var statsContainer = document.querySelector('.statsContainer');

selectElement.addEventListener('change', function() {
    var selectedYear = this.value;
    showStats(selectedYear);
});

function showStats(year) {
    // Hide all stats
    var allStats = statsContainer.getElementsByClassName('stats');
    for (var i = 0; i < allStats.length; i++) {
        allStats[i].style.display = 'none';
    }

    // Show stats for the selected year
    var statsToShow = document.getElementById('stats_' + year);
    if (statsToShow) {
        statsToShow.style.display = 'block';
    }
}
*/

document.addEventListener('DOMContentLoaded', function() {
    const prevYearBtn = document.getElementById('prevYear');
    const nextYearBtn = document.getElementById('nextYear');
    const currentYearBtn = document.getElementById('currentYear');
    
    let currentYearIndex = 0;
    const statsContainers = document.querySelectorAll('.stats');
    const contentStatsContainers = document.querySelectorAll('.content-stats');
    const years = Array.from(statsContainers).map(container => container.id.split('_')[1]);
    const yearsContent = Array.from(contentStatsContainers).map(container => container.id.split('_')[1]);


    function showStatsContainer(index) {
        statsContainers.forEach(container => {
            container.style.display = 'none';
        });
        statsContainers[index].style.display = 'block';
        currentYearBtn.textContent = years[index];
        currentYearIndex = index;
    }

    function showContentStatsContainer(index) {
        contentStatsContainers.forEach(container => {
            container.style.display = 'none';
        });
        contentStatsContainers[index].style.display = 'block';
        currentYearIndex = index;
    }

    prevYearBtn.addEventListener('click', function() {
        currentYearIndex = Math.max(0, currentYearIndex - 1);
        showStatsContainer(currentYearIndex);
        showContentStatsContainer(currentYearIndex);
    });

    nextYearBtn.addEventListener('click', function() {
        currentYearIndex = Math.min(years.length - 1, currentYearIndex + 1);
        showStatsContainer(currentYearIndex);
        showContentStatsContainer(currentYearIndex);
    });

    // Show the initial stats container
    showStatsContainer(currentYearIndex);
    showContentStatsContainer(currentYearIndex);
});



// Get the modal
var modal = document.getElementById("myModal");

var img = document.getElementById("myImg");
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
img.onclick = function(){
  modal.style.display = "block";
  modalImg.src = this.src;
  captionText.innerHTML = this.alt;
}

var modal = document.getElementById("myModal");

window.addEventListener("click", function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
});



// MAIN NEWS IMAGE ERROR
function handleImageError(image) {
    document.getElementById('imageColumn').classList.remove('col-md-7');
    document.getElementById('imageColumn').classList.add('col-md-12');
    image.style.display = 'none';
    document.getElementById('textColumn').classList.remove('col-md-5');
    document.getElementById('textColumn').classList.add('col-md-12');
}