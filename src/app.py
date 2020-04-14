from flask import Flask, request, jsonify, abort, send_from_directory
from image_deallocator.file_tools import load_json

# this is how we initialize a flask application
app = Flask(__name__)


@app.route("/meta", methods=["GET"])
def get_image_meta():
    data = load_json("image_deallocator/meta/data.json")
    return jsonify(data)


@app.route("/meta/<id>", methods=["GET"])
def get_image_meta_id(id: int):
    try:
        id = int(id)
    except ValueError:
        abort(404)
    data = load_json("image_deallocator/meta/data.json")
    if id not in range(0, len(data)):
        abort(404)
    return jsonify(data[id])


@app.route('/upload', methods=['POST'])
def upload_file():
    # checking if the file is present or not.
    if 'file' not in request.files:
        return "No file found"
    file = request.files['file']
    # if file.ends
    file.save("image_deallocator/img/test.png")
    return "file successfully saved"


if __name__ == "__main__":
    # this is how we run the flask server, once the script is run
    app.run(host='0.0.0.0', threaded=True)