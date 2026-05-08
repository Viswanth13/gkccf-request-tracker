from django.urls import path

from requests_app.views import GenerateAIDraftView
from requests_app.views import RequestNoteCreateView
from requests_app.views import ServiceRequestDetailView
from requests_app.views import ServiceRequestListView
from requests_app.views import ServiceRequestStatusUpdateView


urlpatterns = [
    path("requests/", ServiceRequestListView.as_view(), name="request-list"),
    path("requests/<int:pk>/", ServiceRequestDetailView.as_view(), name="request-detail"),
    path("requests/<int:pk>/notes/", RequestNoteCreateView.as_view(), name="request-note-create"),
    path("requests/<int:pk>/status/", ServiceRequestStatusUpdateView.as_view(), name="request-status-update"),
    path("requests/<int:pk>/generate-draft/", GenerateAIDraftView.as_view(), name="request-generate-draft"),
]
