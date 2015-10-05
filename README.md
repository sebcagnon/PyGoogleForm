# PyGoogleForm
A simple Python library to submit Google Forms in Python.

The goal is to be able to submit Google Forms from anything else than a web page (a Desktop app, or any device that doesn't use a browser).

## Installation

Clone the repository or install via PyPI (coming soon).

## How to use

1. Create your form in Google Form, and then click "view live form"
2. Use the url of the page to initialize the GFParser

   ```python
   import PyGoogleForm
   url = "https://docs.google.com/forms/d/1jzDkEha066GwSCcSrCg1yaJJLpJAk0_aIFwf6GQgmmU/viewform"
   gForm = PyGoogleForm.GFParser(url)
   ```

3. Get the questions by IDs
   ```python
   questionIDs = gForm.getQuestionIDs()
   question1 = gForm.getQuestionInfo(questionIDs[0])
   ```

4. Answer the question
   ```python
   # question type
   question1[1]
   # question text
   question[2]
   # for radio, select or checkboxes, list of choices
   question[3]
   gForm.answerQuestion(question[0], "ok")
   ```

5. After answering all questions, submit the form
   ```python
   gForm.submit()
   ```

## Limitations

* can handle only basic types: radio, select, checkbox, text, paragraph text
* doesn't support "required" answers. The form is submitted and the answer recorded in the answer sheet

## Licence
The project uses a permissive MIT Licence. Do whatever you want with it.

## Resource

Special thanks to [Kristler on Reddit](https://www.reddit.com/r/learnprogramming/comments/32xd4s/how_can_i_use_python_to_submit_a_google_form_or/cqfvj4m) for the inspiration.
