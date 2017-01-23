import urllib2
import json
from subprocess import call
import sys

course = sys.argv[1]
assignment = sys.argv[2]
index = course + '-' + assignment + '-'
print index

token = '002fa44e635bdcba526e69f5130f117abc6f1349'

url = 'https://api.github.com/orgs/StevensDeptECE/repos'

req = urllib2.Request(url)
req.add_header('Authorization', 'token %s' % token)
res = urllib2.urlopen(req)
data = json.load(res)


repoNames = []
repoIDs = []
repoClone = []
for repo in data:
	repoNames.append(str(repo['name']))
	repoIDs.append(str(repo['name']))
	repoClone.append(str(repo['clone_url'][8:]))

users = []
dirNames = []
for i in range(0, len(repoClone)):
	if index in repoClone[i]:
		cmd = 'https://%s@%s' % (token, repoClone[i])
		call(["git", "clone", cmd])
		dirNames.append(repoNames[i])
		users.append(repoNames[i].replace(index, ''))
		
		#Grade here
		#research multithreading
		
print users
print dirNames

	
'''	
cmd = 'https://%s%s' % (token, repoClone[7])
call(["git", "clone", repoClone[7]])
call([token])
'''
'''
with open('jsonOut.json', 'w') as outfile:
    json.dump(data, outfile)
'''
