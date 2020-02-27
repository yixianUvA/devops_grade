import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student

import sys

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)

def add_student(student):
    if not student.first_name:
        return 'Cannot create a student without a first name', 405
    if not student.last_name:
        return 'Cannot create a student without a last name', 405

    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    print(student.to_dict(), file=sys.stderr)

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id

def get_student_by_id(student_id, subject):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student

    student = Student.from_dict(student)
    if not subject:
        return student

    print(subject, file=sys.stderr)    
    if subject in student.grades:
        return student

def get_student(last_name):
    queries = []
    query = Query()
    #queries.append(query.last_name == last_name)
    #query = reduce(lambda a, b: a & b, queries)
    query = query.last_name == last_name
    res = student_db.search(query)
    if res:
        print(res, file=sys.stderr)
        return Student.from_dict(res[0])

def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student_db.remove(doc_ids=[int(student_id)])
    return student_id