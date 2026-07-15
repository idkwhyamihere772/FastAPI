from fastapi import FastAPI, HTTPException, status
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

@app.put("/student/{course}/{roll_no}")
def update_student(course : str , roll_no : int ,student_update: NewStudent):
    update_data = student_update.model_dump()
    result = student_collection.update_one({"course" : course , "roll_no" : roll_no} , {"$set" : update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No student exist with roll no {roll_no} in course {course}")
    
    return{
        "message" : "Student updated",
        "Updated" : update_data
    }
@app.put("/department/{courseName}/{courseCode}")
def update_department(courseName:str,courseCode:str,department_update:newdepartment):
    update_Data=department_update.model_dump()
    result=department_collection.update_one({"courseName":courseName,"courseCode":courseCode},{"$set":update_Data})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No department exist with courseName {courseName} courseCode {courseCode}")
        
    
    return{
        "message" : "department updated",
        "Updated" : update_Data
    }
@app.delete("/student/{course}/{roll_no}")
def delete_student(course:str,roll_no:int):
    result=student_collection.delete_one({"course":course,"roll_no":roll_no})
    if result.delete_one==0:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f" cannot delete student with roll no {roll_no} and course {course} doesn't exist")
    return{"status":"deleted",
           "message":"student deleted"}


@app.delete("/department/{courseName}/{courseCode}")
def delete_department(courseName:str,courseCode:str):
    result=department_collection.delete_one({"courseName":courseName,"courseCode":courseCode})
    if result.delete_one==0:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f" cannot delete department with courseName {courseName} courseCode {courseCode} doesn't exist")
    return{"status":"deleted",
           "message":" department deleted"}

                            
                             
    }
