from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("art/", views.ArtListView.as_view(), name="render_Art_list"),
    path("art/create/", views.ArtCreateView.as_view(), name="render_Art_create"),
    path("art/detail/<slug:slug>/", views.ArtDetailView.as_view(), name="render_Art_detail"),
    path("art/update/<slug:slug>/", views.ArtUpdateView.as_view(), name="render_Art_update"),
]
