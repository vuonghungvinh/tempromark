from django.core.urlresolvers import reverse
from django.db import models

from . import ordered_model


class BasicPage(models.Model):

    SLUGS = (
        ('home', 'homepage'),
        ('contact', 'contact page'),
    )

    slug = models.SlugField(
        choices=SLUGS,
        unique=True,
        verbose_name='URL Fragment')
    name = models.CharField(
        max_length=255,
        verbose_name='Page Title')
    meta_title = models.CharField(
        blank=True,
        max_length=255,
        verbose_name='Meta Title')
    meta_description = models.TextField(
        blank=True,
        verbose_name='Page Meta',
        help_text='Set Meta Description for this page.')
    body = models.TextField(
        blank=True)
    created = models.DateTimeField(
        auto_now_add=True)
    updated = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name = 'Basic Page'

    def __unicode__(self):
        return self.name


class BasicImage(models.Model):
    image = models.ImageField(upload_to='cms_pages/%Y/%m/%d/',
        help_text='Add images to this page.')
    page = models.ForeignKey(BasicPage, related_name='basic_images')
    url = models.URLField(
        blank=True,
        help_text='Web site or page address eg. http://tepromark.com/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Image'

    def __unicode__(self):
        return self.image.path


class Page(ordered_model.OrderedModel):

    DRAFT = 'draft'
    ABOUT = 'about'
    SUPPORT = 'support'

    SECTIONS = (
        (DRAFT, 'Draft'),
        (ABOUT, 'About'),
        (SUPPORT, 'Support'),
    )

    section = models.CharField(
        max_length=15,
        choices=SECTIONS,
        default=DRAFT)
    name = models.CharField(max_length=255, verbose_name='Page Title')
    slug = models.SlugField(help_text=('Used to generate URL. '
            'Suggested value generated from title.'),
            unique=True,
            verbose_name='URL Fragment')
    meta_title = models.CharField(
        blank=True,
        max_length=255,
        verbose_name='Meta Title')
    meta_description = models.TextField(
        blank=True,
        verbose_name='Page Meta',
        help_text='Set Meta Description for this page.')
    body = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order',)
        verbose_name = 'Section Page'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('section_page_detail', kwargs={
            'section':self.section,
            'slug': self.slug})


class Image(models.Model):
    image = models.ImageField(upload_to='cms_pages/%Y/%m/%d/',
        help_text='Add images to this page.')
    page = models.ForeignKey(Page, related_name='images')
    url = models.URLField(
        blank=True,
        help_text='Web site or page address eg. http://tepromark.com/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return self.image.path
