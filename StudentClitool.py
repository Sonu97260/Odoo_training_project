import json
import os
from abc import ABC, abstractmethod
import argparse

# abstraction using
class StudentOp(ABC):
    @abstractmethod
    def add_student(self, student_id, name, grade):
        pass

    @abstractmethod
    def del_student(self, student_id):
        pass

    @abstractmethod
    def view_student(self, student_id):
        pass

    @abstractmethod
    def list_students(self, student_id, name, grade):
        pass


class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def display(self):
        print(f"ID:{self.student_id},Name:{self.name},Grade: {self.grade}")

    # data save in file
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grade": self.grade
        }

    @staticmethod
    def from_dict(data):
        return Student(data["student_id"], data["name"], data["grade"])


# inheritance
class ManageDetail(StudentOp):
    def __init__(self, filename="students1.txt"):
        self.filename = filename
        self.students = self.load_students()

    def load_students(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                content = f.read()
                data = json.loads(content)
                return [Student.from_dict(d) for d in data]
        return []

    def save_students(self):
        with open(self.filename, "w") as f:
            json.dump([s.to_dict() for s in self.students], f)

    def add_student(self, student_id, name, grade):
        for student in self.students:
            if student.student_id == student_id:
                print("Student with ID already exist",student_id)
                return
        new_student = Student(student_id, name, grade)
        self.students.append(new_student)
        self.save_students()
        print(f"Student added: ID:{student_id} Name: {name}  Grade: {grade}")

    def view_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                student.display()
                return
        print(f"No student with ID {student_id} found")

    def del_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                self.save_students()
                print(f"Deleted student with id {student_id}")
                return
        print(f"No student with id {student_id} found")

    def list_students(self):
        for student in self.students:
            student.display()
            print(student.to_dict())

def main():
    details = ManageDetail(filename="students1.txt")

    while True:
        print("/Choose one of the following options:")
        print("1.add student")
        print("2.view student")
        print("3.list students")
        print("4.delete student")
        print("5.exit")

        choice = input("Enter your choice between 1 to 5: ")
        if choice == "1":
            student_id = input("Enter student ID: ")
            name = input("Enter name: ")
            grade = input("Enter grade: ")
            details.add_student(student_id, name, grade)

        elif choice == "2":
            student_id = input("Enter student ID: ")
            details.view_student(student_id)

        elif choice == "3":
            details.list_students()

        elif choice == "4":
            student_id = input("Enter student ID: ")
            details.del_student(student_id)

        elif choice == "5":
            exit(0)



if __name__ == "__main__":
    main()
