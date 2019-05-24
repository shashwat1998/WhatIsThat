import os
from io import BytesIO

from flask import Flask, render_template, request, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    image_data =db.Column(db.LargeBinary)


@app.route("/")
def index():
    return render_template("upload_image.html")


@app.route("/upload", methods=['POST'])
def upload_image_method():
    for upload_file in request.files.getlist("file"):
        filename = upload_file.filename
        binary_data = upload_file.read()
        new_file = FileContents(filename=filename, image_data=binary_data)
        db.session.add(new_file)
    db.session.commit()
    return "success"


@app.route('/gallery')
def get_gallery():
    file_data = FileContents.query.all()
    image_list = os.listdir('./images')
    return render_template('gallery.html', table_list=file_data)


@app.route('/upload/<id>')
def send_image(id):
    print("hello image")
    file_data = FileContents.query.filter_by(id=id).first()
    print(type(file_data))
    return send_file(BytesIO(file_data.image_data), attachment_filename='cat.jpeg', mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(port=8080, debug=True)

