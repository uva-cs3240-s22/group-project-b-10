'''  Requests module does not ship natively with Python! '''
import requests
import json
import models

def get():
	url = 'https://api.devhub.virginia.edu/v1/courses'
	data = requests.get(url).json()
	return data
	
class_list = get()['class_schedules']['records']
# print(class_list)
previous_course_title = ""
for c in class_list:
	# print(c)
	if c[-1] == "2022 Spring":
		course_title = str(c[0])+ ' ' +str(c[1])+'-'+str(c[2])+': '+str(c[4])
		if (course_title != previous_course_title):
			course.create().set_title(course_title)