from .extensions import db
#Creating table to store the relationship between student and subject entity.
#Here assuming that one student can have multiple subjects and vice-versa, so relationship will be many-to-many.

"""
association_table=db.Table(
	'student_subject',
	db.Column('stu_id',db.Integer,db.ForeignKey('student.roll_no')),
	db.Column('sub_id',db.Integer,db.ForeignKey('subject.sub_id')),
	db.Column('marks',db.Integer),
	)
"""


#Creating Marks table to store the marks of student in all subjects they have enrolled.
class Marks(db.Model):
	__tablename__= 'marks'
	stu_id = db.Column(db.Integer,db.ForeignKey('student.roll_no',ondelete='CASCADE'),primary_key=True)
	sub_id = db.Column(db.Integer,db.ForeignKey('subject.sub_id',ondelete='CASCADE'),primary_key=True)
	marks_obtained = db.Column(db.Integer())
	subject = db.relationship('Subject')


	def json(self):
		return {"Sub_id":self.sub_id,"Marks":self.marks_obtained}





#Creating Table to store students records
class Student(db.Model):
	__tablename__='student'

	roll_no = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(20))
	gender = db.Column(db.String(1))
	dob = db.Column(db.DateTime)
	contact_no = db.Column(db.String(13))
	city = db.Column(db.String(20))

	#subjects = db.relationship('Subject', secondary=association_table, backref='enrolled_students')
	enrolled_subjects = db.relationship('Marks',cascade="all, delete")



	def __init__(self,name,gender,dob,contact_no,city):
		self.name=name
		self.gender=gender
		self.dob=dob
		self.contact_no=contact_no
		self.city=city


	def __repr__(self):
		return f'<student: {self.name}>'


	def json(self):
		sub=[m.json() for m in self.enrolled_subjects]
		return {"Roll no":self.roll_no,"Name":self.name,"gender":self.gender,"DOB":self.dob,"Contact":self.contact_no,"City":self.city,"Subjects":sub}




#creating table to store subject details
class Subject(db.Model):
	__tablename__='subject'

	sub_id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(20))
	



	def __init__(self,name):
		self.name=name

	def __repr__(self):
		return f'<Subject: {self.name}>'

	def json(self):
		return {"Sub_id":self.sub_id,"Name":self.name}
