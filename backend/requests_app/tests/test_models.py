from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from requests_app.models import AIDraftLog
from requests_app.models import RequestNote
from requests_app.models import ServiceRequest
from requests_app.models import StaffUser
from requests_app.models import StatusHistory


class ModelTests(TestCase):
    def setUp(self):
        self.owner = StaffUser.objects.create(
            name="Sarah Kim",
            role="Donor Services",
            email="sarah.kim@gkccf-demo.org",
        )
        self.service_request = ServiceRequest.objects.create(
            request_id="REQ-2025-1042",
            title="Grant recommendation help",
            requester_name="Mary Smith",
            requester_type=ServiceRequest.RequesterType.DONOR,
            category=ServiceRequest.Category.GRANT_HELP,
            fund_name="Smith Family Fund",
            grant_amount=Decimal("5000.00"),
            nonprofit_name="Local Youth Arts Collective",
            missing_information="Missing EIN and mailing address",
            owner=self.owner,
            priority=ServiceRequest.Priority.MEDIUM,
            status=ServiceRequest.Status.WAITING_ON_DONOR,
            description="Grant review is blocked pending nonprofit details.",
        )

    def test_staff_user_str(self):
        self.assertEqual(str(self.owner), "Sarah Kim (Donor Services)")

    def test_service_request_str(self):
        self.assertEqual(
            str(self.service_request),
            "REQ-2025-1042 - Grant recommendation help",
        )

    def test_request_note_str(self):
        note = RequestNote.objects.create(
            request=self.service_request,
            author_name="Sarah Kim",
            note_text="Follow-up sent to donor.",
        )

        self.assertEqual(str(note), "REQ-2025-1042 note by Sarah Kim")

    def test_status_history_str(self):
        history = StatusHistory.objects.create(
            request=self.service_request,
            old_status=ServiceRequest.Status.IN_REVIEW,
            new_status=ServiceRequest.Status.WAITING_ON_DONOR,
            changed_by="Sarah Kim",
        )

        self.assertEqual(
            str(history),
            "REQ-2025-1042: In Review -> Waiting on Donor by Sarah Kim",
        )

    def test_ai_draft_log_str(self):
        draft_log = AIDraftLog.objects.create(
            request=self.service_request,
            generated_by="Sarah Kim",
            draft_text="Draft response text.",
        )

        self.assertEqual(
            str(draft_log),
            "AI draft for REQ-2025-1042 by Sarah Kim",
        )

    def test_optional_fields_can_be_null_or_blank(self):
        user = StaffUser.objects.create(
            name="Michael Lee",
            role="Donor Services",
            email="michael.lee@gkccf-demo.org",
            avatar_url=None,
        )

        request = ServiceRequest.objects.create(
            request_id="REQ-2025-2000",
            title="Fund balance question",
            requester_name="John Davis",
            requester_type=ServiceRequest.RequesterType.DONOR,
            category=ServiceRequest.Category.FUND_QUESTION,
            fund_name="Davis Family Fund",
            grant_amount=None,
            nonprofit_name=None,
            missing_information="",
            owner=user,
            priority=ServiceRequest.Priority.LOW,
            status=ServiceRequest.Status.IN_REVIEW,
            description="Question about available fund balance.",
        )

        self.assertIsNone(user.avatar_url)
        self.assertIsNone(request.grant_amount)
        self.assertIsNone(request.nonprofit_name)
        self.assertEqual(request.missing_information, "")

    def test_request_note_default_note_type_is_note(self):
        note = RequestNote.objects.create(
            request=self.service_request,
            author_name="Sarah Kim",
            note_text="Default note type should be note.",
        )

        self.assertEqual(note.note_type, RequestNote.NoteType.NOTE)

    def test_service_request_status_and_priority_choices_allow_valid_values(self):
        self.service_request.full_clean()

        self.service_request.status = ServiceRequest.Status.COMPLETED
        self.service_request.priority = ServiceRequest.Priority.HIGH
        self.service_request.full_clean()

        self.assertEqual(self.service_request.status, ServiceRequest.Status.COMPLETED)
        self.assertEqual(self.service_request.priority, ServiceRequest.Priority.HIGH)

    def test_service_request_rejects_invalid_status_choice(self):
        self.service_request.status = "Not A Real Status"

        with self.assertRaises(ValidationError):
            self.service_request.full_clean()
