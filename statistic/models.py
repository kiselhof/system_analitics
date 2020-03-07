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
    (1, 'Bachelor', 'Бакалавр'),
    (8, 'Master', 'Магістр'),
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


class Department(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}'


class Speciality(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} ({self.department})'


class AcademicGroup(models.Model):
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)
    degree = models.IntegerField(choices=GRADE_CHOICES)
    education_start = models.DateField()

    def __str__(self):
        return f'{self.speciality} [{self.degree}] - {self.course} курс'

    @property
    def course(self):  # TODO think about it
        return None


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Student(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(AcademicGroup, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.last_name} {self.first_name}' + \
               f' {self.middle_name}' if self.middle_name else ''


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    value = models.IntegerField()

    def __str__(self):
        return f'{self.semester} - {self.subject} [{self.value}]'
