var index = 1;  
displaySlides(index);  

function afterSlide(n) {  
    displaySlides(index += n);  
}  

function currentSlide(n) {  
    displaySlides(index = n);  
}  

function beforeSlide(n) {
    displaySlides(index -= n )
}


function displaySlides(n) {  
    var i;  
    var slides = document.getElementsByClassName("showSlide");  
    if (n > slides.length) { index = 1 }  
    if (n < 1) { index = slides.length }  
    for (i = 0; i < slides.length; i++) {  
        slides[i].style.display = "none";  
    }  
    slides[index - 1].style.display = "block";  
} 