from fastapi import FastAPI
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel
import os
# hello  world
load_dotenv()
app = FastAPI()

mongo_uri = os.getenv("mongo_uri")
cli = MongoClient(mongo_uri)

db = cli.college
department_collection = db.Department
student_collection = db.Student

class NewStudent(BaseModel):
    name : str
    roll_no : int
    course : str
class newdepartment(BaseModel):
    courseName:str
    courseCode:str

@app.get("/")
def root():
    return {"Message" : "Welcome to College API"}

@app.get("/departments")
def get_departments():
    departments = list(department_collection.find({},{"_id": 0,"courseCode":0}))
    return{"total": len(departments), "departments" : departments}

@app.get("/students")
def get_student():
    student = list(student_collection.find({},{"_id" : 0}))
    return{"total students" : len(student),"Students" :student}

@app.post("/student")
def add_student(student: NewStudent):
    student_dict = student.model_dump()
    student_collection.insert_one(student_dict)
    return {"message" : "Student Added",
            "Added_Student" : student.name}

@app.post("/departments")
def add_departments(department:newdepartment):
    department_dict=department.model_dump()
    department_collection.insert_one(department_dict)
    return {"message" : "department Added",
            "Added_department" : department.courseName}
#nmmmmmi