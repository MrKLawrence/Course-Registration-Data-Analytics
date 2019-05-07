#!/usr/bin/python
#
#  The program is used for illustrating how to perform data crawling on one single webpage,
#  to save this webpage to the working directory of our computer
#

#Note that the structure of the fields from the target webpage is based on the model answer of the NoSQL record insertions, not anyone else

import pymongo
from pymongo import MongoClient
from datetime import datetime
import re # comment this line if you do not want to try out the simpler methods using regular expression
import scrapy
import sys

from scrapy.selector import Selector

# logName = 'UstCourseWebpageSpider.txt'
# logTxt = open(logName,'w', encoding='utf8')

"""
The following is the adaptation of the model answer to be tested
"""
class ustWebpageSpider(scrapy.Spider):
	name = "ustWebpageSpider"
	mongo_uri = 'mongodb://localhost:27017'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		with open('url.txt', 'r') as f:
			url = f.read()
			self.start_urls = [ url ]
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client['hkust']
		# used as cache for database to check whether 
		# courses are already inserted 
		# you can also check from database directly
		self.inserted_courses = set()

	def parse(self, response):
		for a in response.xpath('//ul/li/a'):
			yield response.follow(a, callback=self.parse_snapshot)

	def parse_snapshot(self, response):
		for a in response.xpath('//div[@class="depts"]/a'):
			# #only craw data from COMP or RMBI course
			# if(("COMP" in str(a)) or ("RMBI" in str(a))):
			#only craw data from RMBI course
			if("RMBI" in str(a)):
				yield response.follow(a, callback=self.parse_dept)

	def parse_dept(self, response):
		title = response.xpath('//title/text()').extract_first()
		# ====== extract semester and time =========
		i = title.find(': Snapshot taken at ')
		semester = title[:i-5] # each dept has a length of 4
		time_str = title[i + len(': Snapshot taken at '):]
		year = int(time_str[:4])
		month = int(time_str[5:7])
		day = int(time_str[8:10])
		hour = int(time_str[11:13])
		minute = int(time_str[-2:])
		record_time = datetime(year, month, day, hour, minute)
		# simpler method using regular expression and strptime
		# m = re.search(r'(.*) \w+: Snapshot taken at (.*)', title)
		# semester = m.group(1)
		# record_time = datetime.strptime(m.group(2), '%Y-%m-%d %H:%M')
		# ==========================================
		# comment the following two lines if you do not want the progress to be displayed
		dept = response.url[-9:-5]
		print('Processing %s %s' % (time_str, dept))
		courses = response.xpath('//div[@class="course"]')
		for course in courses:
			self.parse_course(course, semester, record_time)

	def parse_course(self, el, semester, record_time):
		# extract_first() is the same as extract()[0]
		header = el.xpath('.//h2/text()').extract_first()
		i = header.find('-')
		j = header.rfind('(')
		k = header.rfind('unit')
		code = header[:i].replace(' ', '')
		if (code, semester) not in self.inserted_courses:
			course = {
				'code': code,
				'semester': semester
			}
			course['title'] = header[i+1:j].strip()
			course['credits'] = float(header[j+1:k])
			# ========== process 'COURSE INFO' ==============
			# the function fix_case removes '(', ')' , '-' and ' ' from the keys and
			# change them to camel case.
			# e.g., 'PRE-REQUISITE' -> 'prerequisite'
			# 'CO-LIST WITH' -> 'colistWith'
			# you can achieve the same goal using a sequence of 'if-else' statements
			# i.e., 
			# key = ' '.join(tr.xpath('.//th//text()').extract())
			# if key == 'PRE-REQUISITE':
			#     key = 'prerequisite'
			# elif key == 'CO-LIST WITH':
			#     key = 'colistWith'
			# ...
			for tr in el.xpath('.//div[contains(@class, "courseattr")]/div/table/tr'):
				key = self.fix_case(' '.join(tr.xpath('.//th//text()').extract()))
				value = '\t'.join([
					x.strip()
					for x in tr.xpath('.//td//text()').extract()
				])
				course[key] = value
			# =================================================
			self.inserted_courses.add((code, semester))
			self.db.course.insert_one(course)
		self.parse_sections(el.xpath('.//table[@class="sections"]//tr')[1:], code, semester, record_time)

	def parse_sections(self, trs, code, semester, record_time):
		sections = []
		prev_sect = None
		for tr in trs:
			class_name = tr.xpath('./@class').extract_first()
			if 'newsect' in class_name:
				sectionId = tr.xpath('./td[1]/text()').extract_first().split('(', 1)[0].strip()
				section = {
					'recordTime': record_time,
					'sectionId': sectionId,
					'offerings': [
						{
							# most complicated case: 2016-17 Summer MGMT5410
							# 'dateAndTime': '\t'.join(tr.xpath('./td[2]/text()').extract()),
							'dateAndTime': ' '.join(tr.xpath('./td[2]/text()').extract()),
							'room': tr.xpath('./td[3]/text()').extract_first(),
							'instructors': tr.xpath('./td[4]/text()').extract()
						}
					],
					# the text may be inside its children
					# example: 2016-17 Spring ACCT5140 L1
					'quota': int(tr.xpath('./td[5]//text()').extract_first()),
					'enrol': int(tr.xpath('./td[6]//text()').extract_first()),
					# if avail is 0, it is enclosed by <strong>
					#'avail': int(tr.xpath('./td[7]//text()').extract_first()),
					'wait': int(tr.xpath('./td[8]//text()').extract_first())
				}
				remarks = '\t'.join([
					text.strip()
					for text in tr.xpath('./td[9]//text()').extract()
					if text.strip() != ''
				])
				if remarks != '':
					section['remarks'] = remarks
				sections.append(section)
				prev_sect = section
			else:
				offering = {
					# index starts from 1
					# TODO: split dateAndTime to daysOfWeek and time
					'dateAndTime': ' '.join(tr.xpath('./td[1]/text()').extract()),
					'room': tr.xpath('./td[2]/text()').extract_first(),
					'instructors': tr.xpath('./td[3]/text()').extract()
				}
				prev_sect['offerings'].append(offering)
		self.db.course.update_one(
			{ 'code': code, 'semester': semester },
			{ '$push': {
					'sections': {
						'$each': sections
					}
				}
			}
		)

	def closed(self, reason):
		self.client.close()
		print('Data Crawling is successful and all data are inserted into the database')

	def fix_case(self, key):
		# ======= remove characters '(', ')' and '-' ===========
		s = key.translate({ord(c): '' for c in '()-'})
		# using regular expression
		#s = re.sub(r'[()-]', '', key)
		# ======================================================
		res = s.title().replace(' ', '')
		return res[0].lower() + res[1:]

