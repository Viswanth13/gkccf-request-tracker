from django.db.models import Prefetch
from django.db.models import Q
from rest_framework import generics

from requests_app.models import AIDraftLog
from requests_app.models import RequestNote
from requests_app.models import ServiceRequest
from requests_app.models import StatusHistory
from requests_app.serializers import ServiceRequestDetailSerializer
from requests_app.serializers import ServiceRequestListSerializer


class ServiceRequestListView(generics.ListAPIView):
    serializer_class = ServiceRequestListSerializer

    def get_queryset(self):
        queryset = ServiceRequest.objects.select_related("owner").order_by("-updated_at", "-id")

        search = self.request.query_params.get("search")
        category = self.request.query_params.get("category")
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")

        if search:
            queryset = queryset.filter(
                Q(request_id__icontains=search)
                | Q(requester_name__icontains=search)
                | Q(fund_name__icontains=search)
                | Q(nonprofit_name__icontains=search)
                | Q(category__icontains=search)
                | Q(title__icontains=search)
            )

        if category:
            queryset = queryset.filter(category__iexact=category)

        if status:
            queryset = queryset.filter(status__iexact=status)

        if priority:
            queryset = queryset.filter(priority__iexact=priority)

        return queryset


class ServiceRequestDetailView(generics.RetrieveAPIView):
    serializer_class = ServiceRequestDetailSerializer

    queryset = ServiceRequest.objects.select_related("owner").prefetch_related(
        Prefetch("notes", queryset=RequestNote.objects.order_by("created_at", "id")),
        Prefetch(
            "status_history",
            queryset=StatusHistory.objects.order_by("created_at", "id"),
        ),
        Prefetch(
            "ai_draft_logs",
            queryset=AIDraftLog.objects.order_by("-created_at", "-id"),
        ),
    )
