
from django import forms
from django.core.urlresolvers import reverse

from .models import Entry
from .widgets import RedactorTextarea


class EntryForm(forms.ModelForm):
    """
    This form is specifically for providing Entry instance inforation for the
    redactor settings. In this case the PK
    """
    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)

        # Get Entry Object Instance
        instance = kwargs.get('instance')

        # JSON Redactor settings
        settings = []
        settings.append('{')
        settings.append('"minHeight": "350"')
        if instance:
            images_url = reverse('project_images_json', kwargs={'pk': instance.pk})
            settings.append(', "imageGetJson": "{}"'.format(images_url))
        settings.append('}')

        settings = '\n'.join(settings)
        self.fields['body'].widget = RedactorTextarea(attrs={'data-settings': settings})

    class Meta:
        model = Entry
