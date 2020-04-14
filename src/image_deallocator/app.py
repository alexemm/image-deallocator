from flask import Flask, request, jsonify, abort, send_from_directory
from file_tools import load_json

from controller import save_file_from_request

# this is how we initialize a flask application
app = Flask(__name__, static_url_path='')


@app.route("/meta", methods=["GET"])
def get_image_meta():
    data = load_json("meta/data.json")
    return jsonify(data)


@app.route("/meta/<id>", methods=["GET"])
def get_image_meta_id(id: int):
    try:
        id = int(id)
    except ValueError:
        abort(404)
    data = load_json("meta/data.json")
    if id not in range(0, len(data)):
        abort(404)
    return jsonify(data[id])


@app.route('/img/<path:path>')
def send_original_img(path):
    return send_from_directory('img', path)


@app.route('/new_img/<path:path>')
def send_new_img(path):
    return send_from_directory('new_img', path)


@app.route('/upload', methods=['POST'])
def upload_file():
    # checking if the file is present or not.
    if 'file' not in request.files or 'name' not in request.form.keys():
        return "No file found"
    name = request.form['name']
    file = request.files['file']
    save_file_from_request(name, file)
    return "file successfully saved"


if __name__ == "__main__":
    # this is how we run the flask server, once the script is run
    app.run(host='0.0.0.0', threaded=True)