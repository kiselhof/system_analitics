from django.db import models
from model_utils import Choices

__all_ = [
    'Mark',
    'Faculty',
    'Department',
    'Speciality',
    'AcademicGroup',
    'Student',
]

GRADE_CHOICES = Choices(
    (7, 'Bachelor', 'Бакалавр'),
    (8, 'Master', 'Магістр'),
)

EDUCATION_FORM_CHOICES = Choices(
    (0, 'FullTime', 'Денна'),
    (1, 'PartTime', 'Заочна'),
)

SEMESTER_CHOICES = Choices(
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
)


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Speciality(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} ({self.faculty})'


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    education_form = models.IntegerField(choices=EDUCATION_FORM_CHOICES)

    def __str__(self):
        return f'[{EDUCATION_FORM_CHOICES[self.education_form]}] ' \
               f'[{GRADE_CHOICES[self.grade]}] ' \
               f'[{self.speciality}] - ' \
               f'{self.full_name}'


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    value = models.IntegerField()

    def __str__(self):
        return f'{self.student} [{self.semester} семестр] - {self.subject} [{self.value}]'
