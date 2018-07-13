
from django.contrib import admin
from django.db import models
from django import forms


from models import Range, Colour
from widgets import RedactorTextarea


class ColourAdmin(admin.TabularInline):
    extra = 1
    model = Colour
    verbose_name_plural = 'Colours'

class RangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RangeForm, self).__init__(*args, **kwargs)

        # JSON Redactor settings
        settings = '{'
        settings += '"minHeight": "350"'
        settings += '}'

        self.fields['description'].widget = RedactorTextarea(attrs={'data-settings': settings})

    class Meta:
        model = Range

class RangeAdmin(admin.ModelAdmin):
    form = RangeForm
    inlines = (ColourAdmin,)
    list_display = ('name', 'symbol', 'created', 'updated')
    list_per_page = 50
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Range, RangeAdmin)
