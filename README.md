# PyGoogleForm
A simple Python library to submit Google Forms in Python.

The goal is to be able to submit Google Forms from anything else than a web page (a Desktop app, or any device that doesn't use a browser).

## Installation

Clone the repository or install via PyPI (coming soon).

## How to use

First, create your form in Google Form, and then click "view live form". Then in your code:

```python
import PyGoogleForm
# Use the url of the page to initialize the GFParser
url = "https://docs.google.com/forms/d/1jzDkEha066GwSCcSrCg1yaJJLpJAk0_aIFwf6GQgmmU/viewform"
gForm = PyGoogleForm.GFParser(url)

# Get the questions by IDs
questionIDs = gForm.getQuestionIDs()
question1 = gForm.getQuestionInfo(questionIDs[0])
# question1 == [ID, type, question text, [possible choices]]

# Answering a question
gForm.answerQuestion(question[0], "ok")

# Finally, submit the form
gForm.submit()
```

## Limitations

* can handle only basic types: radio, select, checkbox, text, paragraph text
* doesn't support "required" answers. The form is submitted and the answer recorded in the answer sheet

## Licence
The project uses a permissive MIT Licence. Do whatever you want with it.

## Resource

Special thanks to [Kristler on Reddit](https://www.reddit.com/r/learnprogramming/comments/32xd4s/how_can_i_use_python_to_submit_a_google_form_or/cqfvj4m) for the inspiration.
