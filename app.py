from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
from flask_cors import CORS
import uuid

app = Flask(__name__)

CORS(app)  # La parte JS riesce a comunicare con PY
app.secret_key = os.urandom(24)  # Chiave segreta della sessione
ADMIN_PASSWORD = 'admin'  # Password admin.
app.template_folder = "html"

@app.before_request
def ensure_session_exists():
    if "admin_logged_in" not in session:
        session["admin_logged_in"] = False

# Routes
@app.route('/')
def public_home():
    if session["admin_logged_in"]:
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
    film_id = request.args.get('id', None)
    with open('database/film.json') as f:
        films = json.load(f)
    if film_id is not None:
        film = next((film for film in films if film['id'] == film_id), None)
        if film is not None:
            film["locandina"] = url_for('static', filename=f'images/films/{film["id"]}.jpg', _external=True)
            return jsonify(film)
        else:
            return {"error": "Film not found"}, 404
    else:
        for film in films:
            film["locandina"] = url_for('static', filename=f'images/films/{film["id"]}.jpg', _external=True)
        return jsonify(films) or []

@app.route('/create_film', methods=['POST'])
def write_film():
    
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    film_data = request.form.to_dict()
    film_id = film_data.get('id', None)

    if 'image' in request.form:
        image = request.files.get('image', "")
        if film_id is None or not film_id_exists(film_id):
            film_id = uuid.uuid4().hex
        image.save(os.path.join('static/images/films', f'{film_id}.jpg'))
        film_data['id'] = film_id

    with open('database/film.json', 'r+') as f:
        films = json.load(f)
        if film_id is None or not film_id_exists(film_id, films):
            film_id = uuid.uuid4().hex
            film_data['id'] = film_id
            films.append(film_data)
        else:
            for i, film in enumerate(films):
                if film['id'] == film_id:
                    films[i] = film_data
                    break
        f.seek(0)
        json.dump(films, f, indent=4)
        f.truncate()

    return redirect(url_for('admin_home'))

def film_id_exists(film_id, films=None):
    if films is None:
        with open('database/film.json') as f:
            films = json.load(f)
    return any(film['id'] == film_id for film in films)

@app.route("/film", methods=['GET'])
def render_film():
    if session["admin_logged_in"] == False:
        if request.args.get('id') is not None and request.args.get('id') != "":
            return render_template("public/film.html")
        else:
            return redirect(url_for("public_home"))
    else:
        return render_template("admin/film.html")

# Main entry point
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode, host='0.0.0.0')
