from django.db import models
from django.contrib.auth.models import Permission

class CtmAdminPermission(models.Model):
    class Meta:
        permissions = [
            ("view_dashboard", "Can view the dashboard"),
        ]