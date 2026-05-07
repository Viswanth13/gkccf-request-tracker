from django.db import models


class StaffUser(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    avatar_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"


class ServiceRequest(models.Model):
    class RequesterType(models.TextChoices):
        DONOR = "Donor", "Donor"
        ADVISOR = "Advisor", "Advisor"
        COMPANY = "Company", "Company"
        INTERNAL = "Internal", "Internal"

    class Category(models.TextChoices):
        GRANT_HELP = "Grant Help", "Grant Help"
        FUND_QUESTION = "Fund Question", "Fund Question"
        GIVING_PORTAL_ISSUE = "Giving Portal Issue", "Giving Portal Issue"
        ADVISOR_REQUEST = "Advisor Request", "Advisor Request"
        SCHOLARSHIP = "Scholarship", "Scholarship"
        CORPORATE_GIVING = "Corporate Giving", "Corporate Giving"
        UNIQUE_ASSET = "Unique Asset", "Unique Asset"

    class Priority(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"

    class Status(models.TextChoices):
        NEW = "New", "New"
        IN_REVIEW = "In Review", "In Review"
        WAITING_ON_DONOR = "Waiting on Donor", "Waiting on Donor"
        COMPLETED = "Completed", "Completed"

    request_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    requester_name = models.CharField(max_length=255)
    requester_type = models.CharField(max_length=20, choices=RequesterType.choices)
    category = models.CharField(max_length=30, choices=Category.choices)
    fund_name = models.CharField(max_length=255)
    grant_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    nonprofit_name = models.CharField(max_length=255, blank=True, null=True)
    missing_information = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        StaffUser,
        on_delete=models.PROTECT,
        related_name="service_requests",
    )
    priority = models.CharField(max_length=10, choices=Priority.choices)
    status = models.CharField(max_length=20, choices=Status.choices)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.request_id} - {self.title}"


class RequestNote(models.Model):
    class NoteType(models.TextChoices):
        NOTE = "note", "Note"
        SYSTEM = "system", "System"
        STATUS_CHANGE = "status_change", "Status Change"

    request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    author_name = models.CharField(max_length=255)
    note_type = models.CharField(
        max_length=20,
        choices=NoteType.choices,
        default=NoteType.NOTE,
    )
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request.request_id} note by {self.author_name}"


class StatusHistory(models.Model):
    request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="status_history",
    )
    old_status = models.CharField(
        max_length=20,
        choices=ServiceRequest.Status.choices,
    )
    new_status = models.CharField(
        max_length=20,
        choices=ServiceRequest.Status.choices,
    )
    changed_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.request.request_id}: {self.old_status} -> "
            f"{self.new_status} by {self.changed_by}"
        )


class AIDraftLog(models.Model):
    request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="ai_draft_logs",
    )
    generated_by = models.CharField(max_length=255)
    draft_text = models.TextField()
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI draft for {self.request.request_id} by {self.generated_by}"
