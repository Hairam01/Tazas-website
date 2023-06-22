var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  x[slideIndex-1].style.display = "block";  
}

var currentImageIndex = 0;
var images = document.getElementsByClassName('mySlides'); // Obtén todas las imágenes

function changeImage() {
    images[currentImageIndex].style.display = 'none'; // Oculta la imagen actual
    currentImageIndex = (currentImageIndex + 1) % images.length; // Cambia al índice de la siguiente imagen
    images[currentImageIndex].style.display = 'block'; // Muestra la siguiente imagen
}

setInterval(changeImage, 6000); // Cambia la imagen cada 3 segundos
