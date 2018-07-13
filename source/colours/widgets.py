from django.forms import Textarea


class RedactorTextarea(Textarea):
    class Media:
        css = {'all': ('redactor/redactor.css',)}
        js = (
            'animal3/jquery-1.9.1.min.js',
            'redactor/redactor.js', 'redactor/setup.js')

    def __init__(self, attrs=None, **kwargs):
        class_name = attrs.get('class', '')
        redactor_class = class_name and " redactor" or "redactor"
        class_name += redactor_class
        attrs['class'] = class_name
        super(RedactorTextarea, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        return super(RedactorTextarea, self).render(name, value, attrs)
