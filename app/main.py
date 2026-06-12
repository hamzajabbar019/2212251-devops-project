from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Student

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "db": "connected",
        "student": "2212251"
    }


@app.post("/students")
def create_student(student: dict, db: Session = Depends(get_db)):

    existing = db.query(Student).filter(
        Student.reg_no == student["reg_no"]
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student already exists"
        )

    new_student = Student(
        name=student["name"],
        reg_no=student["reg_no"],
        department=student["department"]
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "id": new_student.id,
        "name": new_student.name,
        "reg_no": new_student.reg_no,
        "department": new_student.department
    }


@app.get("/students")
def get_students(db: Session = Depends(get_db)):

    students = db.query(Student).all()

    return [
        {
            "id": s.id,
            "name": s.name,
            "reg_no": s.reg_no,
            "department": s.department
        }
        for s in students
    ]


@app.get("/students/{reg_no}")
def get_student(reg_no: str, db: Session = Depends(get_db)):

    student = db.query(Student).filter(
        Student.reg_no == reg_no
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "id": student.id,
        "name": student.name,
        "reg_no": student.reg_no,
        "department": student.department
    }
