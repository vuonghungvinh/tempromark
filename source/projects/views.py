import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from animal3.templatetags import animal3_thumbnail

from . import models


def index(request):
    """
    Blog hompage
    """
    return render(request, 'projects/index.html', locals())

def category_detail(request, slug, pk):
    try:
        category = models.Category.objects.select_related().get(pk=pk)
    except models.Category.DoesNotExist:
        raise Http404("Category not found with id: {}".format(pk))
    if slug != category.slug:
        raise Http404("Slug in URL does not match category.")
    entries = category.entries.all()
    return render(request, 'projects/category_detail.html', locals())


def entry_detail(request, slug):
    """
    Entry with the given slug
    """
    try:
        entry = models.Entry.objects.get_published().get(slug=slug)
    except models.Entry.DoesNotExist:
        raise Http404
    images = entry.images.all()
    return render(request, 'projects/entry_detail.html', locals())


def search(request):
    entries = query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        query = query.strip()
        entries = models.Entry.objects.filter(body__icontains=query)
    return render(request, 'projects/search.html', locals())


def entry_images_json(request, pk):
    try:
        entry = models.Entry.objects.get(pk=pk)
    except models.Entry.DoesNotExist:
        raise Http404('Entry not found with supplied slug.')

    image_data = []
    if entry.cover_image:
        image_data = _append_image(image_data, entry.cover_image)

    queryset_images = entry.images.all()
    for image in queryset_images:
        image_data = _append_image(image_data, image.image)

    return HttpResponse(
        json.dumps(image_data, indent=4), mimetype="application/json")

def _append_image(image_data, image):
    data = {
        "thumb": animal3_thumbnail.thumbnail_url(image, 'small'),
        "image": animal3_thumbnail.thumbnail_url(image, 'large'),
    }
    image_data.append(data)
    return image_data
