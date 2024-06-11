// CURSOR
// document.addEventListener("DOMContentLoaded", function() {
//     var cursorCircle = document.getElementById("cursor-circle");

//     document.addEventListener("mousemove", function(e) {
//         var x = e.clientX;
//         var y = e.clientY;
//         cursorCircle.style.left = x + "px";
//         cursorCircle.style.top = y + "px";
//     });
// });
var erro = 0

// window.onload = function() {
//     if (window.location.hash) {
//         var hash = window.location.hash;
//         var element = document.querySelector(hash);
//         if (element) {
//             // Get the height of the #pesquise element
//             var yourHeight = window.getComputedStyle(element).height;
//             // Scroll to your element
//             element.scrollIntoView(true);
            
//             // Account for fixed header
//             var scrolledY = window.scrollY;
//             if (scrolledY) {
//                 window.scroll(0, scrolledY - parseInt(yourHeight));
//             }
//         }
//     }
// }

// // Function to determine the device type
// function getDeviceType() {
//     // Check if the user agent contains any mobile-related keywords
//     var userAgent = navigator.userAgent.toLowerCase();
//     var mobileKeywords = ['android', 'webos', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone'];
//     for (var i = 0; i < mobileKeywords.length; i++) {
//         if (userAgent.indexOf(mobileKeywords[i]) !== -1) {
//             return 'mobile';
//         }
//     }
//     // If none of the mobile-related keywords are found, assume it's a computer
//     return 'computer';
// }

// // When the page loads, check the device type and display the appropriate content
// window.onload = function() {
//     var divMobile = document.getElementById('mobileDevice');
//     var divComputer = document.getElementById('computerDevice');

//     var device = getDeviceType();
//     if (device === 'mobile') {
//         divMobile.style.display = 'block';
//         divComputer.style.display = 'none';
//     } else {
//         divComputer.style.display = 'block';
//         divMobile.style.display = 'none';
//     }
// };


// SECONDARY NAV
var currentSecondaryNavSection = null;

function toggleSecondaryNav(section, element) {
    var secondaryNavItems = document.querySelectorAll('#secondaryNav .nav-item');
    var secondaryNav = document.querySelector('#secondaryNavMain');
    var secondaryNavItem = document.getElementById(section + 'Item');

    // If nothing is pressed and the secondary navigation is closed, or if a different section is pressed, open the secondary navigation
    if (currentSecondaryNavSection !== section || secondaryNav.style.display === 'none' || secondaryNav.style.display === '') {
        secondaryNav.style.display = 'block';
        currentSecondaryNavSection = section;

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
    // If the same section is pressed, close the secondary navigation
    else {
        secondaryNav.style.display = 'none';
        currentSecondaryNavSection = null;
        element.parentNode.classList.remove('active-nav-item');
    }   

   
}

////////////////////////////
//         MODAL          //
////////////////////////////
function openModal(imageUrl, imageAlt) {
    var modal = document.getElementById('myModal');
    var modalImage = document.getElementById('modalImage');
    var captionText = document.getElementById('caption');

    modal.style.display = "block"; // Display the modal
    modalImage.src = imageUrl; // Set the src attribute of the modal image
    modalImage.alt = imageAlt; // Set the alt attribute of the modal image
    captionText.textContent = imageAlt; 
}

// Function to close the modal
function closeModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = "none"; // Hide the modal
}

function openImageModal(imageUrl, imageAlt, imageDate, imageRedirectUrl) {
    var modal = document.getElementById('imageModal');
    var modalImage = document.getElementById('imageImageModal');
    var captionText = document.getElementById('titleImageModal');
    var dateText = document.getElementById('dateImageModal');
    var similarityContent = document.getElementById('snippetImageModal');
    var redirectButton = document.getElementById('redirectImageModal');

    modal.style.display = "block";
    modalImage.src = imageUrl;
    modalImage.alt = imageAlt; 
    captionText.textContent = imageAlt; 
    dateText.textContent = imageDate;
    // snippetContent.innerHTML = imageSnippet + "...";
    redirectButton.href = 'noticias?nid=' + imageRedirectUrl;

}

function openImageModalSobre(imageUrl, imageDesc){
    var modal = document.getElementById('imageModalSobre');
    var modalImage = document.getElementById('imageImageModalSobre');
    // var captionText = document.getElementById('titleImageModalSobre');

    modal.style.display = "block";
    modalImage.src = imageUrl;
    modalImage.alt = imageDesc;
    // captionText.textContent = imageDesc;

}

