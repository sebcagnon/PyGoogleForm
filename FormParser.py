import collections
import urllib, urllib2
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
		questionsList = [GFQuestion(qSoup) for qSoup in self.soup.form.findChildren("div", "ss-form-question")]
		self.questions = collections.OrderedDict((q.getID(), q) for q in questionsList)

	def getFormInfos(self):
		"""returns general form info [title, desc]"""
		info = []
		info.append(self.soup.find_all("h1", "ss-form-title")[0].string)
		info.append(self.soup.find_all("div", "ss-form-desc")[0].string)
		return info

	def getQuestionIDs(self):
		"""Returns list of question IDs"""
		return self.questions.keys()

	def getQuestionInfo(self, id):
		"""Returns the info necessary to answer question as a list

		   [id, type, question, choices]
		"""
		return self.questions[id].getQuestionAsList()

	def __getitem__(self, id):
		"""If id is string, same as getQuestionInfo, if int, returns i-th question info"""
		if isinstance(id, basestring):
			return getQuestionInfo(id)
		elif isinstance(id, int):
			return getQuestionInfo(self.questions[self.questions.keys()[id]])
		else:
			raise TypeError("id can only be str (a question id), or int (the index of the question")

	def answerQuestion(self, id, answer):
		"""Saves the answer of question with that id"""
		self.questions[id].answerQuestion(answer)

	def submit(self):
		"""POST current answers to Google Forms"""
		tups = tuple((q.getID(), q.getAnswer()) for q in self.questions.values())
		data = urllib.urlencode(tups)
		postURL = self.soup.form["action"]
		request = urllib2.Request(postURL, data)
		urllib2.urlopen(request)


class GFQuestion(object):
	"""Generic API for Google Form Questions

	   This is used by GFParser to easily find info. Should not be accessed by user.
	"""

	def __init__(self, questionSoup):
		"""Initializes from an ss-form-question div element as soup object"""
		self.soup = questionSoup
		self.type = self.soup.div["class"][1]
		self.id   = None
		self.label = self.soup.label.div.text.strip()
		self._answer = None

	def getType(self):
		"""Returns question type (radio, text, ...) as string"""
		return self.type

	def getID(self):
		"""Returns id of question in the form entry.### as string"""
		if self.id is None:
			if self.type in ["ss-radio", "ss-text", "ss-checkbox"]:
				self.id = self.soup.input["name"]
			elif self.type == "ss-select":
				self.id = self.soup.find("select")["name"]
			elif self.type == "ss-paragraph-text":
				self.id = self.soup.textarea["name"]
		return self.id

	def _getChoices(self):
		"""Returns list of possible answers or empty string, depending on Q type"""
		choices = None
		if self.type in ["ss-radio", "ss-checkbox"]:
			choices = [item.input["value"] for item in self.soup.findChildren("li")]
		elif self.type in ["ss-text", "ss-paragraph-text"]:
			choices = ""
		elif self.type == "ss-select":
			choices = [item.text for item in self.soup.findChildren("option") if item.text!=""]
		return choices

	def getQuestionAsList(self):
		"""Returns [id, type, question, choices]

		choices depends on the question type.
		For radio, select or checkbox, the choices are given as a list.
		For text or paragraph-text, the choices is an empty string."""

		retValue = [self.id, self.type, self.label, self._getChoices()]
		return retValue

	def answerQuestion(self, answer):
		"""Save the answer to the question"""
		# TODO: handle multiple answers for checkbox type!
		answers = self._getChoices()
		if not isinstance(answer, basestring):
			raise ValueError("answer should be string or unicode")
		if answers == "" or answer in answers:
			self._answer = answer
		else:
			errorMessage = 'Answer "{}" is not a posible answer. Possible answers are:\n\t'.format(answer)
			errorMessage += '\n\t'.join(answers)
			raise ValueError(errorMessage)

	def getAnswer(self):
		"""returns the chosen answer(s) or None if no answer was given"""
		return self._answer


def main():
	# Testing GFParser basics
	url = "https://docs.google.com/forms/d/1jzDkEha066GwSCcSrCg1yaJJLpJAk0_aIFwf6GQgmmU/viewform"
	gForm = GFParser(url)
	assert gForm.getFormInfos() == ["Testing", "This form is a test"], "Form info is wrong"
	assert len(gForm.getQuestionIDs()) == 5, "Number of questions ain't right, got {}, should be 5".format(len(gForm.getQuestions()))
	# Testing GFQuestion
	radio = gForm.questions.values()[0]
	assert radio.getType() == "ss-radio", "Wrong type for radio question: " + radio.getType()
	assert radio._getChoices() == ["ok", "no", "Other"], "wrong list of answers for radio"
	assert len(radio.getQuestionAsList()) and type(radio.getQuestionAsList()[3]) is list, "Error in radio.getQuestionAsList"
	try:
		radio.answerQuestion("hello")
		raise AssertionError('radio.answerQuestion("hello") should have thrown a ValueError')
	except ValueError, e:
		print "See the beautiful error message:"
		print e
	radio.answerQuestion("ok")
	assert radio._answer == "ok", 'Error in radio.answerQuestion("ok"), did not save the answer'
	# Testing filling the form and submitting
	questionIDs = gForm.getQuestionIDs()
	for id in questionIDs:
		question = gForm.getQuestionInfo(id)
		if question[1] in ['ss-radio', 'ss-select', 'ss-checkbox']:
			gForm.answerQuestion(question[0], question[3][0])
		else:
			gForm.answerQuestion(question[0], "hello test!")
	gForm.submit()
	import datetime
	print "New answer submitted: " + str(datetime.datetime.now())
	print "All tests succesful!"


if __name__ == '__main__':
	main()