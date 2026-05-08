from django.urls import path

from requests_app.views import ServiceRequestDetailView
from requests_app.views import ServiceRequestListView


urlpatterns = [
    path("requests/", ServiceRequestListView.as_view(), name="request-list"),
    path("requests/<int:pk>/", ServiceRequestDetailView.as_view(), name="request-detail"),
]
