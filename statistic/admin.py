from django.contrib import admin
from statistic.models import Student, Speciality, Faculty, Mark, Subject, AdditionalMark


class MarkInlineAdmin(admin.TabularInline):
    model = Mark


class AdditionalMarkInlineAdmin(admin.TabularInline):
    model = AdditionalMark


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['full_name']
    list_filter = ['education_form', 'grade', 'speciality']
    inlines = (MarkInlineAdmin, AdditionalMarkInlineAdmin)


class SpecialityInlineAdmin(admin.TabularInline):
    model = Speciality


class FacultyAdmin(admin.ModelAdmin):
    inlines = (SpecialityInlineAdmin,)


class StudentInlineAdmin(admin.TabularInline):
    model = Student


class SubjectAdmin(admin.ModelAdmin):
    pass


class SpecialityAdmin(admin.ModelAdmin):
    inlines = (StudentInlineAdmin,)


class AdditionalMarkAdmin(admin.ModelAdmin):
    pass


class MarksAdmin(admin.ModelAdmin):
    search_fields = ['student__full_name', 'student__speciality__name', 'subject__name', 'value']
    list_filter = [
        'semester',
        'student__grade',
        'student__education_form',
        'student__speciality__faculty__name',
        'student__speciality__name',
    ]


admin.site.register(Student, StudentAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Mark, MarksAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(AdditionalMark, AdditionalMarkAdmin)
