import os  
from flask import Flask, flash, redirect, render_template, request, session, url_for,send_file
# import our OCR function
from ocr_core import ocr_core

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):  
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# function to save text file
def txt(str):
    text_file = open('parsed_text.txt', 'w')
    text_file.write(str)
    text_file.close()
# route and function to handle the home page
@app.route('/')
def home_page():  
    return render_template('new_page.html')

# route and function to handle the upload page
@app.route('/', methods=['GET', 'POST'])
def upload_page():  
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('new_page.html', msg='No file chosen!')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('new_page.html', msg='No file chosen!')
        if file and allowed_file(file.filename):
            # Retrieve desired output format from form
            output_format=request.form.get('option')
            if output_format=='Select output format':
                return render_template('new_page.html', msg='Choose valid output format!')
            # call the OCR function on it
            extracted_text = ocr_core(file)
            if output_format=='JSON':
                return render_template('new_page.html', msg='JSON')
            elif output_format=='Plaintext':
                return render_template('new_page.html', msg='Text File')
            else:
                txt(extracted_text)
                path = 'parsed_text.txt'
                return send_file(path, as_attachment=True)
    elif request.method == 'GET':
        return render_template('new_page.html',msg='Hey yo')

if __name__ == "__main__":
  app.run(debug=True)