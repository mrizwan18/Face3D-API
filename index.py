import os

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')
if not os.path.exists(os.path.join(app.instance_path, 'uploads')):
    os.makedirs(os.path.join(app.instance_path, 'uploads'))


@app.route("/", methods=['POST'])
def startProcess():
    try:
        src = request.files['source']
        src.save(os.path.join(app.instance_path,
                              'uploads/', secure_filename(src.filename)))
    except:
        return "Source is empty"

    try:
        print("OK")
        # driver()
    except:
        return "Some error occurred while processing", 400

    try:
        os.remove(os.path.join(app.instance_path,
                               'uploads/', secure_filename(src.filename)))
        name = os.path.splitext(secure_filename(src.filename))[0]
        return send_file(os.path.join(app.instance_path,
                                      'uploads/', name, ".obj"),
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
