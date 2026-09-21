const apiKey =  "032c86cffdaeb54171add0568fd5309b";
const page = Math.floor(Math.random() * 10) + 1;
const poster = document.createElement("img");
const colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"];
let colorIndex = 0;
poster.id = "movie-poster";
poster.alt = "Movie poster";
poster.hidden = true;
document.querySelector(".poster-frame").prepend(poster);
fetch(`https://api.themoviedb.org/3/discover/movie?api_key=${apiKey}&page=${page}`)    
    .then(response => response.json())
    .then(data => {
        const movies = data.results;
        console.log(movies);
    const movieButton = document.querySelector("#pick-movie");
        movieButton.onclick = function (){
            let a = movies;
            let i = Math.floor(Math.random() * a.length);
            let r = a[i];
            document.querySelector("#movie-title").textContent = r.title;
            document.querySelector("#movie-description").textContent = r.overview;
            document.querySelector(".poster-frame").classList.add("has-movie");
            document.querySelector("#movie-title").style.color = colors[colorIndex];
            colorIndex = (colorIndex + 1) % colors.length;
            poster.src = "https://image.tmdb.org/t/p/w500" + r.poster_path;
            poster.alt = r.title + " poster";
            poster.hidden = false;
            console.log(r);
        };    
    })
    .catch(error => {
        console.error("Could not load movies:", error);
    });
    