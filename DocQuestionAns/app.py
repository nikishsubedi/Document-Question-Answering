from flask import Flask, request, render_template, session
from docx2pdf import convert
from qans import answers
import os
import pdf2image
import random

app = Flask(__name__)
app.secret_key = ['abc123']
UPLOAD_FOLDER = 'Files'  # specify the folder where uploaded files will be stored
ALLOWED_EXTENSIONS = {'docx', 'pdf'}  # specify the allowed file extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('home.html')


def convert_to_image(filepath):
    files = list()
    extension = filepath.split('.')[1]
    random_number = random.randint(1, 1e5)
    if extension == 'pdf':
        images = pdf2image.convert_from_path(filepath, dpi=300)
    else:
        convert(filepath, f'{filepath}.pdf')
        images = pdf2image.convert_from_path(f'{filepath}.pdf', dpi=300)
    for i in range(len(images)):
        images[i].save(f'created_img/{random_number}_{i}.png')
        files.append(f'created_img/{random_number}_{i}.png')

    return files


@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        session['filepath'] = filepath
        return render_template('questions.html')
    else:
        return 'Invalid file type'


@app.route('/question', methods=['GET', 'POST'])
def get_QN():
    if request.method == 'POST':
        filepath = session.get('filepath')
        files = convert_to_image(filepath)
        question = request.form.get('question')
        answer = answers(question, files)
        return render_template('questions.html', answer=answer)


if __name__ == '__main__':
    app.run(debug=True)
