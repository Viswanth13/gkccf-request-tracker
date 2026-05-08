from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from requests_app.models import AIDraftLog
from requests_app.models import RequestNote
from requests_app.models import ServiceRequest
from requests_app.models import StaffUser
from requests_app.models import StatusHistory


class RequestApiTests(TestCase):
    def setUp(self):
        self.sarah = StaffUser.objects.create(
            name="Sarah Kim",
            role="Donor Services",
            email="sarah.kim@gkccf-demo.org",
        )
        self.michael = StaffUser.objects.create(
            name="Michael Lee",
            role="Donor Services",
            email="michael.lee@gkccf-demo.org",
        )

        self.request_one = ServiceRequest.objects.create(
            request_id="REQ-2025-1042",
            title="Grant recommendation help",
            requester_name="Mary Smith",
            requester_type=ServiceRequest.RequesterType.DONOR,
            category=ServiceRequest.Category.GRANT_HELP,
            fund_name="Smith Family Fund",
            grant_amount=Decimal("5000.00"),
            nonprofit_name="Local Youth Arts Collective",
            missing_information="Missing EIN and mailing address",
            owner=self.sarah,
            priority=ServiceRequest.Priority.MEDIUM,
            status=ServiceRequest.Status.WAITING_ON_DONOR,
            description="Grant review blocked on missing nonprofit details.",
        )
        self.request_two = ServiceRequest.objects.create(
            request_id="REQ-2025-1041",
            title="Fund balance question",
            requester_name="John Davis",
            requester_type=ServiceRequest.RequesterType.DONOR,
            category=ServiceRequest.Category.FUND_QUESTION,
            fund_name="Davis Family Fund",
            grant_amount=None,
            nonprofit_name=None,
            missing_information="",
            owner=self.michael,
            priority=ServiceRequest.Priority.LOW,
            status=ServiceRequest.Status.IN_REVIEW,
            description="Question about available balance and recent activity.",
        )

        self.note = RequestNote.objects.create(
            request=self.request_one,
            author_name="Sarah Kim",
            note_type=RequestNote.NoteType.NOTE,
            note_text="Initial review completed.",
        )
        self.status_history = StatusHistory.objects.create(
            request=self.request_one,
            old_status=ServiceRequest.Status.IN_REVIEW,
            new_status=ServiceRequest.Status.WAITING_ON_DONOR,
            changed_by="Sarah Kim",
        )
        self.ai_draft_log = AIDraftLog.objects.create(
            request=self.request_one,
            generated_by="Sarah Kim",
            draft_text="AI-generated draft. Human review is required before sending.",
            reviewed=False,
        )

    def test_get_requests_returns_created_requests(self):
        response = self.client.get(reverse("request-list"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["request_id"], "REQ-2025-1041")
        self.assertEqual(
            sorted(data[0].keys()),
            sorted(
                [
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
            ),
        )

    def test_get_request_detail_returns_owner_notes_status_history_and_latest_ai_draft(self):
        response = self.client.get(reverse("request-detail", args=[self.request_one.id]))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["request_id"], "REQ-2025-1042")
        self.assertEqual(data["owner"]["name"], "Sarah Kim")
        self.assertEqual(len(data["notes"]), 1)
        self.assertEqual(data["notes"][0]["note_text"], "Initial review completed.")
        self.assertEqual(len(data["status_history"]), 1)
        self.assertEqual(data["status_history"][0]["new_status"], "Waiting on Donor")
        self.assertIsNotNone(data["latest_ai_draft"])
        self.assertTrue(data["latest_ai_draft"]["human_review_required"])

    def test_get_requests_search_filters_correctly(self):
        response = self.client.get(reverse("request-list"), {"search": "Smith"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["request_id"], "REQ-2025-1042")

    def test_get_requests_category_filters_correctly(self):
        response = self.client.get(
            reverse("request-list"),
            {"category": ServiceRequest.Category.FUND_QUESTION},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["request_id"], "REQ-2025-1041")

    def test_post_notes_creates_a_note(self):
        response = self.client.post(
            reverse("request-note-create", args=[self.request_one.id]),
            data={
                "author_name": "Sarah Kim",
                "note_text": "Follow-up sent to donor requesting EIN and mailing address.",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.request_one.notes.count(), 2)
        created_note = self.request_one.notes.order_by("-id").first()
        self.assertEqual(created_note.note_type, RequestNote.NoteType.NOTE)
        self.assertEqual(
            created_note.note_text,
            "Follow-up sent to donor requesting EIN and mailing address.",
        )
        self.assertEqual(response.json()["note_type"], "note")

    def test_post_notes_rejects_blank_note_text(self):
        response = self.client.post(
            reverse("request-note-create", args=[self.request_one.id]),
            data={
                "author_name": "Sarah Kim",
                "note_text": "   ",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"note_text": ["This field may not be blank."]})

    def test_patch_status_updates_request_and_creates_status_history(self):
        response = self.client.patch(
            reverse("request-status-update", args=[self.request_two.id]),
            data={
                "status": ServiceRequest.Status.COMPLETED,
                "changed_by": "Michael Lee",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.request_two.refresh_from_db()
        self.assertEqual(self.request_two.status, ServiceRequest.Status.COMPLETED)
        self.assertTrue(
            StatusHistory.objects.filter(
                request=self.request_two,
                old_status=ServiceRequest.Status.IN_REVIEW,
                new_status=ServiceRequest.Status.COMPLETED,
                changed_by="Michael Lee",
            ).exists()
        )
        self.assertTrue(
            RequestNote.objects.filter(
                request=self.request_two,
                note_type=RequestNote.NoteType.STATUS_CHANGE,
                author_name="Michael Lee",
            ).exists()
        )
        self.assertEqual(response.json()["message"], "Status updated successfully")

    def test_patch_status_rejects_invalid_status(self):
        response = self.client.patch(
            reverse("request-status-update", args=[self.request_one.id]),
            data={
                "status": "Archived",
                "changed_by": "Sarah Kim",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("status", response.json())

    def test_post_generate_draft_creates_ai_draft_log(self):
        initial_count = AIDraftLog.objects.count()

        response = self.client.post(
            reverse("request-generate-draft", args=[self.request_two.id]),
            data={"generated_by": "Michael Lee"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(AIDraftLog.objects.count(), initial_count + 1)
        latest_log = AIDraftLog.objects.order_by("-id").first()
        self.assertEqual(latest_log.generated_by, "Michael Lee")
        self.assertFalse(latest_log.reviewed)
        self.assertIn("Davis Family Fund", latest_log.draft_text)
        self.assertIn("human_review_required", response.json())
        self.assertTrue(response.json()["human_review_required"])

    def test_generated_draft_includes_human_review_wording(self):
        response = self.client.post(
            reverse("request-generate-draft", args=[self.request_one.id]),
            data={"generated_by": "Sarah Kim"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        draft_text = response.json()["draft_text"]
        self.assertIn("Human review is required before sending.", draft_text)
        self.assertIn("Mary", draft_text)
        self.assertIn("Smith Family Fund", draft_text)
        self.assertIn("Missing EIN and mailing address", draft_text)
