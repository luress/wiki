from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.wiki, name="wiki"),
    path("wiki/<str:name>", views.title, name="title"),
    path("fail", views.fail, name="fail"),
    path("create", views.create, name="create"),
    path("change", views.chan, name="chan"),
    path("wiki/change/<str:name>", views.change, name="change")
]
