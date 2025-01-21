ajax = new XMLHttpRequest();
ajax.open("GET", "http://localhost:5000/read_film", true);
ajax.send();

ajax.onreadystatechange = function() {
    if (ajax.readyState== 4 && ajax.status == 200) {
        var response = JSON.parse(ajax.responseText);

        
        for (var i = 0; i < response.length; i++) {
            var film = response[i];

            var film = document.createElement("div");
            film.className = "film";

            var banner = document.createElement("div");
            banner.className = "banner";

            var img = document.createElement("img");

            var link_locandina = "{{ url_for('static', filename='images/films/"+film.locandina+"') }}"

            img.src = link_locandina;
            banner.appendChild(img);

            film.appendChild(banner);

            var span = document.createElement("span");
            span.innerHTML = response[i].titolo;
            film.appendChild(span);

            document.querySelector(".container").appendChild(film);

        }
    }
}