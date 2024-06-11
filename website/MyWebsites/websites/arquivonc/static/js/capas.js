// MODAL CAPAS
// var modal = document.getElementById("myModal");
// var span = document.getElementsByClassName("close")[0];

// document.addEventListener("DOMContentLoaded", function() {

//     var img = document.getElementsByClassName("news-img");
//     var modalImg = document.getElementById("modal-img");
//     var modalCaption = document.getElementById("caption");
//     for (var i = 0; i < img.length; i++) {
//         img[i].onclick = function(){
//             modal.style.display = "block";
//             modalImg.src = this.src;
//             modalImg.alt = this.alt;
//             modalCaption.innerHTML = `<span class="text-light fw-normal d-inline-block md-title">${this.alt}</span>`;
//         }
//     }

// });

// window.addEventListener("click", function(event) {
//     if (event.target == modal) {
//         modal.style.display = "none";
//     }
//     if (event.target == span) {
//         modal.style.display = "none";
//     }
// });

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

// Wait for all resources to load
window.addEventListener('load', function() {
    hideLoader();
});