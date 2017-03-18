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
file = open(home + "\\LMS640\\github.tok","r")
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
	
i = 0

f = open("8th Week.txt",'w')
sys.stdout = f

Users = ["mperrelli", "xinyuliu679", "ghostqu", "kanbd", "mattmelachrinos", "dillonguarino", "VCneverdie", "stRAWRberry", "cbean03", "lzhu1992", "Daniel0729", "xiyukuangdaoke", "CyanideTD", "FUJICJK", "ybai8", "soberkiller", "Yliuinstevens","yzhan90top", "bhavitha590", "YuYu12", "sihanwang94", "zbinger", "hxiao3", "chunyiguo", "dippanpatel"]

print	"Date: 8th Week"

for	User	in	Users:
	#print	i
	author = "--author=" + Users[i]
	with	open('test.log', "w")	as	outfile:
		subprocess.call(["git","log",author, "-p",'--since="3/11/2017"','--until="3/17/2017"'], stdout=outfile)
#call(["git", "log", "-p", ">test.log"])

	countCommit	=	0
	countLine	=	0
	file	=	open("test.log","r")
	gitlog	=	file.read()
	file.close()
	gitlines = gitlog.splitlines()
#print gitlines

	for	line	in	gitlines:
	#print line
		if	"commit"	in	line:
			countCommit	= countCommit	+	1
		#if	"Author"	in	line:
			#print	line
		#if	"Date"	 in	line:
			#print	line
		if	line.startswith('+')	or	('-'):
			countLine	= countLine	+	1
	
	print	"Author: %s"%Users[i]
	print	"Commit:	%d"%countCommit
	print	"Lines:	%d"	%countLine
	i	=	i	+	1

f.close()
#with open("output.txt", "w") as output:
 #   subprocess.call(["python", "reportUsers.py"], stdout=output)