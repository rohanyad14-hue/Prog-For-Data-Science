"""M1-Q6  Student record manager
Topics: inheritance, csv, string methods, conditionals, exceptions, json, dict.
"""
import csv
import json


class Person:
    def __init__(self, name, email):
        self.name = name.strip().title()
        self.email = email.strip().lower()
        if "@" not in self.email or not self.email.endswith(".ac.in"):
            raise ValueError(f"invalid email '{email.strip()}'")

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Student(Person):
    def __init__(self, reg_no, name, email, marks):
        super().__init__(name, email)           # validates name / email
        self.reg_no = reg_no.strip()
        try:
            self.marks = float(marks)
        except ValueError:
            raise ValueError(f"non-numeric marks '{marks}'") from None
        if not 0 <= self.marks <= 100:
            raise ValueError(f"marks out of range '{marks}'")

    def grade(self):
        if self.marks >= 85:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 50:
            return "C"
        return "Fail"

    def to_dict(self):
        return {"reg_no": self.reg_no, "name": self.name, "email": self.email,
                "marks": self.marks, "grade": self.grade()}


students = []            # list of Student objects
by_reg = {}              # dict keyed by register number
errors = []              # (line number, reason)

with open("students.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for line_no, row in enumerate(reader, start=2):      # line 1 is the header
        try:
            s = Student(row["reg_no"], row["name"], row["email"], row["marks"])
        except ValueError as err:
            errors.append((line_no, row["reg_no"], str(err)))
        else:
            students.append(s)
            by_reg[s.reg_no] = s

with open("errors.log", "w", encoding="utf-8") as log:
    for line_no, reg, reason in errors:
        log.write(f"line {line_no} ({reg}): skipped - {reason}\n")

report = {
    "valid_count": len(students),
    "skipped_count": len(errors),
    "students": [s.to_dict() for s in students],
}
with open("report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("Valid students")
for s in students:
    print(f"  {s.reg_no}  {s.name:<12} {s.marks:>5}  grade {s.grade()}")
print("\nDictionary keys:", list(by_reg))
print("\nerrors.log")
print(open("errors.log", encoding="utf-8").read(), end="")
print("\nreport.json")
print(open("report.json", encoding="utf-8").read())
