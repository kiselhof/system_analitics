import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, Count

from statistic.models import Student, Speciality, Faculty, Mark, Subject, AdditionalMark


class MarkInlineAdmin(admin.TabularInline):
    model = Mark


class AdditionalMarkInlineAdmin(admin.TabularInline):
    model = AdditionalMark


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['full_name']
    list_filter = ['education_form', 'grade', 'speciality']
    inlines = (MarkInlineAdmin, AdditionalMarkInlineAdmin)

    def changelist_view(self, request, extra_context=None):
        choices = [0, 35, 60, 64, 74, 82, 90, 100]
        pairs = list(zip(choices[::], choices[1::]))
        chart_data = [
            self.get_changelist_instance(request).queryset.annotate(average_mark=Avg('mark__value')).filter(average_mark__gte=left).filter(average_mark__lt=right).count() for left, right in pairs
        ]

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


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
