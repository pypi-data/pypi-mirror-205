from django.urls import path
from django.views.generic.base import RedirectView

from . import views

# Define a list of URL patterns to be imported by NetBox. Each pattern maps a URL to
# a specific view so that it can be accessed by users.
urlpatterns = (
    path("", RedirectView.as_view(url="topology/", permanent=True)),
    path("topology/", views.TopologyHomeView.as_view(), name="home"),
    path("images/", views.TopologyImagesView.as_view(), name="images"),
    path("individualoptions/", views.TopologyIndividualOptionsView.as_view(), name="individualoptions"),
)
