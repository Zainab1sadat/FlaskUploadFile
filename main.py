from flask import Flask, Response, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson import ObjectId
import gridfs 
from flask_pymongo import PyMongo



app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['uploadfileflask']
fs = gridfs.GridFS(db)


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload' , methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error":"No file"}),400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error":"No file Selected"}),400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        fs_id = fs.put(file, filename=filename)
        return jsonify({"file_id": str(fs_id)})
    else:
        return jsonify({"error": "File type not allowed"}),400
    

    
@app.route('/retrive/<string:image_id>', methods=['GET'])
def get_uploads(image_id):
     # Convert the string _id to an ObjectId
    image_id = ObjectId(image_id)
    # get the image from GridFS by its ID
    file = fs.get(image_id)
     # Send the image data as a response
    return send_file(file, as_attachment=True, download_name=file.filename)
    # return Response(file.read(), mimetype=file.content_type)
   

if __name__ == '__main__':
    app.run(debug=True)