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
# PATH = r"/bin/tesseract"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'NWHacksLoser'
app.config['UPLOAD_FOLDER'] = 'static/files'

form_submitted = None

# Upload the file
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
    form_submitted = HiddenField("form_submitted")


@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])

def home():
    form = UploadFileForm()

    passed = 0

    # When the form is submitted
    if form.validate_on_submit():
        # Grab the file
        file = form.file.data 

        # Generate a unique filename based on the current time
        current_time = time.strftime("%Y%m%d%H%M%S")
        _, file_extension = os.path.splitext(file.filename)
        filename = f"{current_time}{file_extension}"

        # Save the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename))
        
        # Return the data from the passed resumes
        # This is for Windows
        passed = int(filt.filter(PATH,10, poppler_path=r"../poppler-23.11.0/Library/bin"))

        # This is for Linux
        # passed = int(filt.filter(PATH, 10))

        # Form as been submitted
        form.form_submitted.data = True

    # Return the rendered properties
    return render_template('index.html', form=form, passed=passed)

if __name__ == '__main__':
    app.run(debug=True)