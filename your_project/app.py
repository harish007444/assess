from flask import Flask, request, jsonify, render_template
import jwt
import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Secret key for JWT
app.config['SECRET_KEY'] = 'your_secret_key'

# Create a Limiter to limit API requests
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# Page to upload an image
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            image_name = uploaded_file.filename
            # Save the uploaded image (you can specify a folder for saving)
            # uploaded_file.save('path_to_save/' + image_name)
            return render_template('result.html', image_name=image_name)
    return render_template('upload.html')

# Page to display the uploaded image name
@app.route('/result')
def result():
    image_name = request.args.get('image_name')
    return render_template('result.html', image_name=image_name)

# API route with JWT authentication
@app.route('/api/upload', methods=['POST'])
@limiter.limit("5 per minute")
def api_upload_image():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing"}), 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        # Process the image upload here
        return jsonify({"message": "Image uploaded successfully"})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.DecodeError:
        return jsonify({"message": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(debug=True)
