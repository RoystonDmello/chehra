"""
    Preprocessing needed for training and inference.
"""
import face_recognition as fc
import numpy as np
import cv2


def encode(img):
    """
    Given an image it returns the encodings for all the faces in the image
    :param img: Image or numpy array, the image whose encoding needs to be
    found
    :return: A numpy array of shape (n, 128) where n is the number of faces in
    detected in the image
    """

    face_locations = fc.face_locations(img)

    if face_locations:
        encodings = fc.face_encodings(img, face_locations)
        encodings = np.vstack(encodings)
    else:
        encodings = []

    return encodings


def generate_dataset(vid):
    """
    GIven a video file path it finds the encodings of all the frames with a
    single face in the every frame. It returns a concatenated array which will
    be the training data set
    :param vid: String, full file path of the video
    :return: A numpy array of shape (n, 128) where n is the number of frames
    with a single face in it.
    """
    encodings = []

    cap = cv2.VideoCapture(vid)
    success, frame = cap.read()

    while success:
        corrected_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encoding = encode(corrected_frame)

        if len(encoding) == 1:  # Single face
            encodings.append(encoding)

        success, frame = cap.read()

    if encodings:
        encodings = np.vstack(encodings)
    else:
        encodings = []

    return encodings
