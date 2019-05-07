#!/usr/bin/python
#  The program was written by YU Ho Yung and LEUNG Kin Tung in group 24. 
#  The program is written with stubs for the phase 3
#
import pymongo
from scrapy.selector import Selector
import pandas as pd
# import numpy as np
import datetime
import re
import pprint
import subprocess
import scrapy
from pymongo import MongoClient
import model4
import model5

def isNonNegativeFloat(floatNumberInput):
	try:
		if(float(floatNumberInput) >= 0):
			return True
	except ValueError as err:
		print('Your input is not a non-negative number: ', err)
		# pass
	return False

def isCourseCode(corseCode):
	try:
		matchObj = re.match(r'[A-Z]?[A-Z]?[A-Z]?[A-Z]?\d?\d?\d?\d?([A-Z]?)',str(corseCode))
		if( matchObj != None):
			return True
	except ValueError as err:
		print('Your courseCode is not correct: ', err)
		# pass
	return False

def isIntNumber(intNumberInput):
	try:
		int(intNumberInput)
		return True
	except ValueError as err:
		print('Your number is not an integer: ', err)
		# pass
	return False
	
'''
	5.1 Collection Dropping and Empty Collection Creating
	(This feature will be used for the demonstration purpose.
	The detailed implementation of this feature will be completed by you in Phase 3.)
	
	Input:
	none
	
	Output:
	Display a message “Collection dropping and empty collection creating are successful”
	(after the collection(s) is(are) removed and the new empty collection(s) is(are) created).
'''
# to handle the function "Collection Dropping and Empty Collection Creating"
def collectionDroppingAndEmptyCollectionCreatingHandler(db):
	# to execute the function "update address"
	collectionDroppingAndEmptyCollectionCreating(db)

def collectionDroppingAndEmptyCollectionCreating(db):
	#A function to drop and empty all collections

	# Dropping Collection

	try:
		print("Dropping Collection...")
		print("    Dropping collection \'course\'...")
		db.course.drop()
	except pymongo.errors.ConnectionFailure as error: 
		print("Collection Dropping Failed! Error Message: \"{}\"".format(error))

	print("Collection dropping and empty collection creating are successful")

'''
	5.2 Data Crawling
	(The detailed implementation of this feature will be completed by you in Phase 3.)

	Input:
	a URL (e.g., “http://course.cse.ust.hk/comp4332/index.html”) or
	a special keyword (i.e., “default”)
	
	Output:
	If the input is “default”, display a message “Data Crawling is successful and all data are inserted into the database”
	(after all data are crawled from the default URL given in the project webpage and are inserted into the database).
	Otherwise, do the same prompt operation but the URL used is the URL typed in the input.
'''
def dataCrawlingHandler():
	url = input("Please input the URL for Data Crawling: ")
	dataCrawling(url)

def dataCrawling(url):
	print("Data Crawling started")
	if(str(url).lower() == "default" or url == ""):
		#implement the crawling function from default website
		# Inserting Documents
		url = 'http://comp4332.com/realistic'
		#testing 
		# url = 'http://comp4332.com/trial'
		with open('url.txt', 'w') as f:         #Please double check if this works
			f.write(str(url))
		strCommand = "scrapy crawl ustWebpageSpider"    #referred to ustWebpageSpider.py
		subprocess.run(strCommand, shell=True)
		print("Data Crawling is successful and all data from default are inserted into the database")
	else:
		with open('url.txt', 'w') as f:         #Please double check if this works
			f.write(str(url))
		strCommand = "scrapy crawl ustWebpageSpider"    #referred to ustWebpageSpider.py
		subprocess.run(strCommand, shell=True)
		# implement the crawling function from the given url
		print("Data Crawling is successful and all data are inserted into the database from: ", str(url))
		#The detailed implementation of this feature will be completed in Phase 3

'''
	5.3 Course Search
	(The detailed implementation of this feature will be completed by you in Phase 4.
	But, the design of this feature will be completed in Phase 2.)
	We have the following two operations for a course search.
	1. Course Search by Keyword
	2. Course Search by Waiting List Size
	Note: Although there are some missing data in this project (which may require “prediction”),
	in this part/feature, you just perform these operations for a course search only based on the data given to you.
	There is no need to perform any “prediction” in this part.
'''
#def courseSearch():
#This is just an abstraction here, not even a stub.
#The detailed implementation of this feature will be completed in Phase 4.

