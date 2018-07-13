from django import template

from .. import models


register = template.Library()


@register.inclusion_tag('catalogue/templatetags/carousel.html')
def catalogue_carousel(limit=5):
    products = models.Product.objects.order_by('?')[:limit]
    return {'products': products,}


@register.inclusion_tag('catalogue/templatetags/catalogue-navigation.html')
def catalogue_navigation():
    categories = models.Category.objects.select_related().all()
    return {'categories': categories}


@register.inclusion_tag('catalogue/templatetags/catalogue-navigation-footer.html')
def catalogue_navigation_footer():
    categories = models.Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('catalogue/templatetags/products-featured.html')
def catalogue_featured_products(limit=None):
    products = models.Product.objects.order_by('?').filter(featured=True)[:limit]
    return {'products': products}


@register.inclusion_tag('catalogue/templatetags/product-featured.html')
def catalogue_product_featured(product):
    return {'product': product}


@register.inclusion_tag('catalogue/templatetags/related-products.html')
def related_products(product, limit=None):
    products = product.related_products.all()
    if limit:
        products = products[:limit]
    return {'related_products': products,}


@register.inclusion_tag('catalogue/templatetags/related-projects.html')
def related_projects(product, limit=None):
    projects = product.projects.all()
    if limit:
        projects = projects[:limit]
    return {'related_projects': projects,}


@register.inclusion_tag('catalogue/templatetags/colour_popups.html')
def colour_popups(colour_ranges):
    return {'colour_ranges': colour_ranges, }


@register.assignment_tag
def catalogue_document_sets(category):
    document_sets = models.DocumentSet.objects.prefetch_related('documents').filter(category=category)

    # No need to re-fetch the category object
    for document_set in document_sets:
        document_set.category = category
    return document_sets
