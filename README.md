# grading

This project is an automated system for wrapping test scripts with the ability to integrate with 
[Canvas](https://www.canvaslms.com/). This is done with the `pycanvasgrader.py` script.

## Skeletons

The grader is configured using files called _skeletons_. A skeleton is just a file in the `skeletons/`
folder, written in either TOML or JSON, which tells the grader the series of commands to run in order to
calculate the points for a submission.

A sample skeleton (written using the TOML forms) might look like:
```toml
# What the skeleton selection menu in the grader will call this skeleton
descriptor = "./hello tests"

# Disables the grader from committing to Canvas
disarm = true

[default]
# Defaults which all test cases will inherit unless overridden
command = "./hello"
exact_match = false
point_val = 5

[tests.compile]
command = "gcc"
args = ["%s", "-o", "hello"]
point_val = 10  # override the point_val from 5 to 10

[tests.joe]
args = ["joe"]
output_match = "Hello, Joe!"

[tests.world]
args = ["World"]
output_match = "Hello, World!"
```

## Set up / Configuration

The requirements to the PyCanvasGrader script are 
- [Python 3.6 interpreter](https://www.python.org/downloads/release/python-364/)
- A Canvas access token
  This can be found by going to `Account/Settings` in Canvas and going to the button that says
  `+ New Access Token`.

To set up the grader, clone this repository and then:
```bash
cd grading/pycanvasgrader
python3.6 -m venv .
source bin/activate
pip install -r requirements.txt
```

> __Note__: PyCanvasGrader works best with Python virtual environments. Make sure that you always
  have the virtualenv activated before running the PyCanvasGrader.

Then paste your token into a file named `access.token`, and then everything is installed.
Begin writing your [skeletons](#skeletons), and you'll be good to go.