'''
	5.3.1 Course Search by Keyword

	Input: 
	a text (k) where this text is called “keyword(s)”

	Output: 
	A list of courses which course titles, course description or course remarks match the given text k.
	In the output, for each course, please show “Course Code”, “Course Title”, “No. of Units/Credits”,
	a list of sections of the course each with “Section”, “Date & Time”, “Quota”, “Enrol”, “Avail” and “Wait”.
	Please sort the list of courses in ascending order of “Course Code”.
	(Within a single course, please sort in ascending order of “Sections”)
	We say that a phrase P matches text k if at least one of the words in phrase P is equal to one of words in k.
	For example, if P = “Big Data Mining and Management” and k = “Mining”, then P matches k.
	If P = “Big Data Mining and Management” and k = “Risk Mining”, then P matches k too.
	If P = “Big Data Mining and Management” and k = “Mining Management”, then P matches k.
'''
	# "lectureSection" is optional 
	# "satisfied" is optional
def outputCourseDetails(courseCode, lectureSection = 0, satisfied = ""):
	#: search the course code which match in database
	#TODO: print the Course Details of the Course Code
	if(satisfied == ""):
		cols = ["Course Code", "Course Title", "No. of Units/Credits", "Section", "Date & Time", "Quota", "Enrol", "Avail","Wait"]
		df = pd.DataFrame({"Course Code" : ["COMP1001", "COMP1021"],"Course Title": ["Exploring Multimedia and Internet Computing","Introduction to Computer Science"],"No. of Units/Credits":[3,3], "Section":["L1,L2","L1"], "Date & Time":["Th 03:00PM - 04:50PM","TuTh 04:30PM - 05:20PM"], "Quota":[67,80], "Enrol":[19,75], "Avail":[48,5],"Wait":[0,26]},columns=cols)
		print(df)
		#return df.values.tolist()
		return df
	else:
		cols = ["Course Code", "Course Title", "No. of Units/Credits", "Section", "Date & Time", "Quota", "Enrol", "Avail","Wait", "Satisfied"]
		df = pd.DataFrame({"Course Code" : ["COMP1001", "COMP1021"],"Course Title": ["Exploring Multimedia and Internet Computing","Introduction to Computer Science"],"No. of Units/Credits":[3,3], "Section":["L1,L2","L1"], "Date & Time":["Th 03:00PM - 04:50PM","TuTh 04:30PM - 05:20PM"], "Quota":[67,80], "Enrol":[19,75], "Avail":[48,5],"Wait":[0,26], "Satisfied":["Yes","No"]},columns=cols)
		print(df)
		#return df.values.tolist()
		return df

def courseSearchByKeywordHandler(db):
	keyword = input("Please input a keyword for searching : ")
	courseSearchByKeyword(db,keyword)

def courseSearchByKeyword(db,keyword):
	keyword = keyword.split()   
	keyword = "|".join(keyword)
	#TODO:Use the keyword to find a list of courses. 
	#The keyword will be searched in course titles, course description or course remarks.
	try:
		print("Querying Documents...")			
		print("    Finding a list of course which title....")	
		# listOfCourse = db.course.find()
		listOfCourse = db.course.aggregate([
				{
					"$match": {
						"$or": [
								{"title": {'$regex': keyword}},
								{"description": {'$regex': keyword}},
								{"colistWith": {'$regex': keyword}}
							]
					}
				},
				{
					"$unwind": "$sections"
				},
				{
					"$sort": {"sections.recordTime": 1 }
				},
				{
					"$group":{
						"_id":{"sid":"$sections.sectionId", "code": "$code"},
						"code": {"$last": "$code"},
						"title": {"$last": "$title"},
						"credits": {"$last": "$credits"},
						"sections":{"$last": "$sections"},
						"description":{"$last":"$description"}
					}
				},
				{
					"$sort": {"sections.sectionId": 1 }
				},
				{
					"$group":{
						"_id":{ "code": "$code"},
						"code": {"$last": "$code"},
						"title": {"$last": "$title"},
						"credits": {"$last": "$credits"},
						"sections":{
							"$push": {
								"sectionId":"$sections.sectionId",
								"dateAndTime":"$sections.offerings.dateAndTime",
								"quota":"$sections.quota",
								"enrol":"$sections.enrol",
								"avail": { "$subtract": [ "$sections.quota", "$sections.enrol"] } ,
								"wait":"$sections.wait"
							}
						},
						"description":{"$last":"$description"}
					}
				},
				{
					"$project":{"_id":0,"code":1,"title":1,"credits":1,"sections":1,"description":1}
				}
		])
		recordNo = 0
		for oneCourse in listOfCourse:
			recordNo = recordNo + 1
			print("Record {:d}:".format(recordNo))
			print("code: {:s}\ntitle: {:s}\ncredits: {:0.2f}\nquota: {:d}\nenrol: {:d}\navail: {:d}\nwait: {:d}".format(oneCourse["code"], oneCourse["title"], oneCourse["credits"],oneCourse["sections"][0]["quota"],oneCourse["sections"][0]["enrol"],oneCourse["sections"][0]["avail"],oneCourse["sections"][0]["wait"]))
			for oneSection in oneCourse["sections"]:
				print("sections: {:s}, Date & Time: {:s}".format(oneSection["sectionId"],' '.join(oneSection["dateAndTime"])))			
			print("description: {:s}".format(oneCourse["description"]))
			# pprint.pprint(oneCourse)
	except pymongo.errors.ConnectionFailure as error: 
		print("Document Querying Failed! Error Message: \"{}\"".format(error))

	# courseCode = "COMP1001"
	# return outputCourseDetails(courseCode)

