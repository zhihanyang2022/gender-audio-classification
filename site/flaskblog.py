import os
from flask import Flask, flash, request, redirect, url_for
app = Flask(__name__)
app.secret_key = "super secret key"

UPLOAD_FOLDER = '/Users/yangzhihan/Desktop/projects/'
ALLOWED_EXTENSIONS = {'wav', 'png', 'jpg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def header():
    return f"""
    <h1 style="text-align:center;">The Gender Audio Classification Project</h1>
    <p style="text-align:center;"><u>Author</u>: Zhihan Yang @ Carleton College</p>
    <p style="text-align:center;"><u>Date</u>: March 7 2020</p>
    <hr>
    """


@app.route('/process', methods=['GET', 'POST'])
def process(x=None, y=None):
    return f"""
    {header()}
    File uploaded successfully.
    <img src="bear.png" alt="Italian Trulli">
    """

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = url_for('upload_file2', filename=filename)
            return redirect(url)
    return f'''
    {header()}
    <p style="text-align:center;">
        Before we start, complete steps 1 to 3 in
            <a href="https://github.com/zhihanyang2022/gender_audio_classification/blob/master/README.md#record-and-classify-your-own-voice-using-this-project">
                record and classify your own voice using this project</a> to record a valid WAV for input
    </p>
    <p style="text-align:center;">Upload your WAV: </p>
    <form style="text-align:center;" method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <p style="text-align:center;">Click this button to see the results:</p>
    <form style="text-align:center;" action="/process" method="post">
        <button style="width:200px">Let the model process my wav.</button>
    </form>
    <hr>
    '''

@app.route('/', methods=['GET', 'POST'])
def upload_file2():
    return upload_file()

@app.route("/about")
def about():
    return "<h1>About page</h1>"
