'''  Requests module does not ship natively with Python! '''
import requests
import json
# import .models

def get():
	url = 'https://api.devhub.virginia.edu/v1/courses'
	data = requests.get(url).json()
	return data

class_list = get()['class_schedules']['records']
for c in class_list:
	# print(c)
	if c[-1] == "2022 Spring":
		course_info = str(c[0])+ ' ' +str(c[1])+'-'+str(c[2])
		course_title = str(c[4])
		# print(course_info)
		course.create().set_title(course_title)