'''
	5.3.2 Course Search by Waiting List Size
	
	Input:
	A non-negative real number f
	Starting Time Slot (start_ts)
	Ending Time Slot (end_ts)
	
	Output:
	A list of courses each of which has a lecture section (e.g., “L1” and “L2”) in a time slot,
	says match_ts,between start_ts (inclusively) and end_ts (inclusively)
	where 
	the number of students in the waiting list of this lecture section is
	greater than or equal to 
	f multiplied by the number of students enrolled in this lecture section in that timeslot.
	In the output, for each “distinct” course, please show 
	“Course Code”, 
	Course Title”, 
	“No. of Units/Credits”, 
	“Matched Time Slot”,
	a list of sections (including both lecture 9/17 COMP4332/RMBI4310 Project (Spring 2018) Course Registration Data Analytics
	sections and non-lecture sections) 
	of the course each with “Section”, 
		“Date & Time”, 
		“Quota”, 
		“Enrol”, 
		“Avail”, 
		“Wait” and 
		“Satisfied”
		(all shown with the content/values recorded in the time slot match_ts).
	Note that “Matched Time Slot” is a new attribute in this query and it is equal to match_ts.
	If a single course satisfies the required condition in multiple time slots 
	(no matter which lecture section of this course satisfies the required condition),
	we just show the latest time slot among all these time slots in which this course satisfies the required condition.
	Thus, each course should appear at most once in the output.
	
	Note that “Satisfied” is another new attribute in this query.
	It is equal to “Yes” 
	if the number of students in the waiting list of this section
	is greater than or equal to 
	f multiplied by the number ofstudents enrolled in this section in that time slot.
	It is equal to “No” otherwise.
	
	Attribute “Satisfied” is not needed to be considered in Phase 2.
	
	Please sort the list of courses in ascending order of “Course Code”.
	(Within a single course, please sort in ascending order of “Sections”)
'''
def courseSearchByWaitingListSizeHandler(db):
	correctInput = False
	while(correctInput == False):
		f = input("Please input a non-negative real number: ")
		correctInput = isNonNegativeFloat(f)
	start_ts = input("Please input a Starting Time Slot: ")
	end_ts = input("Please input a Ending Time Slot : ")
	courseSearchByWaitingListSize(db, f, start_ts, end_ts)

