import io
from flask import Flask, request, jsonify, send_file
from encryption import encrypt_image
from decryption import decrypt_image
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

#app = Flask(__name__)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'image' not in request.files or 'message' not in request.form:
        return jsonify({'error': 'Missing image or message'}), 400

    image = request.files['image']
    message = request.form['message']

    image_path = 'temp_image.png'
    output_path = 'encrypted_image.png'

    image.save(image_path)
    encrypt_image(image_path, message, output_path)

    with open(output_path, 'rb') as f:
        img_bytes = io.BytesIO(f.read())

    # Delete temp files
    os.remove(image_path)
    os.remove(output_path)

    return send_file(img_bytes, mimetype='image/png', as_attachment=True, download_name='encrypted_image.png')

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'image' not in request.files:
        return jsonify({'error': 'Missing image'}), 400

    image = request.files['image']
    image_path = 'temp_encrypted_image.png'

    try:
        # Save the uploaded encrypted image
        image.save(image_path)

        # Decrypt the image
        message = decrypt_image(image_path)

        # Remove the temporary file
        os.remove(image_path)

        # Return the decrypted message
        return jsonify({'message': message})

    except Exception as e:
        # If something goes wrong, return an error message
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)