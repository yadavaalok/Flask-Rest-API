from flask import Blueprint,jsonify,request,json
from .models import *

view = Blueprint('view',__name__)



@view.route('/')
def home():
	return "<h1>Assignment</h1>",200



@view.route('/student',methods=['GET','POST'])
def student():

	if request.method=='GET':
		args=request.args
		""" CONSIDERING 3 PARAMETERS: NAME,GENDER,CITY"""
		if args: 
			if ('name' in args):
				try:
					int(args['name'])
					return "Bad Request",400
				except:
					pass

			if ('gender' in args):
				try:
					int(args['gender'])
					return "Bad Request",400
				except:
					pass


			if ('city' in args):
				try:
					int(args['city'])
					return "Bad Request",400
				except:
					pass

				
			s=Student.query.filter_by(**args).all()
			if s:
				return jsonify([ss.json() for ss in s]),200
			return {"message":"No Data present for the given query string"},404

		else:
			s=Student.query.all()
			if len(s):
				return jsonify([ss.json() for ss in s]),200
			else:
				return {"Message":"No Data Present, Kindly Add data of students!"},404



	elif request.method=='POST':
		data=json.loads(request.data)

		#CHeck whether all the required columns data are present in the request
		required_data={'Name','gender','DOB','City','Contact','Subjects'}
		if required_data>data.keys():
			return "Kindly fill all the details required for student",400


		name=data['Name']
		gender=data['gender']
		dob=data['DOB']
		city=data['City']
		contact_no=data['Contact']

		#Checking whether the type of data is valid or invalid

		try:
			int(name)
			return "Bad Request",400
		except:
			pass

		try:
			int(gender)
			return "Bad Request",400
		except:
			pass

		try:
			int(city)
			return "Bad Request",400
		except:
			pass
		

		#Checking the contact number is proper or not

		if len(contact_no)!=13:
			return "Kindly enter contact in following format: +91(10 digits number)",400

		s=Student(name,gender,dob,contact_no,city)
		db.session.add(s)
		db.session.commit()
		subjects=data['Subjects']
		for sub in subjects:

			#Checking whether sub_id and marks are integer type or not
			try:
				int(sub['Sub_id'])
				pass
			except:
				return "Bad Request",400

			try:
				int(sub['Marks'])
				pass
			except:
				return "Bad Request",400


			sub_obj=Subject.query.filter_by(sub_id=sub['Sub_id']).first()

			#Checking whether the provided subject id is present in our database or not
			if sub_obj==None:
				return "Entered Subject id not present",404

			s.enrolled_subjects.append(Marks(marks_obtained=sub['Marks'],subject=sub_obj))
			db.session.add(s)
			db.session.commit()
			
		return "Student Data Added Successfully",201




@view.route('/subject',methods=['GET','POST'])
def subject():


	if request.method=='GET':
		sub=Subject.query.all()
		if len(sub):
			return jsonify([ss.json() for ss in sub]),200
		else:
			return {"Message":"No Data Present, Kindly Add data of subjects!"},200



	elif request.method=='POST':
		data=json.loads(request.data)

		#Check whether all required fields are provided
		required_fields={'Name'}
		if required_fields>data.keys():
			return "Kindly enter all required fields of subject",400

		sub=Subject(data['Name'])
		

		#Check whether correct type of data is provided for the respective fields
		try:
			int(data['Name'])
			return "Bad Request",400
		except:
			pass

		db.session.add(sub)
		db.session.commit()
		return "Subject Data Added Successfully",201