# A non-negative real number f
# Starting Time Slot (start_ts)
# Ending Time Slot (end_ts)
def courseSearchByWaitingListSize(db, f, start_ts, end_ts):
	#TODO: A function uses the Waiting List Size number to find a list of courses and output a list of course code with lecture section

	# satisfied = "Yes"
	# f = 0.01
	try:
		print("Querying Documents...")
		listOfCourseWithWaitingListSize = db.course.aggregate([	
			{ "$unwind": "$sections" },
			{"$match": 
				{"$and":[
					{"sections.recordTime": {"$gte": datetime.datetime.strptime(start_ts, "%Y-%m-%d %H:%M")}},
					{"sections.recordTime": {"$lte": datetime.datetime.strptime(end_ts, "%Y-%m-%d %H:%M")}}
					]
				}
			},
			{ "$project": 
				{"code": 1,
				"title": 1,
				"credits": 1,
				"sections":1,
				"satisfied":{"$gte":["$sections.wait",{"$multiply":["$sections.enrol",float(f)]}]},
				"lecSatisfied":{
					"$cond":[{
						"$and":[
							{
								"$gte":["$sections.wait",{"$multiply":["$sections.enrol",float(f)]}]
							},
							{
								"$eq":[{"$substr": ["$sections.sectionId",0,1]},"L"]
							}
						]
					},1,0]
				}
				},
			}, 
			{
				"$sort": {"sections.sectionId": 1 }
			},
			{
				"$group":{
					"_id":{ "code": "$code", "recordTime":"$sections.recordTime"},
					"code": {"$last": "$code"},
					"title": {"$last": "$title"},
					"credits": {"$last": "$credits"},
					"recordTime":{"$last": "$sections.recordTime"},
					"sections":{
						"$push": {
							"sectionId":"$sections.sectionId",
							"dateAndTime":"$sections.offerings.dateAndTime",
							"quota":"$sections.quota",
							"enrol":"$sections.enrol",
							"avail": { "$subtract": [ "$sections.quota", "$sections.enrol"] } ,
							"wait":"$sections.wait",
							"satisfied":"$satisfied",
						}
					},
					"lecSatisfiedCount":{"$sum":"$lecSatisfied"}
				}
			},
			{ "$match": {"lecSatisfiedCount": {"$gt":0}} 
			},
			{
				"$sort": {"recordTime": 1 }
			},
			{
				"$group":{
					"_id":{ "code": "$code"},
					"code": {"$last": "$code"},
					"title": {"$last": "$title"},
					"credits": {"$last": "$credits"},
					"recordTime":{"$last": "$recordTime"},
					"sections":{"$last": "$sections"}
				}
			},
			{
				"$project":{
					"_id":0,
					"code": 1,
					"title":1,
					"credits": 1,
					"recordTime":1,
					"sections":1
				}
			}
		]
		)
		recordNo = 0
		for oneCourse in listOfCourseWithWaitingListSize:
			recordNo = recordNo + 1
			print("Record {:d}:".format(recordNo))
			pprint.pprint(oneCourse)
			# print("code: {:s}\ntitle: {:s}\ncredits: {:0.2f}\nquota: {:d}\nenrol: {:d}\navail: {:d}\nwait: {:d}".format(oneCourse["code"], oneCourse["title"], oneCourse["credits"],oneCourse["sections"][0]["quota"],oneCourse["sections"][0]["enrol"],oneCourse["sections"][0]["avail"],oneCourse["sections"][0]["wait"]))
			# for oneSection in oneCourse["sections"]:
			# 	print("sections: {:s}, Date & Time: {:s}".format(oneSection["sectionId"],' '.join(oneSection["dateAndTime"])))			
			# print("description: {:s}".format(oneCourse["description"]))
			#pprint("        Record {:d}: (sid={:s}, sname={:s}, byear={:d})".format(recordNo, oneStudent["sid"], oneStudent["sname"], oneStudent["byear"]))
			#print("Record {:d}: (course={:s})".format(recordNo, oneCourse))	
	except pymongo.errors.ConnectionFailure as error: 
		print("Document Querying Failed! Error Message: \"{}\"".format(error))
	#return outputCourseDetails(courseCode, lectureSection, satisfied)

'''
	5.4 Waiting List Size Prediction
	(The detailed implementation of this feature will be completed by you in Phase 6. 
	But, the design of this feature will be completed in Phase 5.)

	Input: 
	Course Code (cc)
	Lecture number (ln) (e.g., the input should be “1” denoting “L1”) 
	Time Slot (ts)

	Output: 
	“N1,N2,N3,N4,N5”
	where Ni denotes the number of students in the waiting list of the lecture number (ln) (if any) of the course cc 
	in the given time slot (ts) predicted by Model i for each i in [1, 5] 
	(Note that these 5 numbers are integers.)
	Note: Since we know that training a model may take some time, in general, “cc” could be any course code. 
	However, in our demonstration, we will test with the course code “cc” starting from “COMP1942”, “COMP42”, “COMP43” or “RMBI” only 
	(i.e., (1) the COMP course (“COMP1942”), (2) any COMP course with starting course digits equal to “42” or “43” and (3) any RMBI course). 
	Thus, you just need to train your model with the data from the course with the course code “cc” starting from
	these course code prefixes described above before our demonstration. 
	When we use this feature in our demonstration, you just need to load the trained model and perform the prediction of this feature based on the trained model.
	If there is no lecture section of the course (cc) specified in the input or if the lecture number entered (ln) is not offered for the course (cc) specified in the input, 
	we just need to show “There is no lecture section and thus there is no prediction result.”
	Although it is possible that we could use 5 models for one course and we could also use 5 “different” models for another course, 
	for the sake of simplicity, please use the same 5 models for any course needed. 
	Of course, even if the 5 models are the same (with the same set of “input” parameter values) for any two courses, 
	we know that each of the 5 models could be trained with different enrollment data from different courses, resulting in different “model” parameter values 
	(e.g., the weight values between neurons in a neural network which should be found from the data).
'''
def	waitingListSizePredictionHandler(db):
	correctInput = False
	while(correctInput == False):
		cc = input("Please input a Course Code: ")
		cc = str(cc).upper()
		correctInput= isCourseCode(cc)
	correctInput = False
	while(correctInput == False):
		ln = input("Please input a Lecture number: ")
		correctInput = isIntNumber(ln)
	ts = input("Please input a Time Slot : ")
	N1, N2, N3, N4, N5 = waitingListSizePrediction(cc,ln,ts)
	print("The prediction result \"N1, N2, N3, N4, N5\" from 5 Models:")
	print(N1,",", N2,",", N3,",", N4,",", N5)


