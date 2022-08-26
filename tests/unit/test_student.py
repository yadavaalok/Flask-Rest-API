import pytest
from app.views import *

class TestStudentCases:

	def test_positivecase_studentParamValidate(self):
		kwargs={"name":"XYZ","city":"Mumbai","gender":"F"}
		assert studentParamValidate(**kwargs)==False


	def test_positivecase_requiredStudentFields(self):
		required_data={'name','gender','dob','city','contact','subjects'}
		data={

        "name": "ABCDEF",
        "gender": "M",
        "dob": "01/02/1999",
        "contact": "+919876543210",
        "city": "Patna",
        "subjects": [
            {
                "sub_id": 5,
                "marks": 80
            }
        ]
		}

		assert (required_data==data.keys())==True


	def test_positivecase_contactFieldLength(self):
		contact_no="+919876543210"

		assert contactLengthValidate(contact_no)==False


	def test_negativecase_studentParamValidate(self):
		kwargs={"name":"XYZ","city":"Mumbai","gender":1}
		assert studentParamValidate(**kwargs)==True


	def test_negativecase_requiredStudentFields(self):
		required_data={'name','gender','dob','city','contact','subjects'}
		data={

        "name": "ABCDEF",
        "dob": "01/02/1999",
        "contact": "+919876543210",
        "city": "Patna",
        "subjects": [
            {
                "sub_id": 5,
                "marks": 80
            }
        ]
		}

		assert (required_data>data.keys())==True


	def test_negativecase_contactFieldLength(self):
		contact_no="+9137292289"

		assert contactLengthValidate(contact_no)==True




