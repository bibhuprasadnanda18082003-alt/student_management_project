
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field, ValidationError

from db import get_connection


# 1. FastAPI Application
app = FastAPI()

# 2. Jinja2 Configuration
templates = Jinja2Templates(directory="templates")


# 3. Student Model
class Student(BaseModel):
    name: str
    age: int = Field(ge=18, le=30)
    gender: str
    marks: int = Field(ge=0, le=100)
    course: str
    image: str
    status: int = Field(ge=0, le=1)


# 4. View All Students
@app.get("/")
def home(req: Request):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()

    connection.close()

    return templates.TemplateResponse(
        request=req,
        name="home.html",
        context={"std": students}
    )


# 5. Add Student Page
@app.get("/students/add")
def add_student_page(req: Request):

    return templates.TemplateResponse(
        request=req,
        name="add.html",
        context={}
    )


# 6. Insert Student
@app.post("/students/add")
def create_student(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    marks: int = Form(...),
    course: str = Form(...),
    image: str = Form(...),
    status: int = Form(...)
):

    std = Student(
        name=name,
        age=age,
        gender=gender,
        marks=marks,
        course=course,
        image=image,
        status=status
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO students
        (name, age, gender, marks, course, image, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            std.name,
            std.age,
            std.gender,
            std.marks,
            std.course,
            std.image,
            std.status
        )
    )

    connection.commit()
    connection.close()

    return RedirectResponse("/", status_code=303)


# 7. View Single Student
@app.get("/students/{id}")
def student_details(id: int, req: Request):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    )

    student = cursor.fetchone()
    connection.close()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return templates.TemplateResponse(
        request=req,
        name="std.html",
        context={"student": student}
    )


# 8. Delete Student
@app.post("/students/delete/{id}")
def delete_student(id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return RedirectResponse("/", status_code=303)


# 9. Edit Student Page
@app.get("/students/edit/{id}")
def edit_student(id: int, req: Request):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    )

    student = cursor.fetchone()
    connection.close()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return templates.TemplateResponse(
        request=req,
        name="edit.html",
        context={"student": student}
    )


# 10. Update Student
@app.post("/students/update/{id}")
def update_student(
    id: int,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    marks: int = Form(...),
    course: str = Form(...),
    image: str = Form(...),
    status: int = Form(...)
):

    std = Student(
        name=name,
        age=age,
        gender=gender,
        marks=marks,
        course=course,
        image=image,
        status=status
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """UPDATE students
        SET name = ?, age = ?, gender = ?, marks = ?,
            course = ?, image = ?, status = ?
        WHERE id = ?""",
        (
            std.name,
            std.age,
            std.gender,
            std.marks,
            std.course,
            std.image,
            std.status,
            id
        )
    )

    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if updated == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return RedirectResponse("/", status_code=303)


# 11. Update Student Attendance
@app.post("/students/attendance/{id}")
def update_attendance(
    id: int,
    status: int = Form(...)
):

    if status not in (0, 1):
        raise HTTPException(status_code=400, detail="Invalid attendance status")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE students SET status = ? WHERE id = ?",
        (status, id)
    )

    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if updated == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return RedirectResponse("/", status_code=303)
