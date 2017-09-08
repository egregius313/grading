#!
"""
Automates the grading of programming assignments on Canvas.
MUST create an 'access.token' file in the same directory as this file with a valid Canvas OAuth2 token
"""

# built-ins
import py
import json
import re
import os
import subprocess
from zipfile import ZipFile

# 3rd-party
import requests

# globals
RUN_WITH_TESTS = False


class TestSkeleton:
    """
    An abstract skeleton to handle testing of a specific group of files
    """
    def __init__(self, commands: list, extensions: str=None, file_regex: str=None):
        """
        :param commands: A list of Command objects. These will be run in the order that they are added.
        :param extensions: Which file extensions this skeleton applies to
        :param file_regex: A regular expression to match files for this skeleton. Combines with extensions
        """
        if not any((extensions, file_regex)):
            raise ValueError('Either extensions or file_regex must be defined')
        self.commands = commands
        self.extensions = extensions
        self.file_regex = file_regex

    # TODO Create tests
    class Command:
        """
        An abstract command to be run in a console
        """
        def __init__(self, command: str, args: str, print_output: bool=True, output_match: str=None, output_regex: str=None, timeout: int=None):
            """
            :param command: The command to be run.
            :param args: The arguments to pass to the command. Use %s to denote the file name
            :param print_output: Whether to visibly print the output
            :param output_match: An exact string that the output should match. If this and output_regex are None, then this Command always 'matches'
            :param output_regex: A regular expression that the string should match. Combines with output_match.
            If this and output_match are None, then this Command always 'matches'
            :param timeout: Time, in seconds, that this Command should run for before timing out

            """
            self.command = command
            self.args = args
            self.output_match = output_match
            self.output_regex = re.compile(output_regex)
            self.print_output = print_output
            self.timeout = timeout

        def run(self):
            """
            Runs the Command
            :return: A dictionary containing its return code, stdout, and stderr
            """
            proc = subprocess.run([self.command, self.args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=self.timeout, encoding='UTF-8')
            return {'returncode': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}

        def run_and_match(self):
            """
            Runs the command and matches the output to the output_match/regex. If neither are defined then this always returns true
            :return: Whether the output matched or not
            """
            result = self.run()
            if self.print_output:
                print(result['stdout'])

            if not any((self.output_match, self.output_regex)):
                return True

            if self.output_match and self.output_match in result['stdout']:
                return True

            if self.output_regex.match(result['stdout']):
                return True
            return False

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


def main():
    # Initialize grading session and fetch courses
    grader = PyCanvasGrader()
    course_list = grader.courses('teacher')

    # Have user select course
    print('Choose a course from the following list:')
    for count, course in enumerate(course_list):
        print('%i.\t%s (%s)' % (count + 1, course.get('name'), course.get('course_code')))
    course_choice = choose_val(len(course_list)) - 1  # the plus and minus 1 are to hide the 0-based numbering

    print('Show only ungraded assignments? (y or n):')
    ungraded = choose_bool()
    course_id = course_list[course_choice].get('id')
    assignment_list = grader.assignments(course_list[course_choice].get('id'), ungraded=ungraded)

    # Have user choose assignment
    print('Choose an assignment to grade:')
    for count, assignment in enumerate(assignment_list):
        print('%i.\t%s' % (count + 1, assignment.get('name')))
    assignment_choice = choose_val(len(assignment_list)) - 1
    assignment_id = assignment_list[assignment_choice].get('id')

    # Remind user to get latest zip file
    print('If you haven\'t already, please download the most current submissions.zip for this assignment:\n' +
          assignment_list[assignment_choice].get('submissions_download_url'))

    input('\nPress enter when this you have placed this zip file into the /zips/ directory')

    # Have user choose zip
    invalid_zip = True
    user_file_dict = {}
    while invalid_zip:
        zip_list = []
        print('Choose a zip file to use:')
        sub = 0  # This is to keep indices visually correct while excluding non-zip files
        for count, zip_name in enumerate(os.listdir('zips')):
            if zip_name.split('.')[-1] != 'zip':
                sub += 1
                continue
            zip_list.append(zip_name)
            print('%i.\t%s' % (count - sub + 1, zip_name))  # Again, the plus and minus 1 are to hide the 0-based numbering

        selection = choose_val(len(zip_list)) - 1
        zip_file = zip_list[selection]

        user_file_dict = parse_zip(zip_file)
        if len(user_file_dict) > 0:
            invalid_zip = False
        else:
            print('This zip is invalid. Make sure you do not change the names inside the zip and try again')

    # Get list of submissions for this assignment
    submission_list = grader.submissions(course_id, assignment_id)
    if len(submission_list) < 1:
        print('There are no submissions for this assignment.')
        grader.close()
        main()
        exit(0)

    # Match the user IDs found in the zip with the IDs who submitted the assignment online
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
        print(str(user_data.get('name')) + '\t(%s)' % user_data.get('email'))

    input('Press enter to begin grading')

    print('done')


if __name__ == '__main__':
    if RUN_WITH_TESTS:
        py.test.cmdline.main()
    main()
