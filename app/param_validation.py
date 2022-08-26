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



#Valid length of contact number
def contactLengthValidate(contact):
	if len(contact)!=13:
		return True
	return False



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
