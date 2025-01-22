
function getIdFromUrl() {
    var urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

var filmId = getIdFromUrl();

ajax = new XMLHttpRequest();
ajax.open("GET", "http://localhost:5000/read_film?id="+filmId, true);
ajax.send();

ajax.onreadystatechange = function() {
    if (ajax.readyState== 4 && ajax.status == 200) {
        var response = JSON.parse(ajax.responseText);

        var container = document.getElementsByClassName('container')[0];



        var iframe = document.createElement('iframe');
        
        iframe.src = response.trailer;
        iframe.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
        iframe.referrerPolicy="strict-origin-when-cross-origin";
        iframe.allowfullscreen = true;
        container.appendChild(iframe);
        
        var row = document.createElement('div');
        row.className = "row";


        var banner = document.createElement('img');
        banner.src = response.locandina;
        banner.className = "banner";

        var bcol = document.createElement('div');
        bcol.appendChild(banner);
        bcol.className="bcol";
        row.appendChild(bcol);

        var col = document.createElement('div');
        col.className = "col";
        var details = [
            { label: "Titolo", value: response.titolo },
            { label: "Anno", value: response.anno },
            { label: "Trama", value: response.trama},
            { label: "Regista", value: response.regista },
            { label: "Attori", value: response.attori },
            { label: "Genere", value: response.genere },
            { label: "Prezzo", value: response.prezzo }
        ];

        details.forEach(function(detail) {
            var p = document.createElement('p');
            p.innerHTML = "<strong>" + detail.label + ":</strong> " + detail.value;
            col.appendChild(p);
        });
        row.appendChild(col);
        
        container.appendChild(row);



        
    }
}

        
