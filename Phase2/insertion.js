// JavaScript source code
//insertion.js

//NoSQL database design 2: Reformat to on Program Requirement 5.3 Course Search project.pdf
//Based on the records in http://comp4332.com/realistic/
//set up the database server 
//Command:
//mongod 

// database selection: use CourseRegistration database
//Command:
//mongo 
//use CourseRegistration  
db = db.getSiblingDB("CourseRegistration")

/*

Write a NoSQL (insertion) script for illustrating how to insert 2
database documents/records each of which corresponds to the course
enrollment status of a single course in a single time slot
(Note: This script just includes 2 examples of document insertions and
thus the contents of 2 documents are hardcoded). 

*/

db.createCollection("student")

db.createCollection("department")

db.createCollection("take")

db.createCollection("Course")

db.student.insert(
    {
        sid: "12345678",
        sname: "Eric Yu",
        byear: "1997",
        email: "hyyab@connect.ust.hk"
    }
)

db.department.insert({
    department_list: [
        {division: "ACCT"},
        {division: "AESF"},
        {division: "BIBU"},
        {division: "BIEN"},
        {division: "BIPH"},
        {division: "BTEC"},
        {division: "CBME"},
        {division: "CENG"},
        {division: "CHEM"},
        {division: "CHMS"},
        {division: "CIEM"},            
        {division: "CIVL"},            
        {division: "COMP"},            
        {division: "CPEG"},                    
        {division: "CSIC"},    
        {division: "CSIT"},            
        {division: "ECON"},            
        {division: "EEMT"},            
        {division: "EESM"},            
        {division: "ELEC"},            
        {division: "ENEG"},            
        {division: "ENGG"},            
        {division: "ENTR"},            
        {division: "ENVR"},            
        {division: "ENVS"},            
        {division: "EVNG"},            
        {division: "EVSM"},
        {division: "FINA"},
        {division: "GBUS"},            
        {division: "GNED"},            
        {division: "HART"},            
        {division: "HLTH"},            
        {division: "HMMA"},            
        {division: "HUMA"},            
        {division: "IBTM"},            
        {division: "IDPO"},            
        {division: "IELM"},            
        {division: "IIMP"},            
        {division: "IMBA"},            
        {division: "ISOM"},            
        {division: "JEVE"},            
        {division: "LABU"},            
        {division: "LANG"},            
        {division: "LIFS"},            
        {division: "MAED"},            
        {division: "MAFS"},            
        {division: "MARK"},            
        {division: "MATH"},            
        {division: "MECH"},            
        {division: "MESF"},            
        {division: "MGCS"},            
        {division: "MGMT"},           
        {division: "MILE"},            
        {division: "MIMT"},            
        {division: "MSBD"},            
        {division: "NANO"},            
        {division: "PDEV"},
        {division: "PHYS"},
        {division: "PPOL"},            
        {division: "RMBI"},            
        {division: "SBMT"},            
        {division: "SCIE"},            
        {division: "SHSS"},            
        {division: "SOSC"},            
        {division: "SSMA"},            
        {division: "SUST"},            
        {division: "TEMG"},            
        {division: "UROP"},            
        {division: "WBBA"}
    ]
})


