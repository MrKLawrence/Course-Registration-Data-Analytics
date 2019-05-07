// JavaScript source code
//query.js

/*

Write a NoSQL (query) script for illustrating how to perform each of
the operations for the first objective (i.e., each of the operations
required in Section 5.3) with one query concrete example.
(Note: This script just includes 1 example of a document query (or a
number of consecutive document queries) for each operation and thus
the contents of queries are hardcoded). 

*/

// query one:
// A list of courses which course titles, course description or course remarks
// match the given text k.
// In the output, for each course, please show “Course Code”, “Course Title”, “No. of
// Units/Credits”, a list of sections of the course each with “Section”, “Date & Time”,
// “Quota”, “Enrol”, “Avail” and “Wait”.
// Please sort the list of courses in ascending order of “Course Code”.
// (Within a single course, please sort in ascending order of “Sections”)
// query one:
print("query one:");
cursor = db.course.aggregate([
    {
        $match: {
            $or:[
                {"cname": {$regex: /Visualizing/}},
                {"listOfSections.remarks": {$regex: /Visualizing/}},
                {"courseInfo.description": {$regex: /Visualizing/}}
            ]
        }
    },
    { 
        $unwind: '$listOfSections' 
    },
    {
        $sort: {cid:1, "listOfSections.section":1}
    },
    {
        $project: {_id:0,cid:1,cname:1,numberOfCredits:1,"listOfSections.section":1, "listOfSections.dateTime":1,"listOfSections.quota":1,"listOfSections.enrol":1,"listOfSections.avail":1,"listOfSections.wait":1,}
    }
])

while (cursor.hasNext()) {
    printjson(cursor.next())
}


// query two:
print("query two:");
cursor = db.course.aggregate([
    { 
        $match: {"timeRecorded" : {"$gte": ISODate("2018-01-26T09:00:00Z")},
                "timeRecorded" : {"$lte": ISODate("2018-02-15T00:30:00Z")} 
        }
    },
    {
        $project: {_id:0,cid:1,cname:1,numberOfCredits:1,"listOfSections.section":1, "listOfSections.dateTime":1,"listOfSections.quota":1,"listOfSections.enrol":1,"listOfSections.avail":1,"listOfSections.wait":1,timeRecorded:1}
    },
    {
        $sort: {cid:1}
    }
])

while (cursor.hasNext()) {
    printjson(cursor.next())
}
