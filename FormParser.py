import urllib2
from bs4 import BeautifulSoup



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