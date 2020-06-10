import os

from PIL import Image
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from demo import driver

app = Flask(__name__, static_url_path='/static')
if not os.path.exists(os.path.join(app.instance_path, 'uploads')):
    os.makedirs(os.path.join(app.instance_path, 'uploads'))


@app.route("/", methods=['POST'])
def startProcess():
    name = ""
    try:
        src = request.files['source']

        path = os.path.join(app.instance_path,
                            'uploads/', secure_filename(src.filename))
        src.save(path)

        image = Image.open(path)
        image.thumbnail((500, 500))
        image.save(path)

        name = os.path.splitext(secure_filename(src.filename))[0]
    except:
        return "Source is empty", 400

    try:
        status = driver(name)
        if status == -1:
            return "Some error occurred while setting args", 400
        elif status == -2:
            return "Some error occurred while calling main(parser)", 400
    except:
        return "Some error occurred while processing", 400

    try:
        os.remove(os.path.join(app.instance_path,
                               'uploads/', secure_filename(src.filename)))
        return send_file(os.path.join(app.instance_path,
                                      'uploads/', name + ".obj"),
                         attachment_filename=name + ".obj")
    except:
        return "Some error occurred while returning image", 418


@app.route("/", methods=['GET'])
def index():
    try:
        return render_template('index.html')
    except:
        return "Some error occurred while trying to fetch data"


if __name__ == "__main__":
    app.run(debug=True)
