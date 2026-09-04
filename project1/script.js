const image = document.querySelector('.hero-image');
const button = document.querySelector('#image-button');
let showingDeer = true;
button.onclick = function () {
    if (showingDeer === true) {
        image.src = 'images/elk.jpeg';
        showingDeer = false;
        button.textContent = 'See Deer';
        console.log(showingDeer);
    } else {
        image.src = 'images/deer.jpeg';
        showingDeer = true;
        button.textContent = 'See Elk';
        console.log(showingDeer);
    }
};