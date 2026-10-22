from django.urls import path
from . import views

urlpatterns = [
    path(
        "applications/new/",
        views.application_create,
        name="application_create",
    ),

        path(
        "applications/search/",
        views.application_search,
        name="application_search",
    ),

        path(
        "applications/list/",
        views.application_list,
        name="application_list",
    ),

       path(
        "applications/<int:pk>/update/",
        views.application_update,
        name="application_update",
    ),

        path(
        "records/",
        views.record_list,
        name="record_list",
    ),
    path(
    "applications/<int:pk>/delete/",
    views.application_delete,
    name="application_delete",
    ),

]

