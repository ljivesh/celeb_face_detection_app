#
import joblib
import tensorflow as tf
import cv2
import numpy as np
import os

    

clf, le, scaler, pca = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),'CNN_Model.pkl'))
vgg_model = tf.keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)),'vgg_model.h5'))

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml')

def load_image(path):
    img = cv2.imread(path, 1)
    # OpenCV loads images with color channels
    # in BGR order. So we need to reverse them
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            return roi_color[...,::-1]

def Predict(img_path):

    # img_path = 'dwayne_johnson.jpg'
    img = load_image(img_path)

    # Normalising pixel values from [0-255] to [0-1]: scale RGB values to interval [0,1]
    img = (img / 255.).astype(np.float32)
    img = cv2.resize(img, dsize = (224,224))

    # Obtain embedding vector for an image
    # Get the embedding vector for the above image using vgg_face_descriptor model and print the shape 
    embedding_vector = vgg_model.predict(np.expand_dims(img, axis=0))[0]
    print(embedding_vector.shape)

    embeddings = np.zeros((1,2622))
    embeddings[0] = embedding_vector
    x_inp = embeddings
    x_inp_scaler = scaler.transform(x_inp)
    x_inp_pca = pca.transform(x_inp_scaler)

    y_predict = clf.predict(x_inp_pca)

    y_predict_decoded = le.inverse_transform(y_predict)

    return y_predict_decoded[0]
