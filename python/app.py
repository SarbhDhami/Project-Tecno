from flask import Flask, render_template
import os

import os
from flask import Flask

template_dir = os.path.abspath('../html')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def public_home():
    return render_template('public/index.html')

@app.route('/admin')
def admin_home():
    return render_template('admin/index.html')


@app.route('read_film')
def read_film():
    
    
    
    return ""



if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode, host='0.0.0.0')