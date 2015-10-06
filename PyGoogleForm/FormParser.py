import collections
import urllib, urllib2
from bs4 import BeautifulSoup

from FormQuestion import GFQuestion

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
		tups = tuple()
		for q in self.questions.values():
			if q.getAnswerData() is not None:
				tups += q.getAnswerData()
		data = urllib.urlencode(tups)
		postURL = self.soup.form["action"]
		request = urllib2.Request(postURL, data)
		urllib2.urlopen(request)


def main():
	# Testing GFParser basics
	url = "https://docs.google.com/forms/d/1jzDkEha066GwSCcSrCg1yaJJLpJAk0_aIFwf6GQgmmU/viewform"
	gForm = GFParser(url)
	assert gForm.getFormInfos() == ["Testing", "This form is a test"], "Form info is wrong"
	assert len(gForm.getQuestionIDs()) == 5, "Number of questions ain't right, got {}, should be 5".format(len(gForm.getQuestions()))
	# Testing filling the form and submitting
	questionIDs = gForm.getQuestionIDs()
	for id in questionIDs:
		question = gForm.getQuestionInfo(id)
		if question[1] in ['ss-radio', 'ss-select']:
			gForm.answerQuestion(question[0], question[3][0])
		elif question[1] == 'ss-checkbox':
			gForm.answerQuestion(question[0], question[3][:-1])
		else:
			gForm.answerQuestion(question[0], "hello test!")
	gForm.submit()
	import datetime
	print "New answer submitted: " + str(datetime.datetime.now())
	print "All tests succesful!"


if __name__ == '__main__':
	main()