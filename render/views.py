from django.shortcuts import render, redirect
from django.views import generic, View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms

from django.db.models import Count, F, Value, Sum, Q

from django.contrib.postgres.search import SearchVector

from django.db.models.fields import *

def index(request):
    response = redirect('/art/')
    return response

search_fields = [
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
    "year",
    "country",
    "value",
    "signature",
    "title",
    "paper",
    "description"
]

SUPPORTED_FIELD_TYPES = [CharField, DecimalField, TextField]

class ArtListView(LoginRequiredMixin, View):
    model = models.Art
    form_class = forms.ArtForm
    search_form = forms.SearchArtForm
    raise_exception = False

    def create_search_list(self, search_term):
        q = Q()
        for field in models.Art._meta.get_fields():
            if type(field) in SUPPORTED_FIELD_TYPES:
                query = "{}__icontains".format(field.name)
                q = q | Q(**{ query:search_term })
                print(q)
        result = models.Art.objects.filter(q)
        return result

    def create_search_vector(self, search_term):
        sv = SearchVector('title')  # need to search something SearchVector()
        for f in search_fields:
            sv += SearchVector(f)
        return sv

    def get(self, request):
        form_class = forms.ArtForm
        art_list = {}
        active_search = False
        search_term = ''
        return render(request,
                    'render/art-list.html',
                    {
                        'object_list': art_list,
                        'form_class': self.form_class,
                        'search_form': self.search_form,
                        'active_search': active_search,
                        'search_term': search_term,
                    }
                )
    def post(self, request):
        form = forms.SearchArtForm(request.POST)
        if form.is_valid():

            search_term = form.cleaned_data['art_identifier']

            if search_term == '':
                active_search = False
            else:
                active_search = True

            # Q Filter Approach
            # art_list = ArtListView.create_search_list(self, search_term)
            # total_value = sum(filter(None, [item.value for item in art_list]))

            # Search Vector Approach
            search_list = ArtListView.create_search_vector(self, search_term)
            art_list = models.Art.objects.annotate(search=search_list).filter(search=search_term)
            total_value = sum(filter(None, [item.value for item in art_list]))
        else:
            print("invalid form?")
            form_class = forms.ArtForm
            art_list = {}

        return render(request,
                    'render/art-list.html',
                    {
                        'object_list': art_list,
                        'form_class': self.form_class,
                        'search_form': self.search_form,
                        'active_search': active_search,
                        'search_term': search_term,
                        'total_value': total_value
                    })


class ArtCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Art
    form_class = forms.ArtForm
    raise_exception = False

class ArtDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Art
    form_class = forms.ArtForm
    raise_exception = False

class ArtUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Art
    form_class = forms.ArtForm
    pk_url_kwarg = "pk"
    raise_exception = False