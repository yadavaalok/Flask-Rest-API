from flask import Blueprint,jsonify,request,json
from .models import *
import requests
from .param_validation import *
from .db_operations import *


view = Blueprint('view',__name__)



@view.route('/home')
def home():
	return "Hello World",200


"""
#query string paramter validation for student 
def studentParamValidate(**kwargs):
	flag=False

	if ('name' in kwargs):
		try:
			int(kwargs['name'])
			flag=True
		except:
			pass

	if ('gender' in kwargs):
		try:
			int(kwargs['gender'])
			flag=True
		except:
			pass


	if ('city' in kwargs):
		try:
			int(kwargs['city'])
			flag=True
		except:
			pass
	return flag
"""

"""
#Valid length of contact number
def contactLengthValidate(contact):
	if len(contact)!=13:
		return True
	return False
"""

"""
#subject fields validation
def subjectParamValidate(**data):
	flag=0
	if 'name' in data:
		try:
			int(data['name'])
			flag=1
		except:
			pass

	if ('sub_id' in data) and (type(data['sub_id'])!=int):
		flag=1 

	if ('marks' in data) and (type(data['marks'])!=int):
		flag=1



	return flag
"""

@view.route('/student',methods=['GET','POST'])
def student():
	
	if request.method=='GET':
		kwargs=dict(request.args)
		""" CONSIDERING 3 PARAMETERS: NAME,GENDER,CITY"""
		if kwargs:
			

			if studentParamValidate(**kwargs):
				return "Bad Request",400

				
			#s=Student.query.filter_by(**kwargs).all()
			s=get_student_query(**kwargs)
			if s:
				return jsonify([ss.json() for ss in s]),200
			return {"message":"No Data present for the given query string"},404

		else:
			#s=Student.query.all()
			s=get_student_query()
			
			if len(s):
				return jsonify([ss.json() for ss in s]),200
			else:
				return {"Message":"No Data Present, Kindly Add data of students!"},404



	elif request.method=='POST':
		data=json.loads(request.data)

		#CHeck whether all the required columns data are present in the request
		required_data={'name','gender','dob','city','contact','subjects'}
		if required_data>data.keys():
			return "Kindly fill all the details required for student",400


		name=data['name']
		gender=data['gender']
		dob=data['dob']
		city=data['city']
		contact_no=data['contact']

		#Checking whether the type of data is valid or invalid
		if studentParamValidate(**data):
			return "Bad Request",400
		

		#Checking the contact number is proper or not

		if contactLengthValidate(contact_no):
			return "Kindly enter contact in following format: +91(10 digits number)",400

		s=Student(name,gender,dob,contact_no,city)
		subjects=data['subjects']
		for sub in subjects:

			#Checking whether sub_id and marks are integer type or not
			if subjectParamValidate(**sub):
				return "Bad Request",400


			#sub_obj=Subject.query.filter_by(sub_id=sub['sub_id']).first()
			sub_obj=get_subject_query(sub['sub_id'])


			#Checking whether the provided subject id is present in our database or not
			if sub_obj==None:
				return "Entered Subject id not present",404

			s.enrolled_subjects.append(Marks(marks_obtained=sub['marks'],subject=sub_obj))
		db.session.add(s)
		db.session.commit()
			
		return "Student Data Added Successfully",201




@view.route('/subject',methods=['GET','POST'])
def subject():

	if request.method=='GET':

		sub=get_subject_query()
		if len(sub):
			return jsonify([ss.json() for ss in sub]),200
		else:
			return {"Message":"No Data Present, Kindly Add data of subjects!"},200



	elif request.method=='POST':
		data=json.loads(request.data)

		#Check whether all required fields are provided
		required_fields={'name'}
		if required_fields>data.keys():
			return "Kindly enter all required fields of subject",400

		sub=Subject(data['name'])
		

		#Check whether correct type of data is provided for the respective fields
		if subjectParamValidate(**data):
			return "Bad Request",400

		db.session.add(sub)
		db.session.commit()
		return "Subject Data Added Successfully",201




