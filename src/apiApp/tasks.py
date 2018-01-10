from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.files.base import File
from rest_framework.response import Response
from django.core.files.storage import default_storage

from .models import StudentData, Student

from tempfile import TemporaryFile
import numpy as np

from chera import preprocessing

import os

@shared_task
def video_process(path, id):
    full_path = default_storage.path(path)

    dataset = preprocessing.generate_dataset(full_path)

    # if not len(dataset):
    #     print("No face found")

    outfile = TemporaryFile()
    np.save(outfile, dataset)

    student = Student.objects.get(student_id=id)
    f = File(outfile, '{0}.npy'.format(student))

    instance = StudentData(student_id=student, data=f)
    instance.save()

    default_storage.delete(path)