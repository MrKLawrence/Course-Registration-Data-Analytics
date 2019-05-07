readme file (readme.txt)

COMP4332 Big Data Mining and Management
COMP4332/RMBI4310 (Spring 2018)
Project: Course Registration Data Analytics
Phase3 report

1. Group Information:
    - Group No. : 24
    - Member: YU, Ho Yung
    - Member: LEUNG, Kin Tung
    
2. File List:
    - main.py
    - readme.txt
    
3. File Description:
    This is the Phase 3 of COMP4332 course project.
    main.py:
    Given a website which contains the information about course enrollment status in a period of a semester,
    this main.py file can provide the following features:
    find a list of courses which match some criteria (with respect to requirement 5.3.1 and 5.3.2).

    To execute the program correctly, the following procedure is recommended to follow:
	For Collection Dropping,
	Type: "1"
	To drop the collection of "course" by calling collectionDroppingAndEmptyCollectionCreating()

	For Insertions two Example Data,
	Type: "2"
	Type: ""
	
	To insert 2 example records in the collection “course” by calling dataCrawling()
	The data structure is the same as the example in comp4332 website

	For Course Search By Keyword,
	Type: "3"
	Type: "Big"

	To search the Keyword “Big” and print the the record by calling courseSearchByKeyword()

	For Course Search By Waiting List Size, 
	Type: "4"
	Type: "0.01"
	Type: "2018-01-26T14:00Z"
	Type: "2018-02-01T11:30Z

	To search the course between the time we type above by calling courseSearchByWaitingListSize()
	For exiting,
	Type: "6"

    (Note: The output of each feature is to print a message or return a list as required in the project specification. The datetime input shown above is for example use.)
    
5. Known Bugs of the System:
    The error handling part is to be completed.

6. Requirements of the program.
    This codes run on python 3 and need the connection with “localhost:27017”. It needs the following library:
	 MongoClient, pymongo, pandas, numpy, datetime, re, pprint

