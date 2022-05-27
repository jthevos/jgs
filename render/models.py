from django.db import models
from django.urls import reverse
from django_extensions.db import fields as extension_fields

from . import storage

fs = storage.SpacesStorage()

# https://www.digitalocean.com/community/questions/how-to-store-django-media-files-to-spaces


class Art(models.Model):

    # Fields
    paid = models.DecimalField(
        max_digits=10, decimal_places=2, default="0.0", null=True
    )
    log_number = models.CharField(max_length=10, null=True, blank=True)
    medium = models.CharField(max_length=255, null=True, blank=True)
    slug = extension_fields.AutoSlugField(populate_from="title", blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(
        max_length=255, storage=fs, upload_to="images/", null=True
    )
    style = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=255, null=True, blank=True)
    art_location = models.TextField(max_length=1000, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=True)
    year = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    available = models.NullBooleanField(default=True)
    country = models.CharField(max_length=255, default="USA", null=True)
    show = models.CharField(max_length=255, null=True, blank=True)
    artist = models.CharField(max_length=255, default="Jonathan Green", null=True)
    certificate = models.NullBooleanField(default=False)
    condition = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(max_length=5000, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    gift = models.NullBooleanField(default=False)
    year_span = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True)
    paper = models.CharField(max_length=255, null=True, blank=True)
    in_progress = models.NullBooleanField(default=False)

    class Meta:
        pass

    def __str__(self):
        if self.log_number == None:
            return self.title + " - no log number!"
        else:
            return self.title + " - " + self.log_number

    def get_absolute_url(self):
        return reverse("firegrass_Art_detail", args=(self.slug,))

    def get_update_url(self):
        return reverse("firegrass_Art_update", args=(self.slug,))

    def get_image_url(self):
        return self.image.url
