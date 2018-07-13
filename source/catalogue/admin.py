
from django.contrib import admin
from django.db import models
from django import forms

from models import (
    Category,
    CategoryImage,
    DocumentSet,
    Document,
    File,
    Group,
    Image,
    Product,
    SubCategory,
)

from widgets import RedactorTextarea



class ImageAdmin(admin.TabularInline):
    extra = 1
    model = Image
    verbose_name_plural = 'Images'


class FileAdmin(admin.TabularInline):
    extra = 1
    model = File
    verbose_name_plural = 'Files'


class ProductForm(forms.ModelForm):
    """
    This form is specifically for providing Entry instance inforation for the
    redactor settings. In this case the PK
    """
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Get Entry Object Instance
        instance = kwargs.get('instance')

        if instance:
            self.fields['group'].queryset = Group.objects.filter(sub_category=instance.sub_category)
        else:
            self.fields['group'].queryset = Group.objects.none()

        # JSON Redactor settings
        settings = '{'
        settings += '"minHeight": "350"'
        settings += '}'

        self.fields['description'].widget = RedactorTextarea(attrs={'data-settings': settings})

    class Meta:
        model = Product


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    filter_horizontal = ('group', 'related_products', 'colour_ranges', 'projects',)
    inlines = (ImageAdmin, FileAdmin,)
    list_display = ('name', 'sub_category', 'order_link', 'format_groups', 'featured', 'created', 'updated')
    list_display_links = ('name',)
    list_filter = ('sub_category', 'group',)
    list_per_page = 50
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description',)

    fieldsets = (
        ('Manage related Products, Projects & Colours', {
            'classes': ('collapse',),
            'fields': ('related_products', 'colour_ranges', 'projects', ),
        }),
        (None, {
            'fields': ('featured', 'sub_category', 'group', 'name', 'slug', 'cover_image', 'excerpt', 'description',),
        }),
    )

    def format_groups(self, product):
        return ', '.join(g.name for g in product.group.all() )
    format_groups.short_description = 'Groups'
    format_groups.admin_order_field = 'Groups'


class CategoryImageAdmin(admin.TabularInline):
    extra = 1
    model = CategoryImage
    verbose_name_plural = 'Images'


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    filter_horizontal = ('colour_ranges',)
    list_display = ('name', 'order_link', 'created', 'updated')
    inlines = (CategoryImageAdmin,)
    list_per_page = 20
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description',)
    settings = '{"minHeight": "200"}' # JSON string
    formfield_overrides = {
        models.TextField: {'widget': RedactorTextarea(attrs={'data-settings': settings})},
    }


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_link_files', 'product',)
    list_display_links = ('name',)
    list_filter = ('product',)
    ordering = ('product', 'order')


class GroupAdminInline(admin.TabularInline):
    extra = 1
    model = Group
    prepopulated_fields = {'slug': ('name',)}


class GroupAdmin(admin.ModelAdmin):
    model = Group
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'sub_category', 'order_link')
    list_filter = ('sub_category',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order_link', 'created', 'updated')
    list_filter = ('category',)
    list_per_page = 20
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description',)
    inlines = (GroupAdminInline,)

    settings = '{"minHeight": "200"}' # JSON string
    formfield_overrides = {
        models.TextField: {'widget': RedactorTextarea(attrs={'data-settings': settings})},
    }


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args,**kwargs)
        instance = kwargs.get('instance')
        settings = '{'
        settings += '"minHeight": "350"'
        if instance:
            settings += ', "imageGetJson": "/cms/images/json/{}/"'.format(instance.pk)
        settings += '}'
        self.fields['body'].widget = RedactorTextarea(attrs={'data-settings': settings})


class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm
    list_display = ('name', 'order_link')
    model = Document


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(DocumentSet)
admin.site.register(Document, DocumentAdmin)
