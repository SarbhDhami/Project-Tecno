ajax = new XMLHttpRequest();
ajax.open("GET", "http://localhost:5000/read_film", true);
ajax.send();

class FilmCard {
    constructor(film_obj) {
        this.film_obj = film_obj;
    }

    createCard() {
        var film = document.createElement("div");
        film.className = "film";

        var link = document.createElement("a");
        link.href = "/film?id=" + this.film_obj.id;
        

        var banner = document.createElement("div");
        banner.className = "banner";

        var img = document.createElement("img");
        img.src = this.film_obj.locandina;
        img.className = "locandina";
        banner.appendChild(img);

        link.appendChild(banner);

        var span = document.createElement("span");
        span.innerHTML = this.film_obj.titolo;
        link.appendChild(span);

        film.appendChild(link);

        return film;
    }
}

ajax.onreadystatechange = function() {
    if (ajax.readyState == 4 && ajax.status == 200) {
        var response = JSON.parse(ajax.responseText);

        for (var i = 0; i < response.length; i++) {
            var film_obj = response[i];
            var filmCard = new FilmCard(film_obj);
            var filmElement = filmCard.createCard();
            document.querySelector(".container").appendChild(filmElement);
        }
    }
}



var addFilmCard = document.createElement("div");
addFilmCard.className = "film add-film";

var addimg = document.createElement("img");
addimg.src = "http://localhost:5000//static/images/utils/plus.png";
addimg.className = "add-film-icon";
addFilmCard.appendChild(addimg);

addFilmCard.onclick = function() {
    window.location.href = "/crea_film";
};

document.querySelector(".container").appendChild(addFilmCard);
