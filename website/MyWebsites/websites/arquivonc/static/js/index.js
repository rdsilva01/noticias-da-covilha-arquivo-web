// LOADER
function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'none';
        const page = document.querySelector('.page');
        if (page) {
            page.style.display = 'block';
        }
    }
}

if (document.getElementById('indexPage')) {

// Wait for all resources to load
window.addEventListener('load', function() {

// document.addEventListener('DOMContentLoaded', function() {
    hideLoader();
      var images = document.querySelectorAll('.25-abril-image ');
    images.forEach(function(image) {
        var containerWidth = image.parentElement.offsetWidth;
        image.style.height = containerWidth + "px";
    });
});

}
// MAIN NEWS IMAGE ERROR
function handleImageError(imageId) {
    const imageContainer = document.getElementById(imageId);
    if (imageContainer) {
        imageContainer.classList.remove('col-md-7');
        imageContainer.classList.add('col-md-12');
        const image = imageContainer.querySelector('.main-article-image');
        if (image) {
            image.style.display = 'none';
        }
        const textColumn = imageContainer.nextElementSibling;
        if (textColumn && textColumn.classList.contains('col-md-5')) {
            textColumn.classList.remove('col-md-5');
            textColumn.classList.add('col-md-12');
        }
    }
}


$(document).ready(function() {
    var showMore = false;
    
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

/////////////////////////
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

// if (document.getElementById('page')) {
// document.addEventListener('DOMContentLoaded', function() {
//     const prevYearBtn = document.getElementById('prevYear');
//     const nextYearBtn = document.getElementById('nextYear');
//     const currentYearBtn = document.getElementById('currentYear');
    
//     let currentYearIndex = 0;
//     const statsContainers = document.querySelectorAll('.stats');
//     const contentStatsContainers = document.querySelectorAll('.content-stats');
//     const years = Array.from(statsContainers).map(container => container.id.split('_')[1]);
//     const yearsContent = Array.from(contentStatsContainers).map(container => container.id.split('_')[1]);


//     function showStatsContainer(index) {
//         statsContainers.forEach(container => {
//             container.style.display = 'none';
//         });
//         statsContainers[index].style.display = 'block';
//         currentYearBtn.textContent = years[index];
//         currentYearBtn.href = `noticias?ano=${years[index]}`;
//         currentYearIndex = index;
//     }

//     function showContentStatsContainer(index) {
//         contentStatsContainers.forEach(container => {
//             container.style.display = 'none';
//         });
//         contentStatsContainers[index].style.display = 'block';
//         currentYearIndex = index;
//     }

//     prevYearBtn.addEventListener('click', function() {
//         currentYearIndex = Math.max(0, currentYearIndex - 1);
//         showStatsContainer(currentYearIndex);
//         showContentStatsContainer(currentYearIndex);
//     });

//     nextYearBtn.addEventListener('click', function() {
//         currentYearIndex = Math.min(years.length - 1, currentYearIndex + 1);
//         showStatsContainer(currentYearIndex);
//         showContentStatsContainer(currentYearIndex);
//     });

//     // Show the initial stats container
//     showStatsContainer(currentYearIndex);
//     showContentStatsContainer(currentYearIndex);
// });
// }

// /////////////////////////
//          MODAL
// /////////////////////////
 function openModal(imageUrl, imageAlt) {
    var modal = document.getElementById('myModal');
    var modalImage = document.getElementById('modalImage');
    var captionText = document.getElementById('caption');

    document.body.style.overflow = 'hidden'; // Disable scrolling

    modal.style.display = "block"; // Display the modal
    modalImage.src = imageUrl; // Set the src attribute of the modal image
    modalImage.alt = imageAlt; // Set the alt attribute of the modal image
    captionText.textContent = imageAlt; 
}

// Function to close the modal
function closeModal() {
    document.body.style.overflow = 'auto'; // Enable scrolling
    
    var modal = document.getElementById('myModal');
    modal.style.display = "none"; // Hide the modal
}

window.addEventListener("click", function(event) {
    var modal = document.getElementById('myModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
});


function updateHiddenField(checkboxId, hiddenFieldId) {
    var checkbox = document.getElementById(checkboxId);
    var hiddenField = document.getElementById(hiddenFieldId);
    if (checkbox.checked) {
        hiddenField.value = 1;
    } else {
        hiddenField.value = 0;
    }
}

// Wait for all resources to load
window.addEventListener('load', function() {
    // Get all images with class "img-news"
    var images = document.querySelectorAll('.img-news');
    var count = 0
    // Iterate through each image
    images.forEach(function(image) {
        count++
        // Check if the image has loaded
        image.addEventListener('load', function() {
            // Check if src attribute is empty
            if (!image.getAttribute('src')) {
                handleImageErrorNews(image)
            }
        });
    });
    console.log(count)
    hideLoader();
});
///////////////////////////
// SINGLE NEWS IMAGE ERROR
///////////////////////////
function handleImageErrorNews(image) {
    // Hide the image by setting its display property to 'none'
    image.style.display = 'none';
    var parentDiv = image.parentElement;
                if (parentDiv) {
                    parentDiv.style.display = 'none';
                }
}

$(document).ready(function(){
    $('#startDate').datepicker({
        format: 'yyyy-mm-dd',
        language: 'pt',
        startDate: '2009-01-01', // Minimum date
        endDate: '2019-12-31', // Maximum date
        defaultViewDate: { year: 2009, month: 0, day: 1 }, // Default date (January 1, 2009)
        setDate: '2009-01-01' // Default value
    });

    $('#endDate').datepicker({
        format: 'yyyy-mm-dd',
        language: 'pt',
        startDate: '2009-01-01', // Minimum date
        endDate: '2019-12-31', // Maximum date
        defaultViewDate: { year: 2019, month: 11, day: 31 }, // Default date (December 31, 2019)
        setDate: '2019-12-31' // Default value
    });
});



$(document).ready(function() {
    $('.btn-ant').on('click', function() {
        $('.slider-main-news').slick('slickPrev');
    });

    $('.btn-prox').on('click', function() {
        $('.slider-main-news').slick('slickNext');
    });

    
});

if (document.getElementById('slider-hero')) {
(function($) {
    $(document).ready(function() {
        $('.slider-hero').slick({
            infinite: false,
            slidesToShow: 3,
            dots: false,
            // focusOnSelect: true,
            // centerMode: true,
            arrows: false,
        });
    });
	
})( jQuery );
}

if (document.getElementById('slider-hero-dois')) {
(function($) {
    $(document).ready(function() {
        $('.slider-hero-dois').slick({
            infinite: false,
            slidesToShow: 2,
            dots: false,
            arrows: false,
        });
    });
	
})( jQuery );
}

if (document.getElementById('slider-hero-um')) {
    (function($) {
        $(document).ready(function() {
            $('.slider-hero-um').slick({
                infinite: false,
                slidesToShow: 1,
                dots: false,
                arrows: false,
            });
        });
        
    })( jQuery );
    }


if (document.getElementById('slider-subcategorias')) {
    (function($) {
        $(document).ready(function() {
            $('.slider-subcategorias').slick({
                infinite: true,
                slidesToShow: 6,
                slidesToScroll: 1,
                variableWidth: false,
                dots: false,
                arrows: false,
                autoplay: true,
                autoplaySpeed: 3000,
                focusOnSelect: false,
                pauseOnHover: false,
                pauseOnFocus: false,
            });
        });
        
    })( jQuery );

    (function($) {
        $(document).ready(function() {
            $('.slider-subcategorias-medium').slick({
                infinite: true,
                slidesToShow: 4,
                slidesToScroll: 1,
                variableWidth: false,
                dots: false,
                arrows: false,
                autoplay: true,
                autoplaySpeed: 3000,
                focusOnSelect: false,
                pauseOnHover: false,
                pauseOnFocus: false,
            });
        });
        
    })( jQuery );

    (function($) {
        $(document).ready(function() {
            $('.slider-subcategorias-small').slick({
                infinite: true,
                slidesToShow: 3,
                slidesToScroll: 1,
                variableWidth: false,
                dots: false,
                arrows: false,
                autoplay: true,
                autoplaySpeed: 3000,
                focusOnSelect: false,
                pauseOnHover: false,
                pauseOnFocus: false,
            });
        });
        
    })( jQuery );

    $(document).ready(function() {
        $('.btn-left').on('click', function() {
            $('.slider-subcategorias-small').slick('slickPrev');
            $('.slider-subcategorias-medium').slick('slickPrev');
            $('.slider-subcategorias').slick('slickPrev');
        });
    
        $('.btn-right').on('click', function() {
            $('.slider-subcategorias-small').slick('slickNext');
            $('.slider-subcategorias-medium').slick('slickNext');
            $('.slider-subcategorias').slick('slickNext');
        });
    });
}

(function($) {
    $(document).ready(function() {
        $('.slider-hero-medium').slick({
            infinite: true,
            slidesToShow: 2,
            slidesToScroll: 2,
            dots: true,
            arrows: true,
            nextArrow:"<button class='slick-next text-dark' aria-label='Next' type='button' style='display: block; content='''><svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' fill='currentColor' class='bi bi-caret-right-fill' viewBox='0 0 16 16'><path d='m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z'/></svg></button>",
            prevArrow:"<button class='slick-prev text-dark' aria-label='Prev' type='button' style='display: block;'><svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' fill='currentColor' class='bi bi-caret-left-fill' viewBox='0 0 16 16'><path d='m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z'/></svg></button>"
        });
    });
	
})( jQuery );


(function($) {
    $(document).ready(function() {
        $('.slider-hero-small').slick({
            infinite: true,
            slidesToShow: 1,
            dots: true,
            arrows: true,
            nextArrow:"<button class='slick-next text-dark' aria-label='Next' type='button' style='display: block; content='''><svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' fill='currentColor' class='bi bi-caret-right-fill' viewBox='0 0 16 16'><path d='m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z'/></svg></button>",
            prevArrow:"<button class='slick-prev text-dark' aria-label='Prev' type='button' style='display: block;'><svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' fill='currentColor' class='bi bi-caret-left-fill' viewBox='0 0 16 16'><path d='m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z'/></svg></button>"
        });
    });
	
})( jQuery );

//  if the id #page exists
if (document.getElementById('page')) {
    (function($) {
        $(document).ready(function() {
            var slider = $('.slider-main-news');
            var sliderOptions = {
                infinite: true,
                slidesToShow: 1,
                dots: false,
                arrows: false,
                fade: true,
                autoplay: false,
                autoplaySpeed: 5000,
                adaptiveHeight: true,
                focusOnSelect: false,
                pauseOnHover: false,
                pauseOnFocus: false,
            };
    
            // Initialize the slider
            slider.slick(sliderOptions);
    
            // Intersection Observer setup
            var observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        slider.slick('slickPlay');
                    } else {
                        slider.slick('slickPause');
                    }
                });
            }, { threshold: 0.7 }); 
    
            // Observe the slider
            observer.observe(slider[0]);
        });
    })(jQuery);
}

