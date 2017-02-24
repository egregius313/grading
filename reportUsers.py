import urllib2
import json
import subprocess
from subprocess import call
import sys
import os

#course = sys.argv[1]
#assignment = sys.argv[2]
#index = course + '-' + assignment + '-'
#print index

home = os.environ['HOME']
file = open(home + "/github.tok","r")
token = file.read()
file.close() 

repo = "LMS640"

userUrl = 'https://api.github.com/repos/StevensDeptECE/LMS640/collaborators'
req = urllib2.Request(userUrl)
req.add_header('Authorization', 'token %s' % token)
res = urllib2.urlopen(req)
users = json.load(res)

userid = []
for user in users:
    userid.append(user['login'])

#for u in userid:
#    call(["git", "log", '--since="yesterday"', "--author=" + u])

#call(["git", "log", '--since="yesterday"'])

with open('test.log', "w") as outfile:
    subprocess.call(["git", "log", "-p"], stdout=outfile)
#call(["git", "log", "-p", ">test.log"])

file = open("test.log","r")
gitlog = file.read()
file.close()
gitlines = gitlog.splitlines();
for line in gitlines:
    print line[0:2]
