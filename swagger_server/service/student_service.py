import json
import logging
import os
import tempfile
import sys

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add_student(student):
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    if (not student.first_name):
        return 'first name required', 405

    if (not student.last_name):
        return 'last name required', 405

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_student_by_id(student_id, subject):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    if not subject:
        return student
    
    if subject in student["grades"]:
        return student
    else:
        return None
    
    return student

def get_student_by_last_name(last_name):
    query = Query()
    student = student_db.search(query.last_name == last_name)
    print(student, file=sys.stderr)

    if not student:
        return None
    
    if len(student) > 0:
        return Student.from_dict(student[0])

    return None

def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student_db.remove(doc_ids=[int(student_id)])
    return student_id