@view.route('/student/<int:id>',methods=['GET','PUT','DELETE','PATCH'])
def student_id(id):


	s=Student.query.filter_by(roll_no=id).first()


	#Checking if the student with the given id is present
	if not s:
		return {"Message":"No record present for the given id"},404

	if request.method=='GET':
		return jsonify(s.json()),200
		

	elif request.method=='PUT':
		data=json.loads(request.data)

		#CHeck whether all the required fields are present in the request
		required_data={'Name','gender','DOB','City','Contact','Subjects'}
		if required_data>data.keys():
			return "Kindly fill all the details required for student",400
		
		s.name=data['Name']
		s.gender=data['gender']
		s.dob=data['DOB']
		s.city=data['City']
		s.contact_no=data['Contact']

		#Checking whether correct type of data is provided for each field.
		try:
			int(s.name)
			return "Bad Request",400
		except:
			pass

		try:
			int(s.gender)
			return "Bad Request",400
		except:
			pass

		try:
			int(s.city)
			return "Bad Request",400
		except:
			pass

		#Checking whether contact number is proper
		if len(data['Contact'])!=13:
			return "Kindly enter contact in following format: +91(10 digits number)",400


		subjects=data['Subjects']
		marks_obj=s.enrolled_subjects
		for m in marks_obj:
			for sub in subjects:
				
				#Checking whether sub_id and marks are integer type or not
				try:
					int(sub['Sub_id'])
					pass
				except:
					return "Bad Request",400

				try:
					int(sub['Marks'])
					pass
				except:
					return "Bad Request",400


				sub_obj=Subject.query.filter_by(sub_id=sub['Sub_id']).first()

				#Checking whether the provided subject id is present in our database or not
				if sub_obj==None:
					return "Entered Subject id is not present",404


				if m.sub_id==sub['Sub_id']:
					m.marks_obtained=sub['Marks']

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
		
		if 'Name' in data.keys():
			try:
				int(data['Name'])
				return "Bad Request",400
			except:
				pass

		if 'gender' in data.keys():
			try:
				int(data['gender'])
				return "Bad Request",400
			except:
				pass

		if 'City' in data.keys():
			try:
				int(data['City'])
				return "Bad Request",400
			except:
				pass



		#Checking whether contact number is proper
		if 'Contact' in data.keys() and len(data['Contact'])!=13:
			return "Kindly enter contact in following format: +91(10 digits number)",400



		for key,value in data.items():
			if key.lower()=="city":
				s.city=value
			elif key.lower()=="gender":
				s.gender=value
			elif key.lower()=="contact":
				s.contact_no=value
			elif key.lower()=="subjects":
				subjects=value
				marks_obj=s.enrolled_subjects
				for m in marks_obj:
					for sub in subjects:

						#Checking type of sub_id and marks
						try:
							int(sub['Sub_id'])
							pass
						except:
							return "Bad Request",400

						try:
							int(sub['Marks'])
							pass
						except:
							return "Bad Request",400


						sub_obj=Subject.query.filter_by(sub_id=sub['Sub_id']).first()

						#Checking whether the provided subject id is present in our database or not
						if sub_obj==None:
							return "Entered Subject id is not present",404


						if m.sub_id==sub['Sub_id']:
							m.marks_obtained=sub['Marks']			

		db.session.add(s)	
		db.session.commit()
		return "Data updated using patch",204





@view.route('/subject/<int:id>',methods=['GET','PUT','DELETE'])
def subject_id(id):

	sub=Subject.query.filter_by(sub_id=id).first()
	if not sub:
		return {"Message":"No record present for the given id"},404

	if request.method=='GET':
		return jsonify(sub.json()),200

	elif request.method=='PUT':
		data=json.loads(request.data)

		#Check whether all required fields are provided
		required_fields={'Name'}
		if required_fields>data.keys():
			return "Kindly enter all required fields of subject",400


		name=data['Name']


		#Check whether correct type of data is provided for the respective fields
		try:
			int(name)
			return "Bad Request",400
		except:
			pass

		sub.name=name
		db.session.add(sub)
		db.session.commit()
		return "Subject Data Updated Successfully",204

	elif request.method=='DELETE':
		db.session.delete(sub)
		db.session.commit()
		return "Subject Data Deleted Successfully",204