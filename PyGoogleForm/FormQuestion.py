import collections

class GFQuestion(object):
	"""Generic API for Google Form Questions

	   This is used by GFParser to easily find info. Should not be accessed by user.
	"""

	SUPPORTED_TYPES = ["ss-radio", "ss-select", "ss-checkbox", "ss-text", "ss-paragraph-text"]

	def __init__(self, questionSoup):
		"""Initializes from an ss-form-question div element as soup object"""
		self.soup = questionSoup
		qClasses = self.soup.div["class"]
		for qClass in qClasses:
			if qClass in self.SUPPORTED_TYPES:
				self.type = qClass
				break
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
		answers = self._getChoices()
		if self.type == "ss-checkbox":
			if not isinstance(answer, collections.Sequence):
				raise ValueError("answer should be string/unicode or list of strings/unicode")
			error = None
			if isinstance(answer, basestring) and answer in answers:
				self._answer = [answer]
			elif isinstance(answer, collections.Sequence):
				self._answer = []
				for ans in answer:
					if ans in answers:
						self._answer.append(ans)
					else:
						error = ans
						break
			else:
				error = answer
			if error is not None:
				errorMessage = 'Answer "{}" is not a posible answer. Possible answers are:\n\t'.format(error)
				errorMessage += '\n\t'.join(answers)
				raise ValueError(errorMessage)
		else:
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

	def getAnswerData(self):
		"""Returns tuple (id, answer), or list of tuples if ss-checkbox"""
		if self.type == "ss-checkbox" and self._answer is not None:
			tup = tuple()
			for answer in self._answer:
				tup += ((self.id, answer),)
			return tup
		else:
			return ((self.id, self._answer),)


def main():
	import FormParser
	url = "https://docs.google.com/forms/d/1jzDkEha066GwSCcSrCg1yaJJLpJAk0_aIFwf6GQgmmU/viewform"
	gForm = FormParser.GFParser(url)
	radio = gForm.questions.values()[0]
	# Testing GFQuestion
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

	print "All tests successful"


if __name__ == '__main__':
	main()