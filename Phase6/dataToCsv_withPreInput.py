import csv
import pymongo
import datetime
import re
def dbToCsv():
	client = pymongo.MongoClient('mongodb://localhost:27017')
	db = client['hkust']

	# print(list(db.course.find({'code': 'RMBI4210'})))

	# cursor = db.course.find(
	# 	{}, {'code': 1, 'sections': 1,'sections.sectionId': 1,'sections.quota':1,'sections.enrol':1,'sections.wait':1,'sections.recordTime':1})
	coursesListForPredict = ["COMP1942","COMP4211","COMP4221","COMP4321","COMP4331","COMP4332","RMBI1010","RMBI3000A","RMBI4210","RMBI4310"]
	for courseName in coursesListForPredict:
		cursor = db.course.aggregate([
			{
				'$match':{'$or':[{'code':'COMP1942'},{'code':{'$regex':'^COMP42'}},{'code':{'$regex':'^COMP43'}},{'code':{'$regex':'^RMBI'}}]}
			},
			{
				'$unwind': '$sections'
			},
			{
				'$match':{'sections.sectionId':{'$regex': '^L[0-9]'}}
			},
			{
				'$sort': {"code": 1,"sections.sectionId": 1,"sections.recordTime": 1}
			}
		])
		earliestTime = datetime.datetime.strptime("2018-01-25T09:00Z", "%Y-%m-%dT%H:%MZ").timestamp()

		fileName = str(courseName)+'TrainingData.csv'
		# fileName = 'allDistinctData.csv'	
		fullContinueData = []
		with open(fileName,'w', encoding='utf-8', newline='') as outfile:
			# fields = ['code', 'sectionId','recordTime','quota','enrol','wait','total']
			fields = ['code', 'sectionId','recordTime','quota','enrol','wait']
			write = csv.DictWriter(outfile, fieldnames=fields)
			write.writeheader()
			for answers_record in cursor:  # Here we are using 'cursor' as an iterator
				answers_record_id = answers_record['code']
				# if("COMP1942" in answers_record_id or "COMP42" in answers_record_id or "COMP43" in answers_record_id or "RMBI" in answers_record_id):
				if(str(courseName) in answers_record_id):
					answer_record = answers_record['sections']
					answer_record_sectionId = answer_record['sectionId']
					if(re.match(r'L\d',answer_record_sectionId)):
						flattened_record = {
							'code': answers_record_id,
							'sectionId': answer_record['sectionId'][1:],
							'recordTime': int((answer_record['recordTime'].timestamp() - earliestTime)/1800),
							'quota': answer_record['quota'],
							'enrol': answer_record['enrol'],
							'wait': answer_record['wait'],
							# 'total': int(answer_record['quota']+answer_record['wait'])
						}
						write.writerow(flattened_record)
						fullContinueData.append(flattened_record)
		
		# print(fullContinueData[0:30])
		missingCount = 0
		for index in range(len(fullContinueData[:-1])+missingCount):
			if int(fullContinueData[index]['recordTime']) + 1 < int(fullContinueData[index+1]['recordTime']):
				# fullContinueData.insert(index+1, {'code':fullContinueData[index]['code'] , 'sectionId': fullContinueData[index]['sectionId'], 'recordTime': int(fullContinueData[index]['recordTime'])+1, 'quota': -1 , 'enrol': -1 , 'wait': -1, 'total':-1})
				fullContinueData.insert(index+1, {'code':fullContinueData[index]['code'] , 'sectionId': fullContinueData[index]['sectionId'], 'recordTime': int(fullContinueData[index]['recordTime'])+1, 'quota': int(fullContinueData[index]['quota']) , 'enrol':  int(fullContinueData[index]['enrol']) , 'wait': -1})
				missingCount += 1
		print("missingCount: "+str(missingCount))

		# print(fullContinueData[0:30])
		# fileName = 'allContinuousData_withPreInput.csv'
		fileName = str(courseName)+'TrainingData_Continuous.csv'	
		with open(fileName,'w', encoding='utf-8', newline='') as outfile:
			# fields = ['code', 'sectionId','recordTime','quota','enrol','wait','total']
			fields = ['code', 'sectionId','recordTime','quota','enrol','wait']
			write = csv.DictWriter(outfile, fieldnames=fields)
			write.writeheader()
			for answer_record in fullContinueData:
				flattened_record = {
					'code': answer_record['code'],
					'sectionId': answer_record['sectionId'],
					'recordTime': answer_record['recordTime'],
					'quota': answer_record['quota'],
					'enrol': answer_record['enrol'],
					'wait': answer_record['wait']
					# 'total': answer_record['total']
				}
				write.writerow(flattened_record)
		
	client.close()
dbToCsv()
