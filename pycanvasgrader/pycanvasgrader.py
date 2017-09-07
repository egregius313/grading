#!
"""
Automates the grading of programming assignments on Canvas.
MUST create an 'access.token' file in the same directory as this file with a valid Canvas OAuth2 token
"""

# built-ins
import py
import json

# 3rd-party
import requests

# globals
RUN_WITH_TESTS = True


class PyCanvasGrader:
    """
    A PyCanvasGrader object; responsible for communicating with the Canvas API
    """
    def __init__(self):
        self.token = self.authenticate()
        if self.token == 'none':
            print('Unable to retrieve OAuth2 token')
            exit()

        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer ' + self.token})

    @staticmethod
    def authenticate() -> str:
        """
        Responsible for retrieving the OAuth2 token for the session.
        :return: The OAuth2 token

        TODO Talk about "proper" OAuth2 authentication
        """

        with open('access.token', 'r', encoding='UTF-8') as access_file:
            for line in access_file:
                token = line.strip()
                if isinstance(token, str) and len(token) > 2:
                    return token
        return 'none'

    def courses(self, enrollment_type: str=None) -> list:
        """

        :param enrollment_type: teacher, student, ta, observer, designer
        :return: A list of the user's courses as dictionaries, optionally filtered by enrollment_type
        """
        url = 'https://canvas.instructure.com/api/v1/courses'
        if enrollment_type is not None:
            url += '?enrollment_type=' + enrollment_type

        r = self.session.get(url)
        response = json.loads(r.text)
        return response


def main():
    g = PyCanvasGrader()
    print(g.courses('ta'))


if __name__ == '__main__':
    if RUN_WITH_TESTS:
        py.test.cmdline.main()
    main()