db.course.insert(
    {
        "department" : "COMP",
        "cid" : "COMP 1942",
        "cname" : "Exploring and Visualizing Data",
        "numberOfCredits" : 3,
        "listOfSections" : [
            {"section" : "L1", 
            "sectionCode" : 1802,
            "dateTime" : "WeFr 03:00PM - 04:20PM", 
            "room" : "G010, CYT Bldg",
            "roomCapacity" : 140,
            "instructor" : "WONG, Raymond Chi Wing",
            "quota" : 125,
            "enrol" : 48,
            "avail" : 77,
            "wait" : 0,
            "remarks" : ""       
            },
            {"section" : "T1", 
            "sectionCode" : 1804,
            "dateTime" : "Fr 01:30PM - 02:20PM", 
            "room" : "Rm 2406, Lift 17-18",
            "roomCapacity" : 76,
            "instructor" : "WONG, Raymond Chi Wing",
            "quota" : 65,
            "enrol" : 24,
            "avail" : 41,
            "wait" : 0,
            "remarks" : ""       
            },
            {"section" : "T2", 
            "sectionCode" : 1806,
            "dateTime" : "We 11:00AM - 11:50AM", 
            "room" : "Rm 2302, Lift 17-18",
            "roomCapacity" : 74,
            "instructor" : "WONG, Raymond Chi Wing",
            "quota" : 60,
            "enrol" : 24,
            "avail" : 36,
            "wait" : 0,
            "remarks" : ""       
            }
        ],
        "courseInfo" : [
            {
                "attributes" : "Common Core (QR) for 4Y programs",
                "exclusion" : [
                    {"cid" : "COMP 4331"},
                    {"cid" : "ISOM 3360"},
                    {"cid" : "RMBI 4310"}
                ],
                "description" : "This course teaches concepts and tools for exploring and visualizing data. There are a lot of real-life decision-making problems (e.g., business, logistics, economics, marketing, finance, resource management, forecasting and engineering) which can be formulated using some existing data analysis models. Existing computer science tools such as Microsoft Excel can help us to model and solve these problems easily, and to visualize the solutions."
            }
        ],
        "timeRecorded" : new Date("2018-01-25T09:30:00Z"),
        "url" : "http://comp4332.com/realistic/2017/Spring/01/25/09/30/subjects/COMP.html",
        "satisfied" : null
    }
    )

