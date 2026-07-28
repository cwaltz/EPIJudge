"""
Rectangles that share only a boundary (width or height of 0) are considered
valid intersections.
"""

from dataclasses import dataclass
from typing import NamedTuple

from test_framework import generic_test
from test_framework.test_failure import PropertyName


class Rect(NamedTuple):
    x: int  # x coordinate of the bottom-left vertex
    y: int  # y coordinate of the bottom-left vertex
    width: int  # width of the rectangle
    height: int  # height of the rectangle


# The following dataclass can replace the above NamedTuple in general.
# But, we are using index access on NamedTuple in res_printer().
# Also, a dataclass does not support unpacking out of the box. You would have
# to write a custom __iter__ method to make the following statement work.
# x, y, width, height = rectangle
@dataclass(frozen=True, slots=True)
class Rectangle:
    x: int
    y: int
    width: int
    height: int


def intersect_rectangle_interview(r1: Rect, r2: Rect) -> Rect:
    """
    #4.11

    Time complexity = O(1)
    Space complexity = O(1)

    Test PASSED (10000/10000) [   1 us]
    Average running time:    1 us
    Median running time:     1 us
    """

    x_intersect_start = max(r1.x, r2.x)
    x_intersect_end = min(r1.x + r1.width, r2.x + r2.width)
    if x_intersect_end < x_intersect_start:
        return Rect(0, 0, -1, -1)
    # Sentinel Values (Code Smell): Returning a "dummy" object like
    # Rect(0, 0, -1, -1) to indicate failure is generally frowned upon in
    # modern Python. In an interview, it is much better to return None
    # (like in the enterprise production version below)
    # (or throw an Exception if guaranteed to intersect) to indicate the
    # absence of an intersection. Using a dummy object forces the caller to
    # write awkward checks like if result.width == -1:.

    y_intersect_start = max(r1.y, r2.y)
    y_intersect_end = min(r1.y + r1.height, r2.y + r2.height)
    if y_intersect_end < y_intersect_start:
        return Rect(0, 0, -1, -1)

    return Rect(
        x_intersect_start,
        y_intersect_start,
        x_intersect_end - x_intersect_start,
        y_intersect_end - y_intersect_start
    )


def intersect_rectangle_prod(r1: Rect, r2: Rect) -> Rect | None:
    """
    Calculates the intersection of two rectangles.

    Returns a new Rect representing the intersection, or None if they do not
    overlap. Rectangles that share only a boundary (width or height of 0) are
    considered valid intersections.
    """
    # Defensive programming: ensure inputs are valid
    if r1.width < 0 or r1.height < 0 or r2.width < 0 or r2.height < 0:
        raise ValueError("Rectangle dimensions cannot be negative.")

    # Calculate X overlap
    x_intersect_start = max(r1.x, r2.x)
    x_intersect_end = min(r1.x + r1.width, r2.x + r2.width)

    # If end is less than start, they do not overlap on the X axis
    if x_intersect_end < x_intersect_start:
        return None

    # Calculate Y overlap
    y_intersect_start = max(r1.y, r2.y)
    y_intersect_end = min(r1.y + r1.height, r2.y + r2.height)

    # If end is less than start, they do not overlap on the Y axis
    if y_intersect_end < y_intersect_start:
        return None

    return Rect(
        x_intersect_start,
        y_intersect_start,
        x_intersect_end - x_intersect_start,
        y_intersect_end - y_intersect_start
    )


def intersect_rectangle_epi(r1: Rect, r2: Rect) -> Rect:
    """
    Violates DRY Principle (Don't Repeat Yourself): It calculates the bounding
    boxes twice—once inside the is_intersect helper function, and again when
    returning the final Rect. The interview/prod version above calculates the
    bounds once, checks for validity, and reuses those variables, making it
    cleaner and slightly more optimal.

    Test PASSED (10000/10000) [   1 us]
    Average running time:    1 us
    Median running time:     1 us
    """

    def is_intersect(s1: Rect, s2: Rect) -> bool:
        return (s1.x <= s2.x + s2.width and s1.x + s1.width >= s2.x
                and s1.y <= s2.y + s2.height and s1.y + s1.height >= s2.y)

    if not is_intersect(r1, r2):
        return Rect(0, 0, -1, -1)  # No intersection.
    return Rect(max(r1.x, r2.x), max(r1.y, r2.y),
                min(r1.x + r1.width, r2.x + r2.width) - max(r1.x, r2.x),
                min(r1.y + r1.height, r2.y + r2.height) - max(r1.y, r2.y))


def intersect_rectangle_wrapper(r1, r2):
    return intersect_rectangle_interview(Rect(*r1), Rect(*r2))


def res_printer(prop, value):
    def fmt(x):
        return [x[0], x[1], x[2], x[3]] if x else None

    if prop in (PropertyName.EXPECTED, PropertyName.RESULT):
        return fmt(value)
    else:
        return value


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('rectangle_intersection.py',
                                       'rectangle_intersection.tsv',
                                       intersect_rectangle_wrapper,
                                       res_printer=res_printer))
