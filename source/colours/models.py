
from django.core.urlresolvers import reverse
from django.db import models

class Range(models.Model):
    name = models.CharField(
        max_length=255)
    description = models.TextField(
        blank=True)
    slug = models.SlugField(
        max_length=50,
        verbose_name='URL Fragment',
        help_text='Suggested value generated from name.')
    symbol = models.CharField(
        max_length=3,
        help_text='Enter a character to represent this colour range.')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Colour Range'
        verbose_name_plural = 'Colour Ranges'

    def get_absolute_url(self):
        return reverse(
            'colour-range-detail',
            kwargs={'slug': self.slug, 'pk': self.pk})

    def __unicode__(self):
        return self.name


class Colour(models.Model):
    range = models.ForeignKey(
        Range,
        related_name='colours')
    name = models.CharField(
        max_length=255)
    image = models.ImageField(
        upload_to='colours/%Y/%m/%d',
        help_text='Image for this colour.',)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name
