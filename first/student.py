class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if (
            isinstance(lecturer, Lecturer)
            and course in lecturer.courses_attached
            and course in self.courses_in_progress
        ):
            lecturer.rate_hw(self, course, grade)
        else:
            return "Ошибка"

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {self.calc_grade()}\n"
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
            f'Завершенные курсы: {", ".join(self.finished_courses)}'
        )

    def calc_grade(self):
        total_grades = sum(sum(course_grades) for course_grades in self.grades.values())
        total_assignments = sum(
            len(course_grades) for course_grades in self.grades.values()
        )
        return (
            round(total_grades / total_assignments, 1) if total_assignments > 0 else 0
        )

    def __lt__(self, other):
        return self.calc_grade() < other.calc_grade()

    def __le__(self, other):
        return self.calc_grade() <= other.calc_grade()

    def __eq__(self, other):
        return self.calc_grade() == other.calc_grade()

    def __ne__(self, other):
        return self.calc_grade() != other.calc_grade()

    def __gt__(self, other):
        return self.calc_grade() > other.calc_grade()

    def __ge__(self, other):
        return self.calc_grade() >= other.calc_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return "Ошибка"

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lecture_grades = {}

    def calc_lecture_grade(self):
        if self.lecture_grades:
            total_grade = sum(sum(grades) for grades in self.lecture_grades.values())
            total_count = sum(len(grades) for grades in self.lecture_grades.values())
            return total_grade / total_count
        else:
            return 0

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.calc_lecture_grade()}"

    def __lt__(self, other):
        return self.calc_lecture_grade() < other.calc_lecture_grade()

    def __le__(self, other):
        return self.calc_lecture_grade() <= other.calc_lecture_grade()

    def __eq__(self, other):
        return self.calc_lecture_grade() == other.calc_lecture_grade()

    def __ne__(self, other):
        return self.calc_lecture_grade() != other.calc_lecture_grade()

    def __gt__(self, other):
        return self.calc_lecture_grade() > other.calc_lecture_grade()

    def __ge__(self, other):
        return self.calc_lecture_grade() >= other.calc_lecture_grade()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw_student(self, student, course, grade):
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return "Ошибка"

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


def calc_hw_grade(students, course):
    total_grade = sum(
        sum(student.grades[course]) for student in students if course in student.grades
    )
    total_assignments = sum(
        len(student.grades[course]) for student in students if course in student.grades
    )
    return round(total_grade / total_assignments, 1) if total_assignments > 0 else 0


def calc_lecture_grade(lecturers, course):
    total_grade = sum(
        sum(lecturer.lecture_grades[course])
        for lecturer in lecturers
        if hasattr(lecturer, "lecture_grades") and course in lecturer.lecture_grades
    )
    total_count = sum(
        len(lecturer.lecture_grades[course])
        for lecturer in lecturers
        if hasattr(lecturer, "lecture_grades") and course in lecturer.lecture_grades
    )
    return round(total_grade / total_count, 1) if total_count > 0 else 0


student1 = Student("George", "Ford", "female")
student2 = Student("Tom", "Metal", "male")

lecturer1 = Lecturer("Rob", "Griffin")
lecturer2 = Lecturer("Olga", "Wood")

reviewer1 = Reviewer("John", "Taylor")
reviewer2 = Reviewer("Arthur", "Brown")

# Assign courses
student1.courses_in_progress.append("Python")
student2.courses_in_progress.append("Python")

lecturer1.courses_attached.append("Python")
lecturer2.courses_attached.append("Python")

reviewer1.courses_attached.append("Python")
reviewer2.courses_attached.append("Python")

# Rate assignments
reviewer1.rate_hw_student(student1, "Python", 10)
reviewer1.rate_hw_student(student2, "Python", 8)

lecturer1.rate_hw(student1, "Python", 9)
lecturer1.rate_hw(student2, "Python", 8)

# Rate lectures
lecturer1.lecture_grades["Python"] = [7, 8, 6]
lecturer2.lecture_grades["Python"] = [8, 7, 7]

# Print student information
print(student1)
print(student2)

# Print lecturer information
print(lecturer1)
print(lecturer2)

# Print reviewer information
print(reviewer1)
print(reviewer2)

# Calculate and print average grades
python_hw_grade = calc_hw_grade([student1, student2], "Python")
print(f"\nСредняя оценка за домашние задания по Python: {python_hw_grade}")

python_lecturers = [lecturer1, lecturer2]
python_lecture_grade = calc_lecture_grade(python_lecturers, "Python")
print(f"Средняя оценка за лекции по Python: {python_lecture_grade}")
