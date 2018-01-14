from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.files.base import File
from rest_framework.response import Response
from django.core.files.storage import default_storage

from push_notifications.models import GCMDevice

from .models import StudentData, Student, Course, CourseData

from tempfile import TemporaryFile
import numpy as np

import pickle as pkl

from chera import preprocessing, modelling

import os

@shared_task
def video_process(path, id):
    full_path = default_storage.path(path)

    dataset = preprocessing.generate_dataset(full_path)

    if len(dataset):
        outfile = TemporaryFile()
        np.save(outfile, dataset)

        student = Student.objects.get(student_id=id)
        f = File(outfile, '{0}.npy'.format(student))

        instance = StudentData(student_id=student, data=f)
        instance.save()
    else:
        student = Student.objects.get(student_id=id)
        user = student.user

        student_device = GCMDevice.objects.filter(user=user)
        student_device.send_message("No face found in video, upload another one!")

    default_storage.delete(path)


@shared_task
def pics_process(imgs, lecture, teacher_user):
    course = lecture.course_id
    model, mappings = pkl.load(course.coursedata.data)

    student_ids = modelling.predict(model, mappings, imgs)
    absent_student_ids = list(set(mappings).difference(set(student_ids)))

    present_students = Student.objects.filter(
        student_id__in=student_ids).all()
    absent_students = Student.objects.filter(
        student_id__in=absent_student_ids).all()

    lecture.students = present_students

    present_users = [st.user for st in present_students]
    absent_users = [st.user for st in absent_students]

    present_devices = GCMDevice.objects.filter(
        user__in=present_users)
    present_devices.send_message("You have been marked {0}"
                                 " for the lecture of {1} on {2}".format(
        'present', course.name, lecture.start_time))

    absent_devices = GCMDevice.objects.filter(
        user__in=absent_users)
    absent_devices.send_message("You have been marked {0}"
                                " for the lecture of {1} on {2}".format(
        'absent', course.name, lecture.start_time))

    teacher_device = GCMDevice.objects.filter(user=teacher_user)
    teacher_device.send_message("Attendance has been marked!",
                                extra={
                                    "click_action": "",
                                    "isNotification": True,
                                    "lect_id": lecture.lect_id,
                                    "lect_no": lecture.lect_no
                                })



@shared_task
def course_process(course_id):
    course = Course.objects.get(course_id=course_id)

    students = course.students.all()

    # to add exception handling for no training data of students
    try:
        datas = [student.studentdata.data for student in students]
        ids = [student.student_id for student in students]

        saveable = modelling.train(ids, datas)

        outfile = TemporaryFile()
        pkl.dump(saveable, outfile)

        f = File(outfile, name='{0}.pkl'.format(course.course_id))

        course_data = CourseData(course_id=course, data=f)
        course_data.save()
    except Exception as e:
        print(e)