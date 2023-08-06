from django.db import models
from django_bleach.models import BleachField
from django.contrib.sites.models import Site


class Page(models.Model):
    site = models.ForeignKey(Site, null=False, on_delete=models.CASCADE)
    key = models.CharField(null=False, max_length=64)
    title = models.CharField(null=False, max_length=128)
    description = models.CharField(blank=True, max_length=256)

    class Meta:
        unique_together = ('site', 'key')

    def __str__(self):
        return '{} - {}'.format(self.key, self.site.domain)


class Text(models.Model):
    content = BleachField(null=False, allowed_tags=['a', 'p', 'i', 'b', 'u'], allowed_attributes=['href'])
    page = models.ForeignKey(Page, null=False, on_delete=models.CASCADE)
    key = models.CharField(null=False, max_length=64)

    class Meta:
        unique_together = ('page', 'key')

    def __str__(self):
        return self.key