from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, SubmitField, HiddenField
from werkzeug.utils import secure_filename
import os
import time
from wtforms.validators import InputRequired

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
    goodjob = False

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
        # filter( tesseract, pdf, time)
        goodjob = True
        form.form_submitted.data = True
        # render_template('index.html', data=data)
        # return "File has been uploaded"

    return render_template('index.html', form=form, goodjob=goodjob)

if __name__ == '__main__':
    app.run(debug=True)