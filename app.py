import os
import uuid
import flask
import urllib
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from keras.applications.inception_v3 import InceptionV3, preprocess_input
import numpy as np
import tensorflow as tf

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from keras.models import load_model, model_from_json
# json_file = open('classify.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# model = model_from_json(loaded_model_json,{"tf":tf})
# # load weights into new model

# model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
# model.load_weights("besmodel.h5")
# # model.evaluate()
# print("Loaded model from disk")
from keras.models import load_model
model = load_model("./model.h5")


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

classes = ['Gasoline can','Hammer','Pliers','Rope','Screw Driver','Tool Box','Wrench','pebbel', 'random']


def predict(filename , model):
    
    img = load_img(filename , target_size = (256,256))
    i = img_to_array(img)
    i = preprocess_input(i)



    input_arr = np.array([i])
    input_arr.shape

    pred = np.argmax(model.predict(input_arr))


    if pred == 0:
        return ("This is a Gasoline Can")

    elif (pred == 1):
        return ("This is a hammer")

    elif (pred == 2):
        return ("This is a Plier ")

    elif pred == 3:
        return ("This is a rope")

    elif pred == 4:
        return ("This is a screw driver")

    elif pred == 5:
        return ("This is a tool box")

    elif pred == 6:
        return ("This is a wrench")

    elif pred == 7:
        return ("This is a pebbel")

    else:
        return ("No this is not a machine part")
	


@app.route('/')
def home():
        return render_template("index.html")

@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd() , 'static\images')
    if request.method == 'POST':
        

            
        if (request.files):
            file = request.files['img1']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename
		path = os.path.join('static\images',file.filename)
                class_result = predict(img_path , model)

            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if(len(error) == 0):
                return  render_template('success.html' , img  = path , prediction = class_result)
            else:
                return render_template('index.html' , error = error)

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
