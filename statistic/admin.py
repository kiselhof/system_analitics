from django.contrib import admin

from statistic.models import Student, AcademicGroup, Department, Speciality, Faculty, Mark, Subject

__all__ = [
    'StudentAdmin',
]


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['last_name', 'first_name', 'middle_name', 'group']
    list_filter = ['group']


class AcademicGroupAdmin(admin.ModelAdmin):
    pass


class FacultyAdmin(admin.ModelAdmin):
    pass


class SubjectAdmin(admin.ModelAdmin):
    pass


class DepartmentAdmin(admin.ModelAdmin):
    pass


class SpecialityAdmin(admin.ModelAdmin):
    pass


class MarksAdmin(admin.ModelAdmin):
    pass


admin.site.register(Student, StudentAdmin)
admin.site.register(AcademicGroup, AcademicGroupAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Mark, MarksAdmin)
admin.site.register(Subject, SubjectAdmin)
