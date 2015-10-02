import urllib2
from bs4 import BeautifulSoup

class GFParser(object):
	"""Allows to access all the questions from a GForm and submit a response"""

	def __init__(self, url):
		"""Loads form from its public page url"""
		self.url = url
		res = urllib2.urlopen(self.url)
		self.soup = BeautifulSoup(res.read(), 'html.parser')
		if len(self.soup.find_all("h1", "ss-form-title")) == 0:
			raise ValueError("The url did not correspond to a valid Google Form")

	def getFormInfos(self):
		"""returns general form info [title, desc]"""
		info = []
		info.append(self.soup.find_all("h1", "ss-form-title")[0].string)
		info.append(self.soup.find_all("div", "ss-form-desc")[0].string)
		return info

	def getQuestions(self):
		"""Returns list of questions"""
		questions = self.soup.form.findChildren("div", "ss-form-question")
		# TODO format questions into usable classes
		return questions


class GFQuestion(object):
	"""Generic API for Google Form Questions"""

	def __init__(self, questionSoup):
		"""Initializes from an ss-form-question div element as soup object"""
		self.soup = questionSoup
		self.type = soup.div["class"][1]
		self.id   = soup.label["for"].replace("_", ".")
		self.label = soup.label.div.text.strip()

	def getType(self):
		"""Returns question type (radio, text, ...) as string"""
		return self.type

	def getID(self):
		"""Returns id of question in the form entry.### as string"""
		return self.id

	def getQuestionAsList(self):
		"""Returns [id, type, question, choices]

		choices depends on the question type.
		For radio, select or checkbox, the choices are given as a list.
		For text or paragraph-text, the choices is an empty string."""

		retValue = [self.id, self.type, self.label]
		if self.type in ["ss-radio", "ss-checkbox"]:
			choices = [item.input["value"] for item in self.soup.findChildren("li")]
			retValue.append(choices)
		elif self.type in ["ss-text", "ss-paragraph-text"]:
			retValue.append("")
		elif self.type == "ss-select":
			choices = [item.text for item in self.soup.findChildren["option"] if item.text!=""]
			retValue.append(choices)
		return retValue


def main():
	url = "https://docs.google.com/forms/d/1jzDkEha066GwSCcSrCg1yaJJLpJAk0_aIFwf6GQgmmU/viewform"
	res = urllib2.urlopen(url)
	soup = BeautifulSoup(res.read(), 'html.parser')
	# get the title
	formTitle = soup.find_all("h1", "ss-form-title")[0].string
	print "Form title: " + formTitle
	# description
	formDesc = soup.find_all("div", "ss-form-desc")[0].string
	print "Form description: " + formDesc
	# post url
	postURL = soup.form['action']
	# get questions
	questions = soup.form.findChildren("div", "ss-form-question")
	print "Number of questions: " + str(len(questions))
	# question ids
	print "Question ids: " + ", ".join(question.label["for"] for question in questions)
	# question type
	print "Question types: " + ", ".join(question.div["class"][1] for question in questions)


if __name__ == '__main__':
	main()