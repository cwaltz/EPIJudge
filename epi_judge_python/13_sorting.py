"""
#13.0
"""


class Student:
    def __init__(self, name: str, grade_point_average: float) -> None:
        self.name = name
        self.grade_point_average = grade_point_average

    def __lt__(self, other: "Student") -> bool:
        return self.name < other.name


def print_students(students: list[Student]) -> None:
    for s in students:
        print(s.name, s.grade_point_average)


students = [
    Student('A', 4.0),
    Student('C', 3.0),
    Student('B', 2.0),
    Student('D', 3.2),
]
print("\nstudents:")
print_students(students)

# Sort according to __lt__ defined in Student. students remained unchanged.
students_sort_by_name = sorted(students)
print("\nstudents sorted by name:")
print_students(students_sort_by_name)

# Sort students in-place by grade_point_average.
students.sort(key=lambda student: student.grade_point_average)
print("\nstudents sorted by gpa:")
print_students(students)


print("\n\nKnow your sorting libraries")
a = [1, 2, 4, 3, 5, 0, 11, 21, 100]
print(f"\na = {a}")
a.sort(key=lambda x: str(x), reverse=True)
print(f"\na.sort(key=lambda x: str(x), reverse=True) = {a}")
b = sorted(a, key=lambda x: str(x))
print(f"\nsorted(a, key=lambda x: str(x)) = {b}")
