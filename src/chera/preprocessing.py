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
    video_capture = cv2.VideoCapture(vid)
    frames = []
    frame_count = 0
    batch_size = 7

    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        frame = frame[:, :, ::-1]
        (h, w) = frame.shape[:2]

        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, 90, 1.0)
        frame = cv2.warpAffine(frame, M, (w, h))

        frame_count += 1
        frames.append(frame)

        if len(frames) == batch_size:
            batch_of_face_locations = fc.\
                batch_face_locations(frames)

            for frame_number_in_batch, face_locations in \
                    enumerate(batch_of_face_locations):
                if len(face_locations) == 1:
                    top, right, bottom, left = face_locations[0]
                    image = frames[frame_number_in_batch]
                    face_image = image[top:bottom, left:right]
                    enc = fc.face_encodings(face_image,
                                            face_locations)[0]
                    if len(enc):
                        encodings.append(enc)
            frames = []

    if encodings:
        encodings = np.vstack(encodings)
    else:
        encodings = []

    return encodings
