# Course-Registration-Data-Analytics
HKUST project
Big Data Mining and Management
Project: Course Registration Data Analytics
#This repository is for internal use only. 
    
## Motivation

There are a hierarchy of files for data crawling:
In main.py inside our working directory:
Given a website which contains the information about course enrollment status in a period of a semester,
this main.py file can provide the following features:
Find a list of courses which matched predictive criteria.

## File Description

Here are a list of Python files (with the following file structure, excluding the .pyc files containing the Python bytecode for interpretation) inside the folder "Phase6":


    To execute the program correctly, the following procedure is recommended to follow:
	First, set up a database for mongo server by cmd:
	mongod
	
	Second, open the main.py by cmd:
	python main.py
	
	For Collection Dropping,
	Type: "1"
	To drop the collection of "course" by calling collectionDroppingAndEmptyCollectionCreating()

	For data crawling and DB Insertions,
	Type: "2"
	Type: ""
	(Note: this is the execution of data crawling, which generates the results inside listOfLink.txt and log.txt)
	The crawling was only to crawl from http://comp4332.com/trial
	The following is the process to generate data crawling result from the model answer
	
    1. scrapy startproject Phase3 / scrapy crawl ustWebpageSpider / scrapy startproject dataCrawling

    2. cd dataCrawling

    3. add the following lines to dataCrawling/settings.py
    # log to file instead of the console.
    LOG_FILE = 'log.txt'

    # only log error messages, ignore irrelevant messages
    # to know more about log levels, see https://doc.scrapy.org/en/latest/topics/logging.html#log-levels
    LOG_LEVEL = 'ERROR'

    # does not redirect standard output to the log file
    # i.e., we want the output from the print() method is shown in the console
    LOG_STDOUT = False

    4. write "dataCrawling/spiders/ustWebpageSpider.py" (i.e., place "ustWebpageSpider.py" found in the zipped file to folder "dataCrawling/spiders")

    5. keep all other files (i.e., __init__.py, items.py, middlewares.py, pipelines.py) unchanged.
    
	The data structure is the same as the example in comp4332 website

	For Course Search By Keyword,
	Type: "3"
	Type: "Big"

	To search the Keyword "Big" and print the the record by calling courseSearchByKeyword()

	For Course Search By Waiting List Size, 
	Type: "4"
	Type: "2"
	Type: "2018-01-28 10:00"
	Type: "2018-01-28 15:00"

	To search the course between the time we type above by calling courseSearchByWaitingListSize()
	For exiting,
	Type: "6"

    (Note: The output of each feature is to print a message or return a list as required in the project specification. The datetime input shown above is for example use.)
    
    In scrapy.cfg, 
    this is the configuration file of "scrapy", which is the Python package for data crawling.

    Inside the sub-folder "dataCrawling", 
    there is "__init__.py" file;
    a Python file "items.py" which is a "project item definition" file;
    a Python file "pipelines.py" which is a "project pipeline" file;
    a Python file "middlewares.py" which is a "middleware" file;
    a Python file "settings.py" which is a "project setting" file;

    And inside another sub-folder "dataCrawling”,there are
    a Python file "__init__.py", and
    a Python file “ustWebpageSpider.py", which accesses the target webpage specified and then stores the content of this webpage in the working directory.

    For the training in each model, the main() function in each model can be called to training each model. 

## Tests/Key notes of the System:

If the "mongod" MongoDB daemon is not set up when running the Python program during data crawling, the database connection is   refused and therefore prevents the program from running properly.

## Installation/ System Requirements

This codes run on python 3 and need the connection with "localhost:27017". It needs the following library:
MongoClient, pymongo, pandas, numpy, datetime, re, pprint
Both of the Python program "main.py" and the NoSQL MongoDB server "mongod" should be executed at the same time to avoid problems of failed connection.

## Contributors

1. Eric YU
2. Kin LEUNG