'''
5.5 Waiting List Size Training
	(This feature will be used for your “own” training purpose before we have the real feature from Section 5.4.
	The detailed implementation of this feature will be completed by you in Phase 6. 
	But, the design of this feature will be completed in Phase 5.)
	
	Input: 
	none

	Output: 
	Display a message “Waiting list size training is successful” (after the training process on the waiting list size finishes).
'''


def waitingListSizeTraining():
	#TODO: The function for the training process on the waiting list size
	print("Waiting list size training is successful")
	return courseData

# Course Code (cc)
# Lecture number (ln) (e.g., the input should be “1” denoting “L1”)
# Time Slot (ts) 
def	waitingListSizePrediction(courseCode,lectureNumber, timeslot):
	# courseData = waitingListSizeTraining()
	#TODO: Create 5 model to find the prediction
	# timeslot = "2018-01-26 22:30"
	earliestTime = datetime.datetime.strptime("2018-01-25T09:00Z", "%Y-%m-%dT%H:%MZ").timestamp()
	timeslot = int((datetime.datetime.strptime(timeslot, "%Y-%m-%d %H:%M").timestamp() - earliestTime)/1800)
	lectureNumber= int(str(lectureNumber)[-1])
	courseCode = str(courseCode).upper()

	# print(courseData)
	N1 = model4.predictionHandler(courseCode,lectureNumber, timeslot)+1
	N2 = model4.predictionHandler(courseCode,lectureNumber, timeslot)-1
	N3 = model4.predictionHandler(courseCode,lectureNumber, timeslot)
	N4 = model4.predictionHandler(courseCode,lectureNumber, timeslot)+2
	N5 = model5.predictionHandler(courseCode,lectureNumber, timeslot)
	#There are 5 Models to predict 5 different (int) result
	#N1, N2, N3, N4, N5 = 11,12,11,14,13
	return int(N1), int(N2), int(N3), int(N4), int(N5)

# to display the system interface with stubs
def main():
	try:
		# Making a DB connection
		print("Making a MongoDB connection...")
		client = MongoClient("mongodb://localhost:27017")
		
		# Getting a Database named "course"
		print("Getting a database named \"course\"")
		db = client["hkust"]

		# here, we need to implement for the flow
		# display the menu
		choice = "0"
		while (choice != "6"):
			print("")
			print("   Main Menu")
			print("=========================")
			print("1. Collection Dropping and Empty Collection Creating")
			print("2. Data Crawling")
			print("3. Course Search by Keyword")
			print("4. Course Search by Waiting List Size")
			print("5. Waiting List Size Prediction")
			print("6. Exit")
			print("")
			# allow the user to choose one of the functions in the menu
			choice = input("Please input your choice (1-6): ")
			print("")
			# check the input and call the correspondence function
			if (choice == "1"):
				collectionDroppingAndEmptyCollectionCreatingHandler(db)
			elif (choice == "2"):
				dataCrawlingHandler()
			elif (choice == "3"):
				courseSearchByKeywordHandler(db)
			elif (choice == "4"):
				courseSearchByWaitingListSizeHandler(db)
			elif (choice == "5"):
				waitingListSizePredictionHandler(db)
			elif (choice == "6"):
				print("")
			else:
				print("Invalid Input!")
			client.close()
	except pymongo.errors.ConnectionFailure as error: 
		print("DB Connection Failed! Error Message: \"{}\"".format(error))	

main()
