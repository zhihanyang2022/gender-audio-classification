import os
from flask import Flask, flash, request, redirect, url_for
app = Flask(__name__)
app.secret_key = "super secret key"

UPLOAD_FOLDER = '/home/yangz2/projects/gender_audio_classification/site/wav'
ALLOWED_EXTENSIONS = {'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def header():
    return """
    <h1 style="text-align:center;">The Gender Audio Classification Project</h1>
    <p style="text-align:center;"><u>Author</u>: Zhihan Yang @ Carleton College</p>
    <p style="text-align:center;"><u>Date</u>: March 7 2020</p>
    <img style="display: block; margin-left: auto; margin-right: auto; width: 50%;" src="static/ad.png" border="2">
    """

def instructions():
    return """
    <p style="text-align:center;"> This minimalist site allows you to upload your own WAV and get a gender classification together with the outputs of the intermediate preprocessing steps. </p>
    <p style="text-align:center;">
    Before we start, complete steps 1 to 3 in <a href="https://github.com/zhihanyang2022/gender_audio_classification/blob/master/README.md#record-and-classify-your-own-voice-using-this-project" target='_blank'> record and classify your own voice using this project</a> to record a valid WAV for input.
    </p>
    <p style="text-align:center;"> If you don't want to record your own WAV, you can download an example WAV from <a href='https://github.com/zhihanyang2022/gender_audio_classification/tree/master/nbs/my_wavs' target='_blank'>here</a>.
    <p style="text-align:center;">Upload a valid WAV: </p>
    """

def see_results():
    return """
    <p style="text-align:center;">After you've hit "Upload", click this button to see the classification:</p>
    <form style="text-align:center;" action="/process" method="post">
        <button style="width:200px">Let the model process my WAV.</button>
    </form>
    """

def promote_this_project():
    
    with open('./log/times_visited.txt', 'r') as txt_f:
        texts = txt_f.readlines()
    
    new_times_visited = int(texts[0].rstrip()) + 1

    with open('./log/times_visited.txt', 'w') as txt_f:
        txt_f.write(str(new_times_visited))
    
    return f"""
    <p style="text-align:center;"> 
    For code and/or more information on the training data, please visit <a href='https://github.com/zhihanyang2022/gender_audio_classification' target='_blank'> Gender Audio Classification</a> @ Github; don't forget to give it a star!
    </p>
    <p style="text-align:center;"> This site has been visited {new_times_visited} times since March 2020. </p>
    """

@app.route('/process', methods=['GET', 'POST'])
def process(x=None, y=None):
    # pseudo-code
    # 1. load WAV
    # 2. preprocess WAV into MFC
    # 3. load model
    # 4. get classification confidence for each class
    # last. clean up wav folder and mfc folder
    return f"""
    {header()}
    File uploaded successfully.
    <img src="/static/bear.png" alt="Italian Trulli">
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
    <hr>
    {instructions()}
    <form style="text-align:center;" method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    {see_results()}
    <hr>
    {promote_this_project()}
    '''

@app.route('/', methods=['GET', 'POST'])
def upload_file2():
    return upload_file()

@app.route("/about")
def about():
    return "<h1>About page</h1>"
