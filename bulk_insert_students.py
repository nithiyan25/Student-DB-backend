"""
Bulk Insert Students Script
This script adds sample student data to your database via the API
"""

import requests
import json

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"
# TODO: Replace with your actual Firebase ID token after logging in as admin
ADMIN_TOKEN = "INhhZQYofYezdsfHVZoT90wyBTp1"

# Sample student data
students_data = [
    {
        "name": "Arjun Kumar",
        "roll_number": "CS2024001",
        "department": "Computer Science",
        "year": "1st Year",
        "dob": "2006-03-15",
        "gender": "Male",
        "phone_number": "9876543210",
        "school_email": "arjun.kumar@school.edu",
        "personal_email": "arjun.kumar@gmail.com",
        "parent_name": "Rajesh Kumar",
        "parent_mobile": "9876543211",
        "mentor_name": "Dr. Priya Sharma",
        "mentor_staff_id": "STAFF001",
        "mentor_email": "priya.sharma@school.edu"
    },
    {
        "name": "Sneha Patel",
        "roll_number": "CS2023045",
        "department": "Computer Science",
        "year": "2nd Year",
        "dob": "2005-07-22",
        "gender": "Female",
        "phone_number": "9876543212",
        "school_email": "sneha.patel@school.edu",
        "personal_email": "sneha.patel@gmail.com",
        "parent_name": "Mahesh Patel",
        "parent_mobile": "9876543213",
        "mentor_name": "Dr. Priya Sharma",
        "mentor_staff_id": "STAFF001",
        "mentor_email": "priya.sharma@school.edu"
    },
    {
        "name": "Rahul Verma",
        "roll_number": "CS2022089",
        "department": "Computer Science",
        "year": "3rd Year",
        "dob": "2004-11-08",
        "gender": "Male",
        "phone_number": "9876543214",
        "school_email": "rahul.verma@school.edu",
        "personal_email": "rahul.verma@gmail.com",
        "parent_name": "Suresh Verma",
        "parent_mobile": "9876543215",
        "mentor_name": "Prof. Amit Singh",
        "mentor_staff_id": "STAFF002",
        "mentor_email": "amit.singh@school.edu"
    },
    {
        "name": "Priya Desai",
        "roll_number": "CS2021034",
        "department": "Computer Science",
        "year": "4th Year",
        "dob": "2003-01-30",
        "gender": "Female",
        "phone_number": "9876543216",
        "school_email": "priya.desai@school.edu",
        "personal_email": "priya.desai@gmail.com",
        "parent_name": "Kiran Desai",
        "parent_mobile": "9876543217",
        "mentor_name": "Prof. Amit Singh",
        "mentor_staff_id": "STAFF002",
        "mentor_email": "amit.singh@school.edu"
    },
    {
        "name": "Vikram Reddy",
        "roll_number": "EC2024012",
        "department": "Electronics",
        "year": "1st Year",
        "dob": "2006-05-12",
        "gender": "Male",
        "phone_number": "9876543218",
        "school_email": "vikram.reddy@school.edu",
        "personal_email": "vikram.reddy@gmail.com",
        "parent_name": "Prakash Reddy",
        "parent_mobile": "9876543219",
        "mentor_name": "Dr. Anjali Menon",
        "mentor_staff_id": "STAFF003",
        "mentor_email": "anjali.menon@school.edu"
    },
    {
        "name": "Divya Krishnan",
        "roll_number": "EC2023056",
        "department": "Electronics",
        "year": "2nd Year",
        "dob": "2005-09-18",
        "gender": "Female",
        "phone_number": "9876543220",
        "school_email": "divya.krishnan@school.edu",
        "personal_email": "divya.krishnan@gmail.com",
        "parent_name": "Suresh Krishnan",
        "parent_mobile": "9876543221",
        "mentor_name": "Dr. Anjali Menon",
        "mentor_staff_id": "STAFF003",
        "mentor_email": "anjali.menon@school.edu"
    },
    {
        "name": "Aditya Joshi",
        "roll_number": "EC2022067",
        "department": "Electronics",
        "year": "3rd Year",
        "dob": "2004-12-25",
        "gender": "Male",
        "phone_number": "9876543222",
        "school_email": "aditya.joshi@school.edu",
        "personal_email": "aditya.joshi@gmail.com",
        "parent_name": "Ramesh Joshi",
        "parent_mobile": "9876543223",
        "mentor_name": "Prof. Ravi Kumar",
        "mentor_staff_id": "STAFF004",
        "mentor_email": "ravi.kumar@school.edu"
    },
    {
        "name": "Kavya Nair",
        "roll_number": "ME2024008",
        "department": "Mechanical",
        "year": "1st Year",
        "dob": "2006-02-20",
        "gender": "Female",
        "phone_number": "9876543224",
        "school_email": "kavya.nair@school.edu",
        "personal_email": "kavya.nair@gmail.com",
        "parent_name": "Mohan Nair",
        "parent_mobile": "9876543225",
        "mentor_name": "Dr. Sunita Rao",
        "mentor_staff_id": "STAFF005",
        "mentor_email": "sunita.rao@school.edu"
    },
    {
        "name": "Rohan Mehta",
        "roll_number": "ME2023041",
        "department": "Mechanical",
        "year": "2nd Year",
        "dob": "2005-06-14",
        "gender": "Male",
        "phone_number": "9876543226",
        "school_email": "rohan.mehta@school.edu",
        "personal_email": "rohan.mehta@gmail.com",
        "parent_name": "Vijay Mehta",
        "parent_mobile": "9876543227",
        "mentor_name": "Dr. Sunita Rao",
        "mentor_staff_id": "STAFF005",
        "mentor_email": "sunita.rao@school.edu"
    },
    {
        "name": "Ananya Iyer",
        "roll_number": "ME2022078",
        "department": "Mechanical",
        "year": "3rd Year",
        "dob": "2004-10-05",
        "gender": "Female",
        "phone_number": "9876543228",
        "school_email": "ananya.iyer@school.edu",
        "personal_email": "ananya.iyer@gmail.com",
        "parent_name": "Balaji Iyer",
        "parent_mobile": "9876543229",
        "mentor_name": "Prof. Karthik Pillai",
        "mentor_staff_id": "STAFF006",
        "mentor_email": "karthik.pillai@school.edu"
    },
    {
        "name": "Siddharth Gupta",
        "roll_number": "CE2024015",
        "department": "Civil",
        "year": "1st Year",
        "dob": "2006-04-08",
        "gender": "Male",
        "phone_number": "9876543230",
        "school_email": "siddharth.gupta@school.edu",
        "personal_email": "siddharth.gupta@gmail.com",
        "parent_name": "Anil Gupta",
        "parent_mobile": "9876543231",
        "mentor_name": "Dr. Meera Shah",
        "mentor_staff_id": "STAFF007",
        "mentor_email": "meera.shah@school.edu"
    },
    {
        "name": "Ishita Sharma",
        "roll_number": "CE2023029",
        "department": "Civil",
        "year": "2nd Year",
        "dob": "2005-08-17",
        "gender": "Female",
        "phone_number": "9876543232",
        "school_email": "ishita.sharma@school.edu",
        "personal_email": "ishita.sharma@gmail.com",
        "parent_name": "Sanjay Sharma",
        "parent_mobile": "9876543233",
        "mentor_name": "Dr. Meera Shah",
        "mentor_staff_id": "STAFF007",
        "mentor_email": "meera.shah@school.edu"
    },
    {
        "name": "Karthik Bose",
        "roll_number": "EE2024019",
        "department": "Electrical",
        "year": "1st Year",
        "dob": "2006-01-11",
        "gender": "Male",
        "phone_number": "9876543234",
        "school_email": "karthik.bose@school.edu",
        "personal_email": "karthik.bose@gmail.com",
        "parent_name": "Partha Bose",
        "parent_mobile": "9876543235",
        "mentor_name": "Prof. Deepak Malhotra",
        "mentor_staff_id": "STAFF008",
        "mentor_email": "deepak.malhotra@school.edu"
    },
    {
        "name": "Neha Kapoor",
        "roll_number": "IT2023052",
        "department": "Information Technology",
        "year": "2nd Year",
        "dob": "2005-03-28",
        "gender": "Female",
        "phone_number": "9876543236",
        "school_email": "neha.kapoor@school.edu",
        "personal_email": "neha.kapoor@gmail.com",
        "parent_name": "Ashok Kapoor",
        "parent_mobile": "9876543237",
        "mentor_name": "Dr. Rajat Saxena",
        "mentor_staff_id": "STAFF009",
        "mentor_email": "rajat.saxena@school.edu"
    },
    {
        "name": "Abhishek Chawla",
        "roll_number": "IT2022091",
        "department": "Information Technology",
        "year": "3rd Year",
        "dob": "2004-09-03",
        "gender": "Male",
        "phone_number": "9876543238",
        "school_email": "abhishek.chawla@school.edu",
        "personal_email": "abhishek.chawla@gmail.com",
        "parent_name": "Dinesh Chawla",
        "parent_mobile": "9876543239",
        "mentor_name": "Dr. Rajat Saxena",
        "mentor_staff_id": "STAFF009",
        "mentor_email": "rajat.saxena@school.edu"
    }
]

