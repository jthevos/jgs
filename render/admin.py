from django.contrib import admin
from django import forms

from . import models


class ArtAdminForm(forms.ModelForm):

    class Meta:
        model = models.Art
        fields = [
            "paid",
            "log_number",
            "medium",
            "image",
            "style",
            "size",
            "art_location",
            "year",
            "available",
            "country",
            "show",
            "artist",
            "certificate",
            "condition",
            "notes",
            "value",
            "signature",
            "gift",
            "title",
            "price",
            "paper",
        ]

        readonly_fields = [
            "slug",
            "created",
            "last_updated",
        ]

class ArtAdmin(admin.ModelAdmin):
    form = ArtAdminForm
    list_display = [
        "paid",
        "log_number",
        "medium",
        "slug",
        "image",
        "style",
        "size",
        "art_location",
        "year",
        "available",
        "country",
        "show",
        "artist",
        "certificate",
        "condition",
        "notes",
        "value",
        "signature",
        "gift",
        "title",
        "price",
        "paper",
    ]

    readonly_fields = [
        'created',
        'last_updated',
    ]


