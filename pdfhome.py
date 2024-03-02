from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image

# Specify the Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './media'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitImage/', methods=['POST'])
def submitImage():
    if 'ocrImage' not in request.files:
        return render_template('error.html', message='No file part')

    image = request.files['ocrImage']

    if image.filename == '':
        return render_template('error.html', message='No selected file')

    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        text_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.txt')
        with open(text_file_path, 'w') as text_file:
            text_file.write(text)

        return render_template('textFile.html', text=text, filename=filename)

    return render_template('error.html', message='Error processing image')

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
