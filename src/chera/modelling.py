"""
This module contains the training and prediction related functions
"""
from functools import reduce

import numpy as np
from sklearn.svm import SVC


def train(student_ids, student_datas):
    """
    Given the list of student ids and student datas this will create a model
    and a mapping between the model predictions and the student_ids
    :param student_ids: List, list of student ids to be trained on
    :param student_datas: List, list of numpy arrays of a datafile
    corresponding to each element in student_ids
    :return: tuple, (model, mappings) where model is an sklearn model and
    mappings is list of student_ids where the index of the list corresponds to
    the model prediction. So mappings[model.predict()] will return the id of
    the student
    """

    arrays = [np.load(file_field.open("rb"))
              for file_field in student_datas]

    data_set = np.vstack(arrays)
    labels = reduce(lambda x, y: x + y,
                    [[i] * arrays[i].shape[0]
                     for i in range(len(student_ids))])

    clf = SVC(C=0.0001).fit(data_set, labels)

    return (clf, student_ids)
