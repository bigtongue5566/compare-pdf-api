import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from lib import pdf_tool, opencv_img_diff
import uuid
import shutil

UPLOAD_FOLDER = 'uploads'
IMAGE_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/compare', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'first' not in request.files or 'second' not in request.files:
            return 'No first file or second file', 400
        first = request.files['first']
        second = request.files['second']
        password = request.form.get('password')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if first.filename == '' or second.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if first and allowed_file(first.filename) and second and allowed_file(second.filename):
            # first_filename = secure_filename(first.filename)
            # second_filename = secure_filename(second.filename)
            # hash_first_filename = uuid.uuid3(namespace, name)hashlib.sha256(os.path.split(first_filename)[0].encode('utf-8')).hexdigest() + os.path.split(first_filename)[1]
            # hash_second_filename = hashlib.sha256(os.path.split(second_filename)[0].encode('utf-8')).hexdigest() + os.path.split(second_filename)[1]
            # print(first_filename)
            first_filename = uuid.uuid4().hex
            second_filename = uuid.uuid4().hex
            first_file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], first_filename + os.path.splitext(first.filename)[1])
            second_file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], second_filename + os.path.splitext(second.filename)[1])
            first.save(first_file_path)
            second.save(second_file_path)
            first_output_dir = os.path.join(app.config['IMAGE_FOLDER'], first_filename)
            second_output_dir = os.path.join(app.config['IMAGE_FOLDER'], second_filename)

            first_paths = pdf_tool.pdf2png(
                first_file_path, first_output_dir, password=password)
            second_paths = pdf_tool.pdf2png(
                second_file_path, second_output_dir, password=password)

            page_rects = []

            for i in range(len(first_paths)):
                compare_result = opencv_img_diff.compare(
                    first_paths[i], second_paths[i])
                if len(compare_result) > 0:
                    page_rects.append({'page': i + 1, 'rects': compare_result})

            diff_filename = pdf_tool.draw_rects(
                second_file_path, page_rects, app.config["UPLOAD_FOLDER"])

            shutil.rmtree(first_output_dir)
            shutil.rmtree(second_output_dir)
            os.remove(first_file_path)
            os.remove(second_file_path)

            return redirect(url_for('download_file', name=diff_filename))

    return ''


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
