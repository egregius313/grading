import urllib2
import json
from subprocess import call
from subprocess import Popen
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
#print token

#url = 'https://api.github.com/orgs/StevensDeptECE/repos'

#req = urllib2.Request(url)
#req.add_header('Authorization', 'token %s' % token)
#res = urllib2.urlopen(req)
#data = json.load(res)

users = []

users = 'https://api.github.com/orgs/StevensDeptECE/repos'


call (["git", "pull"])
#output = subprocess.Popen(["git", "log" "--since=yesterday"], stdout=subprocess.PIPE).communicate()[0]
#print output

call(["git", "log", "--since=yesterday"])


#print users

