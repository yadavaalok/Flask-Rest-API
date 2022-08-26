import pytest
from app.views import *


class TestSubjectCases:


	def test_positivecase_requiredSubjectFields(self):
		required_fields={'name'}
		data={"name":"chemistry"}
		assert (required_fields==data.keys())==True

	def test_positivecase_subjectParamValidate(self):
		data={"name":"chemistry","sub_id":2,"marks":90}
		assert subjectParamValidate(**data)==False

	def test_negativecase_requiredSubjectFields(self):
		required_fields={"name"}
		data={}
		assert (required_fields>data.keys())==True

	def test_negativecase_subjectParamValidate(self):
		data={"name":10,"sub_id":"2","marks":"80"}
		assert subjectParamValidate(**data)==True