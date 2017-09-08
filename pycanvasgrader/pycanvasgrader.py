#!
"""
Automates the grading of programming assignments on Canvas.
MUST create an 'access.token' file in the same directory as this file with a valid Canvas OAuth2 token
"""

# built-ins
import py
import json
import os
from zipfile import ZipFile

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

    def close(self):
        self.session.close()

    def courses(self, enrollment_type: str=None) -> list:
        """
        :param enrollment_type: (Optional) teacher, student, ta, observer, designer
        :return: A list of the user's courses as dictionaries, optionally filtered by enrollment_type
        """
        url = 'https://canvas.instructure.com/api/v1/courses'
        if enrollment_type is not None:
            url += '?enrollment_type=' + enrollment_type

        response = self.session.get(url)
        return json.loads(response.text)

    def assignments(self, course_id: int, ungraded: bool=True) -> list:
        """
        :param course_id: Course ID to filter by
        :param ungraded: Whether to filter assignments by only those that have ungraded work. Default: True
        :return: A list of the course's assignments
        """
        url = 'https://canvas.instructure.com/api/v1/courses/' + str(course_id) + '/assignments'
        if ungraded:
            url += '?bucket=ungraded'

        response = self.session.get(url)
        return json.loads(response.text)

    def submissions(self, course_id: int, assignment_id: int) -> list:
        """
        :param course_id: The ID of the course containing the assignment
        :param assignment_id: The ID of the assignment
        :return: A list of the assignment's submissions
        """
        url = 'https://canvas.instructure.com/api/v1/courses/' + str(course_id) + '/assignments/' + str(assignment_id) + '/submissions'

        response = self.session.get(url)
        return json.loads(response.text)

    def user(self, user_id: int) -> dict:
        """
        :param user_id: The ID of the user
        :return: A dictionary with the user's information
        """
        url = 'https://canvas.instructure.com/api/v1/users/' + str(user_id)

        response = self.session.get(url)
        return json.loads(response.text)


def parse_zip(zip_file: str) -> dict:
    """
    Maps file names to user IDs from a zip of downloaded Canvas submissions
    :param zip_file: The name of the zip file to parse
    :return: if the zip can be parsed, a dictionary containing the user ID's mapped to the parsed file name, otherwise an empty dict
    """
    user_dict = {}

    with ZipFile('zips/' + zip_file, 'r') as z:
        for name in z.namelist():
            if name.count('_') < 3:
                print('Skipping file: ' + name + '. Invalid filename')
            else:
                (name, user_id, unknown, file) = name.split('_', maxsplit=3)
                user_dict[user_id] = file
    if len(user_dict) < 1:
        print('Unable to read any files from the zip. Please check the file and try again')
    return user_dict


def choose_val(hi_num: int) -> int:
    val = 'none'
    while not str.isdigit(val) or (int(val) > hi_num or int(val) <= 0):
        val = input()
    return int(val)


def choose_bool() -> bool:
    val = 'none'
    while not str.lower(val) in ['y', 'n', 'yes', 'no']:
        val = input()
    if val in ['y', 'yes']:
        return True
    else:
        return False


def choose_zip() -> str:
    name = input()
    if name[-4:] != '.zip':
        name += '.zip'
    if not os.path.isfile('zips/' + name):
        print('Could not find the file. Make sure it is in the zips directory and try again:')
        return choose_zip()
    else:
        return name


def main():
    grader = PyCanvasGrader()
    course_list = grader.courses('teacher')

    print('Choose a course from the following list:')
    for count, course in enumerate(course_list):
        print('%i.\t%s (%s)' % (count + 1, course.get('name'), course.get('course_code')))

    course_choice = choose_val(len(course_list)) - 1

    print('Show only ungraded assignments? (y or n):')
    ungraded = choose_bool()

    course_id = course_list[course_choice].get('id')
    assignment_list = grader.assignments(course_list[course_choice].get('id'), ungraded=ungraded)

    print('Choose an assignment to grade:')
    for count, assignment in enumerate(assignment_list):
        print('%i.\t%s' % (count + 1, assignment.get('name')))

    assignment_choice = choose_val(len(assignment_list)) - 1
    assignment_id = assignment_list[assignment_choice].get('id')
    print('If you haven\'t already, please download the most current submissions.zip for this assignment:\n' +
          assignment_list[assignment_choice].get('submissions_download_url'))

    invalid_zip = True
    user_file_dict = {}
    while invalid_zip:
        print('Place the zip in the \'zips\' directory, and then enter the zip\'s name here:')
        zip_file = choose_zip()

        user_file_dict = parse_zip(zip_file)
        if len(user_file_dict) > 0:
            invalid_zip = False

    submission_list = grader.submissions(course_id, assignment_id)
    if len(submission_list) < 1:
        print('There are no submissions for this assignment.')
        grader.close()
        main()
        exit(0)

    user_submission_dict = {}
    for user_id, filename in user_file_dict.items():
        for submission in submission_list:
            if user_id in str(submission.get('user_id')):
                user_submission_dict['user_id'] = submission['id']

    if len(user_submission_dict) < 1:
        print('Could not match any file names in the zip to any online submissions.')
        grader.close()
        main()
        exit(0)

    print('Successfully matched %i submission(s) to files in the zip file. Is this correct? (y or n):' % len(user_submission_dict))
    correct = choose_bool()
    if not correct:
        grader.close()
        main()
        exit(0)

    print('Students to grade: [Name (email)]')
    for user_id in user_submission_dict:
        user_data = grader.user(user_id)
        print(str(user_data.get('name')) + '(%s)' % user_data.get('email'))

    input('Press enter to begin grading')

    print('done')


if __name__ == '__main__':
    if RUN_WITH_TESTS:
        py.test.cmdline.main()
    main()
