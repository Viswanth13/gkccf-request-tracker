from rest_framework import serializers

from requests_app.models import AIDraftLog
from requests_app.models import RequestNote
from requests_app.models import ServiceRequest
from requests_app.models import StaffUser
from requests_app.models import StatusHistory


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = ["id", "name", "role", "email", "avatar_url"]


class RequestNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestNote
        fields = ["id", "author_name", "note_type", "note_text", "created_at"]


class StatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusHistory
        fields = ["id", "old_status", "new_status", "changed_by", "created_at"]


class AIDraftLogSerializer(serializers.ModelSerializer):
    human_review_required = serializers.SerializerMethodField()

    class Meta:
        model = AIDraftLog
        fields = [
            "id",
            "generated_by",
            "draft_text",
            "reviewed",
            "created_at",
            "human_review_required",
        ]

    def get_human_review_required(self, obj):
        return True


class CreateRequestNoteSerializer(serializers.Serializer):
    author_name = serializers.CharField(max_length=255)
    note_text = serializers.CharField()

    def validate_note_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("This field may not be blank.")
        return value.strip()


class UpdateRequestStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=ServiceRequest.Status.choices)
    changed_by = serializers.CharField(max_length=255)


class GenerateDraftSerializer(serializers.Serializer):
    generated_by = serializers.CharField(max_length=255)


class ServiceRequestListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.name", read_only=True)

    class Meta:
        model = ServiceRequest
        fields = [
            "id",
            "request_id",
            "title",
            "requester_name",
            "requester_type",
            "category",
            "fund_name",
            "grant_amount",
            "nonprofit_name",
            "missing_information",
            "owner_name",
            "priority",
            "status",
            "updated_at",
        ]


class ServiceRequestDetailSerializer(serializers.ModelSerializer):
    owner = StaffUserSerializer(read_only=True)
    notes = serializers.SerializerMethodField()
    status_history = serializers.SerializerMethodField()
    latest_ai_draft = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = [
            "id",
            "request_id",
            "title",
            "requester_name",
            "requester_type",
            "category",
            "fund_name",
            "grant_amount",
            "nonprofit_name",
            "missing_information",
            "owner",
            "priority",
            "status",
            "description",
            "created_at",
            "updated_at",
            "notes",
            "status_history",
            "latest_ai_draft",
        ]

    def get_notes(self, obj):
        notes = obj.notes.order_by("created_at", "id")
        return RequestNoteSerializer(notes, many=True).data

    def get_status_history(self, obj):
        history = obj.status_history.order_by("created_at", "id")
        return StatusHistorySerializer(history, many=True).data

    def get_latest_ai_draft(self, obj):
        latest_draft = obj.ai_draft_logs.order_by("-created_at", "-id").first()
        if latest_draft is None:
            return None
        return AIDraftLogSerializer(latest_draft).data
