import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, send_from_directory
)
from werkzeug.utils import secure_filename
import os

bp = Blueprint('byon', __name__, url_prefix='/byon')

@bp.route('', methods=['POST'])
def navbar_data():       
    current_app.config['UPLOAD FOLDER'] = 'static/'
    nb_position = request.form.get('nb-position')    
    if nb_position == 'left':
        position_pass = 'justify-content-start'
    else:
        position_pass = 'justify-content-end'
    nb_bg_color = request.form.get('nb-bg-color')
    nb_text_color = request.form.get('nb-text-color')    
    nb_items = int(request.form.get('nb-items'))     
    if request.form['action'] =='Download':
        with open('portfolio/static/navbar_template.txt', 'r') as f:
                html_to_download = f.read()
                f.close()
        html_to_download = html_to_download.replace('/NB_POSITION/', position_pass)
        html_to_download = html_to_download.replace('/NB_TEXT_COLOR/', nb_text_color)
        html_to_download = html_to_download.replace('/NB_BG_COLOR/', nb_bg_color)
        html_to_download = html_to_download.split ('/SPLIT/')
        ini_string = html_to_download[0]        
        for n in range(nb_items):
            ini_string += html_to_download[1]
        ini_string +=html_to_download[2]
        path = os.path.join(current_app.root_path, current_app.config['UPLOAD FOLDER'])

        with open(path + 'navbar.html', 'w') as f:
            f.write(ini_string)
            f.close


        return send_from_directory(path, 'navbar.html', as_attachment = True)
    
    

    


            