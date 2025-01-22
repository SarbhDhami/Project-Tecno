from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
from flask_cors import CORS

app = Flask(__name__)

CORS(app)  # La parte JS riesce a comunicare con PY
app.secret_key = os.urandom(24)  # Chiave segreta della sessione
ADMIN_PASSWORD = 'admin'  # Password admin. 
app.template_folder = "html"

# Routes
@app.route('/')
def public_home():
    if "admin_logged_in" not in session:
        session["admin_logged_in"] = False
        
    if session["admin_logged_in"] == True:
        return redirect(url_for("admin_home"))
    return render_template('public/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_home'))
        else:
            return "Invalid password ", 403
    return render_template('login.html')



@app.route('/logout')
def logout():
    session['admin_logged_in'] = False
    return redirect(url_for('public_home'))

@app.route('/admin')
def admin_home():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    return render_template('admin/index.html')

@app.route('/read_film', methods=['GET'])
def read_film():
    #Prendo la variabile id dall'url
    film_id = request.args.get('id', None)
    
    #Converto il json in un dizionario python
    with open('database/film.json') as f:
        films = json.load(f)
        
    #Se è presente un id nell'url provo a cercarlo tra tutti i film 
    if film_id is not None:
        
        film = next((film for film in films if film['id'] == film_id), None)
        if film is not None:
            film["locandina"] = url_for('static', filename=f'images/films/{film["id"]}.jpg', _external=True)
            return jsonify(film)
        else:
            return {"error": "Film not found"}, 404
    #Se non è presente un id nell'url ritorno tutti i film
    else:    
        for film in films:
            film["locandina"] = url_for('static', filename=f'images/films/{film["id"]}.jpg', _external=True)
                    
        return jsonify(films) or []

@app.route('/add_film', methods=['POST'])
def write_film():
    #code
    #obbiettivo: creare un film con dei dati passati da una form html. l'id va generato con la funzione 'uuid.uuid4().hex'
    #queesta istruzinoe è eseguibile solo se in modalità admin.
    
    
    return ""

@app.route('/update_film', methods=['POST'])
def update_film():
    #code
    #obbiettivo: come il create MA HA GIA' BISOGNO DI UN ID PER CERCARE IL FILM CORRETTO
    #queesta istruzinoe è eseguibile solo se in modalità admin.
    return ""

# @app.errorhandler(404)
# def not_found():
#     #gestire reindirizzamento alla pagine "404.html"
#     return ""


@app.route("/film", methods=['GET'])
def render_film():
    return render_template("public/film.html")


# Main entry point
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode, host='0.0.0.0')