@view.route('/student/<int:id>',methods=['GET','PUT','DELETE','PATCH'])
def student_id(id):


	s=get_student_by_id_query(id)

	#Checking if the student with the given id is present
	if not s:
		return {"Message":"No record present for the given id"},404

	if request.method=='GET':
		return jsonify(s.json()),200
		

	elif request.method=='PUT':
		data=json.loads(request.data)

		#CHeck whether all the required fields are present in the request
		required_data={'name','gender','dob','city','contact','subjects'}
		if required_data>data.keys():
			return "Kindly fill all the details required for student",400
		
		s.name=data['name']
		s.gender=data['gender']
		s.dob=data['dob']
		s.city=data['city']
		s.contact_no=data['contact']

		#Checking whether correct type of data is provided for each field.
		if studentParamValidate(**data):
			return "Bad Request",400

		#Checking whether contact number is proper
		if contactLengthValidate(data['contact']):
			return "Kindly enter contact in following format: +91(10 digits number)",400


		subjects=data['subjects']
		marks_obj=s.enrolled_subjects
		for m in marks_obj:
			for sub in subjects:
				
				#Checking whether sub_id and marks are integer type or not
				if subjectParamValidate(**sub):
					return "Bad Request",400


				#sub_obj=Subject.query.filter_by(sub_id=sub['sub_id']).first()
				sub_obj=get_subject_query(sub['sub_id'])


				#Checking whether the provided subject id is present in our database or not
				if sub_obj==None:
					return "Entered Subject id is not present",404


				if m.sub_id==sub['sub_id']:
					m.marks_obtained=sub['marks']

		db.session.add(s)
		db.session.commit()
		return "Student Data Updated Successfully",204


	elif request.method=='DELETE':
		db.session.delete(s)
		db.session.commit()
		return "Student Data Deleted Successfully",204


	elif request.method=='PATCH':
		data=json.loads(request.data)


		#Checking whether correct type of data is provided
		if studentParamValidate(**data):
			return "Bad Request",400



		#Checking whether contact number is proper
		if 'contact' in data.keys() and contactLengthValidate(data['contact']):
			return "Kindly enter contact in following format: +91(10 digits number)",400



		for key,value in data.items():
			if key=="city":
				s.city=value
			elif key=="gender":
				s.gender=value
			elif key=="contact":
				s.contact_no=value
			elif key=="subjects":
				subjects=value
				marks_obj=s.enrolled_subjects
				for m in marks_obj:
					for sub in subjects:

						#Checking type of sub_id and marks
						if subjectParamValidate(**sub):
							return "Bad Request",400


						#sub_obj=Subject.query.filter_by(sub_id=sub['sub_id']).first()
						sub_obj=get_subject_query(sub['sub_id'])


						#Checking whether the provided subject id is present in our database or not
						if sub_obj==None:
							return "Entered Subject id is not present",404


						if m.sub_id==sub['sub_id']:
							m.marks_obtained=sub['marks']			

		db.session.add(s)	
		db.session.commit()
		return "Data updated using patch",204




@view.route('/subject/<int:id>',methods=['GET','PUT','DELETE'])
def subject_id(id):

	sub=get_subject_query(id)
	if not sub:
		return {"Message":"No record present for the given id"},404

	if request.method=='GET':
		return jsonify(sub.json()),200

	elif request.method=='PUT':
		data=json.loads(request.data)

		#Check whether all required fields are provided
		required_fields={'name'}
		if required_fields>data.keys():
			return "Kindly enter all required fields of subject",400


		name=data['name']


		#Check whether correct type of data is provided for the respective fields
		if subjectParamValidate(**data):
			return "Bad Request",400

		sub.name=name
		db.session.add(sub)
		db.session.commit()
		return "Subject Data Updated Successfully",204

	elif request.method=='DELETE':
		db.session.delete(sub)
		db.session.commit()
		return "Subject Data Deleted Successfully",204

		