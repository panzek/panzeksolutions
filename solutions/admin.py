from django.contrib import admin
from .models import Solution


class SolutionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'tech_stack',
        'image',
    )


admin.site.register(Solution, SolutionAdmin)
