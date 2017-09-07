"""
Unit tests for PyCanvasGrader
"""
# built-ins
import json

# 3rd-party
import requests

# package-specific
from .pycanvasgrader import PyCanvasGrader


class TestGrader:
    def test_authenticate(self):
        """
        Make sure the authentication function returns a valid key
        """
        token = PyCanvasGrader().authenticate()
        s = requests.Session()
        r = s.get('https://canvas.instructure.com/api/v1/courses', headers={'Authorization': 'Bearer ' + token})
        resp = json.loads(r.text)
        assert type(resp) == list and resp[0].get('id') is not None

    def test_courses(self):
        """
        Make sure that courses always returns a list
        """
        g = PyCanvasGrader()
        courses = g.courses('designer')
        assert type(courses) == list
