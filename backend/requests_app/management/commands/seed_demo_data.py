from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from requests_app.models import RequestNote
from requests_app.models import ServiceRequest
from requests_app.models import StaffUser
from requests_app.models import StatusHistory


class Command(BaseCommand):
    help = "Seed demo staff, service requests, notes, and status history data."

    def handle(self, *args, **options):
        with transaction.atomic():
            staff_users = self._seed_staff_users()
            requests = self._seed_service_requests(staff_users)
            note_count = self._seed_request_notes(requests)
            history_count = self._seed_status_history(requests)

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data seeded successfully. "
                f"Staff users: {len(staff_users)}. "
                f"Service requests: {len(requests)}. "
                f"Timeline notes ensured: {note_count}. "
                f"Status history entries ensured: {history_count}."
            )
        )

    def _seed_staff_users(self):
        staff_data = [
            {
                "name": "Sarah Kim",
                "role": "Donor Services",
                "email": "sarah.kim@gkccf-demo.org",
            },
            {
                "name": "Michael Lee",
                "role": "Donor Services",
                "email": "michael.lee@gkccf-demo.org",
            },
            {
                "name": "Alicia Brown",
                "role": "Grants Operations",
                "email": "alicia.brown@gkccf-demo.org",
            },
            {
                "name": "David Patel",
                "role": "Advisor Services",
                "email": "david.patel@gkccf-demo.org",
            },
        ]

        staff_users = {}
        for item in staff_data:
            user, _ = StaffUser.objects.update_or_create(
                email=item["email"],
                defaults={
                    "name": item["name"],
                    "role": item["role"],
                    "avatar_url": None,
                },
            )
            staff_users[item["name"]] = user

        return staff_users

    def _seed_service_requests(self, staff_users):
        request_data = [
            {
                "request_id": "REQ-2025-1042",
                "title": "Grant recommendation help",
                "requester_name": "Mary Smith",
                "requester_type": ServiceRequest.RequesterType.DONOR,
                "category": ServiceRequest.Category.GRANT_HELP,
                "fund_name": "Smith Family Fund",
                "grant_amount": Decimal("5000.00"),
                "nonprofit_name": "Local Youth Arts Collective",
                "missing_information": "Missing EIN and mailing address",
                "owner": staff_users["Sarah Kim"],
                "priority": ServiceRequest.Priority.MEDIUM,
                "status": ServiceRequest.Status.WAITING_ON_DONOR,
                "description": (
                    "Donor is recommending a $5,000 grant to a local nonprofit. "
                    "We are missing the organization's EIN and mailing address to "
                    "complete review."
                ),
            },
            {
                "request_id": "REQ-2025-1041",
                "title": "Fund balance question",
                "requester_name": "John Davis",
                "requester_type": ServiceRequest.RequesterType.DONOR,
                "category": ServiceRequest.Category.FUND_QUESTION,
                "fund_name": "Davis Family Fund",
                "grant_amount": None,
                "nonprofit_name": None,
                "missing_information": "",
                "owner": staff_users["Michael Lee"],
                "priority": ServiceRequest.Priority.LOW,
                "status": ServiceRequest.Status.IN_REVIEW,
                "description": (
                    "Donor requested clarification about available balance and "
                    "recent fund activity."
                ),
            },
            {
                "request_id": "REQ-2025-1040",
                "title": "Giving portal login issue",
                "requester_name": "Lisa Thompson",
                "requester_type": ServiceRequest.RequesterType.DONOR,
                "category": ServiceRequest.Category.GIVING_PORTAL_ISSUE,
                "fund_name": "Thompson Fund",
                "grant_amount": None,
                "nonprofit_name": None,
                "missing_information": "Needs portal username confirmation",
                "owner": staff_users["Alicia Brown"],
                "priority": ServiceRequest.Priority.MEDIUM,
                "status": ServiceRequest.Status.NEW,
                "description": (
                    "Donor is unable to access the giving portal and needs help "
                    "confirming login details."
                ),
            },
            {
                "request_id": "REQ-2025-1039",
                "title": "Advisor charitable planning question",
                "requester_name": "Mark Johnson",
                "requester_type": ServiceRequest.RequesterType.ADVISOR,
                "category": ServiceRequest.Category.ADVISOR_REQUEST,
                "fund_name": "Johnson Family Fund",
                "grant_amount": None,
                "nonprofit_name": None,
                "missing_information": "",
                "owner": staff_users["David Patel"],
                "priority": ServiceRequest.Priority.HIGH,
                "status": ServiceRequest.Status.IN_REVIEW,
                "description": (
                    "Professional advisor requested information about charitable "
                    "planning options for a client."
                ),
            },
            {
                "request_id": "REQ-2025-1038",
                "title": "Scholarship eligibility question",
                "requester_name": "Emily Rodriguez",
                "requester_type": ServiceRequest.RequesterType.DONOR,
                "category": ServiceRequest.Category.SCHOLARSHIP,
                "fund_name": "Rodriguez Scholarship",
                "grant_amount": None,
                "nonprofit_name": None,
                "missing_information": "",
                "owner": staff_users["Sarah Kim"],
                "priority": ServiceRequest.Priority.LOW,
                "status": ServiceRequest.Status.COMPLETED,
                "description": (
                    "Donor asked about scholarship eligibility rules and "
                    "application timing."
                ),
            },
            {
                "request_id": "REQ-2025-1037",
                "title": "Corporate giving program update",
                "requester_name": "NorthStar Co.",
                "requester_type": ServiceRequest.RequesterType.COMPANY,
                "category": ServiceRequest.Category.CORPORATE_GIVING,
                "fund_name": "NorthStar Fund",
                "grant_amount": None,
                "nonprofit_name": None,
                "missing_information": "Needs updated program contact",
                "owner": staff_users["Michael Lee"],
                "priority": ServiceRequest.Priority.MEDIUM,
                "status": ServiceRequest.Status.WAITING_ON_DONOR,
                "description": (
                    "Company requested updates to its corporate giving program "
                    "contact and grant cycle details."
                ),
            },
            {
                "request_id": "REQ-2025-1036",
                "title": "Unique asset gift inquiry",
                "requester_name": "Robert Wilson",
                "requester_type": ServiceRequest.RequesterType.DONOR,
                "category": ServiceRequest.Category.UNIQUE_ASSET,
                "fund_name": "Wilson Family Fund",
                "grant_amount": None,
                "nonprofit_name": None,
                "missing_information": "Asset details needed",
                "owner": staff_users["Alicia Brown"],
                "priority": ServiceRequest.Priority.MEDIUM,
                "status": ServiceRequest.Status.NEW,
                "description": (
                    "Donor asked whether a privately held business interest could "
                    "be considered as a charitable gift."
                ),
            },
            {
                "request_id": "REQ-2025-1035",
                "title": "Grant purpose clarification",
                "requester_name": "Patricia Allen",
                "requester_type": ServiceRequest.RequesterType.DONOR,
                "category": ServiceRequest.Category.GRANT_HELP,
                "fund_name": "Allen Family Fund",
                "grant_amount": Decimal("2500.00"),
                "nonprofit_name": "Community Food Network",
                "missing_information": "Grant purpose needs clarification",
                "owner": staff_users["Sarah Kim"],
                "priority": ServiceRequest.Priority.HIGH,
                "status": ServiceRequest.Status.IN_REVIEW,
                "description": (
                    "Donor recommended a grant but the purpose description needs "
                    "clarification before review can continue."
                ),
            },
        ]

        requests = {}
        for item in request_data:
            request, _ = ServiceRequest.objects.update_or_create(
                request_id=item["request_id"],
                defaults={
                    "title": item["title"],
                    "requester_name": item["requester_name"],
                    "requester_type": item["requester_type"],
                    "category": item["category"],
                    "fund_name": item["fund_name"],
                    "grant_amount": item["grant_amount"],
                    "nonprofit_name": item["nonprofit_name"],
                    "missing_information": item["missing_information"],
                    "owner": item["owner"],
                    "priority": item["priority"],
                    "status": item["status"],
                    "description": item["description"],
                },
            )
            requests[item["request_id"]] = request

        return requests

    def _seed_request_notes(self, requests):
        note_data = [
            {
                "request": requests["REQ-2025-1042"],
                "author_name": "Sarah Kim",
                "note_type": RequestNote.NoteType.NOTE,
                "note_text": (
                    "Initial review completed. Waiting on donor to provide EIN "
                    "and mailing address."
                ),
            },
            {
                "request": requests["REQ-2025-1042"],
                "author_name": "Sarah Kim",
                "note_type": RequestNote.NoteType.SYSTEM,
                "note_text": (
                    "Missing information flagged for nonprofit verification follow-up."
                ),
            },
            {
                "request": requests["REQ-2025-1041"],
                "author_name": "Michael Lee",
                "note_type": RequestNote.NoteType.NOTE,
                "note_text": (
                    "Reviewed recent transactions and preparing a response on "
                    "current fund balance."
                ),
            },
            {
                "request": requests["REQ-2025-1039"],
                "author_name": "David Patel",
                "note_type": RequestNote.NoteType.NOTE,
                "note_text": (
                    "Gathering internal guidance before responding to the "
                    "advisor's planning question."
                ),
            },
            {
                "request": requests["REQ-2025-1038"],
                "author_name": "Sarah Kim",
                "note_type": RequestNote.NoteType.NOTE,
                "note_text": (
                    "Provided scholarship eligibility overview and closed the "
                    "request after confirmation."
                ),
            },
            {
                "request": requests["REQ-2025-1035"],
                "author_name": "Sarah Kim",
                "note_type": RequestNote.NoteType.NOTE,
                "note_text": (
                    "Need clearer grant purpose language before the request can "
                    "move forward."
                ),
            },
        ]

        ensured_count = 0
        for item in note_data:
            _, created = RequestNote.objects.get_or_create(
                request=item["request"],
                author_name=item["author_name"],
                note_type=item["note_type"],
                note_text=item["note_text"],
            )
            ensured_count += 1 if created else 0

        return ensured_count

    def _seed_status_history(self, requests):
        history_data = [
            {
                "request": requests["REQ-2025-1042"],
                "old_status": ServiceRequest.Status.IN_REVIEW,
                "new_status": ServiceRequest.Status.WAITING_ON_DONOR,
                "changed_by": "Sarah Kim",
            },
            {
                "request": requests["REQ-2025-1041"],
                "old_status": ServiceRequest.Status.NEW,
                "new_status": ServiceRequest.Status.IN_REVIEW,
                "changed_by": "Michael Lee",
            },
            {
                "request": requests["REQ-2025-1039"],
                "old_status": ServiceRequest.Status.NEW,
                "new_status": ServiceRequest.Status.IN_REVIEW,
                "changed_by": "David Patel",
            },
            {
                "request": requests["REQ-2025-1038"],
                "old_status": ServiceRequest.Status.IN_REVIEW,
                "new_status": ServiceRequest.Status.COMPLETED,
                "changed_by": "Sarah Kim",
            },
            {
                "request": requests["REQ-2025-1037"],
                "old_status": ServiceRequest.Status.IN_REVIEW,
                "new_status": ServiceRequest.Status.WAITING_ON_DONOR,
                "changed_by": "Michael Lee",
            },
            {
                "request": requests["REQ-2025-1035"],
                "old_status": ServiceRequest.Status.NEW,
                "new_status": ServiceRequest.Status.IN_REVIEW,
                "changed_by": "Sarah Kim",
            },
        ]

        ensured_count = 0
        for item in history_data:
            _, created = StatusHistory.objects.get_or_create(
                request=item["request"],
                old_status=item["old_status"],
                new_status=item["new_status"],
                changed_by=item["changed_by"],
            )
            ensured_count += 1 if created else 0

        return ensured_count
