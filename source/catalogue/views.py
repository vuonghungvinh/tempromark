
import os, tempfile, time, urllib, zipfile

from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.servers.basehttp import FileWrapper

from . import models
from . import ordered_model
from colours.models import Range


def index(request):
    categories = models.Category.objects.all()
    if categories:
        first_category = categories[:1][0]
        return redirect(first_category)

    return render(request, 'catalogue/index.html', locals())


def category_colour_range(request, slug, pk):
    try:
        category = models.Category.objects.get(pk=pk)
    except models.Category.DoesNotExist:
        raise Http404("Category not found with id: {}".format(pk))
    if slug != category.slug:
        raise Http404("Slug in URL does not match category.")

    sub_categories = category.sub_categories.select_related().all()
    colour_ranges = Range.objects.prefetch_related('colours').filter(category=category.pk)
    return render(request, 'catalogue/category-colours.html', locals())


def category_detail(request, slug, pk):
    try:
        category = models.Category.objects.select_related().get(pk=pk)
    except models.Category.DoesNotExist:
        raise Http404("Category not found with id: {}".format(pk))
    if slug != category.slug:
        raise Http404("Slug in URL does not match category.")

    images = category.category_images.all()
    sub_categories = category.sub_categories.select_related().all()
    return render(request, 'catalogue/category-detail.html', locals())


def sub_category_detail(request, category_slug, slug, pk, group_slug=None):
    try:
        sub_category = models.SubCategory.objects.select_related().get(pk=pk)
    except models.SubCategory.DoesNotExist:
        raise Http404("Sub Category not found with id: {}".format(pk))
    if slug != sub_category.slug:
        raise Http404("Slug in URL does not match sub category.")

    category = sub_category.category
    if category_slug != category.slug:
        raise Http404("Slug in URL does not match category.")

    data = dict()
    groups = sub_category.groups.all()
    for group in groups:
        data[group.id] = list()
        data[group.id].append(group)

    products = sub_category.products.all()
    for product in products:
        for group in product.group.all():
            data[group.id].append(product)

    sub_categories = category.sub_categories.prefetch_related().all()
    return render(request, 'catalogue/sub-category-detail.html', locals())


def product_detail(request, slug, pk):
    try:
        product = models.Product.objects.select_related().get(pk=pk)
    except models.Product.DoesNotExist:
        raise Http404("Product not found with id: {}".format(pk))
    if slug != product.slug:
        raise Http404("Slug in URL does not match product.")

    if request.POST and request.POST.getlist('download-files'):
        return file_download(request, product)

    colour_ranges = product.colour_ranges.all()
    images = product.images.all()
    files = product.files.all()

    sub_category = product.sub_category
    groups = sub_category.groups.all()
    category = sub_category.category

    # Sub navigation extras
    sub_categories = category.sub_categories.all()
    return render(request, 'catalogue/product-detail.html', locals())


def document_detail(request, category_slug, category_pk, pk):
    try:
        document = models.Document.objects.select_related('document_set', 'document_set__category').get(pk=pk)
        document_set = document.document_set
        category = document.document_set.category
    except models.Category.DoesNotExist:
        raise Http404()
    return render(request, 'catalogue/document_detail.html', locals())


def product_search(request):
    query = request.GET.get('q', '').strip()
    products = models.Product.objects.search(query)

    # Paginate
    products = _pagination(request, products)

    def build_url(page, query):
        return urllib.urlencode(dict(page=page, q=query))

    if products.has_previous():
        page_previous = build_url(products.previous_page_number(), query)
    if products.has_next():
        page_next = build_url(products.next_page_number(), query)

    return render(request, 'catalogue/product-search.html', locals())


def file_download(request, product):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory.
    """
    keys = request.POST.getlist('download-files')
    files = models.File.objects.filter(pk__in=keys)

    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for f in files:
        archive.write(f.file.path, os.path.basename(f.file.name))
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')

    filename = time.strftime('{}-%Y-%m-%d.zip'.format(product.slug))
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response


def _pagination(request, products, limit=25):
    paginator = Paginator(products, limit)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        raise Http404('Page not an integer.')
    except EmptyPage:
        raise Http404('Empty page.')
    return products


@staff_member_required
@transaction.commit_on_success
def admin_move_ordered_model(request, direction, model_type_id, model_id):

    ModelClass = ContentType.objects.get(id=model_type_id).model_class()
    if direction == "up":
        ModelClass.move_up(model_type_id, model_id)
    else:
        ModelClass.move_down(model_type_id, model_id)

    url = request.META.get('HTTP_REFERER')
    if url is None:
        app_label = ModelClass._meta.app_label
        model_name = ModelClass.__name__.lower()
        url = "/admin/%s/%s/" % (app_label, model_name)

    return HttpResponseRedirect(url)