// CORRIGIR ISTO
(function($) {
    $(document).ready(function() {
        $('.slider-anos').slick({
            slidesToShow: 12,
            slidesToScroll: 1,
            variableWidth: false,
            dots: false,
            arrows: false,
            autoplay: true,
            autoplaySpeed: 3000,
            focusOnSelect: false,
            pauseOnHover: false,
            pauseOnFocus: false,
        });
    });
	
})( jQuery );

(function($) {
    $(document).ready(function() {
        $('.slider-anos-medium').slick({
            slidesToShow: 5,
            slidesToScroll: 1,
            variableWidth: false,
            dots: false,
            arrows: false,
            autoplay: true,
            autoplaySpeed: 3000,
            focusOnSelect: false,
            pauseOnHover: false,
            pauseOnFocus: false,
        });
    });
	
})( jQuery );

(function($) {
    $(document).ready(function() {
        $('.slider-anos-small').slick({
            slidesToShow: 5,
            slidesToScroll: 1,
            variableWidth: false,
            dots: false,
            arrows: false,
            autoplay: true,
            autoplaySpeed: 3000,
            focusOnSelect: false,
            pauseOnHover: false,
            pauseOnFocus: false,
        });
    });
	
})( jQuery );

// when pressing the left btn goes to the previous slide, using this: $('.your-element').slick('setPosition');
// do that in jquery
$(document).ready(function() {
    $('.btn-left').on('click', function() {
        $('.slider-hero').slick('slickPrev');
        $('.slider-hero-dois').slick('slickPrev');
        $('.slider-hero-um').slick('slickPrev');
        $('.slider-hero-medium').slick('slickPrev');
        $('.slider-hero-small').slick('slickPrev');
        $('.slider-anos').slick('slickPrev');
        $('.slider-anos-medium').slick('slickPrev');
        $('.slider-anos-small').slick('slickPrev');
    });

    $('.btn-right').on('click', function() {
        $('.slider-hero').slick('slickNext');
        $('.slider-hero-dois').slick('slickNext');
        $('.slider-hero-um').slick('slickNext');
        $('.slider-hero-medium').slick('slickNext');
        $('.slider-hero-small').slick('slickNext');
        $('.slider-anos').slick('slickNext');
        $('.slider-anos-medium').slick('slickNext');
        $('.slider-anos-small').slick('slickNext');
    });
});


// TOP BUTTON
$(document).ready(function() {
    // Smooth scrolling when the button is clicked
    $('#scrollToTop').on('click', function() {
        var targetSectionId = 'page';
        var targetSectionOffset = $('#' + targetSectionId).offset().top;
        $('html, body').animate({
            scrollTop: 0
        }, 300); // Adjust the duration as needed
    });
});

