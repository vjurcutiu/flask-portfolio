import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.utils import secure_filename
import os
from PIL import Image

bp = Blueprint('converter', __name__, url_prefix='/converter')


@bp.route('/', methods=['POST'])
def hello():    
    return render_template("converter.html")

@bp.route("/convert", methods=["POST", "GET"])
def convert():           
    current_app.config['UPLOAD_FOLDER'] = 'portfolio/static/images/'
    if request.method == "POST":
        file = request.files["image"]
        format = request.form.get("format")
        outputimage, x = file.filename.split('.')
        outputimage = outputimage + "." + format
        file.save((os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename))))
        with Image.open(file) as image:
            image.convert('RGB').save( outputimage)
            path = current_app.config['UPLOAD_FOLDER'] + outputimage 
            os.rename(outputimage, path )
            filepath = 'images/' + outputimage
            image_url = url_for('static', filename=filepath)
        return render_template("convert.html", image_url=image_url)
    return redirect("/")
    
    