
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models


class OrderedModel(models.Model):
    order = models.PositiveIntegerField(editable=False, default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.order = self.__class__.objects.all().order_by("-order")[0].order + 1
            except IndexError:
                self.order = 0
        super(OrderedModel, self).save(*args, **kwargs)


    def order_link(self):
        model_type_id = ContentType.objects.get_for_model(self.__class__).id
        model_id = self.id
        kwargs = {"direction": "up", "model_type_id": model_type_id, "model_id": model_id}
        url_up = reverse("admin-category-move", kwargs=kwargs)
        kwargs["direction"] = "down"
        url_down = reverse("admin-category-move", kwargs=kwargs)
        return '<a href="%s">up</a> | <a href="%s">down</a>' % (url_up, url_down)
    order_link.allow_tags = True
    order_link.short_description = 'Move'
    order_link.admin_order_field = 'order'


    def order_link_files(self):
        model_type_id = ContentType.objects.get_for_model(self.__class__).id
        model_id = self.id
        kwargs = {"direction": "up", "model_type_id": model_type_id, "model_id": model_id}
        url_up = reverse("admin-files-move", kwargs=kwargs)
        kwargs["direction"] = "down"
        url_down = reverse("admin-files-move", kwargs=kwargs)
        return '<a href="%s">up</a> | <a href="%s">down</a>' % (url_up, url_down)
    order_link_files.allow_tags = True
    order_link_files.short_description = 'Move'
    order_link_files.admin_order_field = 'order'


    @staticmethod
    def move_down(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()

            lower_model = ModelClass.objects.get(id=model_id)
            higher_model = ModelClass.objects.filter(order__gt=lower_model.order)[0]

            lower_model.order, higher_model.order = higher_model.order, lower_model.order

            higher_model.save()
            lower_model.save()
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass

    @staticmethod
    def move_up(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()

            higher_model = ModelClass.objects.get(id=model_id)
            lower_model = ModelClass.objects.filter(order__lt=higher_model.order).reverse()[0]

            lower_model.order, higher_model.order = higher_model.order, lower_model.order

            higher_model.save()
            lower_model.save()
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass

    class Meta:
        ordering = ["order"]
        abstract = True