function closeImageModalSobre() {
    var modal = document.getElementById('imageModalSobre');
    modal.style.display = "none"; // Hide the modal
}

function openImageQueryModal(imageUrl, imageAlt, imageNids, imageSimNews, imageSimUrls, imageSimNids, imageDate) {
    var modal = document.getElementById('imageModal');
    var modalImage = document.getElementById('imageImageModal');
    // var snippetContent = document.getElementById('snippetImageModal');
    var redirectDiv = document.getElementById('redirectImageModal');
    var similarDivMain = document.getElementById('similarImageModal');

    modal.style.display = "block";
    modalImage.src = imageUrl;
    modalImage.onerror = function() {
        handleImageErrorANews(modalImage);
    };
    modalImage.style.scale = '1';
    modalImage.alt = imageAlt; 
    var parentDiv = modalImage.parentElement;
    parentDiv.classList.remove('bg-light')
    parentDiv.classList.remove('border')
    parentDiv.classList.remove('border-1')
    parentDiv.classList.remove('border-dark')

    // var imageNidList = imageNids.split(";");
    // var imageTitlesList = imageTitles.split(";");

    // Create the redirect buttons
    redirectDiv.innerHTML = "";
    redirectDiv.classList.add('row');
    linksDiv = document.createElement('div');
    linksDiv.classList.add('d-flex-column', 'p-1', 'text-start', 'mb-4');
    var redirectDateLink = document.createElement('a');
    redirectDateLink.href = 'noticias?nid=' + imageNids;
    redirectDateLink.textContent = imageDate;
    redirectDateLink.classList.add('d-inline-block');
    redirectDateLink.classList.add('text-dark');
    redirectDateLink.classList.add('link');
    redirectDateLink.classList.add('link-underline-danger');
    redirectDateLink.classList.add('link-underline-opacity-25');
    redirectDateLink.classList.add('link-underline-opacity-100-hover');
    redirectDateLink.classList.add('text-uppercase');
    redirectDateLink.classList.add('font-oswald');
    redirectDateLink.classList.add('fs-1');
    breakLine = document.createElement('br')
    linksDiv.appendChild(redirectDateLink);
    linksDiv.appendChild(breakLine);
    var redirectLink = document.createElement('a');
    redirectLink.href = 'noticias?nid=' + imageNids;
    redirectLink.classList.add('d-inline-block');
    redirectLink.classList.add('link');
    redirectLink.classList.add('link-dark');
    redirectLink.classList.add('link-underline-opacity-0');
    redirectLink.classList.add('link-underline-opacity-100-hover');
    redirectLink.classList.add('text-uppercase');
    redirectLink.classList.add('font-oswald');
    redirectLink.classList.add('fs-3');
    redirectLink.text = imageAlt;
    linksDiv.appendChild(redirectLink);
    redirectDiv.appendChild(linksDiv);

    imageSimNews = imageSimNews.split(";");
    imageSimUrls = imageSimUrls.split(";");
    imageSimNids = imageSimNids.split(";");

    similarDivMain.innerHTML = "";
    similarDivMain.classList.add('row');
    var similarDiv = document.createElement('div');
    similarDiv.classList.add('row', 'gx-0', 'px-0', 'px-md-2', 'pb-3', 'justify-content-center');
    for (var i = 0; i < imageSimNews.length; i++) {
        var similarButtonDiv = document.createElement('div');
        similarButtonDiv.classList.add('col-6', 'col-md-4', 'col-lg-3', 'p-1');
        var similarButtonDivDiv = document.createElement('div');
        similarButtonDivDiv.classList.add('pb-4', 'h-100');
        var similarButtonDivDivDiv = document.createElement('div');
        similarButtonDivDivDiv.classList.add('mb-3', 'border', 'border-1', 'border-dark', 'rounded-1', 'pe-auto', 'bg-white', 'h-100', 'px-2');
        var similarImageDiv = document.createElement('div');
        similarImageDiv.classList.add('field-content-image', 'rounded-1', 'border', 'border-1', 'border-light', 'rounded-1', 'pe-auto');
        
        var similarImageAnchor = document.createElement('a');
        similarImageAnchor.href = 'noticias?nid=' + imageSimNids[i];

        var similarImage = document.createElement('img');
        similarImage.src = imageSimUrls[i];
        similarImage.alt = imageSimNews[i];
        similarImage.classList.add('img-news', 'rounded-1', 'year-article-image');
        similarImage.onerror = function() {
            handleImageErrorANews(similarImage);
        };

        similarImageAnchor.appendChild(similarImage);
        similarImageDiv.appendChild(similarImageAnchor);
        similarButtonDivDivDiv.appendChild(similarImageDiv);

        var similarButtonDivBtn = document.createElement('div');
        similarButtonDivBtn.classList.add('d-flex', 'justify-content-center', 'mb-2');
        var similarButton = document.createElement('a');
        similarButton.href = 'noticias?nid=' + imageSimNids[i];
        similarButton.classList.add('fs-5','font-oswald','link','text-dark','link-underline-danger','link-underline-opacity-25', 'link-underline-opacity-100-hover');
        similarButton.innerHTML = '<span class="">' + imageSimNews[i]  + '</span>'
        similarButtonDivBtn.appendChild(similarButton);
        similarButtonDivDivDiv.appendChild(similarButtonDivBtn);
        similarButtonDivDiv.appendChild(similarButtonDivDivDiv);
        similarButtonDiv.appendChild(similarButtonDivDiv);
        similarDiv.appendChild(similarButtonDiv);
    }
    similarDivMain.appendChild(similarDiv);
}

