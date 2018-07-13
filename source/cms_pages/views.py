import json

from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
import django.http as http
import django.template as template
from django.shortcuts import render_to_response, get_object_or_404, redirect, render

from animal3.templatetags import animal3_thumbnail

from . import models
from . import ordered_model


def basic_page(request, slug):
    try:
        page = models.BasicPage.objects.select_related().get(slug=slug)
    except models.BasicPage.DoesNotExist:
        page = models.BasicPage(name=slug.title(), slug=slug)

    images = page.basic_images.all()
    return render(request, 'cms_pages/{}.html'.format(page.slug), locals())


def section_index(request, section):
    try:
        page = models.Page.objects.filter(section=section)[0]
    except IndexError:
        raise http.Http404("No Pages found")
    return redirect(page)


def section_detail(request, section, slug):
    try:
        page = models.Page.objects.select_related().get(slug=slug)
    except models.Page.DoesNotExist:
        raise http.Http404("No Page found")

    images = page.images.all()
    return render(request, 'cms_pages/detail.html', locals())


def page_images_json(request, pk):
    try:
        page = models.BasicPage.objects.get(pk=pk)
    except models.BasicPage.DoesNotExist:
        raise http.Http404('Page not found with supplied slug.')

    queryset_images = page.basic_images.all()
    images = []
    for image in queryset_images:
        data = {
            "thumb": animal3_thumbnail.thumbnail_url(image.image, 'small'),
            "image": animal3_thumbnail.thumbnail_url(image.image, 'large'),
        }
        images.append(data)

    return http.HttpResponse(
        json.dumps(images, indent=4), mimetype="application/json")


@staff_member_required
@transaction.commit_on_success
def admin_move_ordered_model(request, direction, model_type_id, model_id):
    if direction == "up":
        ordered_model.OrderedModel.move_up(model_type_id, model_id)
    else:
        ordered_model.OrderedModel.move_down(model_type_id, model_id)

    ModelClass = ContentType.objects.get(id=model_type_id).model_class()

    app_label = ModelClass._meta.app_label
    model_name = ModelClass.__name__.lower()

    url = "/admin/%s/%s/" % (app_label, model_name)

    return http.HttpResponseRedirect(url)