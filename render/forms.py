from django import forms
from . import models

class SearchArtForm(forms.Form):
    art_identifier = forms.CharField(label='Title, Log Number, Medium, Year, or Artist ', max_length=100, required=False)

class ArtForm(forms.ModelForm):
    class Meta:
        model = models.Art
        fields = [
            "title",
            "artist",
            "log_number",
            "price",
            "paid",
            "notes",
            "medium",
            "image",
            "style",
            "size",
            "art_location",
            "year",
            "available",
            "country",
            "show",
            "certificate",
            "condition",
            "value",
            "signature",
            "gift",
            "title",
            "paper",
            "description",
            "year_span",
            "location",
            "in_progress",
        ]

        readonly_fields = [
            "slug",
            "created",
            "last_updated",
        ]
