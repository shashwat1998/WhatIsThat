import os
import detect
from io import BytesIO

from flask import Flask, render_template, request, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    image_data = db.Column(db.LargeBinary)
    results = db.relationship('ObjectDetected',backref='image')


class ObjectDetected(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(20))
    object_probability = db.Column(db.Float)
    image_id = db.Column(db.Integer, db.ForeignKey('file_contents.id'))


@app.route("/")
def index():
    return render_template("upload_image.html")


@app.route("/upload", methods=['POST'])
def upload_image_method():
    count = 0
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for upload_file in request.files.getlist("file"):
        filename = upload_file.filename
        destination = "".join([target, filename])
        print(destination)
        upload_file.save(destination)
        binary_data = open(destination, 'rb').read()
        new_file = FileContents(filename=filename, image_data=binary_data)
        db.session.add(new_file)
        db.session.commit()
        list_returned = detect.classify(filename)
        for i in range(5):
            new_data = ObjectDetected(object_name=list_returned[0][i][1],
                                      object_probability=list_returned[0][i][2],
                                      image=new_file)
            db.session.add(new_data)
            db.session.commit()
        count += 1

    return render_template("complete.html", num=count)


@app.route('/gallery')
def get_gallery():
    file_data = FileContents.query.all()
    return render_template('gallery.html', table_list=file_data)


@app.route('/upload/<image_id>')
def send_image(image_id):
    file_data = FileContents.query.filter_by(id=image_id).first()
    print(type(file_data))
    return send_file(BytesIO(file_data.image_data), attachment_filename=file_data.filename, mimetype='image/jpeg')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
