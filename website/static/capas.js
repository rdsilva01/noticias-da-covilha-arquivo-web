// MODAL CAPAS
var modal = document.getElementById("myModal");

document.addEventListener("DOMContentLoaded", function() {

    var img = document.getElementsByClassName("news-img");
    var modalImg = document.getElementById("modal-img");
    var modalCaption = document.getElementById("caption");
    for (var i = 0; i < img.length; i++) {
        img[i].onclick = function(){
            modal.style.display = "block";
            modalImg.src = this.src;
            modalImg.alt = this.alt;
            modalCaption.innerHTML = `<span class="text-light fw-normal d-inline-block md-title">${this.alt}</span>`;
        }
    }

});

window.addEventListener("click", function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
});