// using the esc triggers the close query modal
if (document.getElementById('imageModal')) {
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        closeImageModal();
    }
});
}


function closeImageModal() {
    var modal = document.getElementById('imageModal');
    modal.style.display = "none"; // Hide the modal
}

// to download capas
function downloadImageIndex() {
    var date = document.getElementById('dateCapaModal').innerText;
    var url = "https://arquivonc.ubi.pt/arquivonc/static/img/capas/"+ date +".jpg";
    var filename = url.substring(url.lastIndexOf("/") + 1);

    var current_year = new Date().getFullYear();
    var title_string = ""

    var years_ago = current_year - parseInt(date.substring(0, 4));
    title_string = "Antigamente era assim! Há " + years_ago + " anos, nesta semana, a capa do jornal Notícias da Covilhã (partilhado através do https://arquivonc.ubi.pt)."

    var xhr = new XMLHttpRequest();
    xhr.responseType = 'blob';
    xhr.onload = function() {
        var blob = xhr.response;

        const shareData = {
            files: [new File([blob], filename, { type: blob.type })],
            title: title_string,
            text: title_string
        };

        // Check if Web Share API is available
        if (navigator.share) {
            navigator.share(shareData)
                .catch(error => {
                    if (error.name === 'AbortError') {
                        return;
                    }
                    // If sharing fails, download the image
                    var a = document.createElement('a');
                    a.href = window.URL.createObjectURL(blob);
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                });
        } else {
            // If Web Share API is not available, download the image
            var a = document.createElement('a');
            a.href = window.URL.createObjectURL(blob);
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    };
    xhr.open('GET', url);
    xhr.send();
}

function downloadImage() {
    var date = document.getElementById('dateCapaModal').innerText;
    var url = "https://arquivonc.ubi.pt/arquivonc/static/img/capas/"+ date +".jpg";
    var filename = url.substring(url.lastIndexOf("/") + 1);

    var current_year = new Date().getFullYear();
    var title_string = ""

    var month_list_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    var month_to_string = month_list_pt[parseInt(date.substring(5, 7)) - 1]

    var date_day = parseInt(date.substring(8, 10))

    var years_ago = current_year - parseInt(date.substring(0, 4));

    title_string = "Há " + years_ago + " anos, no dia " + date_day + " de " + month_to_string  + ", esta era a capa do jornal Notícias da Covilhã (partilhado através do https://arquivonc.ubi.pt)."

    var xhr = new XMLHttpRequest();
    xhr.responseType = 'blob';
    xhr.onload = function() {
        var blob = xhr.response;

        const shareData = {
            files: [new File([blob], filename, { type: blob.type })],
            title: title_string,
            text: title_string
        };

        // Check if Web Share API is available
        if (navigator.share) {
            navigator.share(shareData)
                .catch(error => {
                    if (error.name === 'AbortError') {
                        return;
                    }
                    // If sharing fails, download the image
                    var a = document.createElement('a');
                    a.href = window.URL.createObjectURL(blob);
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                });
        } else {
            // If Web Share API is not available, download the image
            var a = document.createElement('a');
            a.href = window.URL.createObjectURL(blob);
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    };
    xhr.open('GET', url);
    xhr.send();
}


function openCapaModal(capaUrl, capaDate) {
    var modal = document.getElementById('capaModal');
    var modalCapa = document.getElementById('capaCapaModal');
    var dateText = document.getElementById('dateCapaModal');
    var shareCapa = document.getElementById('shareCapaModal');
    // var snippetContent = document.getElementById('snippetImageModal');

    modal.style.display = "block";
    modalCapa.src = capaUrl;
    // console.log(capaDate);
    dateText.textContent = capaDate;
    // snippetContent.innerHTML = imageSnippet + "...";
}


function closeCapaModal() {
    var modal = document.getElementById('capaModal');
    modal.style.display = "none"; // Hide the modal
}
function shareCapaOnSocial(typesocial) {
    var date = document.getElementById('dateCapaModal').innerText;
    var url = "https://arquivonc.ubi.pt/arquivonc/static/img/capas/" + date + ".jpg";
    var filename = url.substring(url.lastIndexOf("/") + 1);

    var current_year = new Date().getFullYear();
    var title_string = "";

    var month_list_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    var month_to_string = month_list_pt[parseInt(date.substring(5, 7)) - 1];

    var date_day = parseInt(date.substring(8, 10));

    var years_ago = current_year - parseInt(date.substring(0, 4));
    
    title_string = "Há " + years_ago + " anos, no dia " + date_day + " de " + month_to_string + ", esta era a capa do jornal Notícias da Covilhã (partilhado através do https://arquivonc.ubi.pt).";

    var xhr = new XMLHttpRequest();
    xhr.responseType = 'blob';
    xhr.onload = function () {
        var blob = xhr.response;

        if (navigator.share) {
            const shareData = {
                files: [new File([blob], filename, { type: blob.type })],
                title: title_string,
                text: title_string
            };

            navigator.share(shareData)
                .catch(error => {
                    handleSharingError(error, typesocial, url, blob, filename, title_string, date);
                });
        } else {
            handleSharingError(null, typesocial, url, blob, filename, title_string, date);
        }
    };
    xhr.open('GET', url);
    xhr.send();
}

function handleSharingError(error, typesocial, url, blob, filename, title_string, date) {
    if (error && error.name === 'AbortError') {
        return;
    }

    switch (typesocial) {
        case "facebook":
            openFacebookShareDialog(url);
            break;
        case "twitter":
            shareOnTwitterIndex(title_string, title_string, date, url);
            break;
        case "linkedin":
            openLinkedInShareDialog(url);
            break;
        case "whatsapp":
            openWhatsappShareDialogIndex(date, title_string, title_string, url);
            break;
        case "email":
            shareViaEmail(filename, blob, title_string);
            break;
        default:
            downloadImage(blob, filename);
            break;
    }
}

function shareViaEmail(filename, blob, title_string) {
    var formData = new FormData();
    formData.append('attachment', blob, filename);

    var emailLink = 'mailto:?subject=' + encodeURIComponent(title_string) + '&body=' + encodeURIComponent(title_string);
    emailLink += '&attachments=' + encodeURIComponent(formData);

    window.location.href = emailLink;
}


function downloadImage(blob, filename) {
    var a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function openFacebookShareDialog(url) {
var facebookUrl = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url);
window.open(facebookUrl, 'facebook-share-dialog', 'width=626,height=436');
}


function shareOnTwitterIndex(text, title, date, url) {
    string_url = date + ":%0A" + text + "%0A %0A" + "Partilhado através do ArquivoNC.";
    window.open('http://twitter.com/intent/tweet?url=' + encodeURIComponent(url) + '&text=' + string_url, 'threads-share-dialog', 'width=626,height=436');
}

function shareOnLinkedIn(summary, title, date) {
const shareData = {
    title: title,
    text: date + "\n" + summary,
    url: url,
};

// Check if Web Share API is available
if (navigator.share) {
    navigator.share(shareData)
        .catch(error => {
            // If sharing via Web Share API fails, open LinkedIn share dialog in a new window
            openLinkedInShareDialog(url);
        });
} else {
    // If Web Share API is not available, open LinkedIn share dialog in a new window
    openLinkedInShareDialog(url);
}
}

function openLinkedInShareDialog(url) {
var linkedInUrl = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url);
window.open(linkedInUrl, 'linkedin-share-dialog', 'width=626,height=436');
}
function shareOnThreads() {
    window.open('https://www.threads.net/share?url=' + encodeURIComponent(url), 'threads-share-dialog', 'width=626,height=436');
}

function shareOnWhatsapp(date, title, text) {
const shareData = {
    text: date + ":\n" + title + "\n\n" + "Continue a leitura: " + url + "\n\n" + "Partilhado através do ArquivoNC."
};

if (navigator.share) {
    navigator.share(shareData)
        .catch(error => {
            openWhatsappShareDialogIndex(date, title, text, url);
        });
} else {
    openWhatsappShareDialogIndex(date, title, text, url);
}
}

function openWhatsappShareDialogIndex(date, title, text, url) {
var stringUrl = date + ":%0A" + title;
var whatsappUrl = 'whatsapp://send/?text=' + stringUrl;
window.open(whatsappUrl, 'whatsapp-share-dialog', 'width=626,height=436');
}

window.addEventListener("click", function(event) {
    var modal = document.getElementById('myModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
});

//////////////////////
//////////////////////
// HANDLE ERRORS
//////////////////////
///////////////////////////
// SINGLE NEWS IMAGE ERROR
///////////////////////////
function handleImageErrorANews(image) {
    // Hide the image by setting its display property to 'none'
    // image.style.display = 'none';
    image.src = 'static/img/nc_logo_dark.png';
    image.style.scale = '0.6';
    var parentDiv = image.parentElement;
                if (parentDiv) {
                    parentDiv.classList.add('bg-light')
                    parentDiv.classList.add('border')
                    parentDiv.classList.add('border-1')
                    parentDiv.classList.add('border-dark')
                }
}

function handleImageErrorBNews(image) {
    // Hide the image by setting its display property to 'none'
    // image.style.display = 'none';
    image.src = 'static/img/nc_logo_dark.png';
    image.style.scale = '0.6';
    var parentDiv = image;
                if (parentDiv) {
                    parentDiv.classList.add('bg-light')
                    parentDiv.classList.add('border')
                    parentDiv.classList.add('border-1')
                    parentDiv.classList.add('border-dark')
                }
}

function handleImageErrorNews(image) {
    // Hide the image by setting its display property to 'none'
    image.style.display = 'none';
    var parentDiv = image.parentElement;
                if (parentDiv) {
                    parentDiv.style.display = 'none';
                }
}

window.addEventListener('load', () => {
    // Get all images with class "img-news"
    var images = document.querySelectorAll('.img-news');

    // Iterate through each image
    images.forEach(function(image) {
        // Check if the image has loaded
        image.addEventListener('load', function() {
            // Check if src attribute is empty
            if (!image.getAttribute('src')) {
                handleImageErrorNews(image)
            }
        });
    });
});

function smoothScroll(amount) {
    let currentScroll = slider.scrollLeft;
    const targetScroll = currentScroll + amount;
    
    function scrollAnimation() {
        if ((amount > 0 && currentScroll < targetScroll) || (amount < 0 && currentScroll > targetScroll)) {
            currentScroll += step * Math.sign(amount);
            slider.scrollLeft = currentScroll;
            requestAnimationFrame(scrollAnimation);
        }
    }
    
    scrollAnimation();
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}


// DEFAUTL SCROLL OPTIONS
// Scroll to specific values
// scrollTo is the same
// window.scroll({
//     top: 2500, 
//     left: 0, 
//     behavior: 'smooth'
//   });
  
//   // Scroll certain amounts from current position 
//   window.scrollBy({ 
//     top: 100, // could be negative value
//     left: 0, 
//     behavior: 'smooth' 
//   });
  

////////////////
// CLOSE MENU //
////////////////
// function closeMenu() {
//     var closeButton = document.querySelector('[data-bs-dismiss="modal"]');
//     closeButton.click();
// }


function shareCapaFacebook() {
    var date = document.getElementById('dateCapaModal').innerText;
    var url = "https://arquivonc.ubi.pt/arquivonc/static/img/capas/"+ date +".jpg";
    var current_year = new Date().getFullYear();
    var title_string = ""

    var month_list_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    var month_to_string = month_list_pt[parseInt(date.substring(5, 7)) - 1]

    var date_day = parseInt(date.substring(8, 10))

    var years_ago = current_year - parseInt(date.substring(0, 4));

    title_string = "Há " + years_ago + " anos, no dia " + date_day + " de " + month_to_string  + ", esta era a capa do jornal Notícias da Covilhã (partilhado através do https://arquivonc.ubi.pt)."

    var shareData = {
        title: title_string,
        text: title_string,
        url: url,
    }

    navigator.share(shareData)
        .catch(error => {
            if (error.name === 'AbortError') {
                return;
            }
            // If sharing fails, opens facebook and shares it there
            var facebookUrl = 'https://www.facebook.com/sharer/sharer.php?u=' + url;
            window.open(facebookUrl, '_blank');
        });
}