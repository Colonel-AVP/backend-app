from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_alumni = models.BooleanField(default=False)
    extra_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=255)
    departments = models.ManyToManyField(Department)
    subjects = models.ManyToManyField(Subject, related_name="staff_taught")
    email = models.EmailField(max_length=70, unique=True)

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    WEEK_CHOICES = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    ]
    week = models.CharField(max_length=3, choices=WEEK_CHOICES, blank=True, null=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True, blank=True
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    week_date = models.DateTimeField()

    def __str__(self):
        return self.week


class PNWebPushConfig(models.Model):
    OPT_IN_CHOICES = [
        ("1", 1),
        ("2,", 2),
    ]
    is_web_push_enabled = models.BooleanField(default=False, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=25, null=True, blank=True)
    """type - native/box/bell
    """
    position = models.CharField(max_length=25, null=True, blank=True)
    bg_color = models.CharField(max_length=25, null=True, blank=True)
    native_config = models.JSONField(null=True, blank=True)
    box_config = models.JSONField(null=True, blank=True)
    bell_config = models.JSONField(null=True, blank=True)
    visibility_settings = models.JSONField(null=True, blank=True)
    icon_url = models.TextField(null=True, blank=True)
    badge_url = models.TextField(null=True, blank=True)
    opt_in_option = models.CharField(
        max_length=2, choices=OPT_IN_CHOICES, null=True, blank=True
    )
    allow_button_text = models.CharField(max_length=55, null=True, blank=True)
    dont_allow_button_text = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.message
