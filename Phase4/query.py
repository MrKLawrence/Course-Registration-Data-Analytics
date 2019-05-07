#!/usr/bin/python
#
#  The program was written by Raymond WONG.
#  The program is used for illustrating how to connect MongoDB in Python (using PyMongo)
#
#  Remember to start the MongoDB server before you run this Python script
#
from pymongo import MongoClient
import pymongo

# Creating Collection
def createCollection(db):
	print("Creating Collection...")
	print("    In MongoDB, there is no need to create a collection explicitly (e.g., \'db.createCollection(\"student\")\').")
	print("    When we insert the first document into a collection, the collection will be created automatically.")

# Inserting Documents
def insertDocument(db):
	try:
		print("Inserting Documents...")
		print("   Inserting Document 1")
		db.student.insert(
		{
			"sid": "12345678",
			"sname": "Raymond",
			"byear": 1998
		}
		)
		
		print("   Inserting Document 2")
		db.student.insert( 
		{
			"sid": "87654321",
			"sname": "Peter Chen",
			"byear": 1997
		}  
		)

		print("   Inserting Document 3")
		db.student.insert( 
		{
			"sid": "12341234",
			"sname": "Mary Lau",
			"byear": 1999
		}  
		)

		print("   Inserting Document 4")
		db.student.insert( 
		{
			"sid": "56785678",
			"sname": "David Lee",
			"byear": 1998
		}  
		)
		
		print("   Inserting Document 5")
		db.student.insert( 
		{
			"sid": "88888888",
			"sname": "Test Test",
			"byear": 1998
		}  
		)
	except pymongo.errors.ConnectionFailure as error: 
		print("Document Insertion Failed! Error Message: \"{}\"".format(error))

	
# Updating Documents
def updateDocument(db):
	try:
		print("Updating Documents...")
		print("    Updating the birth year of the student with sid = 12345678 to 2008...")
		db.student.update_many({"sid": "12345678"}, {"$set":{"byear":2008}})
	except pymongo.errors.ConnectionFailure as error: 
		print("Document Update Failed! Error Message: \"{}\"".format(error))

# Querying Documents
def queryDocument(db):
	try:
		print("Querying Documents...")
		
		print("    Finding a list of students whose birth years are 1998 (using \'find\')....")
		listOfStudent = db.student.find({"byear":1998})
		recordNo = 0
		for oneStudent in listOfStudent:
			recordNo = recordNo + 1
			print("        Record {:d}: (sid={:s}, sname={:s}, byear={:d})".format(recordNo, oneStudent["sid"], oneStudent["sname"], oneStudent["byear"]))
			
		print("    Finding a list of students whose birth years are 1998 (using \'aggregate\')....")	
		listOfStudent = db.student.aggregate([{"$match": {"byear": 1998}}])
		recordNo = 0
		for oneStudent in listOfStudent:
			recordNo = recordNo + 1
			print("        Record {:d}: (sid={:s}, sname={:s}, byear={:d})".format(recordNo, oneStudent["sid"], oneStudent["sname"], oneStudent["byear"]))
			
		print("    Finding a list of students with distinct names whose birth years are 1998 (using \'distinct\')....")	
		listOfStudent = db.student.distinct("sname", {"byear":1998})
		recordNo = 0
		for oneStudent in listOfStudent:
			recordNo = recordNo + 1
			print("        Record {:d}: (sname={:s})".format(recordNo, oneStudent))	
	except pymongo.errors.ConnectionFailure as error: 
		print("Document Querying Failed! Error Message: \"{}\"".format(error))
		
# Removing Documents
def removeDocument(db):
	try:
		print("Removing Documents...")
		print("    Removing students whose birth years are 1998...")
		db.student.remove({"byear":1998})
	except pymongo.errors.ConnectionFailure as error: 
		print("Document Removal Failed! Error Message: \"{}\"".format(error))	

# Dropping Collection
def dropCollection(db):
	try:
		print("Dropping Collection...")
		print("    Dropping collection \'student\'...")
		db.student.drop()
	except pymongo.errors.ConnectionFailure as error: 
		print("Collection Dropping Failed! Error Message: \"{}\"".format(error))

def main():

	try:
		# Making a DB connection
		print("Making a MongoDB connection...")
		client = MongoClient("mongodb://localhost:27017")
		
		# Getting a Database named "university"
		print("Getting a database named \"university\"")
		db = client["university"]

		choice = "0"
		while (choice != "7"):
			print(" ")
			print("Please select one of the following.")
			print("-----------------------------------")
			print("  1. Creating Collection")
			print("  2. Inserting Documents")
			print("  3. Updating Documents")
			print("  4. Querying Documents")
			print("  5. Removing Documents")
			print("  6. Dropping Collection")
			print("  7. Exit")
			print("-----------------------------------")
			print(" ")
			
			choice = input("Your Input: ")
			
			print("\n")
			
			if (choice == "1"):
				createCollection(db)
			elif (choice == "2"):
				insertDocument(db)
			elif (choice == "3"):
				updateDocument(db)
			elif (choice == "4"):
				queryDocument(db)
			elif (choice == "5"):
				removeDocument(db)
			elif (choice == "6"):
				dropCollection(db)
			elif (choice == "7"):
				print("")
			else:
				print("Invalid Input!")
			
		# Closing a DB connection
		print("Closing a DB connection...")	
		client.close()
		
	except pymongo.errors.ConnectionFailure as error: 
		print("DB Connection Failed! Error Message: \"{}\"".format(error))	


main()
