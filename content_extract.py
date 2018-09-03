import re
import datetime
from dateutil.parser import parse


class ContentExtractor():
	# Extracts Email addresses, Phone Numbers, and DateTime objects from a given string

	def __init__(self):
		self.extractions = {}
		self.phone_numbers = []
		self.emails = []
		self.datetime_objects = []

	def extract_datetime(self, sentence):

		datetime_results = []

		# keywords
		datetime_keyword_lst = (
		':', 'today', 'tomorrow', 'yesterday', 'am', 'a.m', 'a.m.', 'pm', 'p.m', 'p.m.', 'january', 'february', 'march',
		'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december')

		for keyword in datetime_keyword_lst:

			if keyword in sentence:
				# checking for tomorrow and yesterday in the sentence and adding a datetime object accordingly
				one_day = datetime.timedelta(days=1)
				if "tomorrow" in sentence:
					self.datetime_objects.append(datetime.datetime.now() + one_day)
				elif "yesterday" in sentence:
					self.datetime_objects.append(datetime.datetime.now() - one_day)

				# extracting datetime object from sentence using dateutil.parser.parse
				try:
					self.datetime_objects.append(parse(sentence, fuzzy=True))
				except ValueError:
					if not datetime_results:
						self.datetime_objects = ["None"]
				break

		if not self.datetime_objects:
			self.datetime_objects = ["None"]

		return self.datetime_objects

	def extract_email(self, sentence):

		expression = re.compile(r"[\w\.-]+@[\w\.-]+")
		self.emails = expression.findall(sentence)
		if not self.emails:
			self.emails = ["None"]

		return self.emails

	def extract_phone(self, sentence):

		reg = re.compile(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?", re.S)
		self.phone_numbers = reg.findall(sentence)
		if not self.phone_numbers:
			self.phone_numbers = ["None"]

		return self.phone_numbers

	def extract_all(self, sentence):

		self.extract_email(sentence)
		if self.emails:
			self.extractions['emails'] = self.emails
		else:
			self.extractions['emails'] = []

		self.extract_phone(sentence)
		if self.phone_numbers:
			self.extractions['phones'] = self.phone_numbers
		else:
			self.extractions['phones'] = []

		self.extract_datetime(sentence)
		if self.datetime_objects:
			self.extractions['datetimes'] = self.datetime_objects
		else:
			self.extractions['datetimes'] = []

		return self.extractions

