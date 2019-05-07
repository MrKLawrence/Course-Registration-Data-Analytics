# import pymongo
import csv
import datetime
# import re
def writeToCsv(db):
	##dataFromMongo = list(db.history.find({'$or':[{'cid':{'$regex':'^COMP42'}},{'cid':{'$regex':'^COMP43'}},{'cid':{'$regex':'^RMBI'}},{'cid':'COMP1942'}]}).sort('time', pymongo.ASCENDING))
	dataFromMongo = list(db.history.aggregate([
		{
			'$match':{'$or':[{'cid':{'$regex':'^COMP42'}},{'cid':{'$regex':'^COMP43'}},{'cid':'COMP1942'},{'cid':{'$regex':'^RMBI'}}]}},
		{
			'$unwind': '$record'
		},
		{
			'$match':{'record.section':{'$regex': '^L[0-9]'}}},
		{
			'$sort': {"cid": 1,"record.section": 1,"time": 1}
		}
	]))
	print(len(dataFromMongo))

	timestampDict = {}
	with open('timestamp.txt','r') as timestampTxt:
		timestamp = timestampTxt.read().split('\n')
		#print(len(timestamp))
		for idx, i in enumerate(timestamp):
			timestampDict[i] = idx

	#print(timestampDict)


	with open('model2.csv','w', encoding='utf-8', newline='') as outfile:
		fields = ['cid','section','timestamp','time','quota','enrol','avail','wait']
		write = csv.DictWriter(outfile, fieldnames=fields)
		write.writeheader() 
		for answers_record in dataFromMongo:
			answers_record_id = answers_record['cid']
			answers_record_section = answers_record['record']['section']
			answers_record_time = answers_record['time']
			answers_record_timestamp = answers_record['tid']
			answer_record = answers_record['record']
			flattened_record = {
				'cid': answers_record_id,
				'section': answers_record_section,
				'timestamp': timestampDict[answers_record_timestamp],
				'time': (answers_record_time+ datetime.timedelta(hours=8)),
				'quota': answer_record['quota'],
				'enrol': answer_record['enrol'],
				'avail': answer_record['avail'],
				'wait': answer_record['wait'],
			}
			write.writerow(flattened_record)

	fullContinueData = []
	with open('model2.csv', 'r') as notContinueData:
		reader = csv.DictReader(notContinueData)
		#checkCid = reader[0]['cid']
		checkTimestamp = 0
		#checkSection = reader[0]['section']
		for row in reader:
			if checkTimestamp == int(row['timestamp']):
				fullContinueData.append(row)
				checkTimestamp = checkTimestamp + 1
				if checkTimestamp == 992:
					checkTimestamp = 0
			else:
				for idx in range(checkTimestamp,int(row['timestamp'])+1):
					fullContinueData.append({
						'cid': row['cid'],
						'section': row['section'],
						'timestamp': idx,
						'time': row['time'],
						'quota': -1,
						'enrol': -1,
						'avail': -1,
						'wait': -1,
					})
				checkTimestamp = int(row['timestamp'])+1

	with open('model2.csv','w', encoding='utf-8', newline='') as outfile:
		fields = ['cid','section','timestamp','time','quota','enrol','avail','wait']
		write = csv.DictWriter(outfile, fieldnames=fields)
		write.writeheader() 
		for answers_record in fullContinueData:
			answers_record_id = answers_record['cid']
			answers_record_section = answers_record['section']
			answers_record_time = answers_record['time']
			answers_record_timestamp = answers_record['timestamp']
			answer_record = answers_record
			flattened_record = {
				'cid': answers_record_id,
				'section': answers_record_section,
				'timestamp': int(answers_record_timestamp)+1,
				'time': (answers_record_time),
				'quota': answer_record['quota'],
				'enrol': answer_record['enrol'],
				'avail': answer_record['avail'],
				'wait': answer_record['wait'],
			}
			write.writerow(flattened_record)