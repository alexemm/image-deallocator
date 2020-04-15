from typing import Dict

from flask import Flask, request, jsonify, abort, send_from_directory
from flask.wrappers import Response
from werkzeug.datastructures import FileStorage

from file_tools import load_json
from controller import save_file_from_request, execute_image_deallocation

# this is how we initialize a flask application
app: Flask = Flask(__name__, static_url_path='')
UPLOAD_FOLDER: str = "img/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/meta", methods=["GET"])
def get_image_meta() -> Response:
    """
    Returns information for all the names in json format
    :return: JSON object
    """
    data: Dict[str, any] = load_json("meta/data.json")
    return jsonify(data)


@app.route("/meta/<name>", methods=["GET"])
def get_image_meta_name(name: str) -> Response:
    """
    Returns information for all the entries based on the name in JSON format
    :param name: name of image (not filename)
    :return: JSON object
    """
    data: Dict[str, any] = load_json("meta/data.json")
    if id not in data.keys():
        abort(404)
    return jsonify(data[name])


@app.route('/img/<path:path>')
def send_original_img(path: str) -> Response:
    """
    Serves images on the 'img' path
    :param path: path to image
    :return: File from path
    """
    return send_from_directory('img', path)


@app.route('/new_img/<path:path>')
def send_new_img(path: str) -> Response:
    """
    Serves images on the 'new_img' path
    :param path: path to image
    :return: File from path
    """
    return send_from_directory('new_img', path)


@app.route('/upload', methods=['POST'])
def upload_file() -> str:
    """
    Uploads file from request with form in body with name as string, and file
    :return: Status, how the file upload went
    """
    # checking if the file is present or not.
    if 'file' not in request.files or 'name' not in request.form.keys():
        return "No file found"
    name: str = request.form['name']
    file: FileStorage = request.files['file']
    save_file_from_request(name, file)
    return "file successfully saved"


@app.route('/deallocate', methods=['POST'])
def trigger_image_deallocation() -> str:
    """
    Triggers image deallocation task
    :return: Status, how the task went
    """
    name: str = request.form['name']
    try:
        id: int = int(request.form['id'])
    except ValueError as e:
        print(e)
        abort(404)
    new_name: str = request.form['new_name']
    if 'axis' in request.form.keys():
        try:
            axis: int = int(request.form['axis'])
        except ValueError as e:
            axis: int = 0
    else:
        axis: int = 0
    return_value: bool = execute_image_deallocation(name, id, new_name, axis)
    if return_value:
        return "Task done"
    else:
        return "Task not done"


if __name__ == "__main__":
    # this is how we run the flask server, once the script is run
    app.run(host='0.0.0.0', threaded=True)