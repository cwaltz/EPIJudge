import bisect
import collections
from typing import Tuple, List

Student = collections.namedtuple('Student', ('name', 'grade_point_average'))


def comp_gpa(student: Student) -> Tuple[float, str]:
    return -student.grade_point_average, student.name


def search_student(students: List[Student], target: Student, comp_gpa) -> bool:
    """
    Assuming the i-th element in the sequence can be accessed in O(1) time,
    the time complexity of the program is O(log n).
    """

    i = bisect.bisect_left([comp_gpa(s) for s in students], comp_gpa(target))
    return 0 <= i < len(students) and students[i] == target
