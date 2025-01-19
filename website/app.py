from flask import Flask, render_template, request, url_for, jsonify
from livereload import Server
import numpy as np
from PIL import Image
import io
from os import listdir
import tensorflow as tf

app = Flask(__name__);

label_map = ['Bus', 'Car', 'Truck'];

def preprocess_image(image, pretrained=False):
    if pretrained:
        img_height = 160
        img_width = 160
    else:
        img_height = 224
        img_width = 224
    img_array = tf.convert_to_tensor(image, dtype=tf.float32)
    img_array = tf.image.resize(img_array, [img_height, img_width])
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    return img_array

def load_model(pretrained=False, num=None):
    if not num:
        if pretrained:
            model_path = '../models/pretrained/'
        else:
            model_path = '../models/default/'
        last = len(listdir(model_path))
    else:
        last = num
    return tf.keras.models.load_model(f'{model_path}/vehicle_recognition_{last}.keras')

model_default = load_model()
model_pretrained = load_model(True)

@app.route('/')
def index():
    return render_template('index.html', api_url=url_for('classify'))

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    image_bytes = file.read()
    image = np.array(Image.open(io.BytesIO(image_bytes)))

    input_image_default = preprocess_image(image)
    predictions = model_default.predict(input_image_default)
    predicted_vehicle_default = np.argmax(predictions[0])

    input_image_pretrained = preprocess_image(image, True)
    predictions = model_pretrained.predict(input_image_pretrained)
    predicted_vehicle_pretrained = np.argmax(predictions[0])
    # file.save(f'/uploads/{file.filename}')
    return jsonify({
        'prediction_default': label_map[int(predicted_vehicle_default)],
        'prediction_pretrained': label_map[int(predicted_vehicle_pretrained)]
    })

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve()