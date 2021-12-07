from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


class Student:
    def __init__(self):
        self.students = pd.read_csv("studentRecors.txt", sep="\t")
        columns = {
            "ID": "student_id",
            "Name": "name",
            "Gender": "gender",
            "Age": "age",
            "Enroll date": "enrollment_date",
            "Midterm": "midterm_exam_score",
            "Final": "final_exam_score",
            "GPA": "gpa"
        }
        self.students.rename(columns=columns, inplace=True)
        self.students.student_id = self.students.student_id.astype(str).str.zfill(3)
        self.students["enrollment_date"] = pd.to_datetime(self.students["enrollment_date"], format="%Y/%m/%d")
        self.last_id = int(self.students.tail(1)["student_id"])

    def add(self, name, gender, age, enrollment_date, midterm_exam_score, final_exam_score):
        student_id = str(self.last_id + 1).zfill(3)
        new_line = pd.DataFrame([{
            "student_id": student_id,
            "name": name,
            "gender": gender,
            "age": age,
            "enrollment_date": datetime.strptime(enrollment_date, "%Y/%m/%d"),
            "midterm_exam_score": midterm_exam_score,
            "final_exam_score": final_exam_score,
            "gpa": 0.4 * midterm_exam_score + 0.6 * final_exam_score
        }])
        self.students = pd.concat([self.students, new_line], ignore_index=True)
        self.last_id += 1

    def calculate_gpa(self):
        self.students.gpa = 0.4 * self.students.midterm_exam_score + 0.6 * self.students.final_exam_score
        self.print_all()

    def update(self, student_id, **fields):
        """Update information about student using student_id"""
        self.students.loc[self.students.student_id == student_id, fields.keys()] = fields.values()

    def print_all(self):
        """Sort students by GPA and print all the students"""
        self.students.sort_values(by="gpa", ascending=False, inplace=True)
        print(self.students.to_string(index=False))

    def calculate_grad_date(self, student_id, duration):
        """Calculate the graduation date of a student using student_id"""
        s = duration.split()
        years = int(s[0])
        months = int(s[1])
        enrollment_date = self.students[self.students.student_id == student_id].enrollment_date[0]
        grad_date = enrollment_date + relativedelta(years=years, months=months)
        print(grad_date)

    def save_to_disk(self):
        """Save student information, including gpa, to a tab-separated-values txt file"""
        self.students.sort_values(by="gpa", ascending=False, inplace=True)
        self.students.to_csv("studentRecords_out.txt", sep="\t", index=False)


def main():
    students = Student()
    while True:
        print("""
        1. Add a student
        2. Update a student
        3. Calculate the GPA of students
        4. Calculate the graduation date of a student
        5. Print all students
        6. Save student information to disk
        7. Exit
        """)
        choice = input("Enter your choice: ")
        if choice == "1":
            line = input(
                "Enter student info: \n'name' 'gender, 0 male 1 female' 'age' 'enrollment date yyyy/mm/dd' 'midterm "
                "score' 'final score'\n").split()
            # if there are digits in line, convert them to int
            for i in range(len(line)):
                if line[i].isdigit():
                    line[i] = int(line[i])
            students.add(*line)
        elif choice == "2":
            student_id = input("Enter student id: ")
            line = input("Enter comma separated key-value pairs: \n'key1=val1,key2=val2'\n")
            fields = {}
            for pair in line.split(","):
                key, value = pair.split("=")
                if value.isdigit():
                    value = int(value)
                fields[key] = value
            students.update(student_id, **fields)
        elif choice == "3":
            students.calculate_gpa()
        elif choice == "4":
            student_id = input("Enter student id: ")
            duration = input("Enter duration: \n 'years months'\n")
            students.calculate_grad_date(student_id, duration)
        elif choice == "5":
            students.print_all()
        elif choice == "6":
            students.save_to_disk()
        else:
            break


if __name__ == "__main__":
    main()
