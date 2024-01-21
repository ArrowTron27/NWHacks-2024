from flask import Flask, render_template, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, SubmitField, HiddenField
from werkzeug.utils import secure_filename
import os
import time
from wtforms.validators import InputRequired

import lib.filter as filt
PATH = r"C:\Program Files\Tesseract-OCR/tesseract.exe"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'NWHacksLoser'
app.config['UPLOAD_FOLDER'] = 'static/files'

form_submitted = None

class UploadFileForm(FlaskForm):
    # file = FileField("File", validators=[
    #     FileRequired(),
    #     FileAllowed(['pdf'], 'Only PDF files are allowed!')
    #     ])
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
    form_submitted = HiddenField("form_submitted")


@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])

def home():
    form = UploadFileForm()

    passed = 0

    if form.validate_on_submit():
        # Grab the file
        file = form.file.data 

        # Generate a unique filename based on the current time
        current_time = time.strftime("%Y%m%d%H%M%S")
        _, file_extension = os.path.splitext(file.filename)
        filename = f"{current_time}{file_extension}"

        # Save the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename))
        # Call douglases function
        # function would return something, the goodjob what should be returned

        # This is for Windows
        passed = int(filt.filter(PATH,1, poppler_path=r"../poppler-23.11.0/Library/bin"))
        passed = 0
        # passed = 1
        # This is for Linux
        # filt.filter(PATH, 10, poppler_path=r"../poppler-23.11.0/Library/bin")
        # filter( tesseract, pdf, time)
        form.form_submitted.data = True

    return render_template('index.html', form=form, passed=passed)

if __name__ == '__main__':
    app.run(debug=True)