from .models import *

def get_student_query(**kwargs)->None:
	print("hello")
	if kwargs:
		s=Student.query.filter_by(**kwargs).all()
	else:
		s=Student.query.all()

	return s


def get_student_by_id_query(id):
	s=Student.query.filter_by(roll_no=id).first()
	return s


def get_subject_query(id=None):
	if id:
		sub_obj=Subject.query.filter_by(sub_id=id).first()
	else:
		sub_obj=Subject.query.all()

	return sub_obj