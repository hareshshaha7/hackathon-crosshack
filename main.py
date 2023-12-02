# This is a sample Python script.
import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

import langchain_processing

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

app = Flask(__name__)


@app.get("/")
def hello_world():
    return "Welcome to CrossHack APIs"


ALLOWED_EXTENSIONS = {'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post("/load_data")
def give_me_data():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'error': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'error': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os_path = os.path.join("data", filename)
        file.save(os_path)

        data = langchain_processing.load_file(os_path)
        # print(data)
        tokens = langchain_processing.split_data(data)
        # print(tokens)
        langchain_processing.store_data(tokens)

        os.remove(os_path)
        resp = jsonify({'error': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'error': 'Allowed file type is docx'})
        resp.status_code = 400
        return resp


@app.post("/get_reply")
def give_me_ans():
    if request.is_json:
        body = request.get_json()
        res = langchain_processing.get_answer(body["query"])
        print(res)
        return res

    resp = jsonify({'error': 'Request must be JSON'})
    resp.status_code = 415
    return resp
