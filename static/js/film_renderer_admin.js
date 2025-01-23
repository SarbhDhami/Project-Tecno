
var addFilmCard = document.createElement("div");
addFilmCard.className = "film add-film";

var addimg = document.createElement("img");
addimg.src = "http://localhost:5000//static/images/utils/plus.png";
addimg.className = "add-film-icon";
addFilmCard.appendChild(addimg);

addFilmCard.onclick = function() {
    window.location.href = "/film";
};

document.querySelector(".container").appendChild(addFilmCard);
