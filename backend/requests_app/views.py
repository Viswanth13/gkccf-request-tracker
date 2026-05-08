from django.db.models import Prefetch
from django.db.models import Q
from django.db import transaction
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from requests_app.models import AIDraftLog
from requests_app.models import RequestNote
from requests_app.models import ServiceRequest
from requests_app.models import StatusHistory
from requests_app.serializers import AIDraftLogSerializer
from requests_app.serializers import CreateRequestNoteSerializer
from requests_app.serializers import GenerateDraftSerializer
from requests_app.serializers import RequestNoteSerializer
from requests_app.serializers import ServiceRequestDetailSerializer
from requests_app.serializers import ServiceRequestListSerializer
from requests_app.serializers import UpdateRequestStatusSerializer


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


class RequestNoteCreateView(APIView):
    def post(self, request, pk):
        service_request = generics.get_object_or_404(ServiceRequest, pk=pk)
        serializer = CreateRequestNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note = RequestNote.objects.create(
            request=service_request,
            author_name=serializer.validated_data["author_name"],
            note_type=RequestNote.NoteType.NOTE,
            note_text=serializer.validated_data["note_text"],
        )

        service_request.save(update_fields=["updated_at"])

        return Response(
            RequestNoteSerializer(note).data,
            status=status.HTTP_201_CREATED,
        )


class ServiceRequestStatusUpdateView(APIView):
    def patch(self, request, pk):
        service_request = generics.get_object_or_404(ServiceRequest, pk=pk)
        serializer = UpdateRequestStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]
        changed_by = serializer.validated_data["changed_by"]
        old_status = service_request.status

        with transaction.atomic():
            StatusHistory.objects.create(
                request=service_request,
                old_status=old_status,
                new_status=new_status,
                changed_by=changed_by,
            )
            RequestNote.objects.create(
                request=service_request,
                author_name=changed_by,
                note_type=RequestNote.NoteType.STATUS_CHANGE,
                note_text=f"Status changed from {old_status} to {new_status}.",
            )
            service_request.status = new_status
            service_request.save(update_fields=["status", "updated_at"])

        return Response(
            {
                "id": service_request.id,
                "request_id": service_request.request_id,
                "old_status": old_status,
                "new_status": new_status,
                "message": "Status updated successfully",
            }
        )


class GenerateAIDraftView(APIView):
    def post(self, request, pk):
        service_request = generics.get_object_or_404(
            ServiceRequest.objects.select_related("owner"),
            pk=pk,
        )
        serializer = GenerateDraftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        generated_by = serializer.validated_data["generated_by"]
        draft_text = self._build_draft_text(service_request, generated_by)

        draft_log = AIDraftLog.objects.create(
            request=service_request,
            generated_by=generated_by,
            draft_text=draft_text,
            reviewed=False,
        )

        service_request.save(update_fields=["updated_at"])

        return Response(
            {
                "id": draft_log.id,
                "draft_text": draft_log.draft_text,
                "human_review_required": True,
                "created_at": draft_log.created_at,
            },
            status=status.HTTP_201_CREATED,
        )

    def _build_draft_text(self, service_request, generated_by):
        requester_first_name = service_request.requester_name.split()[0]
        lines = [
            f"Hi {requester_first_name},",
            "",
            f"Thank you for your request regarding the {service_request.fund_name}.",
        ]

        if service_request.missing_information:
            lines.extend(
                [
                    "",
                    "To help us continue our review, could you please provide the following information?",
                    service_request.missing_information,
                ]
            )
        else:
            lines.extend(
                [
                    "",
                    "We are reviewing the request and will follow up with next steps shortly.",
                ]
            )

        lines.extend(
            [
                "",
                "AI-generated draft. Human review is required before sending. "
                "This draft does not provide legal, tax, or compliance advice.",
                "",
                "Thank you,",
                generated_by,
                "Donor Services | GKCCF",
            ]
        )

        return "\n".join(lines)