def insert_students():
    """Insert all students via API"""
    
    if ADMIN_TOKEN == "INhhZQYofYezdsfHVZoT90wyBTp1":
        print("❌ Error: Please update ADMIN_TOKEN with your actual Firebase ID token")
        print("\nTo get your token:")
        print("1. Login to your app in the browser")
        print("2. Open browser DevTools (F12)")
        print("3. Go to Console tab")
        print("4. Type: await firebase.auth().currentUser.getIdToken()")
        print("5. Copy the token and paste it in this script")
        return
    
    headers = {
        "Authorization": f"Bearer {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }
    
    success_count = 0
    failed_count = 0
    
    print(f"🚀 Starting bulk insert of {len(students_data)} students...\n")
    
    for student in students_data:
        try:
            response = requests.post(
                f"{API_BASE_URL}/students/",
                headers=headers,
                json=student
            )
            
            if response.status_code == 200:
                success_count += 1
                print(f"✅ Added: {student['name']} ({student['roll_number']})")
            else:
                failed_count += 1
                print(f"❌ Failed: {student['name']} - {response.json().get('detail', 'Unknown error')}")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ Error adding {student['name']}: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully added: {success_count} students")
    print(f"❌ Failed: {failed_count} students")
    print(f"{'='*60}")

if __name__ == "__main__":
    insert_students()