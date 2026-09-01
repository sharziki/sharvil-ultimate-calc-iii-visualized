"""Canonical MA 26100 Fall 2026 course data.

Every date, lesson split and weight below is transcribed from the two official
PDFs published on the department course page (verified 2026-09-01):

  https://www.math.purdue.edu/academic/courses/semester/202710/ma26100/Schedule261.pages.pdf
  https://www.math.purdue.edu/academic/courses/semester/202710/ma26100/MA261F26GroundRules.pages2.pdf

Nothing here is inferred from a previous semester.
"""

YEAR = 2026
TERM = "Fall 2026"
VERIFIED = "2026-09-01"

SCHED_PDF = ("https://www.math.purdue.edu/academic/courses/semester/202710/"
             "ma26100/Schedule261.pages.pdf")
RULES_PDF = ("https://www.math.purdue.edu/academic/courses/semester/202710/"
             "ma26100/MA261F26GroundRules.pages2.pdf")
COURSE_PAGE = "https://www.math.purdue.edu/ma261"

# lesson number -> (sections string, guide section ids that cover it)
LESSONS = {
    1:  ("13.1-13.4",              ["s131", "s132", "s133", "s133b", "s134"]),
    2:  ("12.1 (to Ex 3), 13.5 lines", ["s121", "s135"]),
    3:  ("13.5 planes, 13.6 (to Ex 2)", ["s135", "s135b", "s136"]),
    4:  ("13.6 (rest)",            ["s136"]),
    5:  ("14.1",                   ["s141"]),
    6:  ("14.2, 14.3 (to Ex 1)",   ["s142", "s143"]),
    7:  ("14.3 (rest)",            ["s143"]),
    8:  ("14.4, 14.5 (to Thm 14.5)", ["s144"]),
    9:  ("15.1",                   ["s151"]),
    10: ("15.2",                   ["s152"]),
    11: ("15.3",                   ["s153"]),
    12: ("15.4",                   ["s154"]),
    13: ("15.5",                   ["s155"]),
    14: ("15.6",                   ["s156"]),
    15: ("15.7 (to Ex 4)",         ["s157"]),
    16: ("15.7 (rest)",            ["s157"]),
    17: ("15.8",                   ["s158"]),
    18: ("16.1",                   ["s161"]),
    19: ("16.2",                   ["s162"]),
    20: ("16.3 (no Ex 6)",         ["s163"]),
    21: ("16.4 (no Ex 5)",         ["s164"]),
    22: ("16.5 cylindrical",       ["s165c"]),
    23: ("16.5 spherical",         ["s165s"]),
    24: ("16.6",                   ["s166"]),
    25: ("17.1",                   ["s171"]),
    26: ("17.2 (to Ex 3)",         ["s172"]),
    27: ("17.2 (rest)",            ["s172"]),
    28: ("17.3",                   ["s173"]),
    29: ("17.4 (omit stream function)", ["s174"]),
    30: ("17.5",                   ["s175"]),
    31: ("17.6 (to Ex 4)",         ["s176p"]),
    32: ("17.6 (Ex 4 to table 17.3)", ["s176a"]),
    33: ("17.6 (rest)",            ["s176f"]),
    34: ("17.7 (to Ex 3)",         ["s177"]),
    35: ("17.7 (rest)",            ["s177"]),
    36: ("17.8 (to Ex 3)",         ["s178"]),
    37: ("17.8 (rest)",            ["s178"]),
}

