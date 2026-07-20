from fastapi import FastAPI, HTTPException, status, Depends
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import jwt
# hello  world
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
# hello  world
Secret_key = os.getenv("Secret_key")
Algorithm = "HS256"
Access_token_expire_minutes = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def create_access_token(data: dict)->str:
    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=Access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Secret_key, algorithm=Algorithm)

mongo_uri = os.getenv("mongo_uri")
cli = MongoClient(mongo_uri)

db = cli.college
department_collection = db.Department
student_collection = db.Student
user_collection = db.User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
class NewStudent(BaseModel):
    name : str
    roll_no : int
    course : str

class newdepartment(BaseModel):
    courseName:str
    courseCode:str

class NewUser(BaseModel):
    username: str
    password : str
    role : str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

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

@app.post("/student", dependencies=[Depends(oauth2_scheme)])
def add_student(student: NewStudent):
    student_dict = student.model_dump()
    student_collection.insert_one(student_dict)
    return {"message" : "Student Added",
            "Added_Student" : student.name}

@app.post("/departments",dependencies=[Depends(oauth2_scheme)])
def add_departments(department:newdepartment):
    department_dict=department.model_dump()
    department_collection.insert_one(department_dict)
    return {"message" : "department Added",
            "Added_department" : department.courseName}

@app.put("/student/{course}/{roll_no}", dependencies=[Depends(oauth2_scheme)])
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
@app.put("/department/{courseName}/{courseCode}",dependencies=[Depends(oauth2_scheme)])
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

@app.delete("/department/{courseName}/{courseCode}",dependencies=[Depends(oauth2_scheme)])
def delete_department(courseName : str , courseCode : str):
    result = department_collection.delete_one({"courseName" : courseName , "courseCode" : courseCode})
    if result.deleted_count == 0:
        raise HTTPException(
            status = status.HTTP_404_NOT_FOUND,
            details = f" {courseName} Department Doesnt exist" 
        )
    return{
        "message" : "Department deleted"
        }

@app.delete("/student/{course}/{roll_no}",dependencies=[Depends(oauth2_scheme)])
def delete_student(course:str,roll_no:int):
    result=student_collection.delete_one({"course":course,"roll_no":roll_no})
    if result.deleted_count==0:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f" cannot delete student with roll no {roll_no} and course {course} doesn't exist")
    return{"status":"deleted",
           "message":"student deleted"}

@app.post("/register",status_code=status.HTTP_201_CREATED)
def register_user(user: NewUser):
    if user.role not in ["admin","student","faculty"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            details="Cant register")
    user_dict = {"username" : user.username , 
                 "password" : hash_password(user.password) ,
                 "role" : user.role}
    
    user_collection.insert_one(user_dict)
    return{
        "message" : f"User {user.username} added"
    }

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user=user_collection.find_one({"username" : form_data.username})
    if not user or not pwd_context.verify(form_data.password,user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username Or Password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(
        data = {"sub" : user["username"], "role" : user["role"]}
    )
    return {"access_token" : access_token, "token_type": "bearer"}
