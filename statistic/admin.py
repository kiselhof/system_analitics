from django.contrib import admin
from statistic.models import Student, Speciality, Faculty, Mark, Subject


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['full_name']
    list_filter = ['education_form', 'grade', 'speciality']


class FacultyAdmin(admin.ModelAdmin):
    pass


class SubjectAdmin(admin.ModelAdmin):
    pass


class SpecialityAdmin(admin.ModelAdmin):
    pass


class MarksAdmin(admin.ModelAdmin):
    search_fields = ['student__full_name', 'student__speciality__name', 'subject__name', 'value']
    list_filter = ['semester', 'student__grade', 'student__education_form']


admin.site.register(Student, StudentAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Mark, MarksAdmin)
admin.site.register(Subject, SubjectAdmin)