db.course.insert(
    {
        "department" : "RMBI",
        "cid" : "RMBI 4310",
        "cname" : "Advanced Data Mining for Risk Management and Business Intelligence",
        "numberOfCredits" : 3,
        "listOfSections" : [
            {"section" : "L1", 
            "sectionCode" : 3592,
            "dateTime" : "WeFr 01:30PM - 02:50PM", 
            "room" : "G010, CYT Bldg",
            "roomCapacity" : 140,
            "instructor" : "WONG, Raymond Chi Wing",
            "quota" : 55,
            "enrol" : 24,
            "avail" : 31,
            "wait" : 0,
            "remarks" : ""       
            },
            {"section" : "T1", 
            "sectionCode" : 3593,
            "dateTime" : "Tu 06:00PM - 06:50PM", 
            "room" : "Rm 4619, Lift 31-32",
            "roomCapacity" : 126,
            "instructor" : "WONG, Raymond Chi Wing",
            "quota" : 55,
            "enrol" : 24,
            "avail" : 31,
            "wait" : 0,
            "remarks" : ""       
            }
        ],
        "courseInfo" : [
            {
                "pre-requisite" : "COMP 4331 or ISOM 3360",
                "co-list" : [
                    {"cid" : "COMP 4332"}
                ],
                "description" : "This course will explore some advanced principles and techniques of data mining, with emphasis on applications in risk management and business intelligence. Topics include data mining process for data transformation and integration, data preprocessing, data mining algorithms and evaluation of data mining models and results. Advanced topics include data stream analysis, using data warehouse for decision support, supervised, semi-supervised and unsupervised learning techniques in data mining. We will cover advanced data mining applications in credit risk analysis, scale up methods for mining massive customer data and various novel applications such as data mining applications in social network analysis. Projects are aimed at familiarize the students with the entire data mining process rather than isolated applications."}
        ],
        "timeRecorded" : new Date("2018-01-25T09:00:00Z"),
        "url" : "http://comp4332.com/realistic/2017/Spring/01/25/09/00/subjects/RMBI.html",
        "satisfied" : null
    }
    )

    db.course.insert(
        {
            "department" : "RMBI",
            "cid" : "RMBI 4310",
            "cname" : "Advanced Data Mining for Risk Management and Business Intelligence",
            "numberOfCredits" : 3,
            "listOfSections" : [
                {"section" : "L1", 
                "sectionCode" : 3592,
                "dateTime" : "WeFr 01:30PM - 02:50PM", 
                "room" : "G010, CYT Bldg",
                "roomCapacity" : 140,
                "instructor" : "WONG, Raymond Chi Wing",
                "quota" : 46,
                "enrol" : 43,
                "avail" : 3,
                "wait" : 0,
                "remarks" : ""       
                },
                {"section" : "T1", 
                "sectionCode" : 3593,
                "dateTime" : "Tu 06:00PM - 06:50PM", 
                "room" : "Rm 4619, Lift 31-32",
                "roomCapacity" : 126,
                "instructor" : "WONG, Raymond Chi Wing",
                "quota" : 46,
                "enrol" : 43,
                "avail" : 3,
                "wait" : 0,
                "remarks" : ""       
                }
            ],
            "courseInfo" : [
                {
                    "pre-requisite" : "COMP 4331 or ISOM 3360",
                    "co-list" : [
                        {"cid" : "COMP 4332"}
                    ],
                    "description" : "This course will explore some advanced principles and techniques of data mining, with emphasis on applications in risk management and business intelligence. Topics include data mining process for data transformation and integration, data preprocessing, data mining algorithms and evaluation of data mining models and results. Advanced topics include data stream analysis, using data warehouse for decision support, supervised, semi-supervised and unsupervised learning techniques in data mining. We will cover advanced data mining applications in credit risk analysis, scale up methods for mining massive customer data and various novel applications such as data mining applications in social network analysis. Projects are aimed at familiarize the students with the entire data mining process rather than isolated applications."}
            ],
            "timeRecorded" : new Date("2018-02-15T00:30:00Z"),
            "url" : "http://comp4332.com/realistic/2017/Spring/02/15/00/30/subjects/RMBI.html",
            "satisfied" : null
        }
        )

        db.course.insert(
            {
                "department" : "RMBI",
                "cid" : "RMBI 4310",
                "cname" : "Advanced Data Mining for Risk Management and Business Intelligence",
                "numberOfCredits" : 3,
                "listOfSections" : [
                    {"section" : "L1", 
                    "sectionCode" : 3592,
                    "dateTime" : "WeFr 01:30PM - 02:50PM", 
                    "room" : "G010, CYT Bldg",
                    "roomCapacity" : 140,
                    "instructor" : "WONG, Raymond Chi Wing",
                    "quota" : 80,
                    "enrol" : 75,
                    "avail" : 5,
                    "wait" : 2,
                    "remarks" : ""       
                    },
                    {"section" : "T1", 
                    "sectionCode" : 3593,
                    "dateTime" : "Tu 06:00PM - 06:50PM", 
                    "room" : "Rm 4619, Lift 31-32",
                    "roomCapacity" : 126,
                    "instructor" : "WONG, Raymond Chi Wing",
                    "quota" : 80,
                    "enrol" : 75,
                    "avail" : 5,
                    "wait" : 2,
                    "remarks" : ""       
                    }
                ],
                "courseInfo" : [
                    {
                        "pre-requisite" : "COMP 4211 OR COMP 4331 OR ISOM 3360",
                        "co-list" : [
                            {"cid" : "RMBI 4310"}
                        ],
                        "description" : "This course will expose students to new and practical issues of real world mining and managing big data. Data mining and management is to effectively support storage, retrieval, and extracting implicit, previously unknown, and potentially useful knowledge from data. This course will place emphasis on two parts. The first part is big data issues such as mining and managing on distributed data, sampling on big data and using some cloud computing techniques on big data. The second part is applications of the techniques learnt on areas such as business intelligence, science and engineering, which aims to uncover facts and patterns in large volumes of data for decision support. This course builds on basic knowledge gained in the introductory data-mining course, and explores how to more effectively mine and manage large volumes of real-world data and to tap into large quantities of data. Working on real world data sets, students will experience all steps of a data-mining and management project, beginning with problem definition and data selection, and continuing through data management, data exploration, data transformation, sampling, portioning, modeling, and assessment."                
                    }],
                "timeRecorded" : new Date("2018-02-15T00:30:00Z"),
                "url" : "http://comp4332.com/realistic/2017/Spring/02/15/00/30/subjects/COMP.html "
            }
        )