
from django import forms
from django.contrib import admin
from django.db import models

from .forms import EntryForm
from .models import Category, Entry, Image


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'created', 'updated')
    list_per_page = 20
    prepopulated_fields = {'slug': ('name',)}


class ImageAdmin(admin.TabularInline):
    extra = 1
    model = Image
    verbose_name_plural = 'Project Images'
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':5, 'cols':60})},
    }


class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    form = EntryForm
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'rows': 5, 'cols': 60})
        },
    }
    date_hierarchy = 'published'
    inlines = (ImageAdmin,)
    list_display = ('title', 'category', 'published', 'featured', 'status')
    list_filter = ( 'published', 'category', 'featured', 'status')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
