from fastapi import FastAPI, Path

app = FastAPI()


student = {1: {"name": "Reeju", "age": 23, "class": "year 23"}}


@app.get("/")
def index():
    return "Backend is running!!!"


@app.get("/api/")
def api_index():
    return "I need more information"


@app.get("/api/student/get/{student_id}")
def api_student_get_one(student_id: int):

    return student[student_id]
