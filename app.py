from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
from flask_cors import CORS


# Configuration
app = Flask(__name__)

CORS(app)  # This will allow all domains to access your backend
app.secret_key = os.urandom(24)  # Secret key for session management
ADMIN_PASSWORD = 'admin'  # Replace with your desired admin password

# Routes
@app.route('/')
def public_home():
    return render_template('public/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_home'))
        else:
            return "Invalid password", 403
    return render_template('admin/login.html')

@app.route('/logout')
def logout():
    session['admin_logged_in'] = False
    return redirect(url_for('public_home'))

@app.route('/admin')
def admin_home():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    return render_template('admin/index.html')

@app.route('/film')
def get_film():
    film_id = request.args.get('id', type=int)
    if film_id is None:
        return {"error": "Film ID is required"}, 400
    
    with open('database/film.json') as f:
        films = json.load(f)
    
    film = next((film for film in films if film['id'] == film_id), None)
    if film is not None:
        return film
    else:
        return {"error": "Film not found"}, 404

@app.route('/read_film')
def read_film():
    with open('database/film.json') as f:
        films = json.load(f)
        
    for film in films:
        film["locandina"] = url_for('static', filename=f'images/films/{film["locandina"]}', _external=True)
        
                
    return jsonify(films)

# Main entry point
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode, host='0.0.0.0')