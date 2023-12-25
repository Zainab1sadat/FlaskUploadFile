from io import BytesIO
from flask import Flask ,render_template ,request ,url_for ,send_file
from werkzeug.utils import secure_filename
from db import db_init ,db
from models import Upload



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db_init(app)


@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload' , methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "ERR_NO_FILE_SPECIFIED"

        file =  request.files['file']

        if file.filename == '':
            return "ERR_NO_FILE_SPECIFIED"

        filename = secure_filename(file.filename)

        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded : {file.filename}'
    return render_template('upload.html')

@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    if upload:
        return "dowloaded".send_file(BytesIO(upload.data), download_name=upload.filename , as_attachment=True)
    return "No Uploaded image"
