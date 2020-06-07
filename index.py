import os

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from demo import driver

app = Flask(__name__)


@app.route("/", methods=['POST'])
def startProcess():
    try:
        src = request.files['source']
    except:
        return "Source is empty"

    src.save(os.path.join("input/", secure_filename(src.filename)))

    try:
        driver()
        os.remove(os.path.join("input/", secure_filename(src.filename)))
        name = os.path.splitext(secure_filename(src.filename))[0]
        return send_file(os.path.join("output/", name, ".obj"),
                         attachment_filename=secure_filename(src.filename) + ".obj")
    except:
        return "Some error occurred while processing", 400


@app.route("/", methods=['GET'])
def index():
    try:
        return render_template('index.html')
    except:
        return "Some error occurred while trying to fetch data"


if __name__ == "__main__":
    app.run(debug=True)