"""
The code below is our original implementation
"""
"""
class ustWebpageSpider(scrapy.Spider):
	name = "ustWebpageSpider"
	# start_urls = [ "http://comp4332.com/realistic/2017/Spring/01/25/09/00/subjects/ENEG.html" ]
	start_urls = [ "http://comp4332.com/realistic/" ] #Please remove the two break in for loop.
	# start_urls = [ "http://comp4332.com/realistic/2017/Spring/01/25/09/00/subjects/ENEG.html" ]
	try:
		print("Making a MongoDB connection...")
		client = MongoClient("mongodb://localhost:27017")
		print("Getting a database named \"course\"")
		db = client["course"]
	except pymongo.errors.ConnectionFailure as error: 
		print("MongoDB Connection Failed! Error Message: \"{}\"".format(error))	

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print("This is called at the beginning.")

	def closed(self, reason):
		print("This is called at the end.")
		try:
			logTxt.close()
			print("Closing MongoDB connection ...")
			self.client.close()
		except pymongo.errors.ConnectionFailure as error: 
			print("MongoDB Connection Failed! Error Message: \"{}\"".format(error))	
			
	def parse(self, response):
		print(response.url)
		crawlFilename = response.url.split("/")[-1]
		if crawlFilename=='':
			crawlFilename = response.url.split("/")[-2]
		with open(crawlFilename, "wb") as f:
			f.write(response.body)
		self.log("Saved File {} ".format(crawlFilename))
		listOfLinks = response.xpath("//a[@href]/@href").extract()
		for link in listOfLinks:
			yield response.follow(link, callback=self.parse_eachTimeslot)

		linkFilename = "listOfLinks.txt"
		with open(linkFilename, "w") as f:
			f.write(str(listOfLinks))
			for link in listOfLinks:
				f.write(link)
				f.write("\n")
		self.log("Saved File {} ".format(linkFilename))

	def parse_eachTimeslot(self, response):
		listOfSubjects = response.xpath("//a[@href]/@href").extract()
		for link in listOfSubjects:
			yield response.follow(link, callback=self.parse_subjects)

	def parse_subjects(self, response):
		coursesInfo =[]
		semester = response.xpath("//title/text()").extract()[0][0:14]
		courseTitles = response.xpath("//h2").extract()
		courseIndex = 0
		for oneCourseTitle in courseTitles:
			coursesInfo.append(dict())
			coursesInfo[courseIndex]['code'] = oneCourseTitle[4 : oneCourseTitle.find(' - ')]
			coursesInfo[courseIndex]['title'] = oneCourseTitle[oneCourseTitle.find(' - ') + 3 : oneCourseTitle.find(' units)') - 3]
			coursesInfo[courseIndex]['credits'] = oneCourseTitle[oneCourseTitle.find(' units)')-1]
			coursesInfo[courseIndex]['sections'] = list()
			courseIndex += 1
		courseIndex = 0
		courseInfoTables = response.xpath('//div[@class="courseattr popup"]/div/table').extract()
		# logTxt.write("course info :\n")
		for oneCourseInfo in courseInfoTables:		
			# logTxt.write(coursesInfo[courseIndex]['code'] + "\n")
			OneCourseInfoHeading = Selector(text = oneCourseInfo.replace('<br>',' ')).xpath("//th/text()").extract()
			dbHeadingDict = {'ATTRIBUTES':'attributes','ALTERNATE CODE(S)':'alternateCodes','CO-LIST WITH' :'colistWith','CO-REQUISITE': 'corequisite', 'DESCRIPTION': 'description','EXCLUSION': 'exclusion', 'INTENDED LEARNING OUTCOMES':'intendedLearningOutcomes','PRE-REQUISITE':'previousCode','VECTOR':'vector'}
			for key, value in dbHeadingDict.items():
				OneCourseInfoHeading = [oneHead.replace(key,value) for oneHead in OneCourseInfoHeading]
			# print("OneCourseInfoHeading :"+ str(OneCourseInfoHeading))
			OneCourseInfoContent = Selector(text = oneCourseInfo.replace('<br>',' ')).xpath("//td/text()").extract()
			for i in range(len(OneCourseInfoHeading)):
				coursesInfo[courseIndex][OneCourseInfoHeading[i]] = OneCourseInfoContent[i]
				# logTxt.write(OneCourseInfoHeading[i] + ": " + str(OneCourseInfoContent[i]) + "\n")
			courseIndex += 1
		courseIndex = 0
		coursesTables = response.xpath('//table[@class="sections"]').extract()
		heading = Selector(text=coursesTables[0]).xpath("//th/text()").extract()
		# print("heading :"+str(heading))
		dbHeadingDict = {'Section':'sectionId', 'Date & Time':'dateAndTime', 'Room':'room', 'Instructor': 'instructors', 'Quota':'quota', 'Enrol':'enrol', 'Avail':'avail', 'Wait':'wait',  'Remarks':'remarks'}
		for key, value in dbHeadingDict.items():
			heading = [oneHead.replace(key,value) for oneHead in heading]
		for courseTable in coursesTables:
			rows = Selector(text=courseTable).xpath("//tr[td]").extract()
			for oneRow in rows :
				sectionData = dict()
				sectionColumn = Selector(text=oneRow).xpath("//td").extract()
				# logTxt.write("sectionColumn: "+'\n'+str(sectionColumn)+"\n")
				if len(sectionColumn) >= len(heading) -1: 
					try:
						# print("heading : "+str(heading))
						for i in range(len(sectionColumn)):	
							sectionData[heading[i]]= Selector(text=sectionColumn[i]).xpath('//text()').extract()
							# if(heading[i] == "remarks"):
							# 	 sectionData[heading[i]].replace('\xa0','')
								#  sectionData['remarks'].replace('> ','')
						coursesInfo[courseIndex]['sections'].append(sectionData)
						# logTxt.write("--- the section is done ---\n"+str(coursesInfo[courseIndex])+"\n")
						# print ("*** one sectionColumn : "+'\n'+'\t'.join(sectionColumn)+"\n")
						
					except Exception as e:
						print ("Exception: "+type(e).__name__+'\n'+'\t'.join(sectionColumn)+"\n")
						# print (.join(sectionColumn)+"\n")
						# logTxt.write("Exception: "+type(e).__name__+'\n'+'\t'.join(sectionColumn)+"\n")
				else: 
					try:
						# print("coursesInfo[courseIndex]['sections'][-1] : "+ str(coursesInfo[courseIndex]['sections'][-1]))
						# logTxt.write("additional sectionColumn: "+'\n'+str(sectionColumn)+"\n")
						coursesInfo[courseIndex]['sections'][-1]['dateAndTime']+=Selector(text=sectionColumn[0]).xpath('//text()').extract()
						# logTxt.write(" sectionColumn(dateAndTime): "+'\n'+str(Selector(text=sectionColumn[0]).xpath('//text()').extract())+"\n")
						coursesInfo[courseIndex]['sections'][-1]['room']+=Selector(text=sectionColumn[1]).xpath('//text()').extract()
						# logTxt.write(" sectionColumn(room): "+'\n'+str(Selector(text=sectionColumn[1]).xpath('//text()').extract())+"\n")
						coursesInfo[courseIndex]['sections'][-1]['instructors']+=Selector(text=sectionColumn[2]).xpath('//text()').extract()
						# logTxt.write(" sectionColumn(instructors): "+'\n'+str(Selector(text=sectionColumn[2]).xpath('//text()').extract())+"\n")

					except Exception as e:
						print("Additional exception: "+type(e).__name__+'\n'+'\t'.join(sectionColumn)+"\n")
						logTxt.write("Additional exception: "+type(e).__name__+'\n'+'\t'.join(sectionColumn)+"\n")
			courseIndex+=1
		urlList = response.request.url.split('/')
		recordTime = urlList[4]+'-'+urlList[6]+'-'+urlList[7]+' '+urlList[8]+':'+urlList[9]
		for oneCourseInfo in coursesInfo:			

			if 'description' not in oneCourseInfo:
				oneCourseInfo['description'] = ''	
			if 'exclusion' not in oneCourseInfo:
				oneCourseInfo['exclusion'] = ''
			if 'prerequisite' not in oneCourseInfo:
				oneCourseInfo['prerequisite'] = ''	
				
		subject = coursesInfo[0]['code'][:4]
		print("inserting subject: " + subject + " with record time slot " + recordTime)

		for oneCourseInfo in coursesInfo:
			courseInfoCode = oneCourseInfo['code'].replace(' ','')
			savedCourse = self.db.course.find({"code" : courseInfoCode})
			self.log("savedCourse {}, type{} ".format(str(savedCourse),str(isinstance(savedCourse, dict))))
			courseExist = False
			if isinstance(savedCourse, dict):
				courseExist = True
			if (not courseExist):
				print ("inserting course " + courseInfoCode)
				self.db.course.insert(
					{ 
						"code": courseInfoCode, 
						"semester": semester,
						"title": oneCourseInfo['title'], 
						"credits" :int(oneCourseInfo['credits']), 
						"prerequisite" : oneCourseInfo['prerequisite'], 
						"exclusion" :  oneCourseInfo['exclusion'], 
						"description": oneCourseInfo['description'], 
						"sections": []
					}
				)
			for oneSection in oneCourseInfo['sections']:
				# print("oneSection['sections'] :"+str(oneSection))				
				# print("oneSection['sections'][0] :"+str(oneSection['sections'][0]))
				self.db.course.update({ "code": courseInfoCode }, {
					"$push": {
						"sections": {
							"recordTime": datetime.datetime.strptime(recordTime, "%Y-%m-%d %H:%M"),
							"sectionId": oneSection['sectionId'][0],
							"offerings": [{
								"dateAndTime": oneSection['dateAndTime'],
								"room": oneSection['room'],
								"instructors": [
									oneSection['instructors']
								]
							}],
							"quota": int(oneSection['quota'][0]),
							"enrol":  int(oneSection['enrol'][0]),
							"avail":  int(oneSection['avail'][0]),
							"wait":  int(oneSection['wait'][0]),
							"remarks":  oneSection['remarks'][0],
						}
					}
				})
"""

