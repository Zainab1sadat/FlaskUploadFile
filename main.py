from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson import ObjectId
import gridfs 



app = Flask(__name__)
# MongoClient object to connect to MongoDB server
client = MongoClient('mongodb://localhost:27017/')
#Access to database
db = client['uploadfileflask']
#Gridfs object for database
fs = gridfs.GridFS(db)


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload' , methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error":"No file"}),201
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error":"No file Selected"}),400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Store file in Gridfs
        fs_id = fs.put(file, filename=filename)
        return jsonify({"file_id": str(fs_id)})
    else:
        return jsonify({"error": "File type not allowed"}),400
    

    
@app.route('/uploaded/<string:file_id>', methods=['GET'])
def get_uploads(file_id):
     # Convert the string _id to an ObjectId
    file_id = ObjectId(file_id)
    # get the image from GridFS by its ID
    file = fs.get(file_id)
     # Send the image data as a response
    return send_file(file, as_attachment=True, download_name=file.filename)
   

if __name__ == '__main__':
    app.run(debug=True)