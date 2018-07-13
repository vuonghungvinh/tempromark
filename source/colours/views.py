
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from . import models


def index(request):
    colour_ranges = models.Range.objects.prefetch_related('colours').all()
    return render(request, 'colours/index.html', locals())
