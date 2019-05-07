import datetime
from pymongo import MongoClient
import pymongo
import pprint
try:
	db = MongoClient("mongodb://localhost:27017")["hkust"]  
	f=0.05
	try:
		print("Querying Documents...")
		listOfCourseWithWaitingListSize = db.course.aggregate([	
			{ "$unwind": "$sections" },
			# { "$project": { "newProduct": {"$multiply": [f, "$sections.enrol"]}, "satisfied": satisfied} }, 
			# { "$project": { "compareResult": {"$gte": ["$sections.wait", "$newProduct"]}, "match_ts" : "$sections.recordTime"} },
			{"$match": #filter timeslot
				{"$and":[
					# {"compareResult": "true"},
					# {"satisfied" : "Yes"},
					#{"sections.sectionId": {"$ne": null}},
					#{"sections.sectionId": {"$exists": true}},
					# {"sections.sectionId": {"$regex": '^L'}},
					{"sections.recordTime": {"$gte": datetime.datetime.strptime("2018-01-26T14:00Z", "%Y-%m-%dT%H:%MZ")}},
					{"sections.recordTime": {"$lte": datetime.datetime.strptime("2018-02-01T11:30Z", "%Y-%m-%dT%H:%MZ")}}
					]
				}
			},
			{ "$project": 
				{"code": 1,
				"title": 1,
				"credits": 1,
				"sections":1,
				# "description":1,
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
					"sections":{"$last": "$sections"},
					"lecSatisfiedCount":{"$last": "$lecSatisfiedCount"}
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
		# pprint.pprint(listOfCourseWithWaitingListSize)
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

except pymongo.errors.ConnectionFailure as error: 
	print("Document Insertion Failed! Error Message: \"{}\"".format(error))


import numpy
import time
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
#Model 1
def trainModel(trainingDataFilename):
	# to set a seed of a random number generator used in the "optimization" tool in the neural network model
	numpy.random.seed(time.time())
	
	# Step 1: to load the data
	# Step 1a: to read the dataset with "numpy" function
	dataset = numpy.loadtxt(trainingDataFilename, delimiter=",")
	
	# Step 1b: to split the dataset into two datasets, namely the input attribute dataset (X) and the target attribute dataset (Y)
	X = dataset[:,0:4]
	Y = dataset[:,4]
	# Step 2: to define the model
	model = Sequential()
	model.add(Dense(13, input_dim=4, activation='relu'))
	model.add(Dense(7, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))
	# Step 3: to compile the model
	model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
	# Step 4: To fit the model
	model.fit(X, Y, validation_split=0.2, epochs=150, batch_size=10)
	# Step 5: To evaluate the model
	scores = model.evaluate(X, Y)
	print("Evaluation: ")
	print("{}: {}".format(model.metrics_names[1], scores[1]*100))
	
	return model

# model 2:
def trainModel2(trainingDataFilename):
	numpy.random.seed(time.time())
	dataset = numpy.loadtxt(trainingDataFilename, delimiter=",")
	X = dataset[:,0:4]
	Y = dataset[:,4]
	# Step 2: to define the model
	model = Sequential()
	model.add(Dense(10, input_dim=4, activation='relu'))
	model.add(Dense(10, activation='relu'))
	model.add(Dense(10, activation='relu'))
	model.add(Dense(10, activation='relu'))
	model.add(Dense(10, activation='relu'))
	model.add(Dense(10, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))
	# Step 3: to compile the model
	model.compile(loss='mean_squared_error', optimizer='sgd', metrics=["accuracy"])
	# Step 4: To fit the model
	model.fit(X, Y, validation_split=0.2, epochs=150, batch_size=10)
	scores = model.evaluate(X, Y)
	print("Evaluation: ")
	print("{}: {}".format(model.metrics_names[1], scores[1]*100))
	return model



# model 3:
def trainModel3(trainingDataFilename):
	numpy.random.seed(time.time())
	dataset = numpy.loadtxt(trainingDataFilename, delimiter=",")
	X = dataset[:,0:4]
	Y = dataset[:,4]
	# Step 2: to define the model
	model = Sequential()
	model.add(Dense(64, input_dim=4, activation='softmax'))
	model.add(Dense(1, activation='sigmoid'))
	# Step 3: to compile the model
	model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=["accuracy"])
	# Step 4: To fit the model
	model.fit(X, Y, validation_split=0.2, epochs=150, batch_size=10)
	scores = model.evaluate(X, Y)
	print("Evaluation: ")
	print("{}: {}".format(model.metrics_names[1], scores[1]*100))
	return model
# model 4:
def trainModel4(trainingDataFilename):
	numpy.random.seed(time.time())
	dataset = numpy.loadtxt(trainingDataFilename, delimiter=",")
	X = dataset[:,0:4]
	Y = dataset[:,4]
	# Step 2: to define the model
	model = Sequential()
	model.add(Dense(13, input_dim=4, activation='softmax'))
	model.add(Dense(7, activation='softmax'))
	model.add(Dense(1, activation='sigmoid'))
	# Step 3: to compile the model
	model.compile(loss='logcosh', optimizer='rmsprop', metrics=["accuracy"])
	# Step 4: To fit the model
	model.fit(X, Y, validation_split=0.3, epochs=300, batch_size=7)
	scores = model.evaluate(X, Y)
	print("Evaluation: ")
	print("{}: {}".format(model.metrics_names[1], scores[1]*100))
	return model
# model 5:
def trainModel5(trainingDataFilename):
	def trainModel5_beforeAddDrop(trainingDataFile_beforeAddDrop):
		numpy.random.seed(time.time())
		dataset = numpy.loadtxt(trainingDataFile_beforeAddDrop, delimiter=",")
		X = dataset[:,0:4]
		Y = dataset[:,4]
		# Step 2: to define the model
		model = Sequential()
		model.add(Dense(13, input_dim=4, activation='relu'))
		model.add(Dense(7, activation='relu'))
		model.add(Dense(1, activation='sigmoid'))
		# Step 3: to compile the model
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
		# Step 4: To fit the model
		model.fit(X, Y, validation_split=0.2, epochs=150, batch_size=10)
		scores = model.evaluate(X, Y)
		print("Evaluation: ")
		print("{}: {}".format(model.metrics_names[1], scores[1]*100))
		return model
	def trainModel5_afterAddDrop(trainingDataFile_afterAddDrop):
		numpy.random.seed(time.time())
		dataset = numpy.loadtxt(trainingDataFile_afterAddDrop, delimiter=",")
		X = dataset[:,0:4]
		Y = dataset[:,4]
		# Step 2: to define the model
		model = Sequential()
		model.add(Dense(13, input_dim=4, activation='relu'))
		model.add(Dense(7, activation='relu'))
		model.add(Dense(1, activation='sigmoid'))
		# Step 3: to compile the model
		model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
		# Step 4: To fit the model
		model.fit(X, Y, validation_split=0.2, epochs=150, batch_size=10)
		scores = model.evaluate(X, Y)
		print("Evaluation: ")
		print("{}: {}".format(model.metrics_names[1], scores[1]*100))
		return model