# Every assessment, in calendar order.
#   id, kind, label, iso date, human date, lessons covered, textbook sections,
#   the question-bank sections that land in this bucket, one-line "what it is"
STOPS = [
    dict(id="q1",  kind="quiz", label="Quiz 1", date="2026-09-01",
         when="Tue Sep 1 · recitation", lessons=[1, 2],
         secs_label="13.1–13.4 · 12.1 · 13.5 lines",
         secs=["13.1", "13.2", "13.3", "13.4", "12.1", "13.5L"],
         blurb="Vectors themselves: components, length, dot, cross — plus "
               "parametric curves and the equations of a line in space."),
    dict(id="q2",  kind="quiz", label="Quiz 2", date="2026-09-08",
         when="Tue Sep 8 · recitation", lessons=[3, 4],
         secs_label="13.5 planes · 13.6",
         secs=["13.5P", "13.6"],
         blurb="Planes — normal vectors, three points, distances — and the six "
               "quadric surfaces you identify from traces."),
    dict(id="q3",  kind="quiz", label="Quiz 3", date="2026-09-15",
         when="Tue Sep 15 · recitation", lessons=[5, 6, 7],
         secs_label="14.1 · 14.2 · 14.3",
         secs=["14.1", "14.2", "14.3"],
         blurb="A vector whose tip moves: space curves, differentiating and "
               "integrating them, and motion in space."),
    dict(id="q4",  kind="quiz", label="Quiz 4", date="2026-09-22",
         when="Tue Sep 22 · recitation", lessons=[8, 9, 10],
         secs_label="14.4 · 14.5 · 15.1 · 15.2",
         secs=["14.4", "14.5", "15.1", "15.2"],
         blurb="Arc length and curvature, then the jump to several variables: "
               "surfaces, level curves, and limits that die along a path."),
    dict(id="q5",  kind="quiz", label="Quiz 5", date="2026-09-29",
         when="Tue Sep 29 · recitation", lessons=[11, 12, 13],
         secs_label="15.3 · 15.4 · 15.5",
         secs=["15.3", "15.4", "15.5"],
         blurb="Partial derivatives, the tree-diagram chain rule, and the "
               "gradient — the single most reused object in the course."),
    dict(id="m1",  kind="exam", label="Midterm 1", date="2026-10-05",
         when="Mon Oct 5 · 8:00 pm", lessons=list(range(1, 17)),
         secs_label="13.1–15.7 (all of Ch. 13–14, Ch. 15 through max/min)",
         secs=["15.6", "15.7"],
         blurb="Lessons 1–16, one hour, multiple choice, no calculator. Stops "
               "in the middle of Chapter 15 — Lagrange is NOT on it.",
         extra="Lessons 14–16 (tangent planes, max/min) are never quizzed. "
               "They arrive between Quiz 5 and this exam, so this is the only "
               "place they are ever tested before the final."),
    dict(id="q6",  kind="quiz", label="Quiz 6", date="2026-10-20",
         when="Tue Oct 20 · recitation", lessons=[17, 18, 19],
         secs_label="15.8 · 16.1 · 16.2",
         secs=["15.8", "16.1", "16.2"],
         blurb="Lagrange multipliers, then double integrals — rectangles "
               "first, then general regions and the order of integration."),
    dict(id="q7",  kind="quiz", label="Quiz 7", date="2026-10-27",
         when="Tue Oct 27 · recitation", lessons=[20, 21, 22],
         secs_label="16.3 · 16.4 · 16.5 cylindrical",
         secs=["16.3", "16.4", "16.5C"],
         blurb="Polar double integrals, triple integrals in Cartesian, and "
               "cylindrical coordinates."),
    dict(id="q8",  kind="quiz", label="Quiz 8", date="2026-11-03",
         when="Tue Nov 3 · recitation", lessons=[23, 24, 25],
         secs_label="16.5 spherical · 16.6 · 17.1",
         secs=["16.5S", "16.6", "17.1"],
         blurb="Spherical coordinates, mass / centre of mass / moments, and "
               "the first look at vector fields."),
    dict(id="q9",  kind="quiz", label="Quiz 9", date="2026-11-10",
         when="Tue Nov 10 · recitation", lessons=[26, 27, 28],
         secs_label="17.2 · 17.3",
         secs=["17.2", "17.3"],
         blurb="Line integrals of functions and of fields, then conservative "
               "fields and the fundamental theorem for line integrals."),
    dict(id="m2",  kind="exam", label="Midterm 2", date="2026-11-18",
         when="Wed Nov 18 · 8:00 pm", lessons=list(range(17, 32)),
         secs_label="15.8–17.6 (Lagrange through surface integrals)",
         secs=["17.4", "17.5"],
         blurb="Lessons 17–31, one hour, multiple choice, no calculator. "
               "Starts at Lagrange.",
         extra="Green's theorem (17.4) and curl / divergence (17.5) are never "
               "quizzed — Lesson 29 and 30 fall between Quiz 9 and this exam. "
               "The ground rules say Lessons 17–31; the calendar teaches "
               "through Lesson 33 before the exam. Assume 17–31 and know 32–33."),
    dict(id="q10", kind="quiz", label="Quiz 10", date="2026-12-01",
         when="Tue Dec 1 · recitation", lessons=[31, 32, 33],
         secs_label="17.6 · all three lessons",
         secs=["17.6"],
         blurb="Surface integrals, all three lessons of them: parametric "
               "surfaces, surface area, and flux."),
    dict(id="fin", kind="exam", label="Final Exam", date="2026-12-14",
         when="Finals week · date TBD", lessons=list(range(1, 38)),
         secs_label="12.1–17.8 · everything",
         secs=["17.7", "17.8"],
         blurb="Two hours, all course content. Stokes and the divergence "
               "theorem appear here and nowhere else.",
         extra="Lessons 34–37 are covered in the last two weeks and are on no "
               "quiz and no midterm. Every point they are worth is on the final."),
]

NO_QUIZ_WEEKS = [
    ("Tue Aug 25", "Quiz 0 — Calc I & II review"),
    ("Tue Oct 6",  "no quiz — Midterm 1 was the night before"),
    ("Tue Oct 13", "no recitation — Fall Break"),
    ("Tue Nov 17", "no quiz — Midterm 2 review"),
    ("Tue Nov 24", "no recitation — Thanksgiving"),
    ("Tue Dec 8",  "no quiz — final review (Lessons 34–37)"),
]

GRADING = [
    ("Quizzes", "15%", "Every recitation, timed, no calculator. "
                       "The 2 lowest are dropped."),
    ("Homework", "15%", "MyLab Math, generally due Tue and Thu 11:59 pm. "
                        "The 3 lowest are dropped."),
    ("Midterm 1", "20%", "Mon Oct 5, 8:00 pm · Lessons 1–16"),
    ("Midterm 2", "20%", "Wed Nov 18, 8:00 pm · Lessons 17–31"),
    ("Final Exam", "30%", "Finals week · everything"),
]

DEADLINES = [
    ("2026-09-04", "Last day to drop with no record on your transcript"),
    ("2026-11-24", "Last day to drop with a W"),
]

# Which quiz/exam bucket a question's data-sec belongs to.
# 13.5 and 16.5 straddle two buckets, so the bank tags them 13.5L/13.5P and
# 16.5C/16.5S when the question itself decides which side it falls on.
SEC_TO_STOP = {}
for s in STOPS:
    for sec in s["secs"]:
        SEC_TO_STOP[sec] = s["id"]
