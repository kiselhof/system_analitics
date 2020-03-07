import csv
import logging
import os
from typing import List, Type, Optional

from django.db import models, transaction
from django.core.management.base import BaseCommand
from model_utils import Choices

from statistic.models import Student, Faculty, Speciality, Subject, EDUCATION_FORM_CHOICES, GRADE_CHOICES, Mark, \
    SEMESTER_CHOICES

logger = logging.getLogger(__name__)


class ImportException(Exception):
    pass


EXPECTED_HEADERS = ['ФІО', 'СПЕЦІАЛЬНІСТЬ', 'КУРС', 'ФОРМА НАВЧАННЯ', 'ФАКУЛЬТЕТ', 'ПРЕДМЕТ', 'ОЦІНКА', 'СЕМЕСТР']


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--file',
            type=str,
            nargs='?',
            help='File name for processing',
        )

    def handle(self, *args, **options):
        if options['file']:
            logger.warning(f'File("{options["file"]}") is being processed...')
            self.__process_csv_file(options['file'])
        else:
            logger.error('No file name!!!')

    @classmethod
    def __process_csv_file(cls, file_name: str):
        path = os.path.join('csv_files', file_name)
        with open(path, newline='') as csv_file:
            csv_data = csv.reader(csv_file)
            headers = next(csv_data)
            if cls.__is_headers_valid(headers):
                for row in csv_data:
                    try:
                        cls.__process_row(row)
                    except ImportException as e:
                        logger.exception(e)

            else:
                logger.exception(f'File with {headers} columns is not supported!')

    @classmethod
    @transaction.atomic
    def __process_row(cls, row: List[str]) -> Student:
        logger.warning(f'Row("{row}" is being processed...')
        keys = [
            'student_full_name', 'speciality_name', 'course', 'education_form',
            'faculty_name', 'subject_name', 'mark', 'semester'
        ]
        data = dict(zip(keys, row))

        faculty = cls.__get_or_create(Faculty, name=data['faculty_name'])

        speciality = cls._process_speciality(data['speciality_name'], faculty)
        grade = cls.__get_grade_by_speciality_name(data['speciality_name'])

        subject = cls.__get_or_create(Subject, name=data['subject_name'])
        education_form = cls.__get_choices_id_by_name(EDUCATION_FORM_CHOICES, data['education_form'])

        student = cls.__get_or_create(
            Student,
            full_name=data['student_full_name'],
            speciality=speciality,
            grade=grade,
            education_form=education_form,
        )

        try:
            semester = int(data['semester'])
            semester = SEMESTER_CHOICES[semester]
        except:
            raise ImportException(f'Unable to process semester(\"{data["semester"]}\")')

        mark = cls.__get_or_create(
            Mark,
            student=student,
            semester=semester,
            value=data['mark'],
            subject=subject,
        )

        return mark

    @classmethod
    def __get_or_create(cls, model: Type[models.Model], **kwargs):
        result = model.objects.filter(**kwargs).first()
        if not result:
            logger.warning(f'{model.__name__}("{kwargs}" created...')
            result = model.objects.create(**kwargs)
        return result

    @classmethod
    def __get_choices_id_by_name(cls, choices: Choices, name: str) -> Optional[int]:
        choices = dict(choices)
        choices = dict(zip(choices.values(), choices.keys()))
        key = choices.get(name)
        if key is None:
            raise ImportException(f'Unknown {choices.__name__}("{name}")!')
        return key

    @classmethod
    def __get_grade_by_speciality_name(cls, name: str):
        if '(МАГ)' in name:
            return GRADE_CHOICES.Master
        else:
            return GRADE_CHOICES.Bachelor

    @classmethod
    def __is_headers_valid(cls, headers: List[str]) -> bool:
        return headers == EXPECTED_HEADERS

    @classmethod
    def _process_speciality(cls, name: str, faculty: Faculty) -> Optional[Speciality]:
        name = name.replace(' (МАГ)', '')
        speciality = cls.__get_or_create(Speciality, name=name, faculty=faculty)
        return speciality
