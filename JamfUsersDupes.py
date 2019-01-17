import requests
import xml.etree.ElementTree as ET
import csv
import os
import pandas as pd

# make a GET request to pull all users from Jamf, set env vars before running script and change url to your server
url = "https://<your jamf server>.jamfcloud.com/JSSResource/users"
username = os.environ['jamf_username']
password = os.environ['jamf_pw']
auth = (username,password)

response = requests.get(url, auth=auth)
print(response.status_code)

# check for good status_code
if response.status_code == 200:
	root = ET.fromstring(response.text)

	# open a file for writing
	all_users = open(os.path.expanduser('~/Desktop/AllJamfUsers.csv'), 'w')

	# create the csv writer object
	csvwriter = csv.writer(all_users)
	users_head = []

	count = 0
	for users in root.findall('user'):
		user = []
		if count == 0:
			name = users.find('name').tag
			users_head.append(name)
			id = users.find('id').tag
			users_head.append(id)
			csvwriter.writerow(users_head)
			count = count + 1

		name = users.find('name').text
		user.append(name)
		id = users.find('id').text
		user.append(id)
		csvwriter.writerow(user)

	# save the csv of All Jamf Users
	all_users.close()
	print('AllJamfUsers.csv created on desktop')

else:
	print('bad status code of', response.status_code)
	quit('quitting script')

# read the csv of All Jamf Users
users = pd.read_csv(os.path.expanduser('~/Desktop/AllJamfUsers.csv'))
users.shape

# check if there are duplicates, sort, write to csv
if users.name.duplicated().any() == True:
	users_dupes = users[users.name.duplicated(keep = False)]
	dupes_sort = users_dupes.sort_values(by=['name'])
	dupes_sort.to_csv(os.path.expanduser('~/Desktop/DupeJamfUsers.csv'), index=False)
	print('DupeJamfUsers.csv created on desktop')
else:
	print('no duplicate names found in user list')	
