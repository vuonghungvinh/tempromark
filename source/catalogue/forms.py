
from django import forms

from . import models


class ProductAdminForm(forms.ModelForm):
    """
    Allow for custom validation of product editing in the product admin.
    """
    class Meta:
        model = models.Product
